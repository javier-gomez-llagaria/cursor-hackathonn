#!/bin/bash

echo "========================================"
echo "Instalando MathGame - Dependencias"
echo "========================================"
echo ""

# Verificar si Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python no está instalado!"
    echo ""
    echo "Por favor instala Python desde: https://www.python.org/downloads/"
    exit 1
fi

echo "[1/3] Python encontrado:"
python3 --version
echo ""

echo "[2/3] Actualizando pip..."
python3 -m pip install --upgrade pip
echo ""

echo "[3/3] Instalando dependencias desde requirements.txt..."
python3 -m pip install -r requirements.txt
echo ""

echo "========================================"
echo "Instalación completada!"
echo "========================================"
echo ""
echo "Para ejecutar la aplicación, usa:"
echo "  python3 app.py"
echo ""

