# Guía de Despliegue - MathGame

## ⚠️ Importante: GitHub Pages NO soporta Flask

GitHub Pages solo sirve sitios estáticos (HTML, CSS, JavaScript). Esta aplicación requiere:
- Un servidor Python (Flask)
- Una base de datos (SQLite/PostgreSQL)
- Procesamiento del lado del servidor

**GitHub Pages NO puede ejecutar aplicaciones Flask.**

## 🚀 Opciones de Despliegue

### Opción 1: Render.com (RECOMENDADO - Gratis)

Render.com ofrece hosting gratuito para aplicaciones Flask.

#### Pasos:

1. **Crear cuenta en Render.com**
   - Ve a https://render.com
   - Regístrate con tu cuenta de GitHub

2. **Preparar el repositorio**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/TU_USUARIO/TU_REPO.git
   git push -u origin main
   ```

3. **Crear servicio en Render**
   - En Render, haz clic en "New +" → "Web Service"
   - Conecta tu repositorio de GitHub
   - Configuración:
     - **Name**: mathgame
     - **Environment**: Python 3
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `gunicorn app:app`
     - **Plan**: Free

4. **Variables de entorno** (opcional)
   - `SECRET_KEY`: Genera una clave secreta segura
   - `FLASK_ENV`: production

5. **Desplegar**
   - Haz clic en "Create Web Service"
   - Render construirá y desplegará tu aplicación automáticamente
   - Tu app estará disponible en: `https://mathgame.onrender.com`

#### Actualizar requirements.txt para producción:

```bash
pip install gunicorn
```

Luego agrega a `requirements.txt`:
```
gunicorn==21.2.0
```

### Opción 2: Railway

Railway también ofrece hosting gratuito.

#### Pasos:

1. **Crear cuenta en Railway**
   - Ve a https://railway.app
   - Regístrate con GitHub

2. **Crear nuevo proyecto**
   - "New Project" → "Deploy from GitHub repo"
   - Selecciona tu repositorio

3. **Configurar**
   - Railway detectará automáticamente que es una app Python
   - Asegúrate de que el `Procfile` esté presente
   - Railway desplegará automáticamente

### Opción 3: Heroku (Requiere tarjeta)

Heroku requiere tarjeta de crédito para el plan gratuito.

#### Pasos:

1. **Instalar Heroku CLI**
   ```bash
   # Descarga desde https://devcenter.heroku.com/articles/heroku-cli
   ```

2. **Login**
   ```bash
   heroku login
   ```

3. **Crear app**
   ```bash
   heroku create mathgame
   ```

4. **Configurar base de datos**
   ```bash
   heroku addons:create heroku-postgresql:mini
   ```

5. **Desplegar**
   ```bash
   git push heroku main
   ```

### Opción 4: Vercel (Solo Frontend - NO RECOMENDADO)

Vercel solo puede servir el frontend. Necesitarías:
- Convertir toda la lógica del backend a JavaScript
- Usar una base de datos como Firebase o Supabase
- Reescritura completa de la aplicación

## 📝 Preparación para Producción

### 1. Actualizar app.py para producción

```python
import os

# Cambiar esto:
app.secret_key = 'tu-clave-secreta-cambiar-en-produccion'

# Por esto:
app.secret_key = os.environ.get('SECRET_KEY', 'dev-key-change-in-production')
```

### 2. Actualizar requirements.txt

Agrega gunicorn:
```
Flask==3.0.0
Werkzeug==3.0.1
gunicorn==21.2.0
```

### 3. Configurar base de datos para producción

Para producción, considera usar PostgreSQL en lugar de SQLite:

```python
# En database.py, agregar soporte para PostgreSQL
import os

DATABASE_URL = os.environ.get('DATABASE_URL')
if DATABASE_URL and DATABASE_URL.startswith('postgres://'):
    # Usar PostgreSQL
    import psycopg2
    # Configurar conexión PostgreSQL
else:
    # Usar SQLite (desarrollo)
    DATABASE = 'database.db'
```

## 🔒 Seguridad

1. **Cambiar SECRET_KEY**: Genera una clave secreta segura
   ```python
   import secrets
   print(secrets.token_hex(32))
   ```

2. **Variables de entorno**: No subas claves secretas al repositorio

3. **HTTPS**: Render, Railway y Heroku proporcionan HTTPS automáticamente

## 📊 Monitoreo

- Render: Dashboard con logs y métricas
- Railway: Dashboard con logs
- Heroku: `heroku logs --tail`

## 🎯 Recomendación Final

**Usa Render.com** porque:
- ✅ Gratis
- ✅ Fácil de configurar
- ✅ Soporta Flask y bases de datos
- ✅ HTTPS automático
- ✅ Despliegue automático desde GitHub

¿Quieres que te ayude a configurar el despliegue en Render.com paso a paso?

