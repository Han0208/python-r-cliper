# =====================================================
# SCRIPT DE VALIDACIÓN DEL MODELO R-CLIPER
# Verifica cálculos y analiza comportamiento de las curvas
# =====================================================

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Coeficientes del modelo (mismos que en main.py)
a0, b0 = 0.5, 0.02   # T0
a1, b1 = 1.2, 0.05   # Tm
a2, b2 = 30, -0.2    # rm (km)
a3, b3 = 60, -0.3    # re (km)

def r_cliper_debug(Vm, r):
    """Versión con debug del modelo R-CLIPER"""
    T0 = a0 + b0 * Vm
    Tm = a1 + b1 * Vm
    rm = max(a2 + b2 * Vm, 1)
    re = max(a3 + b3 * Vm, 1)
    
    print(f"Para Vm = {Vm:.2f} m/s:")
    print(f"  T0 = {T0:.3f} mm/h")
    print(f"  Tm = {Tm:.3f} mm/h")
    print(f"  rm = {rm:.3f} km")
    print(f"  re = {re:.3f} km")
    print(f"  Ratio Tm/T0 = {Tm/T0:.3f}")
    print()
    
    # Calcular precipitación
    T = np.where(r < rm,
                 T0 + (Tm - T0) * (r / rm),  # Parte lineal
                 Tm * np.exp(-(r - rm) / re))  # Parte exponencial
    
    return T, (T0, Tm, rm, re)

# Crear rango de radios
r = np.linspace(0, 400, 400)

# Probar diferentes velocidades de viento
velocidades = [10, 20, 30, 40, 50]  # m/s (equivale a ~19, 39, 58, 78, 97 kt)

print("=== ANÁLISIS DE PARÁMETROS DEL MODELO R-CLIPER ===\n")

# Análisis de parámetros
parametros_df = []
for Vm in velocidades:
    T, params = r_cliper_debug(Vm, r)
    T0, Tm, rm, re = params
    
    parametros_df.append({
        'Vm_ms': Vm,
        'Vm_kt': Vm / 0.5144,  # Convertir a nudos
        'T0': T0,
        'Tm': Tm,
        'rm': rm,
        're': re,
        'Max_T': np.max(T),
        'T_at_0km': T[0],
        'T_at_50km': T[50] if len(T) > 50 else T[-1],
        'T_at_100km': T[100] if len(T) > 100 else T[-1]
    })

parametros_df = pd.DataFrame(parametros_df)
print("TABLA DE PARÁMETROS:")
print(parametros_df.round(3))
print()

# Verificar si hay problemas en los coeficientes
print("=== ANÁLISIS DE COEFICIENTES ===")
print(f"Coeficiente b2 = {b2} (negativo = rm decrece con Vm)")
print(f"Coeficiente b3 = {b3} (negativo = re decrece con Vm)")
print()

# Revisar rangos de rm y re
print("RANGOS DE PARÁMETROS:")
for Vm in velocidades:
    rm = max(a2 + b2 * Vm, 1)
    re = max(a3 + b3 * Vm, 1)
    print(f"Vm={Vm:2d} m/s: rm={rm:5.1f} km, re={re:5.1f} km")
print()

# Crear gráficas de validación
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))

# Gráfica 1: Perfiles de precipitación
for Vm in velocidades:
    T, params = r_cliper_debug(Vm, r)
    ax1.plot(r, T, label=f'Vm={Vm} m/s ({Vm/0.5144:.0f} kt)', linewidth=2)

ax1.set_xlabel('Radio (km)')
ax1.set_ylabel('Precipitación (mm/h)')
ax1.set_title('Perfiles de Precipitación R-CLIPER')
ax1.legend()
ax1.grid(True, alpha=0.3)
ax1.set_xlim(0, 200)

# Gráfica 2: Zoom en los primeros 100 km
for Vm in velocidades:
    T, params = r_cliper_debug(Vm, r)
    ax2.plot(r[:100], T[:100], label=f'Vm={Vm} m/s', linewidth=2)

ax2.set_xlabel('Radio (km)')
ax2.set_ylabel('Precipitación (mm/h)')
ax2.set_title('Zoom: Primeros 100 km')
ax2.legend()
ax2.grid(True, alpha=0.3)

# Gráfica 3: Parámetros vs Velocidad del viento
ax3_twin = ax3.twinx()

ax3.plot(parametros_df['Vm_ms'], parametros_df['T0'], 'o-', label='T0', color='blue')
ax3.plot(parametros_df['Vm_ms'], parametros_df['Tm'], 's-', label='Tm', color='red')
ax3_twin.plot(parametros_df['Vm_ms'], parametros_df['rm'], '^-', label='rm', color='green')
ax3_twin.plot(parametros_df['Vm_ms'], parametros_df['re'], 'v-', label='re', color='orange')

