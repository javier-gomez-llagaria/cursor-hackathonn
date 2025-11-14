# Script de instalación para MathGame
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Instalando MathGame - Dependencias" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Verificar si Python está instalado
try {
    $pythonVersion = python --version 2>&1
    Write-Host "[1/3] Python encontrado: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "ERROR: Python no está instalado!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Por favor instala Python desde: https://www.python.org/downloads/" -ForegroundColor Yellow
    Write-Host "Asegúrate de marcar 'Add Python to PATH' durante la instalación" -ForegroundColor Yellow
    Write-Host ""
    pause
    exit 1
}

Write-Host ""
Write-Host "[2/3] Actualizando pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip

Write-Host ""
Write-Host "[3/3] Instalando dependencias desde requirements.txt..." -ForegroundColor Yellow
python -m pip install -r requirements.txt

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Instalación completada!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Para ejecutar la aplicación, usa:" -ForegroundColor Yellow
Write-Host "  python app.py" -ForegroundColor White
Write-Host ""

