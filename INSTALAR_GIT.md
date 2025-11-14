# 🔧 Instalar Git en Windows

## Opción 1: Descarga Manual (RECOMENDADO)

1. **Ve a**: https://git-scm.com/download/win
2. **Descarga** el instalador (se descargará automáticamente)
3. **Ejecuta** el instalador descargado
4. **Sigue el asistente**:
   - Click "Next" en todas las pantallas
   - **Marca todas las opciones por defecto**
   - No cambies nada, solo click "Next"
   - Al final, click "Install"
5. **Espera** a que termine la instalación
6. **Reinicia PowerShell** (ciérralo y ábrelo de nuevo)

## Opción 2: Usando winget (si está disponible)

Abre PowerShell como Administrador y ejecuta:

```powershell
winget install --id Git.Git -e --source winget
```

Luego reinicia PowerShell.

## Verificar Instalación

Después de instalar y reiniciar PowerShell, ejecuta:

```powershell
git --version
```

Deberías ver algo como: `git version 2.42.0` (o similar)

## Después de Instalar Git

Una vez instalado Git, vuelve a la carpeta del proyecto y ejecuta:

```powershell
cd "C:\Users\zablt\OneDrive\Pictures\Screenshots\mathgame"
git init
git add .
git commit -m "Initial commit - MathGame platform"
```

---

**Nota**: Es importante reiniciar PowerShell después de instalar Git para que reconozca el comando.

