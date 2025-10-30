import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from math import radians, sin, cos, sqrt, atan2
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Set-ExecutionPolicy RemoteSigned -Scope Process

class RCliperModel:
    """
    Implementación del modelo R-CLIPER en Python
    Basado en Marks & DeMaria (2003) y tesis de Nashla Renata de la Parra Arias
    """
    
    def __init__(self):
        # Parámetros de la Tabla I.1 de la tesis
        self.a = [-1.10, -1.60, 64.5, 150.0]  # [T0, Tm, rm, re] - ordenadas
        self.b = [3.96, 4.80, -13.0, -16.0]   # [T0, Tm, rm, re] - pendientes
    
    def calcular_viento_normalizado(self, Vm):
        """
        Calcula el viento máximo normalizado U
        U = 1 + (Vm - 35)/33  (Ecuación 6 de la tesis)
        
        Args:
            Vm (float): Velocidad máxima del viento en nudos
            
        Returns:
            float: Viento normalizado (adimensional)
        """
        U = 1 + (Vm - 35) / 33
        return U
    
    def calcular_parametros(self, Vm):
        """
        Calcula los 4 parámetros del modelo en función del viento máximo
        T0, Tm, rm, re = f(U) según ecuaciones 2-5 de la tesis
        
        Args:
            Vm (float): Velocidad máxima del viento en nudos
            
        Returns:
            tuple: (T0, Tm, rm, re) - parámetros del modelo
        """
        U = self.calcular_viento_normalizado(Vm)
        
        # Calcula cada parámetro usando: parametro = a + b*U
        T0 = self.a[0] + self.b[0] * U  # Tasa de lluvia en r=0 (mm/día)
        Tm = self.a[1] + self.b[1] * U  # Tasa de lluvia máxima (mm/día)
        rm = self.a[2] + self.b[2] * U  # Radio de máxima precipitación (km)
        re = self.a[3] + self.b[3] * U  # Radio de decaimiento exponencial (km)
        
        return T0, Tm, rm, re
    
    def calcular_trmm(self, r, Vm):
        """
        Calcula la tasa de lluvia TRMM para un radio y viento dado
        
        Args:
            r (float): Radio desde el centro del ciclón (km)
            Vm (float): Velocidad máxima del viento (nudos)
            
        Returns:
            float: Tasa de lluvia (mm/día)
        """
        # Obtiene los 4 parámetros del modelo
        T0, Tm, rm, re = self.calcular_parametros(Vm)
        
        # Aplica la ecuación principal (1) de la tesis
        if r < rm:
            # Zona interior: variación lineal de r=0 a r=rm
            TRMM = T0 + (Tm - T0) * (r / rm)
        else:
            # Zona exterior: decaimiento exponencial para r >= rm
            TRMM = Tm * np.exp(-(r - rm) / re)
        
        # Asegura que no haya valores negativos de precipitación
        return max(TRMM, 0)
    
    def generar_campo_parametrico(self, Vm, radios):
        """
        Genera el campo paramétrico completo de precipitación
        
        Args:
            Vm (float): Velocidad máxima del viento (nudos)
            radios (array): Array de radios desde el centro (km)
            
        Returns:
            array: Array con tasas de lluvia para cada radio
        """
        precipitacion = np.zeros(len(radios))
        
        # Calcula TRMM para cada radio
        for i, r in enumerate(radios):
            precipitacion[i] = self.calcular_trmm(r, Vm)
            
        return precipitacion
    
    def graficar_perfil_radial(self, Vm):
        """
        Genera una gráfica del perfil radial de precipitación
        
        Args:
            Vm (float): Velocidad máxima del viento a simular
        """
        radios = np.arange(0, 501, 10)  # Radios de 0 a 500 km en pasos de 10 km
        precipitacion = self.generar_campo_parametrico(Vm, radios)
        
        plt.figure(figsize=(10, 6))
        plt.plot(radios, precipitacion, 'b-', linewidth=2)
        plt.grid(True, alpha=0.3)
        plt.xlabel('Radio desde el centro (km)')
        plt.ylabel('Tasa de lluvia (mm/día)')
        plt.title(f'Perfil R-CLIPER - Viento máximo: {Vm} nudos')
        
        # Marca el radio de máxima precipitación
        _, _, rm, _ = self.calcular_parametros(Vm)
        plt.axvline(x=rm, color='red', linestyle='--', linewidth=1, 
                   label=f'Radio máximo: {rm:.1f} km')
        plt.legend()
        plt.tight_layout()
        plt.show()

def calcular_distancia_km(lat1, lon1, lat2, lon2):
    """
    Calcula distancia entre dos puntos geográficos usando fórmula de Haversine
    
    Args:
        lat1, lon1: Coordenadas del punto 1 (grados decimales)
        lat2, lon2: Coordenadas del punto 2 (grados decimales)
        
    Returns:
        float: Distancia en kilómetros
    """
    R = 6371  # Radio de la Tierra en km
    
    # Convertir a radianes
