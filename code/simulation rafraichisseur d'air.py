# -*- coding: utf-8 -*-
"""
Created on Wed Jun 25 11:07:07 2025
@author: tetique
"""

import numpy as np
import matplotlib.pyplot as plt

# Données physiques
c_water = 4186           # Capacité thermique de l'eau [J/kg·K]
c_air = 1005             # Capacité thermique de l'air [J/kg·K]
rho_air = 1.2            # Masse volumique air [kg/m³]
k = 2000                 # Coefficient empirique de h_air
CFM = 20                 # Débit d'air en CFM
mass_water = 3           # Masse d'eau [kg]
T_air_in = 30            # Température air [°C]
T_air_out = 27           # Objectif sortie air [°C]
T_water_init = 15        # Température initiale de l'eau [°C]
Ep = 0.002               # Épaisseur paroi [m]
Lda_cuivre = 380         # Conductivité cuivre [W/m/K]
Hf = 1000                # Coefficient convection eau
  
# Simulation dynamique
dt = 1                   # Pas de temps [s]
t_max = 3600             # Durée max [s]
time = np.arange(0, t_max + dt, dt)
T_water = [T_water_init]

for t in time[1:]:
    CFM = CFM+0.1
    qv_air = CFM * 0.0004719
    Hc = k * qv_air ** 0.8
    U = 1 / (1/Hc + Ep/Lda_cuivre + 1/Hf)
    m_air = rho_air * qv_air
    Q_dot_air = m_air * c_air * (T_air_in - T_air_out)  # Puissance à extraire
    delta_T_moy = ((T_air_in - T_water_init) + (T_air_out - T_water_init)) / 2
    A_min = Q_dot_air / (U * delta_T_moy)
    delta_T = T_air_in - T_water[-1]
    
    if delta_T <= 0:
        break  # plus de transfert de chaleur possible
        
    if CFM >= 220:
        break
    Q_dot = U * A_min * delta_T
    dT = (Q_dot * dt) / (mass_water * c_water)
    T_next = T_water[-1] + dT
    T_water.append(T_next)

# Redimension du temps
time = time[:len(T_water)]

# Affichage
plt.figure(figsize=(10, 5))
plt.plot(time, T_water, label="Température de l'eau [°C]", color="blue")
plt.axhline(T_air_out, linestyle='--', color='red', label="Seuil utile")
plt.xlabel("Temps (s)")
plt.ylabel("Température (°C)")
plt.title("Évolution de la température de l'eau")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()

# === SIMULATION SPATIALE 1D DU JET D'AIR REFROIDI ===

# Paramètres physiques
L = 100.0                  # Longueur de simulation (m)
Nx = 300                 # Nombre de points dans l’espace
dx = L / (Nx - 1)
x = np.linspace(0, L, Nx)

t_max = 60               # Durée de la simulation (s)
dt = 0.01                # Pas de temps (s)
Nt = int(t_max / dt)

alpha = 20e-6           # Diffusivité thermique de l'air (m²/s)

# Conversion du CFM en vitesse moyenne approximative (jet circulaire)
diam_jet = 0.2          # diamètre de sortie [m] (5 cm)
A_jet = np.pi * (diam_jet / 2)**2
v = qv_air / A_jet       # vitesse d'écoulement approximative [m/s]

print(v)

# Initialisation température
T = np.ones(Nx) * 30     # air ambiant
T[0] = T_air_out                # sortie du jet

# Préparation pour animation
T_history = [T.copy()]

# Schéma numérique : advection + diffusion 1D (upwind + FTCS)
for n in range(Nt):
    T_new = T.copy()
    for i in range(1, Nx - 1):
        adv = -v * (T[i] - T[i-1]) / dx
        diff = alpha * (T[i+1] - 2*T[i] + T[i-1]) / dx**2
        T_new[i] = T[i] + dt * (adv + diff)
    T = T_new
    if n % 100 == 0:  # enregistre toutes les 100 itérations (~1s)
        T_history.append(T.copy())

# Affichage final (t = t_max)
plt.figure(figsize=(10, 5))
plt.plot(x, T, label="Température finale (t = %.1fs)" % t_max, color="blue")
plt.axhline(T_air_out, color='red', linestyle='--', label='Seuil')
plt.axvline(0.5, color='green', linestyle='--', label='Portée cible (0.5m)')
plt.xlabel("Distance depuis la sortie (m)")
plt.ylabel("Température (°C)")
plt.title("Gradient de température dans l'air après la sortie")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()

