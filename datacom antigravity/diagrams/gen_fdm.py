"""Generate FDM spectrum visualization."""
import numpy as np
import matplotlib.pyplot as plt
import os

plt.style.use('dark_background')

# Create a frequency axis
f = np.linspace(0, 100, 1000)

# Define 3 channels (triangle spectrums to simulate message spectrum)
def make_channel(f_c, bw, max_amp):
    y = np.zeros_like(f)
    mask = (f >= f_c - bw) & (f <= f_c + bw)
    y[mask] = max_amp * (1 - np.abs(f[mask] - f_c) / bw)
    return y

bw = 8  # bandwidth per channel
guard = 2 # guard band
fc1 = 20
fc2 = fc1 + 2*bw + guard
fc3 = fc2 + 2*bw + guard

ch1 = make_channel(fc1, bw, 1.0)
ch2 = make_channel(fc2, bw, 0.8)
ch3 = make_channel(fc3, bw, 0.9)

fig, ax = plt.subplots(figsize=(10, 4))
fig.patch.set_facecolor('#1a1a2e')
ax.set_facecolor('#1a1a2e')

colors = ['#f7a440', '#00b4d8', '#e94560']

ax.fill_between(f, 0, ch1, color=colors[0], alpha=0.6, label='Channel 1')
ax.plot(f, ch1, color=colors[0], linewidth=2)

ax.fill_between(f, 0, ch2, color=colors[1], alpha=0.6, label='Channel 2')
ax.plot(f, ch2, color=colors[1], linewidth=2)

ax.fill_between(f, 0, ch3, color=colors[2], alpha=0.6, label='Channel 3')
ax.plot(f, ch3, color=colors[2], linewidth=2)

# Annotate guard bands
ax.annotate('Guard Band', xy=(fc1+bw+guard/2, 0.2), xytext=(fc1+bw+guard/2, 0.5),
            arrowprops=dict(facecolor='white', shrink=0.05, width=1, headwidth=5),
            color='white', ha='center')

ax.set_title('Frequency Division Multiplexing (FDM) Spectrum', color='white', fontsize=12, fontweight='bold')
ax.set_xlabel('Frequency (kHz)', color='#aaa')
ax.set_ylabel('Magnitude', color='#aaa')
ax.legend()
ax.grid(True, alpha=0.15)
for spine in ax.spines.values():
    spine.set_color('#333')

plt.tight_layout()
out = os.path.join(os.path.dirname(__file__), 'fdm_spectrum.png')
plt.savefig(out, dpi=180, facecolor='#1a1a2e', bbox_inches='tight')
plt.close()
print(f"Saved: {out}")
