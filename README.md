# Modelo R-CLIPER para Análisis de Precipitación en Ciclones Tropicales

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## 📋 Descripción

Este proyecto implementa el modelo **R-CLIPER** (Rainfall-Climatology and Persistence) para analizar y predecir la distribución radial de precipitación en ciclones tropicales basándose en datos históricos de trayectorias de huracanes en Cuba.

El modelo calcula tasas de precipitación en función de:
- Velocidad máxima sostenida del viento (VMAX)
- Distancia radial desde el centro del ciclón
- Parámetros climáticos calibrados para la región

## 🚀 Características

- ✅ Procesamiento automático de múltiples archivos de datos históricos
- ✅ Soporte para formatos CSV y Excel (.xlsx, .xls)
- ✅ Conversión automática de unidades (nudos a m/s)
- ✅ Generación de perfiles radiales de precipitación
- ✅ Visualizaciones automáticas con matplotlib
- ✅ Exportación de resultados en formato CSV
- ✅ Configuración flexible de parámetros del modelo

## 🔧 Instalación

### Opción 1: Script de instalación automática

**Windows:**
```bash
install_windows.bat
```

**Linux/macOS:**
```bash
chmod +x install_unix.sh
./install_unix.sh
```

### Opción 2: Instalación manual

1. **Clonar el repositorio:**
```bash
git clone https://github.com/Han0208/tesis_carlos.git
cd tesis_carlos
```

2. **Crear entorno virtual:**
```bash
# Python 3.8+
python -m venv venv

# Activar entorno virtual
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate
```

3. **Instalar dependencias:**
```bash
pip install -r requirements.txt
```

## 📁 Estructura del Proyecto

```
tesis_carlos/
├── main.py                    # Script principal del modelo R-CLIPER
├── requirements.txt           # Dependencias de Python
├── README.md                 # Este archivo
├── install_windows.bat       # Script de instalación para Windows
├── install_unix.sh          # Script de instalación para Linux/macOS
├── historical_data/         # Carpeta con datos de entrada
│   ├── TC_0002_track.xlsx   # Archivos de trayectorias de ciclones
│   ├── TC_0003_track.xlsx
│   └── ...
└── result/                  # Carpeta de resultados (se crea automáticamente)
    ├── TC_0002_track_RCLIPER_resultados.csv
    ├── TC_0002_track_perfil_promedio.png
    └── ...
```

## 📊 Formato de Datos de Entrada

Los archivos de datos deben contener al menos las siguientes columnas en orden:

| Columna | Descripción | Unidades |
|---------|-------------|----------|
| FECHA_REAL | Fecha del registro | Fecha/hora |
| TIME | Tiempo en formato numérico | Días |
| RMAX | Radio de vientos máximos | km |
| X | Longitud | Grados |
| Y | Latitud | Grados |
| VMAX | Velocidad máxima sostenida | kt o m/s |
| PC | Presión central | hPa |

**Nota:** El script selecciona automáticamente las primeras 7 columnas y convierte las velocidades de nudos a m/s si está habilitado.

## 🎯 Uso

1. **Preparar los datos:**
   - Colocar archivos CSV o Excel en la carpeta `historical_data/`
   - Asegurar que tengan el formato correcto

2. **Ejecutar el modelo:**
```bash
# Activar entorno virtual si no está activo
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# Ejecutar el script
python main.py
```

3. **Revisar resultados:**
   - Los archivos CSV con resultados se guardan en `result/`
   - Las gráficas PNG se generan automáticamente

## ⚙️ Configuración del Modelo

El modelo R-CLIPER utiliza los siguientes parámetros configurables en `main.py`:

```python
# Parámetros del modelo
a0, b0 = 0.5, 0.02   # T0 (precipitación en el centro)
a1, b1 = 1.2, 0.05   # Tm (precipitación máxima)
a2, b2 = 30, -0.2    # rm (radio de precipitación máxima)
a3, b3 = 60, -0.3    # re (radio de decaimiento exponencial)

# Configuración de conversión
convertir_kt_a_ms = True  # Convertir velocidades de nudos a m/s
```

### Ecuaciones del Modelo

El modelo calcula la tasa de precipitación T(r) como:

- **T₀ = a₀ + b₀ × Vₘ** (precipitación en el centro)
- **Tₘ = a₁ + b₁ × Vₘ** (precipitación máxima)
- **rₘ = a₂ + b₂ × Vₘ** (radio de precipitación máxima)
- **rₑ = a₃ + b₃ × Vₘ** (radio de decaimiento exponencial)

Para r < rₘ: **T(r) = T₀ + (Tₘ - T₀) × (r/rₘ)**

Para r ≥ rₘ: **T(r) = Tₘ × exp(-(r-rₘ)/rₑ)**

## 📈 Resultados

El script genera para cada ciclón:

1. **Archivo CSV** con:
   - Fecha y hora de cada observación
   - Velocidad máxima en m/s
   - Parámetros del modelo (T₀, Tₘ, rₘ, rₑ)
   - Pico de precipitación calculado

2. **Gráfica PNG** con:
   - Perfil radial promedio de precipitación
   - Distancia desde el centro (0-400 km)
   - Tasa de precipitación (mm/h)

## 🔍 Ejemplo de Salida

```
Archivos encontrados: ['TC_0002_track.xlsx', 'TC_0003_track.xlsx', ...]
Procesando TC_0002_track.xlsx - Shape: (78, 23)
✅ TC_0002_track procesado correctamente (78 registros).
...
=== Procesamiento completado para todos los ciclones ===
```

## 🛠️ Dependencias

- **Python 3.8+**
- **pandas**: Manipulación de datos
- **numpy**: Cálculos numéricos
- **matplotlib**: Generación de gráficas
- **openpyxl**: Lectura de archivos Excel

## 📝 Notas Importantes

- El script procesa automáticamente todos los archivos CSV/Excel en `historical_data/`
- Las velocidades se asumen en nudos por defecto (se pueden cambiar en configuración)
- Los resultados se sobrescriben si ya existen archivos con el mismo nombre
- Se requiere Python 3.8 o superior para compatibilidad completa

## 🤝 Contribuciones

1. Fork el proyecto
2. Crear una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles.

## 👥 Autores

- **Nashla R. De La Parra Arias** - *Desarrollo del modelo original*
- **ChatGPT** - *Adaptación y optimización del código*

## 📞 Soporte

Si tienes problemas o preguntas:

1. Revisa la documentación
2. Verifica que tengas Python 3.8+ instalado
3. Asegúrate de que las dependencias estén instaladas correctamente
4. Abre un issue en GitHub con detalles del problema

---

**⚡ ¡Listo para analizar ciclones tropicales!** 🌪️