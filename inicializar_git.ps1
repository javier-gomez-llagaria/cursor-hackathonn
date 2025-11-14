# Script para inicializar Git en el repositorio
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Inicializando Repositorio Git" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Verificar si Git está instalado
try {
    $gitVersion = git --version 2>&1
    Write-Host "[✓] Git encontrado: $gitVersion" -ForegroundColor Green
} catch {
    Write-Host "[✗] ERROR: Git no está instalado" -ForegroundColor Red
    Write-Host ""
    Write-Host "Por favor instala Git primero:" -ForegroundColor Yellow
    Write-Host "1. Ve a: https://git-scm.com/download/win" -ForegroundColor White
    Write-Host "2. Descarga e instala Git" -ForegroundColor White
    Write-Host "3. Reinicia PowerShell" -ForegroundColor White
    Write-Host "4. Ejecuta este script de nuevo" -ForegroundColor White
    Write-Host ""
    pause
    exit 1
}

Write-Host ""
Write-Host "Inicializando repositorio..." -ForegroundColor Yellow

# Inicializar Git
if (Test-Path ".git") {
    Write-Host "[!] Ya existe un repositorio Git" -ForegroundColor Yellow
    $response = Read-Host "¿Quieres reinicializarlo? (s/n)"
    if ($response -eq "s") {
        Remove-Item -Recurse -Force .git
        git init
        Write-Host "[✓] Repositorio reinicializado" -ForegroundColor Green
    }
} else {
    git init
    Write-Host "[✓] Repositorio inicializado" -ForegroundColor Green
}

Write-Host ""
Write-Host "Agregando archivos..." -ForegroundColor Yellow
git add .
Write-Host "[✓] Archivos agregados" -ForegroundColor Green

Write-Host ""
Write-Host "Creando commit inicial..." -ForegroundColor Yellow
git commit -m "Initial commit - MathGame platform"
Write-Host "[✓] Commit creado" -ForegroundColor Green

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Repositorio Git listo!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Siguiente paso: Subir a GitHub" -ForegroundColor Yellow
Write-Host ""
Write-Host "1. Crea un repositorio en GitHub (https://github.com)" -ForegroundColor White
Write-Host "2. Luego ejecuta:" -ForegroundColor White
Write-Host ""
Write-Host "   git branch -M main" -ForegroundColor Cyan
Write-Host "   git remote add origin https://github.com/TU_USUARIO/mathgame.git" -ForegroundColor Cyan
Write-Host "   git push -u origin main" -ForegroundColor Cyan
Write-Host ""
Write-Host "Ver SETUP_GIT.md para más detalles" -ForegroundColor Yellow
Write-Host ""

