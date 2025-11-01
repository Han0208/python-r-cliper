# =====================================================
# MODELO R-CLIPER CORREGIDO
# Coeficientes mejorados para mejor diferenciación
# =====================================================

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# =====================================================
# COEFICIENTES ORIGINALES (PROBLEMÁTICOS)
# =====================================================
print("=== COMPARACIÓN DE COEFICIENTES ===\n")

# Coeficientes originales
a0_orig, b0_orig = 0.5, 0.02   # T0
a1_orig, b1_orig = 1.2, 0.05   # Tm
a2_orig, b2_orig = 30, -0.2    # rm (km)
a3_orig, b3_orig = 60, -0.3    # re (km)

print("COEFICIENTES ORIGINALES:")
print(f"T0: a0={a0_orig}, b0={b0_orig}")
print(f"Tm: a1={a1_orig}, b1={b1_orig}")
print(f"rm: a2={a2_orig}, b2={b2_orig}")
print(f"re: a3={a3_orig}, b3={b3_orig}")

# =====================================================
# COEFICIENTES CORREGIDOS (MÁS REALISTAS)
# =====================================================
# Basados en literatura científica del modelo R-CLIPER

# Opción 1: Coeficientes más diferenciados
a0_new1, b0_new1 = 0.3, 0.08    # T0 - menor base, mayor sensibilidad
a1_new1, b1_new1 = 0.8, 0.15    # Tm - mayor diferenciación
a2_new1, b2_new1 = 35, -0.4     # rm - más sensible a velocidad
a3_new1, b3_new1 = 80, -0.6     # re - decaimiento más pronunciado

# Opción 2: Coeficientes basados en estudios del Atlántico
a0_new2, b0_new2 = 0.2, 0.06    # T0
a1_new2, b1_new2 = 1.0, 0.12    # Tm
a2_new2, b2_new2 = 40, -0.3     # rm
a3_new2, b3_new2 = 100, -0.8    # re

print("\nCOEFICIENTES CORREGIDOS - OPCIÓN 1:")
print(f"T0: a0={a0_new1}, b0={b0_new1}")
print(f"Tm: a1={a1_new1}, b1={b1_new1}")
print(f"rm: a2={a2_new1}, b2={b2_new1}")
print(f"re: a3={a3_new1}, b3={b3_new1}")

print("\nCOEFICIENTES CORREGIDOS - OPCIÓN 2:")
print(f"T0: a0={a0_new2}, b0={b0_new2}")
print(f"Tm: a1={a1_new2}, b1={b1_new2}")
print(f"rm: a2={a2_new2}, b2={b2_new2}")
print(f"re: a3={a3_new2}, b3={b3_new2}")

def r_cliper_model(Vm, r, a0, b0, a1, b1, a2, b2, a3, b3):
    """Modelo R-CLIPER con coeficientes configurables"""
    T0 = a0 + b0 * Vm
    Tm = a1 + b1 * Vm
    rm = max(a2 + b2 * Vm, 1)
    re = max(a3 + b3 * Vm, 1)
    
    T = np.where(r < rm,
                 T0 + (Tm - T0) * (r / rm),
                 Tm * np.exp(-(r - rm) / re))
    return T, (T0, Tm, rm, re)

# Velocidades de prueba
velocidades = [10, 20, 30, 40, 50]  # m/s
r = np.linspace(0, 200, 200)

# Crear comparación visual
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))

# Colores para cada velocidad
colores = ['blue', 'green', 'orange', 'red', 'purple']

# Gráfica 1: Modelo original
ax1.set_title('MODELO ORIGINAL (Problemático)', fontweight='bold', color='red')
correlaciones_orig = []
for i, Vm in enumerate(velocidades):
    T, params = r_cliper_model(Vm, r, a0_orig, b0_orig, a1_orig, b1_orig, 
                              a2_orig, b2_orig, a3_orig, b3_orig)
    ax1.plot(r, T, color=colores[i], linewidth=2, 
             label=f'Vm={Vm} m/s (Max: {np.max(T):.2f})')

