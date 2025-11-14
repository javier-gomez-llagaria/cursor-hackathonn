# 📤 Cómo Subir MathGame a GitHub - Guía Paso a Paso

## Paso 1: Instalar Git (si no lo tienes)

1. **Descarga Git**: https://git-scm.com/download/win
2. **Instala Git**:
   - Ejecuta el instalador descargado
   - Marca todas las opciones por defecto
   - Click "Next" en todos los pasos
3. **Reinicia PowerShell** después de instalar

**Verificar instalación:**
```powershell
git --version
```
Deberías ver algo como: `git version 2.x.x`

---

## Paso 2: Abrir PowerShell en la Carpeta del Proyecto

1. Abre PowerShell
2. Navega a la carpeta del proyecto:
```powershell
cd "C:\Users\zablt\OneDrive\Pictures\Screenshots\mathgame"
```

---

## Paso 3: Inicializar Git

Ejecuta estos comandos uno por uno:

```powershell
# Inicializar repositorio Git
git init

# Agregar todos los archivos
git add .

# Crear commit inicial
git commit -m "Initial commit - MathGame platform"
```

**O usa el script automático:**
```powershell
.\inicializar_git.ps1
```

---

## Paso 4: Crear Repositorio en GitHub

1. **Ve a GitHub**: https://github.com
2. **Inicia sesión** (o crea una cuenta si no tienes)
3. **Crea nuevo repositorio**:
   - Click en el botón **"+"** (arriba derecha)
   - Selecciona **"New repository"**
   - **Repository name**: `mathgame` (o el nombre que prefieras)
   - **Description**: "Plataforma gamificada para aprender matemáticas"
   - **Visibility**: Public o Private (tú decides)
   - **NO marques** "Add a README file"
   - **NO marques** "Add .gitignore" (ya lo tenemos)
   - **NO marques** "Choose a license"
   - Click en **"Create repository"**

---

## Paso 5: Conectar y Subir el Código

GitHub te mostrará comandos. Ejecuta estos en PowerShell (reemplaza `TU_USUARIO` con tu usuario de GitHub):

```powershell
# Cambiar a rama main
git branch -M main

# Conectar con GitHub (reemplaza TU_USUARIO con tu usuario)
git remote add origin https://github.com/TU_USUARIO/mathgame.git

# Subir código
git push -u origin main
```

**Ejemplo si tu usuario es "juan123":**
```powershell
git remote add origin https://github.com/juan123/mathgame.git
```

---

## Paso 6: Autenticación (si te lo pide)

Si Git te pide usuario y contraseña:

### Opción A: Personal Access Token (RECOMENDADO)

1. **Genera un token**:
   - Ve a: https://github.com/settings/tokens
   - Click en **"Generate new token (classic)"**
   - **Note**: "MathGame Deploy"
   - **Expiration**: Elige una fecha (o "No expiration")
   - Marca: **`repo`** (todos los permisos de repo)
   - Click **"Generate token"**
   - **COPIA EL TOKEN** (solo se muestra una vez)

2. **Usa el token**:
   - **Username**: Tu usuario de GitHub
   - **Password**: Pega el token que copiaste

### Opción B: GitHub CLI (Alternativa)

Si prefieres, puedes instalar GitHub CLI:
```powershell
winget install GitHub.cli
gh auth login
```

---

## ✅ Verificar que Funcionó

1. Ve a tu repositorio en GitHub: `https://github.com/TU_USUARIO/mathgame`
2. Deberías ver todos tus archivos allí
3. ¡Listo! Tu código está en GitHub

---

## 🔄 Actualizar el Código en el Futuro

Cada vez que hagas cambios, ejecuta:

```powershell
git add .
git commit -m "Descripción de los cambios"
git push
```

---

## 🚀 Siguiente Paso: Desplegar Online

Ahora que tu código está en GitHub, puedes desplegarlo en:
- **Render.com** (gratis): https://render.com
- **Railway** (gratis): https://railway.app

Ver `COMO_DESPLEGAR.md` para más detalles.

---

## ❓ Solución de Problemas

### Error: "git no se reconoce"
- **Solución**: Instala Git desde https://git-scm.com/download/win
- Reinicia PowerShell después de instalar

### Error: "remote origin already exists"
- **Solución**: 
```powershell
git remote remove origin
git remote add origin https://github.com/TU_USUARIO/mathgame.git
```

### Error: "authentication failed"
- **Solución**: Usa un Personal Access Token en lugar de tu contraseña
- Ve a: https://github.com/settings/tokens

### Error: "repository not found"
- **Solución**: Verifica que el nombre del repositorio sea correcto
- Asegúrate de que el repositorio existe en GitHub

---

## 📝 Resumen Rápido

1. ✅ Instala Git
2. ✅ `cd` a la carpeta mathgame
3. ✅ `git init`
4. ✅ `git add .`
5. ✅ `git commit -m "Initial commit"`
6. ✅ Crea repositorio en GitHub
7. ✅ `git remote add origin https://github.com/TU_USUARIO/mathgame.git`
8. ✅ `git push -u origin main`
9. ✅ ¡Listo!

¿Necesitas ayuda? Sigue cada paso cuidadosamente.

