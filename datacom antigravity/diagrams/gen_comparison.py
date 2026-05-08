"""Generate comparison charts: bandwidth efficiency, BER curves, and trade-off radar."""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import os

plt.style.use('dark_background')

fig = plt.figure(figsize=(14, 10))
fig.patch.set_facecolor('#1a1a2e')

# --- Chart 1: Spectral Efficiency bar chart ---
ax1 = fig.add_subplot(2, 2, 1)
mods = ['BPSK', 'QPSK', '8-PSK', '16-QAM', '64-QAM', '256-QAM']
eff = [1, 2, 3, 4, 6, 8]
colors = ['#f7a440', '#00b4d8', '#e94560', '#90be6d', '#c77dff', '#ff6b6b']
bars = ax1.barh(mods, eff, color=colors, edgecolor='white', linewidth=0.5, height=0.6)
for bar, e in zip(bars, eff):
    ax1.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height()/2, f'{e} bits/Hz',
             va='center', fontsize=9, color='white', fontweight='bold')
ax1.set_title('Spectral Efficiency (bits/s/Hz)', color='#f7a440', fontsize=12, fontweight='bold')
ax1.set_xlabel('bits/s/Hz', color='#aaa')
ax1.set_facecolor('#1a1a2e')

# --- Chart 2: BER vs SNR curves ---
ax2 = fig.add_subplot(2, 2, 2)
snr_db = np.linspace(0, 20, 200)
snr = 10**(snr_db / 10)
from scipy.special import erfc
ber_bpsk = 0.5 * erfc(np.sqrt(snr))
ber_qpsk = 0.5 * erfc(np.sqrt(snr))  # same as BPSK per bit
ber_16qam = (3/8) * erfc(np.sqrt(snr * 2/5))
ber_64qam = (7/24) * erfc(np.sqrt(snr * 1/7))

ax2.semilogy(snr_db, ber_bpsk, color='#f7a440', lw=2, label='BPSK')
ax2.semilogy(snr_db, ber_16qam, color='#90be6d', lw=2, label='16-QAM')
ax2.semilogy(snr_db, ber_64qam, color='#c77dff', lw=2, label='64-QAM')
ax2.set_ylim(1e-6, 1)
ax2.set_title('BER vs Eb/N0', color='#e94560', fontsize=12, fontweight='bold')
ax2.set_xlabel('Eb/N0 (dB)', color='#aaa'); ax2.set_ylabel('BER', color='#aaa')
ax2.legend(fontsize=9); ax2.grid(True, alpha=0.15)
ax2.set_facecolor('#1a1a2e')

# --- Chart 3: Bandwidth requirement comparison ---
ax3 = fig.add_subplot(2, 2, 3)
mods2 = ['AM\n(DSB)', 'FM\n(Wide)', 'BPSK', 'QPSK', '16-QAM', 'OFDM\n(64 sc)']
bw_relative = [2, 10, 1, 1, 1, 0.8]  # relative to baseband
ax3.bar(mods2, bw_relative, color=['#f7a440','#00b4d8','#e94560','#90be6d','#c77dff','#ff6b6b'],
        edgecolor='white', linewidth=0.5, width=0.5)
ax3.set_title('Relative Bandwidth (per unit data rate)', color='#00b4d8', fontsize=12, fontweight='bold')
ax3.set_ylabel('Relative BW', color='#aaa')
ax3.set_facecolor('#1a1a2e')

# --- Chart 4: Trade-off radar/comparison table ---
ax4 = fig.add_subplot(2, 2, 4)
ax4.axis('off')
ax4.set_facecolor('#1a1a2e')
table_data = [
    ['Scheme', 'BW Eff.', 'Noise', 'Complex.', 'Power'],
    ['AM',     '★★☆☆', '★☆☆☆', '★★★★', '★★☆☆'],
    ['FM',     '★☆☆☆', '★★★★', '★★★☆', '★★★☆'],
    ['BPSK',   '★☆☆☆', '★★★★', '★★★★', '★★★★'],
    ['QPSK',   '★★☆☆', '★★★★', '★★★☆', '★★★☆'],
    ['16-QAM', '★★★☆', '★★☆☆', '★★☆☆', '★★☆☆'],
    ['64-QAM', '★★★★', '★☆☆☆', '★☆☆☆', '★☆☆☆'],
]
table = ax4.table(cellText=table_data[1:], colLabels=table_data[0],
                  cellLoc='center', loc='center')
table.auto_set_font_size(False)
table.set_fontsize(9)
for key, cell in table.get_celld().items():
    cell.set_facecolor('#16213e')
    cell.set_edgecolor('#333')
    cell.set_text_props(color='white')
    if key[0] == 0:
        cell.set_facecolor('#0f3460')
        cell.set_text_props(color='white', fontweight='bold')
    cell.set_height(0.12)
ax4.set_title('Modulation Trade-Off Matrix', color='#90be6d', fontsize=12, fontweight='bold', pad=20)

for ax in [ax1, ax2, ax3]:
    ax.tick_params(colors='#666')
    for s in ax.spines.values(): s.set_color('#333')

plt.suptitle('Modulation Comparison — Efficiency, BER, Bandwidth, Trade-Offs',
             fontsize=14, color='white', fontweight='bold', y=1.01)
plt.tight_layout()
out = os.path.join(os.path.dirname(__file__), 'comparison_charts.png')
plt.savefig(out, dpi=180, facecolor='#1a1a2e', bbox_inches='tight')
plt.close()
print(f"Saved: {out}")
