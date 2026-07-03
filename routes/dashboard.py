from flask import Blueprint, render_template, jsonify
from models import Producto, Venta
from routes import login_requerido
from datetime import datetime, timedelta
import requests

dashboard_bp = Blueprint('dashboard', __name__)

LAT = -34.6037
LON = -58.3816

CODIGOS_LLUVIA = {51, 53, 55, 56, 57, 61, 63, 65, 66, 67, 71, 73, 75, 77, 80, 81, 82, 95, 96, 99}

DESCRIPCION_WMO = {
    0: 'Cielo despejado', 1: 'Mayormente despejado', 2: 'Parcialmente nublado', 3: 'Nublado',
    45: 'Niebla', 48: 'Niebla con escarcha',
    51: 'Llovizna leve', 53: 'Llovizna moderada', 55: 'Llovizna densa',
    61: 'Lluvia leve', 63: 'Lluvia moderada', 65: 'Lluvia intensa',
    80: 'Chaparrones leves', 81: 'Chaparrones moderados', 82: 'Chaparrones violentos',
    95: 'Tormenta', 96: 'Tormenta con granizo', 99: 'Tormenta con granizo intenso',
}


def _obtener_clima():
    try:
        url = 'https://api.open-meteo.com/v1/forecast'
        params = {
            'latitude': LAT,
            'longitude': LON,
            'current': 'temperature_2m,weathercode',
            'timezone': 'America/Argentina/Buenos_Aires'
        }
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()

        codigo = data['current']['weathercode']
        temperatura = round(data['current']['temperature_2m'])
        descripcion = DESCRIPCION_WMO.get(codigo, f'Codigo {codigo}')
        lluvia = codigo in CODIGOS_LLUVIA

        return {
            'descripcion': descripcion,
            'temperatura': temperatura,
            'lluvia': lluvia,
            'error': None
        }
    except requests.exceptions.Timeout:
        return {'error': 'El servicio de clima no respondio a tiempo.', 'lluvia': False}
    except requests.exceptions.RequestException:
        return {'error': 'No se pudo conectar al servicio de clima.', 'lluvia': False}


@dashboard_bp.route('/')
@login_requerido
def index():
    clima = _obtener_clima()

    alertas_stock = Producto.query.filter(
        Producto.stock <= Producto.stock_minimo
    ).all()

    hoy_inicio = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    hoy_fin = hoy_inicio + timedelta(days=1)
    ventas_hoy = Venta.query.filter(
        Venta.fecha_hora >= hoy_inicio,
        Venta.fecha_hora < hoy_fin
    ).all()
    total_hoy = sum(float(v.total) for v in ventas_hoy)

    return render_template(
        'dashboard.html',
        clima=clima,
        alertas_stock=alertas_stock,
        ventas_hoy=len(ventas_hoy),
        total_hoy=total_hoy
    )


@dashboard_bp.route('/api/clima')
@login_requerido
def api_clima():
    clima = _obtener_clima()
    return jsonify(clima)