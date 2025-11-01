@echo off
echo ================================================
echo   MODELO R-CLIPER - Ejecutor Rapido
echo ================================================
echo.

:: Verificar si existe el entorno virtual
if not exist "venv\Scripts\activate.bat" (
    echo ❌ ERROR: Entorno virtual no encontrado.
    echo.
    echo Ejecuta primero: install_windows.bat
    pause
    exit /b 1
)

:: Activar entorno virtual
echo 🔧 Activando entorno virtual...
call venv\Scripts\activate.bat

:: Verificar si existe main.py
if not exist "main.py" (
    echo ❌ ERROR: main.py no encontrado.
    pause
    exit /b 1
)

:: Verificar si existe la carpeta de datos
if not exist "historical_data" (
    echo ❌ ERROR: Carpeta 'historical_data' no encontrada.
    echo.
    echo Crea la carpeta y coloca tus archivos de datos ahi.
    pause
    exit /b 1
)

echo.
echo 🚀 Ejecutando modelo R-CLIPER...
echo.
python main.py

echo.
echo ✅ Ejecucion completada!
echo.
echo 📊 Revisa los resultados en la carpeta 'result\'
pause