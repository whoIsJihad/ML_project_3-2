"""Generate FM waveform visualizations: message, carrier, FM signal, instantaneous frequency."""
import numpy as np
import matplotlib.pyplot as plt
import os

plt.style.use('dark_background')

t = np.linspace(0, 1, 8000)
fm = 3        # message frequency
fc = 40       # carrier frequency
Am = 1.0
Ac = 1.0
delta_f = 15  # frequency deviation
beta = delta_f / fm  # modulation index

message = Am * np.cos(2 * np.pi * fm * t)
carrier = Ac * np.cos(2 * np.pi * fc * t)
fm_signal = Ac * np.cos(2 * np.pi * fc * t + beta * np.sin(2 * np.pi * fm * t))
inst_freq = fc + delta_f * np.cos(2 * np.pi * fm * t)  # not exact derivative but illustrative

fig, axes = plt.subplots(4, 1, figsize=(12, 10))
fig.patch.set_facecolor('#1a1a2e')

colors = ['#f7a440', '#00b4d8', '#e94560', '#90be6d']

# Message
axes[0].plot(t, message, color=colors[0], linewidth=1.5)
axes[0].set_title('Message Signal m(t) = cos(2π·3t)', color=colors[0], fontsize=11, fontweight='bold')
axes[0].set_ylabel('Amplitude', color='#aaa')

# Carrier
axes[1].plot(t, carrier, color=colors[1], linewidth=0.8)
axes[1].set_title('Carrier Signal c(t) = cos(2π·40t)', color=colors[1], fontsize=11, fontweight='bold')
axes[1].set_ylabel('Amplitude', color='#aaa')

# FM Signal
axes[2].plot(t, fm_signal, color=colors[2], linewidth=0.8)
axes[2].set_title(f'FM Signal (Δf = {delta_f} Hz, β = {beta:.1f})', color=colors[2], fontsize=11, fontweight='bold')
axes[2].set_ylabel('Amplitude', color='#aaa')

# Instantaneous frequency
axes[3].plot(t, inst_freq, color=colors[3], linewidth=2)
axes[3].axhline(y=fc, color='#555', linestyle='--', linewidth=1)
axes[3].fill_between(t, fc, inst_freq, alpha=0.2, color=colors[3])
axes[3].set_title('Instantaneous Frequency f(t) = fc + Δf·cos(2πfm·t)', color=colors[3], fontsize=11, fontweight='bold')
axes[3].set_ylabel('Freq (Hz)', color='#aaa')
axes[3].set_xlabel('Time (s)', color='#aaa')
axes[3].annotate(f'fc + Δf = {fc + delta_f}', xy=(0.25, fc + delta_f), fontsize=9, color='white')
axes[3].annotate(f'fc - Δf = {fc - delta_f}', xy=(0.25, fc - delta_f), fontsize=9, color='white')
axes[3].annotate(f'fc = {fc}', xy=(0.5, fc + 1), fontsize=9, color='#777')

for ax in axes:
    ax.set_facecolor('#1a1a2e')
    ax.tick_params(colors='#666')
    ax.grid(True, alpha=0.15)
    for spine in ax.spines.values():
        spine.set_color('#333')

plt.suptitle('Frequency Modulation (FM) — Time Domain Analysis', fontsize=14, color='white', fontweight='bold', y=1.01)
plt.tight_layout()
out = os.path.join(os.path.dirname(__file__), 'fm_waveform.png')
plt.savefig(out, dpi=180, facecolor='#1a1a2e', bbox_inches='tight')
plt.close()
print(f"Saved: {out}")
