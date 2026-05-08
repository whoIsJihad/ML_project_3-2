"""Generate Huffman tree diagrams for the information theory notes."""
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import os

plt.style.use('dark_background')

# ─── Helper ───
def draw_node(ax, x, y, label, prob, color='#16213e', textcolor='white', radius=0.28):
    circle = plt.Circle((x, y), radius, facecolor=color, edgecolor='#555', linewidth=1.5, zorder=5)
    ax.add_patch(circle)
    ax.text(x, y + 0.06, label, ha='center', va='center', fontsize=8, color=textcolor, fontweight='bold', zorder=6)
    ax.text(x, y - 0.10, f'{prob}', ha='center', va='center', fontsize=7, color='#aaa', zorder=6)

def draw_edge(ax, x1, y1, x2, y2, label='', color='#555'):
    ax.plot([x1, x2], [y1, y2], color=color, lw=2, zorder=2)
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2
    if label:
        # offset label to the side
        dx = x2 - x1
        offset = -0.15 if dx < 0 else 0.15
        ax.text(mx + offset, my + 0.08, label, ha='center', va='center',
                fontsize=9, color='#f7a440', fontweight='bold', zorder=7)

# ═══════════════════════════════════════════════════
# TREE 1: Binary Huffman — Second-Order Extension
# ═══════════════════════════════════════════════════
fig1, ax1 = plt.subplots(figsize=(10, 7))
fig1.patch.set_facecolor('#1a1a2e')
ax1.set_facecolor('#1a1a2e')
ax1.set_xlim(-1.5, 5.5)
ax1.set_ylim(-0.5, 4.5)
ax1.axis('off')

# Root
draw_node(ax1, 2.5, 4, 'Root', '1.00', color='#0f3460')
# Level 1
draw_node(ax1, 1.0, 2.8, 'm₁m₁', '0.64', color='#2d6a4f')
draw_node(ax1, 4.0, 2.8, 'Node B', '0.36', color='#16213e')
draw_edge(ax1, 2.5, 4 - 0.28, 1.0, 2.8 + 0.28, '0', '#90be6d')
draw_edge(ax1, 2.5, 4 - 0.28, 4.0, 2.8 + 0.28, '1', '#e94560')
# Level 2
draw_node(ax1, 3.0, 1.4, 'm₁m₂', '0.16', color='#2d6a4f')
draw_node(ax1, 5.0, 1.4, 'Node A', '0.20', color='#16213e')
draw_edge(ax1, 4.0, 2.8 - 0.28, 3.0, 1.4 + 0.28, '0', '#90be6d')
draw_edge(ax1, 4.0, 2.8 - 0.28, 5.0, 1.4 + 0.28, '1', '#e94560')
# Level 3
draw_node(ax1, 4.2, 0.0, 'm₂m₁', '0.16', color='#2d6a4f')
draw_node(ax1, 5.8, 0.0, 'm₂m₂', '0.04', color='#2d6a4f')
draw_edge(ax1, 5.0, 1.4 - 0.28, 4.2, 0.0 + 0.28, '0', '#90be6d')
draw_edge(ax1, 5.0, 1.4 - 0.28, 5.8, 0.0 + 0.28, '1', '#e94560')

# Code labels at leaves
ax1.text(1.0, 2.8 - 0.45, 'Code: 0', ha='center', fontsize=8, color='#f7a440', style='italic')
ax1.text(3.0, 1.4 - 0.45, 'Code: 10', ha='center', fontsize=8, color='#f7a440', style='italic')
ax1.text(4.2, 0.0 - 0.45, 'Code: 110', ha='center', fontsize=8, color='#f7a440', style='italic')
ax1.text(5.8, 0.0 - 0.45, 'Code: 111', ha='center', fontsize=8, color='#f7a440', style='italic')

ax1.set_title('Binary Huffman Tree — Second-Order Extension (N=2)',
              color='white', fontsize=14, fontweight='bold', pad=15)

plt.tight_layout()
out1 = os.path.join(os.path.dirname(__file__), 'huffman_binary_n2.png')
fig1.savefig(out1, dpi=180, facecolor='#1a1a2e', bbox_inches='tight')
plt.close(fig1)
print(f"Saved: {out1}")

# ═══════════════════════════════════════════════════
# TREE 2: Quaternary (4-ary) Huffman — 6 messages
# ═══════════════════════════════════════════════════
fig2, ax2 = plt.subplots(figsize=(12, 7))
fig2.patch.set_facecolor('#1a1a2e')
ax2.set_facecolor('#1a1a2e')
ax2.set_xlim(-1, 11)
ax2.set_ylim(-0.8, 4.5)
ax2.axis('off')

# Root
draw_node(ax2, 5, 4, 'Root', '1.00', color='#0f3460')
# Level 1 — 4 branches
positions_l1 = [(1.5, 2.5), (3.5, 2.5), (6.5, 2.5), (9, 2.5)]
labels_l1 = ['m₁', 'Combined', 'm₂', 'm₃']
probs_l1 = ['0.30', '0.30', '0.25', '0.15']
codes_l1 = ['0', '1', '2', '3']
colors_l1 = ['#2d6a4f', '#16213e', '#2d6a4f', '#2d6a4f']

for (x, y), lab, p, code, c in zip(positions_l1, labels_l1, probs_l1, codes_l1, colors_l1):
    draw_node(ax2, x, y, lab, p, color=c)
    draw_edge(ax2, 5, 4 - 0.28, x, y + 0.28, code, '#c77dff')

# Level 2 — expand "Combined" into 4 branches
positions_l2 = [(1.8, 0.6), (3.3, 0.6), (4.8, 0.6), (6.3, 0.6)]
labels_l2 = ['m₄', 'm₅', 'm₆', 'm₇\n(dummy)']
probs_l2 = ['0.12', '0.10', '0.08', '0.00']
codes_l2 = ['0', '1', '2', '3']
colors_l2 = ['#2d6a4f', '#2d6a4f', '#2d6a4f', '#462a2a']

for (x, y), lab, p, code, c in zip(positions_l2, labels_l2, probs_l2, codes_l2, colors_l2):
    draw_node(ax2, x, y, lab, p, color=c)
    draw_edge(ax2, 3.5, 2.5 - 0.28, x, y + 0.28, code, '#c77dff')

# Code labels at leaves
leaf_codes = {
    (1.5, 2.5): 'Code: 0', (6.5, 2.5): 'Code: 2', (9, 2.5): 'Code: 3',
    (1.8, 0.6): 'Code: 10', (3.3, 0.6): 'Code: 11', (4.8, 0.6): 'Code: 12',
    (6.3, 0.6): 'Code: 13'
}
for (x, y), code in leaf_codes.items():
    ax2.text(x, y - 0.42, code, ha='center', fontsize=7, color='#f7a440', style='italic')

ax2.set_title('Quaternary (4-ary) Huffman Tree — 6 Messages + 1 Dummy',
              color='white', fontsize=14, fontweight='bold', pad=15)

plt.tight_layout()
out2 = os.path.join(os.path.dirname(__file__), 'huffman_quaternary.png')
fig2.savefig(out2, dpi=180, facecolor='#1a1a2e', bbox_inches='tight')
plt.close(fig2)
print(f"Saved: {out2}")
