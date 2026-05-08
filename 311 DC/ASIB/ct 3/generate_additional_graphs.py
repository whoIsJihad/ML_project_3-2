"""
Additional reference visualization: Frequency spectrum evolution through modulation stages
This creates a visual reference for understanding how signals transform in the frequency domain
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyBboxPatch
import os

os.makedirs('graphs', exist_ok=True)

print("Generating additional reference visualizations...")

# ============================================================================
# Spectrum Evolution Through Modulation
# ============================================================================

fig = plt.figure(figsize=(16, 10))
fig.suptitle('Frequency Domain Evolution: From Baseband to Modulated Signal', 
             fontsize=18, fontweight='bold', y=0.98)

# Define frequency axis
f = np.linspace(-300, 300, 1000)
f_c = 100  # carrier
B = 30     # bandwidth

# Create subplots in a 3x2 grid for different scenarios
scenarios = [
    ('Baseband Signal', lambda: np.exp(-((f)/25)**2)),
    ('DSB-SC Modulation (Suppressed Carrier)', lambda: 0.5*np.exp(-((f-f_c)/25)**2) + 0.5*np.exp(-((f+f_c)/25)**2)),
    ('Conventional AM (with Carrier)', lambda: 1.5*np.exp(-(np.abs(f-f_c)-25)**2/100) + 0.5*np.exp(-((f-f_c)/25)**2) + 0.5*np.exp(-((f+f_c)/25)**2)),
    ('SSB-USB (Upper Sideband Only)', lambda: np.exp(-((f-f_c)/25)**2) * (f > f_c-B)),
    ('VSB (Partial Suppression)', lambda: np.exp(-((f-f_c)/25)**2) + 0.3*np.exp(-((f+f_c)/25)**2)),
    ('Filtered Signal (Bandpass)', lambda: np.exp(-((f-f_c)/25)**2) * (1/(1+(2*(f-f_c)/50)**4)))
]

colors_scenario = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b']

for idx, (title, spectrum_func) in enumerate(scenarios, 1):
    ax = plt.subplot(2, 3, idx)
    
    spectrum = spectrum_func()
    spectrum = np.maximum(spectrum, 0)  # Ensure non-negative
    
    ax.fill_between(f, spectrum, alpha=0.5, color=colors_scenario[idx-1])
    ax.plot(f, spectrum, linewidth=2.5, color=colors_scenario[idx-1])
    
    # Add carrier frequency markers
    if idx > 1:
        ax.axvline(f_c, color='red', linestyle='--', linewidth=1.5, alpha=0.6, label=f'f_c = {f_c} MHz')
        ax.axvline(-f_c, color='red', linestyle='--', linewidth=1.5, alpha=0.6)
        # Bandwidth annotation
        ax.axvspan(f_c-B, f_c+B, alpha=0.1, color='green')
        ax.text(f_c, -0.05, f'2B = {2*B} MHz', ha='center', fontsize=9, 
               bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
    else:
        ax.axvspan(-B, B, alpha=0.1, color='green')
        ax.text(0, -0.05, f'B = {B} MHz', ha='center', fontsize=9,
               bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
    
    ax.set_xlabel('Frequency (MHz)', fontsize=10, fontweight='bold')
    ax.set_ylabel('Magnitude', fontsize=10, fontweight='bold')
    ax.set_title(title, fontsize=11, fontweight='bold', pad=10)
    ax.set_xlim([-300, 300])
    ax.set_ylim([-0.15, max(spectrum)*1.1])
    ax.grid(True, alpha=0.3)
    if idx > 1:
        ax.legend(loc='upper right', fontsize=9)

plt.tight_layout()
plt.savefig('graphs/08_spectrum_evolution.png', dpi=300, bbox_inches='tight')
print("✓ 08_spectrum_evolution.png")
plt.close()

# ============================================================================
# Modulation Index and Efficiency Detailed Analysis
# ============================================================================

fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('Conventional AM: Modulation Index & Efficiency Analysis', 
             fontsize=16, fontweight='bold')

# Plot 1: Time domain signals for different modulation indices
t = np.linspace(0, 5, 1000)
f_m = 1  # message frequency
f_c_sig = 10  # carrier frequency
m_t = np.sin(2*np.pi*f_m*t)

ax = axes[0, 0]
mu_values = [0.5, 0.8, 1.0]
colors_mu = ['#1f77b4', '#ff7f0e', '#2ca02c']

for mu, color in zip(mu_values, colors_mu):
    envelope_upper = 1 + mu*m_t
    ax.plot(t, envelope_upper, label=f'μ={mu} (envelope)', color=color, linewidth=2, linestyle='--')
    ax.plot(t, -envelope_upper, color=color, linewidth=2, linestyle='--')

ax.axhline(0, color='black', linewidth=0.5)
ax.set_xlabel('Time (s)', fontsize=10, fontweight='bold')
ax.set_ylabel('Envelope Amplitude', fontsize=10, fontweight='bold')
ax.set_title('AM Envelope for Different Modulation Indices', fontweight='bold')
ax.legend()
ax.grid(True, alpha=0.3)
ax.set_ylim([-2.2, 2.2])

# Plot 2: Efficiency vs modulation index with examples
mu_range = np.linspace(0, 1.2, 100)
efficiency = mu_range**2 / (2 + mu_range**2)
efficiency[mu_range > 1] = np.nan  # Undefined for over-modulation

ax = axes[0, 1]
ax.plot(mu_range, efficiency*100, linewidth=3, color='#1f77b4')
ax.fill_between(mu_range, efficiency*100, alpha=0.3, color='#1f77b4')
ax.scatter([0.5, 0.8, 1.0], 
          [0.5**2/(2+0.5**2)*100, 0.8**2/(2+0.8**2)*100, 1.0**2/(2+1.0**2)*100],
          s=150, c='red', zorder=5, edgecolors='black', linewidth=2)
ax.axvline(1.0, color='red', linestyle=':', linewidth=2, label='Over-modulation limit')
ax.set_xlabel('Modulation Index (μ)', fontsize=10, fontweight='bold')
ax.set_ylabel('Efficiency (%)', fontsize=10, fontweight='bold')
ax.set_title('Power Efficiency vs Modulation Index', fontweight='bold')
ax.legend()
ax.grid(True, alpha=0.3)
ax.set_xlim([0, 1.2])
ax.set_ylim([0, 40])

# Plot 3: Power distribution pie chart
ax = axes[1, 0]
mu_demo = 1.0
carrier_frac = 1 / (1 + mu_demo**2/2)
sideband_frac = (mu_demo**2/2) / (1 + mu_demo**2/2)

labels = ['Carrier\n(Wasted)', 'Sidebands\n(Message)']
sizes = [carrier_frac*100, sideband_frac*100]
colors_pie = ['#d62728', '#2ca02c']
explode = (0.1, 0)

ax.pie(sizes, explode=explode, labels=labels, colors=colors_pie, autopct='%1.1f%%',
       shadow=True, startangle=90, textprops={'fontsize': 11, 'fontweight': 'bold'})
ax.set_title(f'Power Distribution (μ={mu_demo})\nAM at Maximum Modulation', fontweight='bold')

# Plot 4: Required transmit power comparison
ax = axes[1, 1]
techniques_power = ['DSB-SC\n(Same SNR)', 'AM (50%)\nmod.', 'AM (100%)\nmod.']
power_required = [1.0, np.sqrt(3)/2, np.sqrt(3)]
colors_power = ['#2ca02c', '#ff7f0e', '#d62728']

bars = ax.bar(techniques_power, power_required, color=colors_power, alpha=0.7, edgecolor='black', linewidth=2)
ax.set_ylabel('Relative Transmit Power', fontsize=10, fontweight='bold')
ax.set_title('Power Requirements for Equivalent Link Performance', fontweight='bold')
ax.set_ylim([0, 2])
ax.grid(True, alpha=0.3, axis='y')

# Add value labels
for bar, power in zip(bars, power_required):
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height + 0.05,
            f'{power:.2f}x', ha='center', va='bottom', fontweight='bold', fontsize=10)

plt.tight_layout()
plt.savefig('graphs/09_modulation_index_analysis.png', dpi=300, bbox_inches='tight')
print("✓ 09_modulation_index_analysis.png")
plt.close()

# ============================================================================
# Demodulation Comparison
# ============================================================================

fig, axes = plt.subplots(1, 2, figsize=(14, 6))
fig.suptitle('Demodulation Methods: Coherent vs Envelope Detection', 
             fontsize=16, fontweight='bold')

# Coherent detection phase error impact
ax = axes[0]
phase_errors = np.linspace(0, 180, 100)
signal_amplitude = np.cos(np.deg2rad(phase_errors))
signal_amplitude_db = 20 * np.log10(np.abs(signal_amplitude))

ax.plot(phase_errors, signal_amplitude_db, linewidth=3, color='#1f77b4', label='Signal Recovery')
ax.fill_between(phase_errors, signal_amplitude_db, -40, alpha=0.3, color='#1f77b4')
ax.axhline(-3, color='red', linestyle='--', linewidth=2, label='3dB loss threshold')
ax.axvline(90, color='#d62728', linestyle=':', linewidth=2.5, label='Complete loss (90°)')
ax.set_xlabel('Phase Error (degrees)', fontsize=11, fontweight='bold')
ax.set_ylabel('Signal Recovery (dB)', fontsize=11, fontweight='bold')
ax.set_title('Coherent Detection: Sensitivity to Phase Error', fontweight='bold')
ax.legend(fontsize=10)
ax.grid(True, alpha=0.3)
ax.set_xlim([0, 180])
ax.set_ylim([-40, 5])

# Envelope detection robustness
ax = axes[1]
phase_errors_env = np.linspace(0, 180, 100)
# Envelope detection is immune to phase errors (envelope is independent of phase for μ < 1)
env_recovery = np.ones_like(phase_errors_env)
# But over-modulation causes distortion
over_mod = 0.95 - 0.2*np.sin(np.deg2rad(phase_errors_env/10))

ax.plot(phase_errors_env, env_recovery, linewidth=3, color='#2ca02c', label='Optimal (μ < 1)')
ax.fill_between(phase_errors_env, env_recovery, alpha=0.3, color='#2ca02c')
ax.plot(phase_errors_env, over_mod, linewidth=2.5, color='#d62728', linestyle='--', label='Over-modulated (μ > 1)')
ax.set_xlabel('Phase Error (degrees)', fontsize=11, fontweight='bold')
ax.set_ylabel('Envelope Recovery Fidelity', fontsize=11, fontweight='bold')
ax.set_title('Envelope Detection: Phase Independent', fontweight='bold')
ax.legend(fontsize=10)
ax.grid(True, alpha=0.3)
ax.set_xlim([0, 180])
ax.set_ylim([0.5, 1.1])

plt.tight_layout()
plt.savefig('graphs/10_demodulation_comparison.png', dpi=300, bbox_inches='tight')
print("✓ 10_demodulation_comparison.png")
plt.close()

print("\n✅ All additional visualizations generated successfully!")
print("Total generated: 10 high-quality visualization files")
