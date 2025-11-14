# 🔧 Configurar Git y Subir a GitHub

## Paso 1: Instalar Git

1. **Descarga Git**: https://git-scm.com/download/win
2. **Instala Git** (marca todas las opciones por defecto)
3. **Reinicia PowerShell** después de instalar

## Paso 2: Inicializar Repositorio

Abre PowerShell en esta carpeta (`mathgame`) y ejecuta:

```powershell
# Inicializar Git
git init

# Agregar todos los archivos
git add .

# Crear commit inicial
git commit -m "Initial commit - MathGame platform"
```

## Paso 3: Crear Repositorio en GitHub

1. Ve a: https://github.com
2. Click en **"+"** → **"New repository"**
3. **Nombre**: `mathgame`
4. **NO marques** "Initialize with README"
5. Click **"Create repository"**

## Paso 4: Conectar y Subir

Ejecuta estos comandos (reemplaza `TU_USUARIO`):

```powershell
git branch -M main
git remote add origin https://github.com/TU_USUARIO/mathgame.git
git push -u origin main
```

**Si te pide autenticación:**
- Usa un **Personal Access Token** de GitHub
- Ve a: https://github.com/settings/tokens
- Genera nuevo token con permisos `repo`
- Úsalo como contraseña

## Paso 5: Desplegar en Render.com

1. Ve a: https://render.com
2. Crea cuenta con GitHub
3. "New +" → "Web Service"
4. Conecta tu repositorio `mathgame`
5. Configuración:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`
   - Plan: Free
6. Click "Create Web Service"
7. ¡Listo! Tu app estará online

---

**Tu app estará en**: `https://mathgame.onrender.com`

