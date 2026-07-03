from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from datetime import datetime

db = SQLAlchemy()
bcrypt = Bcrypt()


class Usuario(db.Model):
    __tablename__ = 'usuario'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    rol = db.Column(db.String(20), nullable=False, default='empleado')  # 'dueño' o 'empleado'

    ventas = db.relationship('Venta', backref='empleado', lazy=True)

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<Usuario {self.email}>'


class Proveedor(db.Model):
    __tablename__ = 'proveedor'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    telefono = db.Column(db.String(20))
    email = db.Column(db.String(150))

    def __repr__(self):
        return f'<Proveedor {self.nombre}>'


class Producto(db.Model):
    __tablename__ = 'producto'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False, unique=True)
    precio = db.Column(db.Numeric(10, 2), nullable=False)
    stock = db.Column(db.Integer, nullable=False, default=0)
    stock_minimo = db.Column(db.Integer, nullable=False, default=5)
    id_proveedor = db.Column(db.Integer, db.ForeignKey('proveedor.id'), nullable=True)

    proveedor = db.relationship('Proveedor', backref='productos')
    detalles = db.relationship('DetalleVenta', backref='producto', lazy=True)

    @property
    def stock_bajo(self):
        """Devuelve True si el stock está en o debajo del mínimo (lógica de HU1)."""
        return self.stock <= self.stock_minimo

    def __repr__(self):
        return f'<Producto {self.nombre}>'


class Venta(db.Model):
    __tablename__ = 'venta'

    id = db.Column(db.Integer, primary_key=True)
    fecha_hora = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    total = db.Column(db.Numeric(10, 2), nullable=False, default=0)
    estado = db.Column(db.String(20), nullable=False, default='pendiente')
    id_empleado = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=True)

    detalles = db.relationship('DetalleVenta', backref='venta', lazy=True, cascade='all, delete-orphan')

    def calcular_total(self):
        self.total = sum(d.subtotal for d in self.detalles)

    def __repr__(self):
        return f'<Venta {self.id} - ${self.total}>'


class DetalleVenta(db.Model):
    __tablename__ = 'detalle_venta'

    id = db.Column(db.Integer, primary_key=True)
    id_venta = db.Column(db.Integer, db.ForeignKey('venta.id'), nullable=False)
    id_producto = db.Column(db.Integer, db.ForeignKey('producto.id'), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    precio_unitario = db.Column(db.Numeric(10, 2), nullable=False)  # precio al momento de la venta
    subtotal = db.Column(db.Numeric(10, 2), nullable=False)

    def __repr__(self):
        return f'<DetalleVenta venta={self.id_venta} producto={self.id_producto}>'