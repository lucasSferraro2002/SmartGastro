from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db, Proveedor
from routes import login_requerido

proveedores_bp = Blueprint('proveedores', __name__)


@proveedores_bp.route('/proveedores')
@login_requerido
def index():
    proveedores = Proveedor.query.order_by(Proveedor.nombre).all()
    return render_template('proveedores.html', proveedores=proveedores)


@proveedores_bp.route('/proveedores/nuevo', methods=['POST'])
@login_requerido
def nuevo():
    try:
        proveedor = Proveedor(
            nombre=request.form['nombre'].strip(),
            telefono=request.form.get('telefono', '').strip() or None,
            email=request.form.get('email', '').strip() or None
        )
        db.session.add(proveedor)
        db.session.commit()
        flash(f"Proveedor '{proveedor.nombre}' agregado.", 'success')
    except Exception as e:
        db.session.rollback()
        flash('Error al guardar el proveedor.', 'error')
    return redirect(url_for('proveedores.index'))


@proveedores_bp.route('/proveedores/<int:id>/editar', methods=['GET', 'POST'])
@login_requerido
def editar(id):
    proveedor = Proveedor.query.get_or_404(id)

    if request.method == 'POST':
        try:
            proveedor.nombre = request.form['nombre'].strip()
            proveedor.telefono = request.form.get('telefono', '').strip() or None
            proveedor.email = request.form.get('email', '').strip() or None
            db.session.commit()
            flash('Proveedor actualizado.', 'success')
            return redirect(url_for('proveedores.index'))
        except Exception as e:
            db.session.rollback()
            flash('Error al actualizar el proveedor.', 'error')

    return render_template('editar_proveedor.html', proveedor=proveedor)


@proveedores_bp.route('/proveedores/<int:id>/eliminar', methods=['POST'])
@login_requerido
def eliminar(id):
    proveedor = Proveedor.query.get_or_404(id)
    try:
        db.session.delete(proveedor)
        db.session.commit()
        flash(f"Proveedor '{proveedor.nombre}' eliminado.", 'success')
    except Exception as e:
        db.session.rollback()
        flash('No se puede eliminar: tiene productos asociados.', 'error')
    return redirect(url_for('proveedores.index'))