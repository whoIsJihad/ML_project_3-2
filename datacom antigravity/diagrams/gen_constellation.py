"""Generate PSK and QAM constellation diagrams."""
import numpy as np
import matplotlib.pyplot as plt
import os

plt.style.use('dark_background')

fig, axes = plt.subplots(2, 3, figsize=(14, 9))
fig.patch.set_facecolor('#1a1a2e')

def draw_constellation(ax, points, title, color='#e94560', label_points=True):
    ax.set_facecolor('#1a1a2e')
    circle = plt.Circle((0, 0), 1, fill=False, color='#333', linestyle='--', lw=1)
    ax.add_patch(circle)
    ax.axhline(0, color='#333', lw=0.5); ax.axvline(0, color='#333', lw=0.5)
    for i, (x, y) in enumerate(points):
        ax.plot(x, y, 'o', color=color, markersize=10, markeredgecolor='white', markeredgewidth=1.5)
        if label_points:
            bits = format(i, f'0{int(np.log2(len(points)))}b')
            ax.annotate(bits, (x, y), textcoords="offset points", xytext=(8, 8),
                       fontsize=7, color='#ccc', family='monospace')
    ax.set_title(title, color=color, fontsize=12, fontweight='bold')
    ax.set_xlabel('In-Phase (I)', color='#888', fontsize=9)
    ax.set_ylabel('Quadrature (Q)', color='#888', fontsize=9)
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.1)
    for s in ax.spines.values(): s.set_color('#333')
    ax.tick_params(colors='#666')

# BPSK
bpsk = [(-1, 0), (1, 0)]
draw_constellation(axes[0,0], bpsk, 'BPSK (1 bit/symbol)', '#f7a440')

# QPSK
qpsk = [(np.cos(np.pi/4 + i*np.pi/2), np.sin(np.pi/4 + i*np.pi/2)) for i in range(4)]
draw_constellation(axes[0,1], qpsk, 'QPSK (2 bits/symbol)', '#00b4d8')

# 8-PSK
psk8 = [(np.cos(i*np.pi/4), np.sin(i*np.pi/4)) for i in range(8)]
draw_constellation(axes[0,2], psk8, '8-PSK (3 bits/symbol)', '#e94560')

# 16-QAM
qam16 = []
for i in [-3, -1, 1, 3]:
    for q in [-3, -1, 1, 3]:
        qam16.append((i/3, q/3))
draw_constellation(axes[1,0], qam16, '16-QAM (4 bits/symbol)', '#90be6d', label_points=False)
axes[1,0].set_xlim(-1.5, 1.5); axes[1,0].set_ylim(-1.5, 1.5)

# 64-QAM
qam64 = []
vals = np.linspace(-7, 7, 8)
for i in vals:
    for q in vals:
        qam64.append((i/7, q/7))
draw_constellation(axes[1,1], qam64, '64-QAM (6 bits/symbol)', '#c77dff', label_points=False)
axes[1,1].set_xlim(-1.5, 1.5); axes[1,1].set_ylim(-1.5, 1.5)

# Comparison: decision regions for QPSK
ax = axes[1,2]
ax.set_facecolor('#1a1a2e')
ax.fill_between([-1.5, 0], 0, 1.5, alpha=0.15, color='#f7a440')
ax.fill_between([0, 1.5], 0, 1.5, alpha=0.15, color='#00b4d8')
ax.fill_between([-1.5, 0], -1.5, 0, alpha=0.15, color='#90be6d')
ax.fill_between([0, 1.5], -1.5, 0, alpha=0.15, color='#e94560')
for i, (x, y) in enumerate(qpsk):
    ax.plot(x, y, 'o', color='white', markersize=12, markeredgecolor='white', markeredgewidth=2)
    bits = format(i, '02b')
    ax.annotate(bits, (x, y), textcoords="offset points", xytext=(10, 10),
               fontsize=11, color='white', fontweight='bold', family='monospace')
ax.axhline(0, color='white', lw=1); ax.axvline(0, color='white', lw=1)
ax.set_title('QPSK Decision Regions', color='white', fontsize=12, fontweight='bold')
ax.set_xlabel('I', color='#888', fontsize=9); ax.set_ylabel('Q', color='#888', fontsize=9)
ax.set_aspect('equal'); ax.set_xlim(-1.5, 1.5); ax.set_ylim(-1.5, 1.5)
ax.grid(True, alpha=0.1)
for s in ax.spines.values(): s.set_color('#333')
ax.tick_params(colors='#666')

plt.suptitle('Constellation Diagrams — PSK & QAM', fontsize=15, color='white', fontweight='bold', y=1.01)
plt.tight_layout()
out = os.path.join(os.path.dirname(__file__), 'constellation_diagrams.png')
plt.savefig(out, dpi=180, facecolor='#1a1a2e', bbox_inches='tight')
plt.close()
print(f"Saved: {out}")
