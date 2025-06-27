import numpy as np
import matplotlib.pyplot as plt

# === Constantes ===
c_eau = 4186       # J/kg·K
c_air = 1000       # J/kg·K
rho_air = 1.2      # kg/m³

# === Réservoir ===
m_eau_total = 2.0  # kg (volume du réservoir = 1L)
T_eau_init = 15    # °C

# === Air ===
T_air_in = 30              # °C
deltaT_air_cible = 3       # °C
debit_air_m3h = 42


# === Eau en circulation ===
debit_eau_lph = 2


# === Simulation ===
t_sim = 3600  # secondes
dt = 1       # secondes
steps = int(t_sim / dt)

T_eau = np.zeros(steps)
T_eau[0] = T_eau_init

for t in range(1, steps):
    
    debit_air_m3s = debit_air_m3h / 3600
    m_dot_air = debit_air_m3s * rho_air  # kg/s
    P_air = m_dot_air * c_air * deltaT_air_cible  # W
    
    debit_eau_lps = debit_eau_lph / 3600  # L/s = kg/s
    m_dot_eau = debit_eau_lps             # kg/s
    deltaT_eau_max = 3                    # °C (température max que l'eau peut prendre dans l’échangeur)
    P_eau_max = m_dot_eau * c_eau * deltaT_eau_max  # W


    # === Puissance réellement absorbée par l’eau ===
    P_absorbee = min(P_air, P_eau_max)
    
    dQ = P_absorbee * dt
    dT = dQ / (m_eau_total * c_eau)
    T_eau[t] = T_eau[t - 1] + dT
    
    debit_eau_lph = debit_eau_lph +0.01
    debit_air_m3h = debit_air_m3h -0.008
    
    if debit_air_m3h <=0:
        break

# === Tracé ===
time = np.arange(0, t_sim, dt)

plt.figure(figsize=(10, 5))
plt.plot(time / 60, T_eau, label="Température de l'eau (°C)", color='blue')
plt.axhline(25, color='gray', linestyle='--', label='Seuil de purge (25°C)')
plt.xlabel("Temps (minutes)")
plt.ylabel("Température (°C)")
plt.title("Effet du débit d'eau sur la température du réservoir")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()

# === Durée utile ===
if np.any(T_eau >= 25):
    t_max = np.argmax(T_eau >= 25)
    print(f"L’eau atteint 25 °C après {t_max} s ≈ {t_max/60:.1f} min.")
else:
    print("L’eau reste sous les 25 °C pendant toute la simulation.")
