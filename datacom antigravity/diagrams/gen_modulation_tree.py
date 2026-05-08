"""Generate a modulation family tree diagram."""
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import os

fig, ax = plt.subplots(1, 1, figsize=(14, 9))
ax.set_xlim(0, 14)
ax.set_ylim(0, 9)
ax.axis('off')
fig.patch.set_facecolor('#1a1a2e')

def draw_box(x, y, text, color='#16213e', border='#e94560', fontsize=10, w=2.2, h=0.6):
    box = mpatches.FancyBboxPatch((x - w/2, y - h/2), w, h,
                                   boxstyle="round,pad=0.1",
                                   facecolor=color, edgecolor=border, linewidth=2)
    ax.add_patch(box)
    ax.text(x, y, text, ha='center', va='center', fontsize=fontsize,
            color='white', fontweight='bold', family='monospace')

def draw_arrow(x1, y1, x2, y2, color='#e94560'):
    ax.annotate('', xy=(x2, y2 + 0.3), xytext=(x1, y1 - 0.3),
                arrowprops=dict(arrowstyle='->', color=color, lw=1.8))

# Root
draw_box(7, 8.2, 'MODULATION', color='#0f3460', border='#e94560', fontsize=13, w=3, h=0.7)

# Level 1: Analog vs Digital
draw_box(4, 6.5, 'Analog\nModulation', color='#16213e', border='#f7a440', w=2.5, h=0.8)
draw_box(10, 6.5, 'Digital\nModulation', color='#16213e', border='#00b4d8', w=2.5, h=0.8)
draw_arrow(7, 8.2, 4, 6.5, '#f7a440')
draw_arrow(7, 8.2, 10, 6.5, '#00b4d8')

# Level 2: Analog types
draw_box(2, 4.8, 'AM', color='#1a1a2e', border='#f7a440', w=1.6)
draw_box(4, 4.8, 'FM', color='#1a1a2e', border='#f7a440', w=1.6)
draw_box(6, 4.8, 'PM', color='#1a1a2e', border='#f7a440', w=1.6)
draw_arrow(4, 6.5, 2, 4.8, '#f7a440')
draw_arrow(4, 6.5, 4, 4.8, '#f7a440')
draw_arrow(4, 6.5, 6, 4.8, '#f7a440')

# Level 2: Digital types
draw_box(8.2, 4.8, 'ASK', color='#1a1a2e', border='#00b4d8', w=1.6)
draw_box(10, 4.8, 'FSK', color='#1a1a2e', border='#00b4d8', w=1.6)
draw_box(11.8, 4.8, 'PSK', color='#1a1a2e', border='#00b4d8', w=1.6)
draw_arrow(10, 6.5, 8.2, 4.8, '#00b4d8')
draw_arrow(10, 6.5, 10, 4.8, '#00b4d8')
draw_arrow(10, 6.5, 11.8, 4.8, '#00b4d8')

# Level 3: AM variants
draw_box(1.2, 3.2, 'DSB-FC', color='#1a1a2e', border='#f7a440', w=1.5, fontsize=8)
draw_box(2.8, 3.2, 'DSB-SC', color='#1a1a2e', border='#f7a440', w=1.5, fontsize=8)
draw_arrow(2, 4.8, 1.2, 3.2, '#f7a44088')
draw_arrow(2, 4.8, 2.8, 3.2, '#f7a44088')

# Level 3: PSK variants
draw_box(11, 3.2, 'BPSK', color='#1a1a2e', border='#00b4d8', w=1.4, fontsize=8)
draw_box(12.6, 3.2, 'QPSK', color='#1a1a2e', border='#00b4d8', w=1.4, fontsize=8)
draw_arrow(11.8, 4.8, 11, 3.2, '#00b4d888')
draw_arrow(11.8, 4.8, 12.6, 3.2, '#00b4d888')

# Hybrid: QAM
draw_box(7, 3.2, 'QAM', color='#0f3460', border='#e94560', w=1.8, h=0.7)
# QAM connects from ASK and PSK
draw_arrow(8.2, 4.8, 7, 3.2, '#e9456088')
draw_arrow(11.8, 4.8, 7, 3.2, '#e9456088')

# PAM bridge
draw_box(4.5, 3.2, 'PAM', color='#0f3460', border='#90be6d', w=1.6)
draw_arrow(2, 4.8, 4.5, 3.2, '#90be6d88')  # from AM
draw_arrow(8.2, 4.8, 4.5, 3.2, '#90be6d88')  # connects to ASK conceptually

# OFDM at bottom
draw_box(7, 1.5, 'OFDM', color='#0f3460', border='#e94560', w=2, h=0.7)
draw_arrow(7, 3.2, 7, 1.5, '#e94560')

# QAM variants
draw_box(5.2, 1.5, '16-QAM', color='#1a1a2e', border='#e94560', w=1.5, fontsize=8)
draw_box(8.8, 1.5, '64-QAM', color='#1a1a2e', border='#e94560', w=1.5, fontsize=8)

# Labels
ax.text(4, 7.5, 'Continuous signals', fontsize=8, color='#f7a440', ha='center', style='italic')
ax.text(10, 7.5, 'Discrete symbols', fontsize=8, color='#00b4d8', ha='center', style='italic')
ax.text(4.5, 2.5, 'Sampling\nbridge', fontsize=7, color='#90be6d', ha='center', style='italic')
ax.text(7, 2.5, 'Multi-carrier', fontsize=7, color='#e94560', ha='center', style='italic')

ax.set_title('Modulation Family Tree', fontsize=16, color='white', fontweight='bold', pad=10, family='monospace')

plt.tight_layout()
out = os.path.join(os.path.dirname(__file__), 'modulation_tree.png')
plt.savefig(out, dpi=180, facecolor='#1a1a2e', bbox_inches='tight')
plt.close()
print(f"Saved: {out}")