ax3.set_xlabel('Velocidad del viento (m/s)')
ax3.set_ylabel('Precipitación (mm/h)', color='black')
ax3_twin.set_ylabel('Radio (km)', color='black')
ax3.set_title('Parámetros vs Velocidad del Viento')

# Combinar leyendas
lines1, labels1 = ax3.get_legend_handles_labels()
lines2, labels2 = ax3_twin.get_legend_handles_labels()
ax3.legend(lines1 + lines2, labels1 + labels2, loc='upper left')
ax3.grid(True, alpha=0.3)

# Gráfica 4: Análisis de sensibilidad
# Verificar cómo cambia la forma de la curva
ratios = []
for Vm in velocidades:
    T, params = r_cliper_debug(Vm, r)
    T0, Tm, rm, re = params
    
    # Calcular algunos ratios importantes
    ratio_centro_max = T0 / Tm if Tm > 0 else 0
    ratio_50km_max = (T[50] / Tm) if len(T) > 50 and Tm > 0 else 0
    
    ratios.append({
        'Vm': Vm,
        'Centro/Max': ratio_centro_max,
        '50km/Max': ratio_50km_max,
        'Pendiente_inicial': (Tm - T0) / rm if rm > 0 else 0
    })

ratios_df = pd.DataFrame(ratios)

ax4.plot(ratios_df['Vm'], ratios_df['Centro/Max'], 'o-', label='T(0)/Tmax')
ax4.plot(ratios_df['Vm'], ratios_df['50km/Max'], 's-', label='T(50km)/Tmax')
ax4.plot(ratios_df['Vm'], ratios_df['Pendiente_inicial']/10, '^-', label='Pendiente/10')

ax4.set_xlabel('Velocidad del viento (m/s)')
ax4.set_ylabel('Ratio')
ax4.set_title('Análisis de Forma de Curvas')
ax4.legend()
ax4.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('validacion_modelo_rcliper.png', dpi=300, bbox_inches='tight')
plt.show()

# Análisis de problemas potenciales
print("=== ANÁLISIS DE PROBLEMAS POTENCIALES ===")

# 1. Verificar si rm se vuelve muy pequeño
rm_min = min([max(a2 + b2 * Vm, 1) for Vm in velocidades])
print(f"1. Radio mínimo rm = {rm_min:.1f} km")

# 2. Verificar si re se vuelve muy pequeño  
re_min = min([max(a3 + b3 * Vm, 1) for Vm in velocidades])
print(f"2. Radio mínimo re = {re_min:.1f} km")

# 3. Verificar la relación T0/Tm
ratios_T = [parametros_df.iloc[i]['T0']/parametros_df.iloc[i]['Tm'] for i in range(len(parametros_df))]
print(f"3. Rango de T0/Tm: {min(ratios_T):.3f} - {max(ratios_T):.3f}")

# 4. Verificar pendientes iniciales
pendientes = [(parametros_df.iloc[i]['Tm'] - parametros_df.iloc[i]['T0'])/parametros_df.iloc[i]['rm'] 
              for i in range(len(parametros_df))]
print(f"4. Rango de pendientes iniciales: {min(pendientes):.4f} - {max(pendientes):.4f} mm/h/km")

# 5. Verificar si las curvas son demasiado similares
print(f"\n5. SIMILITUD DE CURVAS:")
for i in range(len(velocidades)-1):
    Vm1, Vm2 = velocidades[i], velocidades[i+1]
    T1, _ = r_cliper_debug(Vm1, r)
    T2, _ = r_cliper_debug(Vm2, r)
    
    # Calcular correlación entre curvas
    correlacion = np.corrcoef(T1[:100], T2[:100])[0,1]
    
    # Calcular diferencia promedio
    diff_promedio = np.mean(np.abs(T2[:100] - T1[:100]))
    
    print(f"   Vm {Vm1} vs {Vm2} m/s: Correlación = {correlacion:.4f}, Diff promedio = {diff_promedio:.3f} mm/h")

print("\n=== RECOMENDACIONES ===")
if min(ratios_T) > 0.8:
    print("⚠️  ADVERTENCIA: T0 y Tm son muy similares (pendientes suaves)")
if max(pendientes) - min(pendientes) < 0.001:
    print("⚠️  ADVERTENCIA: Pendientes iniciales muy similares entre velocidades")
if rm_min < 5:
    print("⚠️  ADVERTENCIA: Radio rm muy pequeño para vientos altos")
if re_min < 10:
    print("⚠️  ADVERTENCIA: Radio re muy pequeño para vientos altos")
    
print("\n✅ Validación completada. Revisa el archivo 'validacion_modelo_rcliper.png'")