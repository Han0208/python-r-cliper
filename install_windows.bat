@echo off
echo ================================================
echo   INSTALADOR DEL MODELO R-CLIPER
echo   Analisis de Precipitacion en Ciclones Tropicales
echo ================================================
echo.

:: Verificar si Python esta instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ ERROR: Python no esta instalado en este sistema.
    echo.
    echo Por favor instala Python 3.8+ desde: https://www.python.org/downloads/
    echo Asegurate de marcar "Add Python to PATH" durante la instalacion.
    pause
    exit /b 1
)

echo ✅ Python detectado:
python --version

echo.
echo 📦 Creando entorno virtual...
python -m venv venv
if errorlevel 1 (
    echo ❌ ERROR: No se pudo crear el entorno virtual.
    pause
    exit /b 1
)

echo ✅ Entorno virtual creado exitosamente.

echo.
echo 🔧 Activando entorno virtual...
call venv\Scripts\activate.bat

echo.
echo 📥 Instalando dependencias...
pip install --upgrade pip
pip install -r requirements.txt
if errorlevel 1 (
    echo ❌ ERROR: No se pudieron instalar las dependencias.
    echo Verifica que el archivo requirements.txt existe.
    pause
    exit /b 1
)

echo.
echo ✅ Instalacion completada exitosamente!
echo.
echo 📁 Estructura del proyecto:
echo   - Coloca tus archivos de datos en: historical_data\
echo   - Los resultados se guardaran en: result\
echo.
echo 🚀 Para ejecutar el modelo:
echo   1. Ejecuta: venv\Scripts\activate
echo   2. Ejecuta: python main.py
echo.
echo 📚 Lee el README.md para mas informacion.
echo.
pause