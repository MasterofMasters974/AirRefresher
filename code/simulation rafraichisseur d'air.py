# -*- coding: utf-8 -*-
"""
Created on Wed Jun 25 11:07:07 2025

@author: tetique
"""

import numpy as np
import matplotlib.pyplot as plt

# Données physiques
c_water = 4186           # Capacité thermique de l'eau [J/kg·K]
k = 2000                 # Empirique
CFM = 82.1               # débit d'air en unité de cul
mass_water = 1           # Masse d'eau [kg]
T_air = 30               # Température constante de l'air [°C]
T_water_init = 15        # Température initiale de l'eau [°C]
Hc = k * CFM * 0.0004719 # Coefficient de convection thermique de l'air à 30°C
Hf = 1000                # Coefficient de convection thermique de l'eau à 15°C
Ep = 0.002               # Epassieur paroi [m]
Lda = 380                # Coefficient de conductivité thermique du cuivre [W/m/K]
A = 0.08                 # Surface d’échange [m²]
U = 1/(1/Hc+Ep/Lda+1/Hf)

print(U)

# Simulation
dt = 1                   # Pas de temps [s]
t_max = 3600             # Durée max [s]
time = np.arange(0, t_max + dt, dt)

T_water = [T_water_init]

for t in time[1:]:
    delta_T = T_air - T_water[-1]
    if delta_T <= 0:
        break  # plus de transfert de chaleur
    Q_dot = U * A * delta_T
    dT = (Q_dot * dt) / (mass_water * c_water)
    T_next = T_water[-1] + dT
    T_water.append(T_next)

# Redimensionner le temps
time = time[:len(T_water)]

# Affichage
plt.figure(figsize=(10, 5))
plt.plot(time, T_water, label="Température de l'eau [°C]", color="blue")
plt.axhline(27, linestyle='--', color='red', label="Seuil utile (27°C)")
plt.xlabel("Temps (s)")
plt.ylabel("Température (°C)")
plt.title("Évolution de la température de l'eau avec U·A·ΔT")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()