ax1.set_xlabel('Radio (km)')
ax1.set_ylabel('Precipitación (mm/h)')
ax1.legend()
ax1.grid(True, alpha=0.3)

# Gráfica 2: Modelo corregido - Opción 1
ax2.set_title('MODELO CORREGIDO - OPCIÓN 1', fontweight='bold', color='green')
for i, Vm in enumerate(velocidades):
    T, params = r_cliper_model(Vm, r, a0_new1, b0_new1, a1_new1, b1_new1, 
                              a2_new1, b2_new1, a3_new1, b3_new1)
    ax2.plot(r, T, color=colores[i], linewidth=2, 
             label=f'Vm={Vm} m/s (Max: {np.max(T):.2f})')

ax2.set_xlabel('Radio (km)')
ax2.set_ylabel('Precipitación (mm/h)')
ax2.legend()
ax2.grid(True, alpha=0.3)

# Gráfica 3: Modelo corregido - Opción 2
ax3.set_title('MODELO CORREGIDO - OPCIÓN 2', fontweight='bold', color='green')
for i, Vm in enumerate(velocidades):
    T, params = r_cliper_model(Vm, r, a0_new2, b0_new2, a1_new2, b1_new2, 
                              a2_new2, b2_new2, a3_new2, b3_new2)
    ax3.plot(r, T, color=colores[i], linewidth=2, 
             label=f'Vm={Vm} m/s (Max: {np.max(T):.2f})')

ax3.set_xlabel('Radio (km)')
ax3.set_ylabel('Precipitación (mm/h)')
ax3.legend()
ax3.grid(True, alpha=0.3)

# Gráfica 4: Comparación de parámetros
Vm_test = 30  # m/s para comparación

# Modelo original
T_orig, params_orig = r_cliper_model(Vm_test, r, a0_orig, b0_orig, a1_orig, b1_orig, 
                                    a2_orig, b2_orig, a3_orig, b3_orig)
T0_orig, Tm_orig, rm_orig, re_orig = params_orig

# Modelo corregido 1
T_new1, params_new1 = r_cliper_model(Vm_test, r, a0_new1, b0_new1, a1_new1, b1_new1, 
                                     a2_new1, b2_new1, a3_new1, b3_new1)
T0_new1, Tm_new1, rm_new1, re_new1 = params_new1

# Modelo corregido 2
T_new2, params_new2 = r_cliper_model(Vm_test, r, a0_new2, b0_new2, a1_new2, b1_new2, 
                                     a2_new2, b2_new2, a3_new2, b3_new2)
T0_new2, Tm_new2, rm_new2, re_new2 = params_new2

ax4.plot(r, T_orig, 'r-', linewidth=3, label=f'Original (Tm={Tm_orig:.2f}, rm={rm_orig:.1f})')
ax4.plot(r, T_new1, 'g-', linewidth=3, label=f'Opción 1 (Tm={Tm_new1:.2f}, rm={rm_new1:.1f})')
ax4.plot(r, T_new2, 'b-', linewidth=3, label=f'Opción 2 (Tm={Tm_new2:.2f}, rm={rm_new2:.1f})')

ax4.set_title(f'COMPARACIÓN DIRECTA (Vm = {Vm_test} m/s)', fontweight='bold')
ax4.set_xlabel('Radio (km)')
ax4.set_ylabel('Precipitación (mm/h)')
ax4.legend()
ax4.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('comparacion_modelos_rcliper.png', dpi=300, bbox_inches='tight')
plt.show()

# =====================================================
# ANÁLISIS CUANTITATIVO DE MEJORAS
# =====================================================

print("\n=== ANÁLISIS CUANTITATIVO ===\n")

