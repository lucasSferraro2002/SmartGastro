# SmartGastro Web

Sistema de gestión para foodtrucks — Segunda Entrega
**Materia:** Análisis y Metodología de Sistemas
**Docente:** Juan Sebastián Stenico
**Integrantes:** Dattoma Lucas · Ferraro Lucas

---

## Instalación

```bash
# 1. Clonar el repositorio
git clone https://github.com/lucasSferr aro2002/SmartGastro.git
cd SmartGastro

# 2. Crear entorno virtual
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Mac/Linux

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar variables de entorno
cp .env.example .env
# Editar .env y completar OPENWEATHER_API_KEY

# 5. Ejecutar la aplicación
python app.py
```

La app corre en `http://localhost:5000`

---

## Credencial de prueba

| Email | `admin@smartgastro.com` |
| Contraseña | `admin123` |

---

## Variables de entorno (.env)

```
SECRET_KEY=clave-secreta-segura
DATABASE_URL=sqlite:///smartgastro.db
OPENWEATHER_API_KEY=tu_api_key_aqui
