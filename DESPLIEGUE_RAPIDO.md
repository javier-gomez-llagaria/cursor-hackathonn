# 🚀 Despliegue Rápido - MathGame Online

## Opción 1: Render.com (RECOMENDADO - Gratis)

### Paso 1: Subir a GitHub

**Opción A: Usar el script automático**
```powershell
.\desplegar.ps1
```

**Opción B: Manual**
```bash
git init
git add .
git commit -m "Preparado para deploy"
git branch -M main
git remote add origin https://github.com/TU_USUARIO/mathgame.git
git push -u origin main
```

### Paso 2: Desplegar en Render.com

1. **Crear cuenta**: https://render.com → "Get Started for Free" → "Sign up with GitHub"

2. **Crear Web Service**:
   - Click en "New +" → "Web Service"
   - Conecta tu repositorio de GitHub
   - Selecciona el repositorio `mathgame`

3. **Configuración**:
   - **Name**: `mathgame`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Plan**: `Free`

4. **Variables de entorno** (opcional):
   - Click en "Advanced"
   - Agregar:
     - Key: `SECRET_KEY`
     - Value: (genera una clave segura o déjala vacía para que Render la genere)

5. **Desplegar**:
   - Click en "Create Web Service"
   - Espera 2-5 minutos
   - Tu app estará en: `https://mathgame.onrender.com`

---

## Opción 2: Railway (Alternativa Gratis)

1. **Crear cuenta**: https://railway.app → "Start a New Project" → "Deploy from GitHub repo"

2. **Seleccionar repositorio**: Elige tu repositorio `mathgame`

3. **Railway detecta automáticamente** que es Python y desplegará

4. Tu app estará en: `https://mathgame.up.railway.app`

---

## ⚠️ Notas Importantes

### Base de Datos
- SQLite funciona en Render/Railway, pero los datos se pierden al reiniciar
- Para producción, considera PostgreSQL (Render lo ofrece gratis)

### Plan Gratuito
- Render: La app "duerme" después de 15 min de inactividad
- Railway: Similar, puede tener límites de uso

### Dominio Personalizado
- Puedes agregar tu propio dominio en Render/Railway
- Configura DNS según las instrucciones

---

## 🔧 Solución de Problemas

### Error: "Module not found"
- Verifica que `requirements.txt` tenga todas las dependencias
- Revisa los logs de build

### Error: "Application failed to respond"
- Verifica que el `Start Command` sea: `gunicorn app:app`
- Asegúrate de que `Procfile` esté presente

### La app se "duerme"
- Normal en plan gratuito
- El primer acceso después de dormir tarda ~30 segundos

---

## ✅ Checklist Pre-Despliegue

- [ ] Todos los archivos están en GitHub
- [ ] `requirements.txt` incluye `gunicorn`
- [ ] `Procfile` existe
- [ ] `.gitignore` incluye `database.db`
- [ ] `app.py` usa `os.environ.get('SECRET_KEY')`

---

## 🎯 Después del Despliegue

1. Prueba la URL de tu app
2. Crea una cuenta de prueba
3. Verifica que todo funcione
4. Comparte la URL con tus usuarios

¡Listo! Tu app estará online y accesible desde cualquier lugar. 🎉

