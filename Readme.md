# SmartGastro Web

Sistema de gestion para foodtrucks — Segunda Entrega  
**Materia:** Analisis y Metodologia de Sistemas  
**Docente:** Juan Sebastian Stenico  
**Integrantes:** Dattoma Lucas — Ferraro Lucas

---

## Descripcion

SmartGastro es una aplicacion web desarrollada con Flask que permite a duenos de foodtrucks gestionar su inventario, registrar ventas y consultar alertas de stock, con integracion de datos climaticos en tiempo real para mejorar la toma de decisiones.

---

## Tecnologias utilizadas

- Python + Flask
- SQLAlchemy con SQLite
- Flask-Bcrypt
- Jinja2
- Open-Meteo API (clima en tiempo real, sin API key)
- HTML + CSS + JavaScript (fetch async)

---

## Instalacion

```
# 1. Clonar el repositorio
git clone https://github.com/lucasSferr aro2002/SmartGastro.git
cd SmartGastro

# 2. Crear entorno virtual
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar variables de entorno
cp .env.example .env

# 5. Ejecutar la aplicacion
python app.py
```

La app corre en `http://localhost:5001`

---

## Variables de entorno

Crear un archivo `.env` en la raiz del proyecto con el siguiente contenido:

```
SECRET_KEY=clave-secreta-segura
DATABASE_URL=sqlite:///smartgastro.db
```

La API del clima usa Open-Meteo.

---

# Mail de test
Email  `admin@smartgastro.com` 
Contrasena  `admin123` 


# Funcionalidades

- Login y logout con contrasenas encriptadas
- Dashboard con clima en tiempo real y alertas de stock bajo
- CRUD completo de productos (alta via fetch asincrono sin recargar la pagina)
- Registro y eliminacion de ventas con descuento de stock
- Rutas protegidas por sesion (te redirige al login si no esta autenticado)
