"""Generate PM waveform: message, PM signal, instantaneous phase, FM vs PM comparison."""
import numpy as np
import matplotlib.pyplot as plt
import os

plt.style.use('dark_background')

t = np.linspace(0, 1, 8000)
fm = 3
fc = 40
Am = 1.0
Ac = 1.0
kp = 3.0       # phase sensitivity (rad/V)
delta_f = 15   # FM deviation for comparison
beta_fm = delta_f / fm

message = Am * np.cos(2 * np.pi * fm * t)

# PM: phase proportional to message
pm_signal = Ac * np.cos(2 * np.pi * fc * t + kp * message)
inst_phase_pm = 2 * np.pi * fc * t + kp * message

# FM for comparison
fm_signal = Ac * np.cos(2 * np.pi * fc * t + beta_fm * np.sin(2 * np.pi * fm * t))

fig, axes = plt.subplots(4, 1, figsize=(12, 10))
fig.patch.set_facecolor('#1a1a2e')

colors = ['#f7a440', '#00b4d8', '#e94560', '#90be6d']

# Message
axes[0].plot(t, message, color=colors[0], linewidth=1.5)
axes[0].set_title('Message Signal m(t)', color=colors[0], fontsize=11, fontweight='bold')
axes[0].set_ylabel('Amplitude', color='#aaa')

# PM signal
axes[1].plot(t, pm_signal, color=colors[2], linewidth=0.8)
axes[1].set_title(f'PM Signal — Phase ∝ m(t), kp = {kp} rad/V', color=colors[2], fontsize=11, fontweight='bold')
axes[1].set_ylabel('Amplitude', color='#aaa')

# Instantaneous phase deviation
phase_dev = kp * message
axes[2].plot(t, phase_dev, color=colors[3], linewidth=2)
axes[2].fill_between(t, 0, phase_dev, alpha=0.2, color=colors[3])
axes[2].axhline(y=0, color='#555', linestyle='--', linewidth=1)
axes[2].set_title('Phase Deviation Δφ(t) = kp · m(t)', color=colors[3], fontsize=11, fontweight='bold')
axes[2].set_ylabel('Phase (rad)', color='#aaa')
axes[2].annotate(f'Max Δφ = {kp:.1f} rad', xy=(0.25, kp), fontsize=9, color='white')

# FM vs PM comparison
axes[3].plot(t, pm_signal, color=colors[2], linewidth=0.8, alpha=0.7, label='PM')
axes[3].plot(t, fm_signal, color=colors[1], linewidth=0.8, alpha=0.7, label='FM')
axes[3].set_title('PM vs FM Comparison — Same message, different encoding', color='white', fontsize=11, fontweight='bold')
axes[3].set_ylabel('Amplitude', color='#aaa')
axes[3].set_xlabel('Time (s)', color='#aaa')
axes[3].legend(loc='upper right', fontsize=9)

for ax in axes:
    ax.set_facecolor('#1a1a2e')
    ax.tick_params(colors='#666')
    ax.grid(True, alpha=0.15)
    for spine in ax.spines.values():
        spine.set_color('#333')

plt.suptitle('Phase Modulation (PM) — Analysis & FM Comparison', fontsize=14, color='white', fontweight='bold', y=1.01)
plt.tight_layout()
out = os.path.join(os.path.dirname(__file__), 'pm_waveform.png')
plt.savefig(out, dpi=180, facecolor='#1a1a2e', bbox_inches='tight')
plt.close()
print(f"Saved: {out}")
