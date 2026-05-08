"""Generate Shannon capacity diagrams: C vs SNR and infinite BW limit."""
import numpy as np
import matplotlib.pyplot as plt
import os

plt.style.use('dark_background')

fig = plt.figure(figsize=(14, 6))
fig.patch.set_facecolor('#1a1a2e')

# ═══════════════════════════════════════
# LEFT: Shannon Capacity vs SNR for different bandwidths
# ═══════════════════════════════════════
ax1 = fig.add_subplot(1, 2, 1)
ax1.set_facecolor('#1a1a2e')

snr_db = np.linspace(0, 30, 300)
snr_lin = 10**(snr_db / 10)

bandwidths = [1e3, 3.4e3, 10e3, 1e6]
bw_labels = ['B = 1 kHz', 'B = 3.4 kHz (phone)', 'B = 10 kHz', 'B = 1 MHz']
colors = ['#c77dff', '#f7a440', '#00b4d8', '#90be6d']

for B, label, color in zip(bandwidths, bw_labels, colors):
    C = B * np.log2(1 + snr_lin)
    if B >= 1e6:
        ax1.plot(snr_db, C / 1e6, color=color, lw=2.5, label=label)
    elif B >= 1e3:
        ax1.plot(snr_db, C / 1e3, color=color, lw=2.5, label=label)

# Since mixed units are confusing, let's do separate: just show B = 3.4kHz (phone line)
ax1.clear()
ax1.set_facecolor('#1a1a2e')

B = 3400  # Hz
C = B * np.log2(1 + snr_lin)
ax1.plot(snr_db, C / 1e3, color='#f7a440', lw=3)
ax1.fill_between(snr_db, C / 1e3, alpha=0.1, color='#f7a440')

# Mark the V.34 modem point
ax1.scatter([30], [B * np.log2(1 + 1000) / 1e3], color='#e94560', s=120,
            zorder=10, edgecolor='white', linewidth=1.5)
ax1.annotate('V.34 modem limit\n≈ 33.9 kbps', xy=(30, 33.9), xytext=(20, 28),
             fontsize=9, color='#e94560', fontweight='bold',
             arrowprops=dict(arrowstyle='->', color='#e94560', lw=1.5))

# Mark dial-up 56k theoretical
ax1.axhline(y=33.9, color='#e94560', linestyle=':', alpha=0.5)

ax1.set_xlabel('SNR (dB)', color='#aaa', fontsize=12)
ax1.set_ylabel('Capacity (kbps)', color='#aaa', fontsize=12)
ax1.set_title('Shannon Capacity — Phone Line (B = 3.4 kHz)\nC = B log₂(1 + S/N)',
              color='white', fontsize=12, fontweight='bold', pad=10)
ax1.grid(True, alpha=0.15)
ax1.tick_params(colors='#666')
for s in ax1.spines.values():
    s.set_color('#333')

# ═══════════════════════════════════════
# RIGHT: Capacity vs Bandwidth (infinite BW limit)
# ═══════════════════════════════════════
ax2 = fig.add_subplot(1, 2, 2)
ax2.set_facecolor('#1a1a2e')

S = 1.0       # signal power (normalized)
N0 = 0.001    # noise spectral density

B_range = np.linspace(1, 5000, 1000)
N_range = N0 * B_range
C_range = B_range * np.log2(1 + S / N_range)
C_inf = (S / N0) * np.log2(np.e)  # = 1.44 * S/N0

ax2.plot(B_range, C_range, color='#00b4d8', lw=3, label='C = B log₂(1 + S/N₀B)')
ax2.axhline(y=C_inf, color='#e94560', linestyle='--', lw=2, label=f'C∞ = 1.44 S/N₀ = {C_inf:.0f}')
ax2.fill_between(B_range, C_range, alpha=0.1, color='#00b4d8')

ax2.annotate(f'Limit: C∞ = {C_inf:.0f} bits/sec', xy=(4500, C_inf), xytext=(3000, C_inf * 0.75),
             fontsize=10, color='#e94560', fontweight='bold',
             arrowprops=dict(arrowstyle='->', color='#e94560', lw=1.5))

ax2.set_xlabel('Bandwidth B (Hz)', color='#aaa', fontsize=12)
ax2.set_ylabel('Capacity C (bits/sec)', color='#aaa', fontsize=12)
ax2.set_title('Infinite Bandwidth Limit\nMore BW → diminishing returns',
              color='white', fontsize=12, fontweight='bold', pad=10)
ax2.grid(True, alpha=0.15)
ax2.legend(fontsize=10, loc='center right')
ax2.tick_params(colors='#666')
for s in ax2.spines.values():
    s.set_color('#333')

plt.tight_layout()
out = os.path.join(os.path.dirname(__file__), 'shannon_capacity.png')
plt.savefig(out, dpi=180, facecolor='#1a1a2e', bbox_inches='tight')
plt.close()
print(f"Saved: {out}")
