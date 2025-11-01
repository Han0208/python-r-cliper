# =====================================================
# Modelo R-CLIPER aplicado a datos históricos de Cuba
# Autor: Nashla R. De La Parra Arias
# Adaptado por: ChatGPT
# =====================================================

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# =====================================================
# 1️⃣ CONFIGURACIÓN INICIAL
# =====================================================

# Carpeta con tus archivos CSV
input_folder = "daD:\Tesis\tesis_carlos\Datos Historicos/"       # <-- Cambia por tu ruta
output_folder = "D:\Tesis\tesis_carlos\Resultados/"       # Carpeta de salida

os.makedirs(output_folder, exist_ok=True)

# Si tus vientos están en nudos (kt), convertir a m/s (1 kt = 0.5144 m/s)
convertir_kt_a_ms = True

# =====================================================
# 2️⃣ COEFICIENTES DEL MODELO R-CLIPER
# =====================================================
# (Usa los coeficientes que ajustaste para México o calibra para Cuba)
a0, b0 = 0.5, 0.02   # T0
a1, b1 = 1.2, 0.05   # Tm
a2, b2 = 30, -0.2    # rm (km)
a3, b3 = 60, -0.3    # re (km)

# =====================================================
# 3️⃣ FUNCIÓN DEL MODELO R-CLIPER
# =====================================================
def r_cliper(Vm, r):
    """Calcula la tasa de precipitación (mm/h) para un viento máximo Vm (m/s) y radios r (km)."""
    T0 = a0 + b0 * Vm
    Tm = a1 + b1 * Vm
    rm = max(a2 + b2 * Vm, 1)   # evitar valores negativos
    re = max(a3 + b3 * Vm, 1)

    T = np.where(r < rm,
                 T0 + (Tm - T0) * (r / rm),
                 Tm * np.exp(-(r - rm) / re))
    return T, (T0, Tm, rm, re)

# =====================================================
# 4️⃣ LECTURA Y PROCESAMIENTO DE ARCHIVOS
# =====================================================
files = [f for f in os.listdir(input_folder) if f.endswith('.csv')]

for file in files:
    path = os.path.join(input_folder, file)
    df = pd.read_csv(path)

    # Asegurar nombres coherentes
    df.columns = ["Fecha", "Time", "RMAX", "X", "Y", "VMAX", "PC"]

    # Convertir VMAX a m/s si está en nudos
    if convertir_kt_a_ms:
        df["VMAX"] = df["VMAX"] * 0.5144

    # Cálculo de precipitación para cada registro
    r = np.linspace(0, 400, 400)  # radios (km)
    resultados = []

    for i, row in df.iterrows():
        Vm = row["VMAX"]
        T, params = r_cliper(Vm, r)
        resultados.append({
            "Fecha": row["Fecha"],
            "Hora": row["Time"],
            "VMAX_m_s": Vm,
            "T0": params[0],
            "Tm": params[1],
            "rm_km": params[2],
            "re_km": params[3],
            "Pico_lluvia_mm_h": np.max(T)
        })

    resultados_df = pd.DataFrame(resultados)

    # Guardar resultados numéricos
    nombre_evento = os.path.splitext(file)[0]
    resultados_df.to_csv(os.path.join(output_folder, f"{nombre_evento}_RCLIPER_resultados.csv"), index=False)

    # Perfil de lluvia promedio (Vm medio)
    Vm_mean = df["VMAX"].mean()
    T_prom, _ = r_cliper(Vm_mean, r)

    plt.figure(figsize=(8,5))
    plt.plot(r, T_prom, lw=2, color='teal')
    plt.title(f"Perfil radial promedio de lluvia - {nombre_evento}")
    plt.xlabel("Distancia radial (km)")
    plt.ylabel("Precipitación (mm/h)")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(output_folder, f"{nombre_evento}_perfil_promedio.png"))
    plt.close()

    print(f"✅ {nombre_evento} procesado correctamente ({len(df)} registros).")

print("\n=== Procesamiento completado para todos los ciclones ===")
