#!/bin/bash

echo "================================================"
echo "  MODELO R-CLIPER - Ejecutor Rapido"
echo "================================================"
echo

# Verificar si existe el entorno virtual
if [ ! -f "venv/bin/activate" ]; then
    echo "❌ ERROR: Entorno virtual no encontrado."
    echo
    echo "Ejecuta primero: ./install_unix.sh"
    exit 1
fi

# Activar entorno virtual
echo "🔧 Activando entorno virtual..."
source venv/bin/activate

# Verificar si existe main.py
if [ ! -f "main.py" ]; then
    echo "❌ ERROR: main.py no encontrado."
    exit 1
fi

# Verificar si existe la carpeta de datos
if [ ! -d "historical_data" ]; then
    echo "❌ ERROR: Carpeta 'historical_data' no encontrada."
    echo
    echo "Crea la carpeta y coloca tus archivos de datos ahi:"
    echo "mkdir historical_data"
    exit 1
fi

echo
echo "🚀 Ejecutando modelo R-CLIPER..."
echo
python main.py

echo
echo "✅ Ejecucion completada!"
echo
echo "📊 Revisa los resultados en la carpeta 'result/'"