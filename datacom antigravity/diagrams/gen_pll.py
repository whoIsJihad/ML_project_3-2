"""Generate PLL lock time visualization."""
import numpy as np
import matplotlib.pyplot as plt
import os

plt.style.use('dark_background')

t = np.linspace(0, 1, 1000)
# Incoming signal frequency jumps at t=0.2
f_in = np.ones_like(t) * 10
f_in[t >= 0.2] = 15

# Simulate PLL VCO tracking
f_vco = np.ones_like(t) * 10
tau = 0.05 # time constant of loop filter

for i in range(1, len(t)):
    dt = t[i] - t[i-1]
    # Simple exponential tracking (first-order loop approximation)
    df = (f_in[i-1] - f_vco[i-1]) * (dt / tau)
    f_vco[i] = f_vco[i-1] + df

# Control voltage is proportional to f_vco
v_control = f_vco - 10

fig, axes = plt.subplots(2, 1, figsize=(10, 6))
fig.patch.set_facecolor('#1a1a2e')

colors = ['#f7a440', '#00b4d8']

# Frequency tracking
axes[0].plot(t, f_in, color='white', linestyle='--', linewidth=1.5, label='Incoming Frequency')
axes[0].plot(t, f_vco, color=colors[0], linewidth=2.5, label='VCO Frequency')
axes[0].set_title('PLL Frequency Tracking', color=colors[0], fontsize=11, fontweight='bold')
axes[0].set_ylabel('Frequency (Hz)', color='#aaa')
axes[0].legend()

# Control Voltage
axes[1].plot(t, v_control, color=colors[1], linewidth=2.5, label='VCO Control Voltage (Demodulated Output)')
axes[1].set_title('Loop Filter Output / FM Demodulated Signal', color=colors[1], fontsize=11, fontweight='bold')
axes[1].set_xlabel('Time (s)', color='#aaa')
axes[1].set_ylabel('Voltage', color='#aaa')

for ax in axes:
    ax.set_facecolor('#1a1a2e')
    ax.tick_params(colors='#666')
    ax.grid(True, alpha=0.15)
    for spine in ax.spines.values():
        spine.set_color('#333')

plt.tight_layout()
out = os.path.join(os.path.dirname(__file__), 'pll_tracking.png')
plt.savefig(out, dpi=180, facecolor='#1a1a2e', bbox_inches='tight')
plt.close()
print(f"Saved: {out}")
