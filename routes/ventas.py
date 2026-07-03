from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from models import db, Venta, DetalleVenta, Producto
from routes import login_requerido
from datetime import datetime

ventas_bp = Blueprint('ventas', __name__)


@ventas_bp.route('/ventas')
@login_requerido
def index():
    ventas = Venta.query.order_by(Venta.fecha_hora.desc()).limit(50).all()
    return render_template('ventas.html', ventas=ventas)


@ventas_bp.route('/ventas/nueva', methods=['GET', 'POST'])
@login_requerido
def nueva():
    productos = Producto.query.filter(Producto.stock > 0).order_by(Producto.nombre).all()

    if request.method == 'POST':
        try:
            from flask import session
            venta = Venta(
                fecha_hora=datetime.utcnow(),
                estado='completada',
                id_empleado=session.get('user_id')
            )
            db.session.add(venta)
            db.session.flush()

            ids = request.form.getlist('producto_id')
            cantidades = request.form.getlist('cantidad')

            if not ids:
                flash('Seleccioná al menos un producto.', 'error')
                return render_template('nueva_venta.html', productos=productos)

            for pid, cant in zip(ids, cantidades):
                cant = int(cant)
                if cant <= 0:
                    continue
                producto = Producto.query.get(int(pid))
                if not producto or producto.stock < cant:
                    raise ValueError(f"Stock insuficiente para {producto.nombre if producto else pid}")

                detalle = DetalleVenta(
                    id_venta=venta.id,
                    id_producto=producto.id,
                    cantidad=cant,
                    precio_unitario=producto.precio,
                    subtotal=producto.precio * cant
                )
                producto.stock -= cant
                db.session.add(detalle)

            venta.calcular_total()
            db.session.commit()
            flash(f'Venta #{venta.id} registrada. Total: ${venta.total}', 'success')
            return redirect(url_for('ventas.index'))

        except ValueError as e:
            db.session.rollback()
            flash(str(e), 'error')
        except Exception as e:
            db.session.rollback()
            flash('Error al registrar la venta.', 'error')

    return render_template('nueva_venta.html', productos=productos)


@ventas_bp.route('/ventas/<int:id>/eliminar', methods=['POST'])
@login_requerido
def eliminar(id):
    venta = Venta.query.get_or_404(id)
    try:
        for detalle in venta.detalles:
            detalle.producto.stock += detalle.cantidad
        db.session.delete(venta)
        db.session.commit()
        flash(f'Venta #{id} eliminada y stock restaurado.', 'success')
    except Exception as e:
        db.session.rollback()
        flash('No se pudo eliminar la venta.', 'error')
    return redirect(url_for('ventas.index'))