# -*- coding: utf-8 -*-
"""
Created on Mon Jun 30 13:48:32 2025

@author: tetique
"""

# === Constantes ===
c_air = 1000       # J/kg·K
rho_air = 1.2      # kg/m³
deltaT_air = 3     # °C (objectif de refroidissement)
T_air = 30         # °C
T_eau = 25         # °C
deltaT_air_eau = T_air - T_eau

# === Débit d'air fourni ===
CFM = 45
debit_air_m3s = CFM * 0.0283 / 60
m_dot_air = debit_air_m3s * rho_air   # kg/s

# === Puissance thermique à extraire pour chuter de 3°C ===
P_air = m_dot_air * c_air * deltaT_air  # en watts

# === Hypothèse pour coefficient de transfert thermique (modéré) ===
h = 50  # W/m²·K

# === Surface minimale requise ===
A_min = P_air / (h * deltaT_air_eau)  # m²

# === Résultat
print(f"Puissance thermique à extraire (P_air) : {P_air:.2f} W")
print(f"Surface minimale de l’échangeur nécessaire : {A_min:.2f} m²")
