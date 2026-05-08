"""Generate PAM visualization: original signal, sampled, quantized PAM, and reconstruction."""
import numpy as np
import matplotlib.pyplot as plt
import os

plt.style.use('dark_background')

t_cont = np.linspace(0, 1, 4000)
signal = 0.6 * np.sin(2*np.pi*3*t_cont) + 0.3 * np.sin(2*np.pi*7*t_cont) + 0.1 * np.cos(2*np.pi*12*t_cont)

fs = 30
t_samples = np.arange(0, 1, 1/fs)
samples = 0.6*np.sin(2*np.pi*3*t_samples) + 0.3*np.sin(2*np.pi*7*t_samples) + 0.1*np.cos(2*np.pi*12*t_samples)

levels = 16
q_step = (signal.max() - signal.min()) / levels
samples_q = np.round((samples - signal.min()) / q_step) * q_step + signal.min()

fig, axes = plt.subplots(4, 1, figsize=(12, 10))
fig.patch.set_facecolor('#1a1a2e')
colors = ['#f7a440', '#00b4d8', '#e94560', '#90be6d']

axes[0].plot(t_cont, signal, color=colors[0], lw=1.5)
axes[0].set_title('Original Analog Signal', color=colors[0], fontsize=11, fontweight='bold')

axes[1].plot(t_cont, signal, color=colors[0], lw=0.5, alpha=0.3)
axes[1].stem(t_samples, samples, linefmt=colors[1], markerfmt='o', basefmt=' ')
axes[1].set_title(f'Sampled (fs={fs} Hz, Nyquist: 2×12=24 Hz ✓)', color=colors[1], fontsize=11, fontweight='bold')

axes[2].plot(t_cont, signal, color=colors[0], lw=0.5, alpha=0.3)
for ts, sq in zip(t_samples, samples_q):
    axes[2].bar(ts, sq, width=1/(fs*1.5), color=colors[2], alpha=0.7, edgecolor=colors[2])
axes[2].set_title(f'Flat-Top PAM ({levels} levels = 4 bits)', color=colors[2], fontsize=11, fontweight='bold')

reconstructed = np.zeros_like(t_cont)
for i, ts in enumerate(t_samples):
    reconstructed += samples[i] * np.sinc((t_cont - ts) * fs)
axes[3].plot(t_cont, signal, color=colors[0], lw=1, alpha=0.4, label='Original')
axes[3].plot(t_cont, reconstructed, color=colors[3], lw=1.5, label='Reconstructed')
axes[3].set_title('Sinc Interpolation Reconstruction', color=colors[3], fontsize=11, fontweight='bold')
axes[3].legend(loc='upper right', fontsize=9)
axes[3].set_xlabel('Time (s)', color='#aaa')

for ax in axes:
    ax.set_facecolor('#1a1a2e'); ax.tick_params(colors='#666'); ax.grid(True, alpha=0.15)
    ax.set_ylabel('Amplitude', color='#aaa')
    for s in ax.spines.values(): s.set_color('#333')

plt.suptitle('PAM — Sampling → Quantization → Reconstruction', fontsize=14, color='white', fontweight='bold', y=1.01)
plt.tight_layout()
out = os.path.join(os.path.dirname(__file__), 'pam_waveform.png')
plt.savefig(out, dpi=180, facecolor='#1a1a2e', bbox_inches='tight')
plt.close()
print(f"Saved: {out}")
