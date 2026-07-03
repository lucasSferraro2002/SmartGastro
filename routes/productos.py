from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from models import db, Producto, Proveedor
from routes import login_requerido

productos_bp = Blueprint('productos', __name__)


@productos_bp.route('/productos')
@login_requerido
def index():
    productos = Producto.query.order_by(Producto.nombre).all()
    proveedores = Proveedor.query.order_by(Proveedor.nombre).all()
    return render_template('productos.html', productos=productos, proveedores=proveedores)


# --- Endpoint asíncrono (fetch desde el frontend) ---
@productos_bp.route('/api/productos', methods=['POST'])
@login_requerido
def api_crear_producto():
    """Alta de producto vía fetch() sin recargar la página."""
    data = request.get_json()
    if not data:
        return jsonify({'error': 'JSON inválido'}), 400

    nombre = data.get('nombre', '').strip()
    precio = data.get('precio')
    stock = data.get('stock')
    stock_minimo = data.get('stock_minimo')

    if not nombre or precio is None or stock is None or stock_minimo is None:
        return jsonify({'error': 'Todos los campos son obligatorios'}), 400

    if Producto.query.filter_by(nombre=nombre).first():
        return jsonify({'error': f"El producto '{nombre}' ya existe"}), 409

    try:
        producto = Producto(
            nombre=nombre,
            precio=float(precio),
            stock=int(stock),
            stock_minimo=int(stock_minimo),
            id_proveedor=data.get('id_proveedor') or None
        )
        db.session.add(producto)
        db.session.commit()
        return jsonify({
            'id': producto.id,
            'nombre': producto.nombre,
            'precio': float(producto.precio),
            'stock': producto.stock,
            'stock_minimo': producto.stock_minimo,
            'stock_bajo': producto.stock_bajo
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Error al guardar el producto'}), 500


@productos_bp.route('/productos/<int:id>/editar', methods=['GET', 'POST'])
@login_requerido
def editar(id):
    producto = Producto.query.get_or_404(id)
    proveedores = Proveedor.query.order_by(Proveedor.nombre).all()

    if request.method == 'POST':
        try:
            producto.nombre = request.form['nombre'].strip()
            producto.precio = float(request.form['precio'])
            producto.stock = int(request.form['stock'])
            producto.stock_minimo = int(request.form['stock_minimo'])
            producto.id_proveedor = request.form.get('id_proveedor') or None
            db.session.commit()
            flash('Producto actualizado correctamente.', 'success')
            return redirect(url_for('productos.index'))
        except Exception as e:
            db.session.rollback()
            flash('Error al actualizar el producto.', 'error')

    return render_template('editar_producto.html', producto=producto, proveedores=proveedores)


@productos_bp.route('/productos/<int:id>/eliminar', methods=['POST'])
@login_requerido
def eliminar(id):
    producto = Producto.query.get_or_404(id)
    try:
        db.session.delete(producto)
        db.session.commit()
        flash(f"Producto '{producto.nombre}' eliminado.", 'success')
    except Exception as e:
        db.session.rollback()
        flash('No se pudo eliminar el producto.', 'error')
    return redirect(url_for('productos.index'))