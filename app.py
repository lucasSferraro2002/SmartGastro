from flask import Flask
from models import db, bcrypt
from dotenv import load_dotenv
import os

load_dotenv()

def create_app():
    app = Flask(__name__)

    # --- Configuración ---
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///smartgastro.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # --- Extensiones ---
    db.init_app(app)
    bcrypt.init_app(app)

    # --- Blueprints ---
    from routes.auth import auth_bp
    from routes.dashboard import dashboard_bp
    from routes.productos import productos_bp
    from routes.ventas import ventas_bp
    from routes.proveedores import proveedores_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(productos_bp)
    app.register_blueprint(ventas_bp)
    app.register_blueprint(proveedores_bp)

    # --- Crear tablas y usuario admin por defecto ---
    with app.app_context():
        db.create_all()
        _crear_admin_si_no_existe()

    return app


def _crear_admin_si_no_existe():
    from models import Usuario
    if not Usuario.query.filter_by(email='admin@smartgastro.com').first():
        admin = Usuario(
            nombre='Administrador',
            email='admin@smartgastro.com',
            rol='dueño'
        )
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()
        print('Usuario admin creado: admin@smartgastro.com / admin123')


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5001)