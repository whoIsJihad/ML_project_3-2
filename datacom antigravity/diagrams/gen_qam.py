"""Generate QAM Time Domain Waveform visualization."""
import numpy as np
import matplotlib.pyplot as plt
import os

plt.style.use('dark_background')

# Time axis
t = np.linspace(0, 4, 2000)

# Carrier frequency
fc = 2

# Bit sequence (for I and Q) - assume 16-QAM PAM levels (-3, -1, 1, 3)
# We will show 4 symbols
I_levels = [3, -1, -3, 1]
Q_levels = [1, 3, -1, -3]

I_signal = np.zeros_like(t)
Q_signal = np.zeros_like(t)

for i in range(4):
    mask = (t >= i) & (t < (i+1))
    I_signal[mask] = I_levels[i]
    Q_signal[mask] = Q_levels[i]

# Carriers
cos_carrier = np.cos(2 * np.pi * fc * t)
sin_carrier = -np.sin(2 * np.pi * fc * t)  # Minus sign for standard QAM math

I_mod = I_signal * cos_carrier
Q_mod = Q_signal * sin_carrier

qam_signal = I_mod + Q_mod

fig, axes = plt.subplots(4, 1, figsize=(12, 10))
fig.patch.set_facecolor('#1a1a2e')

colors = ['#f7a440', '#00b4d8', '#e94560', '#90be6d']

axes[0].plot(t, I_signal, color=colors[0], linewidth=2, label='In-Phase (I) Baseband')
axes[0].set_title('In-Phase (I) Baseband Signal (PAM levels)', color=colors[0], fontsize=11, fontweight='bold')

axes[1].plot(t, Q_signal, color=colors[1], linewidth=2, label='Quadrature (Q) Baseband')
axes[1].set_title('Quadrature (Q) Baseband Signal (PAM levels)', color=colors[1], fontsize=11, fontweight='bold')

axes[2].plot(t, I_mod, color=colors[0], linewidth=1.5, alpha=0.8, label='I_mod = I * cos(ωt)')
axes[2].plot(t, Q_mod, color=colors[1], linewidth=1.5, alpha=0.8, label='Q_mod = Q * (-sin(ωt))')
axes[2].set_title('Modulated Sub-carriers (I and Q)', color='white', fontsize=11, fontweight='bold')
axes[2].legend(loc='upper right', fontsize=9)

axes[3].plot(t, qam_signal, color=colors[3], linewidth=2)
axes[3].set_title('Composite QAM Signal = I_mod + Q_mod', color=colors[3], fontsize=11, fontweight='bold')

for i in range(1, 4):
    for ax in axes:
        ax.axvline(i, color='#444', linestyle='--', linewidth=1)

for ax in axes:
    ax.set_facecolor('#1a1a2e')
    ax.tick_params(colors='#666')
    ax.grid(True, alpha=0.15)
    for spine in ax.spines.values():
        spine.set_color('#333')

plt.suptitle('16-QAM Time-Domain Waveform Generation', fontsize=14, color='white', fontweight='bold', y=1.01)
plt.tight_layout()
out = os.path.join(os.path.dirname(__file__), 'qam_waveform.png')
plt.savefig(out, dpi=180, facecolor='#1a1a2e', bbox_inches='tight')
plt.close()
print(f"Saved: {out}")
