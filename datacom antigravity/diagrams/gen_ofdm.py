"""Generate OFDM subcarrier visualization: individual subcarriers, composite, spectrum."""
import numpy as np
import matplotlib.pyplot as plt
import os

plt.style.use('dark_background')

N = 8  # number of subcarriers
T = 1.0  # symbol duration
t = np.linspace(0, T, 2000)

np.random.seed(42)
data = np.random.choice([-1, 1], N)  # BPSK data on each subcarrier
f0 = 4  # base frequency

fig, axes = plt.subplots(3, 1, figsize=(12, 9))
fig.patch.set_facecolor('#1a1a2e')
cmap = plt.cm.plasma(np.linspace(0.2, 0.9, N))

# Individual subcarriers
for k in range(N):
    fk = f0 + k / T
    sc = data[k] * np.cos(2 * np.pi * fk * t)
    axes[0].plot(t, sc + k * 2.5, color=cmap[k], lw=1, alpha=0.8, label=f'f{k}={fk:.0f}Hz')
axes[0].set_title(f'Individual OFDM Subcarriers (N={N}, orthogonal spacing Δf=1/T={1/T:.0f} Hz)',
                   color='#e94560', fontsize=11, fontweight='bold')
axes[0].set_ylabel('Subcarrier (offset)', color='#aaa')
axes[0].legend(loc='upper right', fontsize=7, ncol=4)

# Composite signal
composite = np.zeros_like(t)
for k in range(N):
    fk = f0 + k / T
    composite += data[k] * np.cos(2 * np.pi * fk * t)
axes[1].plot(t, composite, color='#00b4d8', lw=1.2)
axes[1].fill_between(t, composite, alpha=0.15, color='#00b4d8')
axes[1].set_title('Composite OFDM Signal (sum of all subcarriers)', color='#00b4d8', fontsize=11, fontweight='bold')
axes[1].set_ylabel('Amplitude', color='#aaa')

# Spectrum — show orthogonal subcarrier peaks
freqs = np.linspace(0, 20, 2000)
spectrum = np.zeros_like(freqs)
for k in range(N):
    fk = f0 + k / T
    sinc_resp = T * np.sinc((freqs - fk) * T)
    spectrum += np.abs(sinc_resp)
    axes[2].fill_between(freqs, np.abs(sinc_resp), alpha=0.2, color=cmap[k])
    axes[2].plot(freqs, np.abs(sinc_resp), color=cmap[k], lw=1, alpha=0.6)
    axes[2].axvline(fk, color=cmap[k], lw=0.5, linestyle=':', alpha=0.5)

axes[2].set_title('OFDM Spectrum — Overlapping but Orthogonal Subcarriers', color='#90be6d', fontsize=11, fontweight='bold')
axes[2].set_ylabel('Magnitude', color='#aaa')
axes[2].set_xlabel('Frequency (Hz)', color='#aaa')
axes[2].set_xlim(0, 16)

for ax in axes:
    ax.set_facecolor('#1a1a2e'); ax.tick_params(colors='#666'); ax.grid(True, alpha=0.1)
    for s in ax.spines.values(): s.set_color('#333')

plt.suptitle('OFDM — Orthogonal Frequency Division Multiplexing', fontsize=14, color='white', fontweight='bold', y=1.01)
plt.tight_layout()
out = os.path.join(os.path.dirname(__file__), 'ofdm_subcarriers.png')
plt.savefig(out, dpi=180, facecolor='#1a1a2e', bbox_inches='tight')
plt.close()
print(f"Saved: {out}")
