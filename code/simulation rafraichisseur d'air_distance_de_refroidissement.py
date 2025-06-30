# -*- coding: utf-8 -*-
"""
Created on Mon Jun 30 13:41:23 2025

@author: tetique
"""

import numpy as np
import matplotlib.pyplot as plt

def simulate_air_cooling(CFM=45, diameter=0.4, h=10, 
                         T_amb=30, T_out=27, length=0.5, steps=100):
    """
    Simule la remontée en température d'un jet d'air refroidi sur une distance donnée.

    Paramètres :
    - CFM : débit d'air en Cubic Feet per Minute
    - diameter : diamètre du conduit (m)
    - h : coefficient de convection (W/m²·K)
    - T_amb : température ambiante (°C)
    - T_out : température à la sortie de l’échangeur (°C)
    - length : distance à simuler (m)
    - steps : nombre de points de discrétisation
    """
    # Constantes physiques
    rho_air = 1.2      # kg/m³
    c_air = 1000       # J/kg·K

    # Conversion du débit CFM -> m³/s
    m3_per_s = CFM * 0.0283 / 60
    m_dot_air = m3_per_s * rho_air  # kg/s

    # Périmètre du jet cylindrique
    P = np.pi * diameter  # périmètre (m)

    # Discrétisation de la distance
    x = np.linspace(0, length, steps)

    # Formule exponentielle : modèle 1D simplifié
    factor = -h * P / (m_dot_air * c_air)
    T_x = T_amb - (T_amb - T_out) * np.exp(factor * x)

    # Affichage
    plt.figure(figsize=(8, 4))
    plt.plot(x, T_x, label="Température de l'air", color='blue')
    plt.axhline(T_amb, color='gray', linestyle='--', label=f"Air ambiant ({T_amb} °C)")
    plt.axhline(T_out, color='green', linestyle=':', label=f"Sortie échangeur ({T_out} °C)")
    plt.xlabel("Distance depuis l'échangeur (m)")
    plt.ylabel("Température (°C)")
    plt.title("Évolution de la température de l'air après l'échangeur")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

# Exemple d'utilisation
simulate_air_cooling()
