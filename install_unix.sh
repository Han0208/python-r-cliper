#!/bin/bash

echo "================================================"
echo "  INSTALADOR DEL MODELO R-CLIPER"
echo "  Analisis de Precipitacion en Ciclones Tropicales"
echo "================================================"
echo

# Verificar si Python esta instalado
if ! command -v python3 &> /dev/null; then
    if ! command -v python &> /dev/null; then
        echo "❌ ERROR: Python no esta instalado en este sistema."
        echo
        echo "Por favor instala Python 3.8+ usando:"
        echo "  Ubuntu/Debian: sudo apt install python3 python3-pip python3-venv"
        echo "  CentOS/RHEL:   sudo yum install python3 python3-pip"
        echo "  macOS:         brew install python3"
        echo "  o descarga desde: https://www.python.org/downloads/"
        exit 1
    else
        PYTHON_CMD="python"
    fi
else
    PYTHON_CMD="python3"
fi

echo "✅ Python detectado:"
$PYTHON_CMD --version

# Verificar version de Python
PYTHON_VERSION=$($PYTHON_CMD -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
REQUIRED_VERSION="3.8"

if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" != "$REQUIRED_VERSION" ]; then
    echo "❌ ERROR: Se requiere Python 3.8 o superior. Version actual: $PYTHON_VERSION"
    exit 1
fi

echo
echo "📦 Creando entorno virtual..."
$PYTHON_CMD -m venv venv
if [ $? -ne 0 ]; then
    echo "❌ ERROR: No se pudo crear el entorno virtual."
    echo "Intenta instalar python3-venv: sudo apt install python3-venv"
    exit 1
fi

echo "✅ Entorno virtual creado exitosamente."

echo
echo "🔧 Activando entorno virtual..."
source venv/bin/activate

echo
echo "📥 Instalando dependencias..."
pip install --upgrade pip
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "❌ ERROR: No se pudieron instalar las dependencias."
    echo "Verifica que el archivo requirements.txt existe."
    exit 1
fi

echo
echo "✅ Instalacion completada exitosamente!"
echo
echo "📁 Estructura del proyecto:"
echo "  - Coloca tus archivos de datos en: historical_data/"
echo "  - Los resultados se guardaran en: result/"
echo
echo "🚀 Para ejecutar el modelo:"
echo "  1. Ejecuta: source venv/bin/activate"
echo "  2. Ejecuta: python main.py"
echo
echo "📚 Lee el README.md para mas informacion."
echo