import numpy as np
import matplotlib.pyplot as plt

plt.style.use('seaborn-v0_8-darkgrid')

# Parameters (MHz units for readability)
fc = 100.0   # carrier frequency (MHz)
B = 30.0     # baseband bandwidth (MHz)

# Frequency axis (MHz)
f = np.linspace(-250, 250, 4000)

# Baseband spectrum (Gaussian-shaped for clarity)
sigma = B / 3.0
M = np.exp(-0.5 * (f / sigma) ** 2)
M[f > B/2] *= 0  # sharpen edges a little for visual clarity
M[f < -B/2] *= 0

# DSB-SC spectrum: shifted copies (scaled by 1/2 per modulation theorem)
S_dsb = 0.5 * np.exp(-0.5 * ((f - fc) / sigma) ** 2)
S_dsb += 0.5 * np.exp(-0.5 * ((f + fc) / sigma) ** 2)

# AM spectrum: same sidebands + an explicit carrier spike (narrow Gaussian)
S_am = 0.5 * np.exp(-0.5 * ((f - fc) / sigma) ** 2)
S_am += 0.5 * np.exp(-0.5 * ((f + fc) / sigma) ** 2)
carrier_spike = 1.5 * np.exp(-0.5 * ((f - fc) / 0.6) ** 2)
carrier_spike += 1.5 * np.exp(-0.5 * ((f + fc) / 0.6) ** 2)
S_am_with_carrier = S_am + carrier_spike

# Plot
fig, axes = plt.subplots(1, 3, figsize=(15, 4), sharey=True)

# Top-level formatting
titles = ['Baseband (M(f))', 'DSB-SC Spectrum', 'Conventional AM Spectrum']
for ax, title in zip(axes, titles):
    ax.set_xlabel('Frequency (MHz)')
    ax.set_xlim(-200, 200)
    ax.set_ylim(-0.05, 1.25)
    ax.set_title(title, fontweight='bold')
    ax.grid(True, alpha=0.25)

# Left: baseband
axes[0].plot(f, M, color='#1f77b4')
axes[0].fill_between(f, 0, M, color='#1f77b4', alpha=0.25)
axes[0].axvspan(-B/2, B/2, color='green', alpha=0.08)
axes[0].text(0, 0.9, f'Bandwidth ≈ {B} MHz', ha='center', va='center', fontsize=9, bbox=dict(fc='white', ec='none', alpha=0.7))

# Middle: DSB-SC
axes[1].plot(f, S_dsb, color='#ff7f0e')
axes[1].fill_between(f, 0, S_dsb, color='#ff7f0e', alpha=0.25)
axes[1].axvline(fc, color='red', linestyle='--', linewidth=1)
axes[1].axvline(-fc, color='red', linestyle='--', linewidth=1)
axes[1].text(fc, 0.6, 'Upper\nsideband', ha='center', va='center', fontsize=8)
axes[1].text(-fc, 0.6, 'Lower\nsideband', ha='center', va='center', fontsize=8)

# Right: Conventional AM (with carrier spike)
axes[2].plot(f, S_am_with_carrier, color='#2ca02c')
axes[2].fill_between(f, 0, S_am_with_carrier, color='#2ca02c', alpha=0.18)
axes[2].axvline(fc, color='red', linestyle='--', linewidth=1)
axes[2].axvline(-fc, color='red', linestyle='--', linewidth=1)
axes[2].text(fc, 1.05, 'Carrier spike\n(at $f_c$)', ha='center', va='center', fontsize=9, bbox=dict(fc='white', ec='gray', alpha=0.8))

# Annotations to compare
fig.suptitle('Focused Spectrum: Baseband → DSB‑SC → Conventional AM', fontsize=14, fontweight='bold')
fig.tight_layout(rect=[0, 0, 1, 0.95])
plt.savefig('graphs/11_dsbsc_am_spectrum.png', dpi=300, bbox_inches='tight')
print('✓ graphs/11_dsbsc_am_spectrum.png')
plt.close()
