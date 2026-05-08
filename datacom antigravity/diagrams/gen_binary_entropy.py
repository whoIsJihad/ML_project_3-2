"""Generate the binary entropy function H(p) curve."""
import numpy as np
import matplotlib.pyplot as plt
import os

plt.style.use('dark_background')

fig, ax = plt.subplots(figsize=(8, 5))
fig.patch.set_facecolor('#1a1a2e')
ax.set_facecolor('#1a1a2e')

p = np.linspace(0.001, 0.999, 500)
H = -(p * np.log2(p) + (1 - p) * np.log2(1 - p))

ax.plot(p, H, color='#f7a440', lw=3, zorder=5)
ax.fill_between(p, H, alpha=0.15, color='#f7a440')

# Mark key points
key_ps = [0.5]
key_Hs = [1.0]
ax.scatter(key_ps, key_Hs, color='#e94560', s=100, zorder=10, edgecolor='white', linewidth=1.5)
ax.annotate('H(0.5) = 1 bit\n(maximum uncertainty)',
            xy=(0.5, 1.0), xytext=(0.68, 0.85),
            fontsize=10, color='white', fontweight='bold',
            arrowprops=dict(arrowstyle='->', color='#e94560', lw=2))

# Mark p=0 and p=1
ax.annotate('Certain event\nH = 0', xy=(0.05, 0.0), xytext=(0.12, 0.25),
            fontsize=9, color='#90be6d',
            arrowprops=dict(arrowstyle='->', color='#90be6d', lw=1.5))
ax.annotate('Certain event\nH = 0', xy=(0.95, 0.0), xytext=(0.75, 0.25),
            fontsize=9, color='#90be6d',
            arrowprops=dict(arrowstyle='->', color='#90be6d', lw=1.5))

ax.set_xlabel('Probability p', color='#aaa', fontsize=12)
ax.set_ylabel('H(p)  (bits)', color='#aaa', fontsize=12)
ax.set_title('Binary Entropy Function  H(p) = −[p log₂p + (1−p) log₂(1−p)]',
             color='white', fontsize=13, fontweight='bold')
ax.set_xlim(0, 1)
ax.set_ylim(-0.05, 1.15)
ax.grid(True, alpha=0.15)
ax.tick_params(colors='#666')
for s in ax.spines.values():
    s.set_color('#333')

plt.tight_layout()
out = os.path.join(os.path.dirname(__file__), 'binary_entropy.png')
plt.savefig(out, dpi=180, facecolor='#1a1a2e', bbox_inches='tight')
plt.close()
print(f"Saved: {out}")
