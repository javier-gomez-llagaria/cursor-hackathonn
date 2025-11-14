# 🌐 Cómo Alojar MathGame Online - Guía Completa

## 📋 Requisitos Previos

### 1. Instalar Git (si no lo tienes)

**Descargar Git:**
1. Ve a: https://git-scm.com/download/win
2. Descarga el instalador para Windows
3. Ejecuta el instalador
4. **Importante**: Durante la instalación, marca todas las opciones por defecto
5. Reinicia PowerShell después de instalar

**Verificar instalación:**
```powershell
git --version
```

---

## 🚀 Opción 1: Render.com (RECOMENDADO - Gratis)

### Paso 1: Preparar el Código

Abre PowerShell en la carpeta del proyecto (`C:\Users\zablt\OneDrive\Pictures\Screenshots`) y ejecuta:

```powershell
# Inicializar Git
git init

# Agregar todos los archivos
git add .

# Crear commit
git commit -m "MathGame - Listo para desplegar"
```

### Paso 2: Crear Repositorio en GitHub

1. **Ve a GitHub**: https://github.com
2. **Inicia sesión** o crea una cuenta (es gratis)
3. **Crea nuevo repositorio**:
   - Click en el botón **"+"** (arriba derecha)
   - Selecciona **"New repository"**
   - **Nombre**: `mathgame` (o el que prefieras)
   - **Descripción**: "Plataforma gamificada para aprender matemáticas"
   - **NO marques** "Add a README file"
   - **NO marques** "Add .gitignore" (ya lo tenemos)
   - Click en **"Create repository"**

### Paso 3: Subir Código a GitHub

GitHub te mostrará comandos. Ejecuta estos en PowerShell (reemplaza `TU_USUARIO` con tu usuario de GitHub):

```powershell
# Cambiar a rama main
git branch -M main

# Conectar con GitHub (reemplaza TU_USUARIO)
git remote add origin https://github.com/TU_USUARIO/mathgame.git

# Subir código
git push -u origin main
```

**Si te pide autenticación:**
- **Usuario**: Tu usuario de GitHub
- **Contraseña**: NO uses tu contraseña de GitHub
- **Usa un Personal Access Token**:
  1. Ve a: https://github.com/settings/tokens
  2. Click en "Generate new token (classic)"
  3. Nombre: "MathGame Deploy"
  4. Marca: `repo` (todos los permisos de repo)
  5. Click en "Generate token"
  6. **Copia el token** (solo se muestra una vez)
  7. Úsalo como contraseña cuando Git te lo pida

### Paso 4: Desplegar en Render.com

1. **Crear cuenta en Render**:
   - Ve a: https://render.com
   - Click en **"Get Started for Free"**
   - Selecciona **"Sign up with GitHub"**
   - Autoriza Render a acceder a tus repositorios

2. **Crear Web Service**:
   - En el dashboard, click en **"New +"**
   - Selecciona **"Web Service"**
   - Si no ves tu repositorio, click en **"Configure account"** y autoriza todos los repos
   - Selecciona tu repositorio `mathgame`

3. **Configurar el servicio**:
   - **Name**: `mathgame` (o el que prefieras)
   - **Region**: Elige el más cercano (ej: `Frankfurt` para Europa)
   - **Branch**: `main`
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

4. **Variables de entorno** (OPCIONAL):
   - Click en **"Advanced"**
   - Agregar variable:
     - **Key**: `SECRET_KEY`
     - **Value**: (déjala vacía, Render la generará automáticamente)

5. **Desplegar**:
   - Click en **"Create Web Service"**
   - Render comenzará a construir tu aplicación
   - Verás los logs en tiempo real
   - Tarda 2-5 minutos
   - Cuando termine, tu app estará en: `https://mathgame.onrender.com`

---

## ✅ Verificar que Funciona

1. Abre la URL que Render te dio (ej: `https://mathgame.onrender.com`)
2. Deberías ver la página de login
3. Prueba crear una cuenta o usar "Continue as Guest"
4. Resuelve un problema para verificar que todo funciona

---

## 🎯 Tu App Está Online

Una vez desplegada:
- ✅ Accesible desde cualquier lugar
- ✅ HTTPS automático (seguro)
- ✅ Despliegue automático: cada vez que hagas `git push`, Render actualiza la app

---

## 🔧 Solución de Problemas

### Error: "git no se reconoce"
- **Solución**: Instala Git desde https://git-scm.com/download/win
- Reinicia PowerShell después de instalar

### Error al hacer push a GitHub
- **Solución**: Usa un Personal Access Token en lugar de tu contraseña
- Ve a: https://github.com/settings/tokens

### Error en Render: "Module not found"
- **Solución**: Verifica que `requirements.txt` tenga todas las dependencias
- Revisa los logs de build en Render

### La app se "duerme" después de inactividad
- **Normal en plan gratuito**: La app se duerme después de 15 min
- **Primer acceso**: Tarda ~30 segundos en "despertar"
- **Solución**: Considera el plan de pago si necesitas que esté siempre activa

---

## 📝 Resumen Rápido

1. ✅ Instala Git
2. ✅ Crea repositorio en GitHub
3. ✅ Sube código con `git push`
4. ✅ Crea cuenta en Render.com
5. ✅ Conecta repositorio y despliega
6. ✅ ¡Listo! Tu app está online

¿Necesitas ayuda con algún paso? Sigue la guía detallada arriba.