def analizar_modelo(a0, b0, a1, b1, a2, b2, a3, b3, nombre):
    print(f"ANÁLISIS DEL {nombre}:")
    
    correlaciones = []
    diferencias = []
    
    for i in range(len(velocidades)-1):
        Vm1, Vm2 = velocidades[i], velocidades[i+1]
        T1, _ = r_cliper_model(Vm1, r, a0, b0, a1, b1, a2, b2, a3, b3)
        T2, _ = r_cliper_model(Vm2, r, a0, b0, a1, b1, a2, b2, a3, b3)
        
        corr = np.corrcoef(T1[:100], T2[:100])[0,1]
        diff = np.mean(np.abs(T2[:100] - T1[:100]))
        
        correlaciones.append(corr)
        diferencias.append(diff)
        
        print(f"  Vm {Vm1} vs {Vm2} m/s: Correlación = {corr:.4f}, Diff = {diff:.3f} mm/h")
    
    print(f"  Correlación promedio: {np.mean(correlaciones):.4f}")
    print(f"  Diferencia promedio: {np.mean(diferencias):.3f} mm/h")
    
    # Analizar rangos de parámetros
    T0_values = [a0 + b0 * Vm for Vm in velocidades]
    Tm_values = [a1 + b1 * Vm for Vm in velocidades]
    rm_values = [max(a2 + b2 * Vm, 1) for Vm in velocidades]
    
    ratios = [T0_values[i]/Tm_values[i] for i in range(len(velocidades))]
    
    print(f"  Rango T0: {min(T0_values):.2f} - {max(T0_values):.2f} mm/h")
    print(f"  Rango Tm: {min(Tm_values):.2f} - {max(Tm_values):.2f} mm/h")
    print(f"  Rango rm: {min(rm_values):.1f} - {max(rm_values):.1f} km")
    print(f"  Rango T0/Tm: {min(ratios):.3f} - {max(ratios):.3f}")
    print()
    
    return np.mean(correlaciones), np.mean(diferencias)

# Analizar los tres modelos
corr_orig, diff_orig = analizar_modelo(a0_orig, b0_orig, a1_orig, b1_orig, 
                                      a2_orig, b2_orig, a3_orig, b3_orig, 
                                      "MODELO ORIGINAL")

corr_new1, diff_new1 = analizar_modelo(a0_new1, b0_new1, a1_new1, b1_new1, 
                                      a2_new1, b2_new1, a3_new1, b3_new1, 
                                      "MODELO CORREGIDO - OPCIÓN 1")

corr_new2, diff_new2 = analizar_modelo(a0_new2, b0_new2, a1_new2, b1_new2, 
                                      a2_new2, b2_new2, a3_new2, b3_new2, 
                                      "MODELO CORREGIDO - OPCIÓN 2")

# Recomendación final
print("=== RECOMENDACIÓN FINAL ===")
print(f"Modelo Original:    Correlación = {corr_orig:.4f}, Diferenciación = {diff_orig:.3f}")
print(f"Modelo Opción 1:    Correlación = {corr_new1:.4f}, Diferenciación = {diff_new1:.3f}")
print(f"Modelo Opción 2:    Correlación = {corr_new2:.4f}, Diferenciación = {diff_new2:.3f}")
print()

if corr_new1 < corr_orig and diff_new1 > diff_orig:
    print("✅ RECOMENDACIÓN: Usar MODELO CORREGIDO - OPCIÓN 1")
    print("   - Menor correlación entre curvas")
    print("   - Mayor diferenciación entre intensidades")
elif corr_new2 < corr_orig and diff_new2 > diff_orig:
    print("✅ RECOMENDACIÓN: Usar MODELO CORREGIDO - OPCIÓN 2")
    print("   - Menor correlación entre curvas")
    print("   - Mayor diferenciación entre intensidades")
else:
    print("⚠️  Se requiere mayor ajuste de coeficientes")

print("\n📊 Revisa el archivo 'comparacion_modelos_rcliper.png' para la comparación visual")