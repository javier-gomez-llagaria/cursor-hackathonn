# Script para desplegar MathGame en Render.com
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Despliegue de MathGame en Render.com" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Verificar si Git está instalado
try {
    $gitVersion = git --version 2>&1
    Write-Host "[✓] Git encontrado: $gitVersion" -ForegroundColor Green
} catch {
    Write-Host "[✗] ERROR: Git no está instalado" -ForegroundColor Red
    Write-Host "Instala Git desde: https://git-scm.com/downloads" -ForegroundColor Yellow
    exit 1
}

Write-Host ""
Write-Host "Paso 1: Verificando estado de Git..." -ForegroundColor Yellow

# Verificar si ya es un repositorio Git
if (Test-Path ".git") {
    Write-Host "[✓] Ya es un repositorio Git" -ForegroundColor Green
} else {
    Write-Host "[!] Inicializando repositorio Git..." -ForegroundColor Yellow
    git init
    Write-Host "[✓] Repositorio inicializado" -ForegroundColor Green
}

Write-Host ""
Write-Host "Paso 2: Agregando archivos..." -ForegroundColor Yellow
git add .
Write-Host "[✓] Archivos agregados" -ForegroundColor Green

Write-Host ""
Write-Host "Paso 3: Creando commit..." -ForegroundColor Yellow
$commitMessage = "Preparado para deploy en Render.com"
git commit -m $commitMessage
Write-Host "[✓] Commit creado" -ForegroundColor Green

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Siguiente paso: Subir a GitHub" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. Ve a https://github.com y crea un nuevo repositorio" -ForegroundColor White
Write-Host "2. NO marques 'Initialize with README'" -ForegroundColor White
Write-Host "3. Copia la URL del repositorio (ej: https://github.com/TU_USUARIO/mathgame.git)" -ForegroundColor White
Write-Host ""
Write-Host "Luego ejecuta estos comandos (reemplaza TU_USUARIO y mathgame):" -ForegroundColor Yellow
Write-Host ""
Write-Host "  git branch -M main" -ForegroundColor Cyan
Write-Host "  git remote add origin https://github.com/TU_USUARIO/mathgame.git" -ForegroundColor Cyan
Write-Host "  git push -u origin main" -ForegroundColor Cyan
Write-Host ""
Write-Host "Si te pide autenticación, usa un Personal Access Token:" -ForegroundColor Yellow
Write-Host "  GitHub → Settings → Developer settings → Personal access tokens" -ForegroundColor White
Write-Host ""
Write-Host "Después de subir a GitHub, ve a Render.com para desplegar" -ForegroundColor Green
Write-Host ""

