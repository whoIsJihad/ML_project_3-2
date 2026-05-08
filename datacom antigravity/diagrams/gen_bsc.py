"""Generate BSC diagram and capacity curve."""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import os

plt.style.use('dark_background')

fig = plt.figure(figsize=(14, 6))
fig.patch.set_facecolor('#1a1a2e')

# ═══════════════════════════════════════
# LEFT: BSC Channel Diagram
# ═══════════════════════════════════════
ax1 = fig.add_subplot(1, 2, 1)
ax1.set_facecolor('#1a1a2e')
ax1.set_xlim(-0.5, 4.5)
ax1.set_ylim(-0.5, 3.5)
ax1.axis('off')

# Input nodes
for y, label in [(2.5, 'x = 0'), (0.5, 'x = 1')]:
    circle = plt.Circle((0.5, y), 0.3, facecolor='#0f3460', edgecolor='#00b4d8', lw=2, zorder=5)
    ax1.add_patch(circle)
    ax1.text(0.5, y, label, ha='center', va='center', fontsize=10, color='white', fontweight='bold', zorder=6)

# Output nodes
for y, label in [(2.5, 'y = 0'), (0.5, 'y = 1')]:
    circle = plt.Circle((3.5, y), 0.3, facecolor='#0f3460', edgecolor='#e94560', lw=2, zorder=5)
    ax1.add_patch(circle)
    ax1.text(3.5, y, label, ha='center', va='center', fontsize=10, color='white', fontweight='bold', zorder=6)

# Correct transmission arrows (straight)
ax1.annotate('', xy=(3.2, 2.5), xytext=(0.8, 2.5),
             arrowprops=dict(arrowstyle='->', color='#90be6d', lw=2.5))
ax1.text(2.0, 2.75, '1 − Pₑ', ha='center', fontsize=11, color='#90be6d', fontweight='bold')

ax1.annotate('', xy=(3.2, 0.5), xytext=(0.8, 0.5),
             arrowprops=dict(arrowstyle='->', color='#90be6d', lw=2.5))
ax1.text(2.0, 0.2, '1 − Pₑ', ha='center', fontsize=11, color='#90be6d', fontweight='bold')

# Error arrows (crossed)
ax1.annotate('', xy=(3.2, 0.5), xytext=(0.8, 2.5),
             arrowprops=dict(arrowstyle='->', color='#e94560', lw=2, linestyle='--'))
ax1.text(1.2, 1.2, 'Pₑ', ha='center', fontsize=11, color='#e94560', fontweight='bold')

ax1.annotate('', xy=(3.2, 2.5), xytext=(0.8, 0.5),
             arrowprops=dict(arrowstyle='->', color='#e94560', lw=2, linestyle='--'))
ax1.text(2.8, 1.8, 'Pₑ', ha='center', fontsize=11, color='#e94560', fontweight='bold')

# Labels
ax1.text(0.5, 3.3, 'INPUT', ha='center', fontsize=11, color='#00b4d8', fontweight='bold')
ax1.text(3.5, 3.3, 'OUTPUT', ha='center', fontsize=11, color='#e94560', fontweight='bold')
ax1.set_title('Binary Symmetric Channel (BSC)', color='white', fontsize=14, fontweight='bold', pad=15)

# ═══════════════════════════════════════
# RIGHT: Capacity vs Pe curve
# ═══════════════════════════════════════
ax2 = fig.add_subplot(1, 2, 2)
ax2.set_facecolor('#1a1a2e')

pe = np.linspace(0.001, 0.999, 500)
H_pe = -(pe * np.log2(pe) + (1 - pe) * np.log2(1 - pe))
Cs = 1 - H_pe

ax2.plot(pe, Cs, color='#00b4d8', lw=3, zorder=5)
ax2.fill_between(pe, Cs, alpha=0.12, color='#00b4d8')

# Key points
key_points = [(0.0, 1.0, 'Perfect\nCₛ = 1'), (0.5, 0.0, 'Useless\nCₛ = 0'), (1.0, 1.0, 'Inverter\nCₛ = 1')]
for px, cy, lbl in key_points:
    ax2.scatter([px], [cy], color='#e94560', s=100, zorder=10, edgecolor='white', linewidth=1.5)

ax2.annotate('Pₑ = 0\nPerfect channel', xy=(0.01, 0.97), xytext=(0.12, 0.75),
             fontsize=9, color='#90be6d', fontweight='bold',
             arrowprops=dict(arrowstyle='->', color='#90be6d', lw=1.5))
ax2.annotate('Pₑ = 0.5\nUseless channel', xy=(0.5, 0.02), xytext=(0.55, 0.25),
             fontsize=9, color='#e94560', fontweight='bold',
             arrowprops=dict(arrowstyle='->', color='#e94560', lw=1.5))
ax2.annotate('Pₑ = 1\nJust invert!', xy=(0.98, 0.97), xytext=(0.78, 0.75),
             fontsize=9, color='#f7a440', fontweight='bold',
             arrowprops=dict(arrowstyle='->', color='#f7a440', lw=1.5))

ax2.set_xlabel('Error Probability  Pₑ', color='#aaa', fontsize=12)
ax2.set_ylabel('Channel Capacity  Cₛ  (bits/use)', color='#aaa', fontsize=12)
ax2.set_title('BSC Capacity:  Cₛ = 1 − H(Pₑ)', color='white', fontsize=14, fontweight='bold', pad=15)
ax2.set_xlim(0, 1)
ax2.set_ylim(-0.05, 1.1)
ax2.grid(True, alpha=0.15)
ax2.tick_params(colors='#666')
for s in ax2.spines.values():
    s.set_color('#333')

plt.tight_layout()
out = os.path.join(os.path.dirname(__file__), 'bsc_channel.png')
plt.savefig(out, dpi=180, facecolor='#1a1a2e', bbox_inches='tight')
plt.close()
print(f"Saved: {out}")
