@echo off
echo ========================================
echo Instalando MathGame - Dependencias
echo ========================================
echo.

REM Verificar si Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python no esta instalado!
    echo.
    echo Por favor instala Python desde: https://www.python.org/downloads/
    echo Asegurate de marcar "Add Python to PATH" durante la instalacion
    echo.
    pause
    exit /b 1
)

echo [1/3] Python encontrado:
python --version
echo.

echo [2/3] Actualizando pip...
python -m pip install --upgrade pip
echo.

echo [3/3] Instalando dependencias desde requirements.txt...
python -m pip install -r requirements.txt
echo.

echo ========================================
echo Instalacion completada!
echo ========================================
echo.
echo Para ejecutar la aplicacion, usa:
echo   python app.py
echo.
pause

