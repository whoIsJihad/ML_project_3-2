"""Generate mutual information / entropy Venn diagram and extension efficiency bar chart."""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
import os

plt.style.use('dark_background')

fig = plt.figure(figsize=(14, 6))
fig.patch.set_facecolor('#1a1a2e')

# ═══════════════════════════════════════
# LEFT: Entropy Venn Diagram
# ═══════════════════════════════════════
ax1 = fig.add_subplot(1, 2, 1)
ax1.set_facecolor('#1a1a2e')
ax1.set_xlim(-2.5, 2.5)
ax1.set_ylim(-1.8, 2.2)
ax1.set_aspect('equal')
ax1.axis('off')

# Two overlapping circles
circle1 = plt.Circle((-0.5, 0), 1.3, facecolor='#00b4d8', alpha=0.2, edgecolor='#00b4d8', lw=2.5)
circle2 = plt.Circle((0.5, 0), 1.3, facecolor='#e94560', alpha=0.2, edgecolor='#e94560', lw=2.5)
ax1.add_patch(circle1)
ax1.add_patch(circle2)

# Labels
ax1.text(-1.1, 0, 'H(X|Y)', ha='center', va='center', fontsize=13, color='#00b4d8', fontweight='bold')
ax1.text(0, 0, 'I(X;Y)', ha='center', va='center', fontsize=14, color='white', fontweight='bold')
ax1.text(1.1, 0, 'H(Y|X)', ha='center', va='center', fontsize=13, color='#e94560', fontweight='bold')

ax1.text(-0.5, 1.7, 'H(X)', ha='center', va='center', fontsize=12, color='#00b4d8', fontweight='bold')
ax1.text(0.5, 1.7, 'H(Y)', ha='center', va='center', fontsize=12, color='#e94560', fontweight='bold')

# Brace for H(X,Y)
ax1.annotate('', xy=(-1.8, -1.5), xytext=(1.8, -1.5),
             arrowprops=dict(arrowstyle='<->', color='#f7a440', lw=2))
ax1.text(0, -1.75, 'H(X, Y)', ha='center', va='center', fontsize=12, color='#f7a440', fontweight='bold')

ax1.set_title('Entropy & Mutual Information — Venn Diagram',
              color='white', fontsize=13, fontweight='bold', pad=15)

# ═══════════════════════════════════════
# RIGHT: Extension Efficiency Bar Chart
# ═══════════════════════════════════════
ax2 = fig.add_subplot(1, 2, 2)
ax2.set_facecolor('#1a1a2e')

orders = ['N=1\n(single)', 'N=2\n(pairs)', 'N=3\n(triples)', 'N→∞\n(limit)']
efficiencies = [72.2, 92.6, 99.2, 100.0]
avg_lengths = [1.000, 0.780, 0.728, 0.722]
colors = ['#e94560', '#f7a440', '#90be6d', '#00b4d8']

bars = ax2.bar(orders, efficiencies, color=colors, edgecolor='white', linewidth=0.5, width=0.55)
for bar, eff, L in zip(bars, efficiencies, avg_lengths):
    ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1.5,
             f'{eff}%', ha='center', fontsize=11, color='white', fontweight='bold')
    ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height()/2,
             f'L = {L:.3f}', ha='center', fontsize=9, color='white', alpha=0.8)

# Entropy line
ax2.axhline(y=72.2, color='#e94560', linestyle=':', lw=1.5, alpha=0.5)
ax2.text(3.6, 73.5, 'H = 0.722 bits', fontsize=8, color='#e94560', alpha=0.7)

ax2.set_ylabel('Code Efficiency η (%)', color='#aaa', fontsize=12)
ax2.set_title('Source Extension — Efficiency Improvement\n(p₁=0.8, p₂=0.2, binary Huffman)',
              color='white', fontsize=12, fontweight='bold', pad=10)
ax2.set_ylim(0, 115)
ax2.grid(True, alpha=0.1, axis='y')
ax2.tick_params(colors='#666')
for s in ax2.spines.values():
    s.set_color('#333')

plt.tight_layout()
out = os.path.join(os.path.dirname(__file__), 'mutual_info_and_extensions.png')
plt.savefig(out, dpi=180, facecolor='#1a1a2e', bbox_inches='tight')
plt.close()
print(f"Saved: {out}")
