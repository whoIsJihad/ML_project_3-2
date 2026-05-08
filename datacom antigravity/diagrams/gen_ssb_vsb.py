"""Generate SSB and VSB spectrum visualizations."""
import numpy as np
import matplotlib.pyplot as plt
import os

plt.style.use('dark_background')

f = np.linspace(-30, 30, 1000)

# Helper for triangle spectrum
def spec(center, width):
    y = np.zeros_like(f)
    mask = (f >= center) & (f <= center + width)
    y[mask] = 1 - (f[mask] - center) / width
    return y

# Baseband message
M_f = spec(0, 10) + spec(-10, 10)[::-1]  # positive and negative frequencies

# DSB Spectrum (centered at fc=15)
fc = 15
DSB_f = spec(fc, 10) + spec(fc-10, 10)[::-1]

# SSB (USB) Spectrum
SSB_USB_f = spec(fc, 10)

# VSB Spectrum
VSB_f = spec(fc, 10) + (spec(fc-5, 5)[::-1] * 0.5) # Vestige

fig, axes = plt.subplots(4, 1, figsize=(10, 8))
fig.patch.set_facecolor('#1a1a2e')

titles = ['Message Spectrum M(f)', 'DSB Spectrum (USB + LSB)', 'SSB Spectrum (USB Only)', 'VSB Spectrum (USB + Vestige)']
data = [M_f, DSB_f, SSB_USB_f, VSB_f]
colors = ['#f7a440', '#e94560', '#00b4d8', '#90be6d']

for i, ax in enumerate(axes):
    ax.fill_between(f, 0, data[i], color=colors[i], alpha=0.6)
    ax.plot(f, data[i], color=colors[i], linewidth=2)
    ax.set_title(titles[i], color=colors[i], fontsize=11, fontweight='bold')
    ax.set_xlim(-5, 30)
    if i > 0:
        ax.axvline(fc, color='white', linestyle='--', alpha=0.5, label='Carrier f_c')
        ax.legend(loc='upper right', fontsize=8)
    ax.set_facecolor('#1a1a2e')
    ax.tick_params(colors='#666')
    ax.grid(True, alpha=0.15)
    for spine in ax.spines.values():
        spine.set_color('#333')

plt.tight_layout()
out = os.path.join(os.path.dirname(__file__), 'ssb_vsb_spectrum.png')
plt.savefig(out, dpi=180, facecolor='#1a1a2e', bbox_inches='tight')
plt.close()
print(f"Saved: {out}")
