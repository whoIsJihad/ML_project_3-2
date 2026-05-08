"""Generate AM waveform visualizations: message, carrier, AM signal, spectrum."""
import numpy as np
import matplotlib.pyplot as plt
import os

plt.style.use('dark_background')

t = np.linspace(0, 1, 4000)
fm = 5       # message frequency
fc = 50      # carrier frequency
Am = 1.0     # message amplitude
Ac = 1.0     # carrier amplitude
m = 0.8      # modulation index

message = Am * np.cos(2 * np.pi * fm * t)
carrier = Ac * np.cos(2 * np.pi * fc * t)
am_signal = Ac * (1 + m * np.cos(2 * np.pi * fm * t)) * np.cos(2 * np.pi * fc * t)
envelope_upper = Ac * (1 + m * np.cos(2 * np.pi * fm * t))
envelope_lower = -Ac * (1 + m * np.cos(2 * np.pi * fm * t))

fig, axes = plt.subplots(4, 1, figsize=(12, 10))
fig.patch.set_facecolor('#1a1a2e')

colors = ['#f7a440', '#00b4d8', '#e94560', '#90be6d']

# Message
axes[0].plot(t, message, color=colors[0], linewidth=1.5)
axes[0].set_title('Message Signal m(t) = cos(2π·5t)', color=colors[0], fontsize=11, fontweight='bold')
axes[0].set_ylabel('Amplitude', color='#aaa')

# Carrier
axes[1].plot(t, carrier, color=colors[1], linewidth=0.8)
axes[1].set_title('Carrier Signal c(t) = cos(2π·50t)', color=colors[1], fontsize=11, fontweight='bold')
axes[1].set_ylabel('Amplitude', color='#aaa')

# AM Signal
axes[2].plot(t, am_signal, color=colors[2], linewidth=0.8)
axes[2].plot(t, envelope_upper, color=colors[0], linewidth=1.5, linestyle='--', alpha=0.8, label='Envelope')
axes[2].plot(t, envelope_lower, color=colors[0], linewidth=1.5, linestyle='--', alpha=0.8)
axes[2].set_title(f'AM Signal (modulation index m = {m})', color=colors[2], fontsize=11, fontweight='bold')
axes[2].set_ylabel('Amplitude', color='#aaa')
axes[2].legend(loc='upper right', fontsize=9)

# Spectrum
N = len(t)
freqs = np.fft.fftfreq(N, d=t[1]-t[0])
spectrum = np.abs(np.fft.fft(am_signal)) / N
mask = freqs >= 0
axes[3].stem(freqs[mask][:200], spectrum[mask][:200], linefmt=colors[3], markerfmt='o', basefmt=' ')
axes[3].set_title('AM Spectrum |S(f)| — Carrier ± Message frequency', color=colors[3], fontsize=11, fontweight='bold')
axes[3].set_ylabel('Magnitude', color='#aaa')
axes[3].set_xlabel('Frequency (Hz)', color='#aaa')
axes[3].set_xlim(0, 100)
axes[3].annotate('fc = 50', xy=(50, spectrum[mask][50]), fontsize=9, color='white',
                 xytext=(60, spectrum[mask][50]), arrowprops=dict(arrowstyle='->', color='white'))
axes[3].annotate(f'fc-fm = {fc-fm}', xy=(45, 0.3), fontsize=8, color=colors[0])
axes[3].annotate(f'fc+fm = {fc+fm}', xy=(55, 0.3), fontsize=8, color=colors[0])

for ax in axes:
    ax.set_facecolor('#1a1a2e')
    ax.tick_params(colors='#666')
    ax.grid(True, alpha=0.15)
    for spine in ax.spines.values():
        spine.set_color('#333')

plt.suptitle('Amplitude Modulation (AM) — Time & Frequency Domain', fontsize=14, color='white', fontweight='bold', y=1.01)
plt.tight_layout()
out = os.path.join(os.path.dirname(__file__), 'am_waveform.png')
plt.savefig(out, dpi=180, facecolor='#1a1a2e', bbox_inches='tight')
plt.close()
print(f"Saved: {out}")
