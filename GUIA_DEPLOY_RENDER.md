# 🚀 Guía Paso a Paso: Desplegar en Render.com

## ⚠️ IMPORTANTE: GitHub Pages NO funciona con Flask

GitHub Pages **solo sirve sitios estáticos** (HTML, CSS, JavaScript). Tu aplicación necesita:
- ✅ Un servidor Python (Flask)
- ✅ Una base de datos
- ✅ Procesamiento del lado del servidor

**Por eso usaremos Render.com** que es gratis y soporta Flask perfectamente.

---

## 📋 Paso 1: Preparar el Código

Ya he preparado los archivos necesarios:
- ✅ `Procfile` - Para decirle a Render cómo iniciar la app
- ✅ `requirements.txt` - Con gunicorn incluido
- ✅ `.gitignore` - Para no subir archivos innecesarios
- ✅ `app.py` - Actualizado para usar variables de entorno

---

## 📦 Paso 2: Subir a GitHub

### 2.1. Inicializar Git (si no lo has hecho)

Abre PowerShell o Terminal en la carpeta del proyecto y ejecuta:

```bash
git init
git add .
git commit -m "Preparado para deploy en Render"
```

### 2.2. Crear repositorio en GitHub

1. Ve a https://github.com
2. Haz clic en el botón **"+"** (arriba derecha) → **"New repository"**
3. Nombre: `mathgame` (o el que prefieras)
4. **NO marques** "Initialize with README"
5. Haz clic en **"Create repository"**

### 2.3. Conectar y subir

GitHub te mostrará comandos. Ejecuta estos (reemplaza `TU_USUARIO` con tu usuario de GitHub):

```bash
git branch -M main
git remote add origin https://github.com/TU_USUARIO/mathgame.git
git push -u origin main
```

Si te pide autenticación, usa un **Personal Access Token** (no tu contraseña):
- Ve a GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
- Genera nuevo token con permisos `repo`
- Úsalo como contraseña

---

## 🌐 Paso 3: Desplegar en Render.com

### 3.1. Crear cuenta

1. Ve a https://render.com
2. Haz clic en **"Get Started for Free"**
3. Elige **"Sign up with GitHub"** (recomendado)
4. Autoriza Render a acceder a tus repositorios

### 3.2. Crear Web Service

1. En el dashboard de Render, haz clic en **"New +"**
2. Selecciona **"Web Service"**
3. Conecta tu repositorio:
   - Si no aparece, haz clic en **"Configure account"** y autoriza todos los repos
   - Selecciona tu repositorio `mathgame`

### 3.3. Configurar el servicio

Completa estos campos:

- **Name**: `mathgame` (o el que prefieras)
- **Region**: Elige el más cercano (ej: `Frankfurt` para Europa)
- **Branch**: `main` (o `master` si usas esa rama)
- **Root Directory**: (deja vacío)
- **Environment**: `Python 3`
- **Build Command**: 
  ```
  pip install -r requirements.txt
  ```
- **Start Command**: 
  ```
  gunicorn app:app
  ```
- **Plan**: Selecciona **"Free"**

### 3.4. Variables de entorno (OPCIONAL pero recomendado)

Haz clic en **"Advanced"** y agrega:

- **Key**: `SECRET_KEY`
- **Value**: Genera una clave segura ejecutando esto en Python:
  ```python
  import secrets
  print(secrets.token_hex(32))
  ```
  O usa cualquier string largo y aleatorio.

### 3.5. Desplegar

1. Haz clic en **"Create Web Service"**
2. Render comenzará a construir tu aplicación (tarda 2-5 minutos)
3. Verás los logs en tiempo real
4. Cuando termine, tu app estará en: `https://mathgame.onrender.com`

---

## ✅ Paso 4: Verificar que Funciona

1. Abre la URL que Render te dio (ej: `https://mathgame.onrender.com`)
2. Deberías ver la página de login
3. Crea una cuenta y prueba resolver problemas

---

## 🔧 Solución de Problemas

### Error: "Module not found"
- Verifica que `requirements.txt` tenga todas las dependencias
- Revisa los logs de build en Render

### Error: "Application failed to respond"
- Verifica que el `Start Command` sea: `gunicorn app:app`
- Asegúrate de que `Procfile` esté presente

### La base de datos no funciona
- SQLite funciona en Render, pero los datos se pierden al reiniciar
- Para producción, considera PostgreSQL (Render lo ofrece gratis)

### La app se "duerme" después de inactividad
- En el plan gratuito, Render "duerme" la app después de 15 min de inactividad
- El primer acceso después de dormir tarda ~30 segundos en despertar
- Esto es normal en el plan gratuito

---

## 🎯 Próximos Pasos (Opcional)

### Usar PostgreSQL en lugar de SQLite

1. En Render, crea una nueva **PostgreSQL Database**
2. Copia la **Internal Database URL**
3. En tu Web Service, agrega variable de entorno:
   - Key: `DATABASE_URL`
   - Value: (pega la URL que copiaste)

Luego actualiza `database.py` para usar PostgreSQL cuando `DATABASE_URL` esté presente.

### Dominio personalizado

1. En Render, ve a tu servicio → Settings
2. Scroll hasta "Custom Domains"
3. Agrega tu dominio
4. Sigue las instrucciones para configurar DNS

---

## 📝 Resumen

✅ **GitHub Pages NO funciona** - Necesitas un servicio que soporte Flask  
✅ **Render.com es la mejor opción** - Gratis y fácil  
✅ **Tu app estará en**: `https://mathgame.onrender.com` (o el nombre que elijas)  
✅ **Despliegue automático** - Cada vez que hagas `git push`, Render actualiza la app

¿Necesitas ayuda con algún paso específico?

