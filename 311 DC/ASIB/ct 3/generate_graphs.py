"""
Generate visualizations for Amplitude Modulation study guide
Run this script to generate all graphs used in the markdown files
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from scipy.special import erfc
import os

# Create output directory
os.makedirs('graphs', exist_ok=True)

# Set style
plt.style.use('seaborn-v0_8-darkgrid')
colors = {'primary': '#1f77b4', 'secondary': '#ff7f0e', 'success': '#2ca02c', 'danger': '#d62728'}

print("Generating visualizations...")

# ============================================================================
# 1. ANTENNA PROBLEM - Frequency vs Wavelength vs Antenna Size
# ============================================================================

fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('The Antenna Problem: Why Modulation is Necessary', fontsize=16, fontweight='bold')

# Frequency response
frequencies = np.array([3e3, 1e5, 1e6, 100e6, 1e9])
wavelengths = 3e8 / frequencies
antenna_sizes = wavelengths / 2

ax1.bar(range(len(frequencies)), frequencies/1e6, color=colors['primary'], alpha=0.7)
ax1.set_ylabel('Frequency (MHz)', fontsize=11, fontweight='bold')
ax1.set_xticks(range(len(frequencies)))
ax1.set_xticklabels(['Audio\n3kHz', 'AM Band\n100kHz', 'AM Radio\n1MHz', 'FM Band\n100MHz', 'Cellular\n1GHz'], fontsize=9)
ax1.set_title('Frequencies in Communication', fontweight='bold')
ax1.set_yscale('log')
ax1.grid(True, alpha=0.3)

# Wavelengths
ax2.bar(range(len(frequencies)), wavelengths/1000, color=colors['secondary'], alpha=0.7)
ax2.set_ylabel('Wavelength (km)', fontsize=11, fontweight='bold')
ax2.set_xticks(range(len(frequencies)))
ax2.set_xticklabels(['Audio\n3kHz', 'AM Band\n100kHz', 'AM Radio\n1MHz', 'FM Band\n100MHz', 'Cellular\n1GHz'], fontsize=9)
ax2.set_title('Wavelengths (λ = c/f)', fontweight='bold')
ax2.set_yscale('log')
ax2.grid(True, alpha=0.3)

# Antenna sizes
ax3.bar(range(len(frequencies)), antenna_sizes/1000, color=colors['danger'], alpha=0.7)
ax3.axhline(y=0.1, color='red', linestyle='--', linewidth=2, label='Practical antenna limit (100m)')
ax3.set_ylabel('Antenna Length (km)', fontsize=11, fontweight='bold')
ax3.set_xticks(range(len(frequencies)))
ax3.set_xticklabels(['Audio\n3kHz', 'AM Band\n100kHz', 'AM Radio\n1MHz', 'FM Band\n100MHz', 'Cellular\n1GHz'], fontsize=9)
ax3.set_title('Required Antenna Sizes (λ/2 dipole)', fontweight='bold')
ax3.set_yscale('log')
ax3.legend()
ax3.grid(True, alpha=0.3)

# Efficiency improvement
reduction_factor = antenna_sizes[0] / antenna_sizes[1:]
ax4.bar(range(1, len(frequencies)), reduction_factor, color=colors['success'], alpha=0.7)
ax4.set_ylabel('Size Reduction Factor', fontsize=11, fontweight='bold')
ax4.set_xticks(range(1, len(frequencies)))
ax4.set_xticklabels(['vs 100kHz', 'vs 1MHz', 'vs 100MHz', 'vs 1GHz'], fontsize=9)
ax4.set_title('Antenna Size Reduction by Modulation', fontweight='bold')
ax4.set_yscale('log')
ax4.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('graphs/01_antenna_problem.png', dpi=300, bbox_inches='tight')
print("✓ 01_antenna_problem.png")
plt.close()

# ============================================================================
# 2. DSB-SC vs AM - Power Efficiency Comparison
# ============================================================================

fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('DSB-SC vs Conventional AM: Power Efficiency Trade-off', fontsize=16, fontweight='bold')

# Efficiency vs modulation index
mu = np.linspace(0.1, 1.0, 50)
efficiency = mu**2 / (2 + mu**2)

ax1.plot(mu, efficiency*100, linewidth=3, color=colors['primary'])
ax1.fill_between(mu, efficiency*100, alpha=0.3, color=colors['primary'])
ax1.axvline(x=1.0, color='red', linestyle='--', linewidth=2, label='Max modulation (μ=1)')
ax1.axhline(y=33.3, color='green', linestyle='--', linewidth=2, label='Max efficiency ≈ 33%')
ax1.set_xlabel('Modulation Index (μ)', fontsize=11, fontweight='bold')
ax1.set_ylabel('Efficiency (%)', fontsize=11, fontweight='bold')
ax1.set_title('AM Power Efficiency vs Modulation Index', fontweight='bold')
ax1.legend()
ax1.grid(True, alpha=0.3)
ax1.set_ylim([0, 40])

# Power distribution for AM
techniques = ['DSB-SC', 'AM\n(50% mod.)', 'AM\n(100% mod.)']
carrier_power = [0, 50, 66.7]
sideband_power = [100, 50, 33.3]

x_pos = np.arange(len(techniques))
width = 0.6

ax2.bar(x_pos, carrier_power, width, label='Carrier Power (Wasted)', color=colors['danger'], alpha=0.8)
ax2.bar(x_pos, sideband_power, width, bottom=carrier_power, label='Sideband Power (Message)', color=colors['success'], alpha=0.8)
ax2.set_ylabel('Power Distribution (%)', fontsize=11, fontweight='bold')
ax2.set_title('Power Allocation by Technique', fontweight='bold')
ax2.set_xticks(x_pos)
ax2.set_xticklabels(techniques)
ax2.legend()
ax2.set_ylim([0, 105])
ax2.grid(True, alpha=0.3, axis='y')

# SNR Performance
snr_db = np.linspace(0, 30, 100)
snr_linear = 10**(snr_db/10)
ber_coherent = 0.5 * erfc(np.sqrt(snr_linear))
ber_envelope = 0.5 * erfc(np.sqrt(snr_linear * 0.5))  # Worse for envelope

ax3.semilogy(snr_db, ber_coherent, linewidth=2.5, label='DSB-SC (Coherent)', color=colors['primary'])
ax3.semilogy(snr_db, ber_envelope, linewidth=2.5, label='AM (Envelope)', color=colors['secondary'])
ax3.set_xlabel('SNR (dB)', fontsize=11, fontweight='bold')
ax3.set_ylabel('Bit Error Rate', fontsize=11, fontweight='bold')
ax3.set_title('Performance Comparison', fontweight='bold')
ax3.legend()
ax3.grid(True, alpha=0.3, which='both')
ax3.set_ylim([1e-10, 1])

# Complexity vs Performance (decluttered)
methods = ['DSB-SC', 'Conventional\nAM', 'SSB', 'QAM']
complexity = [3, 1, 4, 4]
efficiency_vals = [100, 33, 100, 100]

# smaller, distinct markers + gentle transparency
marker_colors = ['#6a5acd', '#5b9bd5', '#d62728', '#9acd32']
marker_sizes = [300, 180, 260, 260]
ax4.scatter(complexity, efficiency_vals, s=marker_sizes, alpha=0.75, c=marker_colors, edgecolors='k', linewidths=0.8)

# Smart annotations: offset labels + callouts to avoid overlap
offsets = [(0,10), (-30,-8), (0,10), (30,-8)]  # (x,y) in points
for i, method in enumerate(methods):
    x = complexity[i]
    y = efficiency_vals[i]
    dx, dy = offsets[i]
    # label box for readability
    bbox = dict(boxstyle='round,pad=0.2', fc='white', ec='gray', lw=0.4, alpha=0.95)
    if abs(dx) > 5 or abs(dy) > 5:
        ax4.annotate(method, xy=(x, y), xytext=(dx, dy), textcoords='offset points', ha='center', va='center', fontsize=9, bbox=bbox,
                     arrowprops=dict(arrowstyle='-', color='gray', lw=0.7, shrinkA=0, shrinkB=0))
    else:
        ax4.annotate(method, xy=(x, y), xytext=(dx, dy), textcoords='offset points', ha='center', va='center', fontsize=9, bbox=bbox)
    # small numeric efficiency label below the marker
    ax4.text(x, y-7, f'{y}%', ha='center', fontsize=8, color='black', bbox=dict(fc='white', ec='none', alpha=0.7))

# qualitative complexity ticks to make x-axis meaningful
ax4.set_xticks([1, 2, 3, 4])
ax4.set_xticklabels(['Low', 'Medium', 'High', 'Very High'], fontsize=9)
ax4.set_xlabel('Receiver Complexity (qualitative)', fontsize=11, fontweight='bold')
ax4.set_ylabel('Power Efficiency (%)', fontsize=11, fontweight='bold')
ax4.set_title('Efficiency vs Complexity Trade-off', fontweight='bold')
ax4.set_xlim([0.5, 4.5])
ax4.set_ylim([20, 110])
ax4.grid(True, alpha=0.22)


plt.tight_layout()
plt.savefig('graphs/02_power_efficiency.png', dpi=300, bbox_inches='tight')
print("✓ 02_power_efficiency.png")
plt.close()

# ============================================================================
# 3. QAM - Constellation Diagrams
# ============================================================================

fig, axes = plt.subplots(2, 2, figsize=(12, 12))
fig.suptitle('QAM Constellations: Orthogonal I-Q Modulation', fontsize=16, fontweight='bold')

# BPSK (2-QAM)
ax = axes[0, 0]
symbols_bpsk = np.array([[1, 0], [-1, 0]])
ax.scatter(symbols_bpsk[:, 0], symbols_bpsk[:, 1], s=300, c=colors['primary'], alpha=0.7, edgecolors='black', linewidth=2)
for i, (x, y) in enumerate(symbols_bpsk):
    ax.annotate(['0', '1'][i], (x, y), fontsize=12, fontweight='bold', ha='center', va='center', color='white')
ax.set_xlim([-1.5, 1.5])
ax.set_ylim([-1.5, 1.5])
ax.axhline(0, color='black', linewidth=0.5)
ax.axvline(0, color='black', linewidth=0.5)
ax.set_xlabel('I (In-phase)', fontsize=10, fontweight='bold')
ax.set_ylabel('Q (Quadrature)', fontsize=10, fontweight='bold')
ax.set_title('BPSK (2-QAM): 1 bit/symbol', fontweight='bold')
ax.grid(True, alpha=0.3)
ax.set_aspect('equal')

# QPSK (4-QAM)
ax = axes[0, 1]
symbols_qpsk = np.array([[1, 1], [-1, 1], [-1, -1], [1, -1]]) / np.sqrt(2)
ax.scatter(symbols_qpsk[:, 0], symbols_qpsk[:, 1], s=300, c=colors['secondary'], alpha=0.7, edgecolors='black', linewidth=2)
for i, (x, y) in enumerate(symbols_qpsk):
    ax.annotate(f'{i:02b}', (x, y), fontsize=11, fontweight='bold', ha='center', va='center', color='white')
ax.set_xlim([-1.5, 1.5])
ax.set_ylim([-1.5, 1.5])
ax.axhline(0, color='black', linewidth=0.5)
ax.axvline(0, color='black', linewidth=0.5)
ax.set_xlabel('I (In-phase)', fontsize=10, fontweight='bold')
ax.set_ylabel('Q (Quadrature)', fontsize=10, fontweight='bold')
ax.set_title('QPSK (4-QAM): 2 bits/symbol', fontweight='bold')
ax.grid(True, alpha=0.3)
ax.set_aspect('equal')

# 16-QAM
ax = axes[1, 0]
i_vals = [-3, -1, 1, 3]
q_vals = [-3, -1, 1, 3]
symbols_16qam = np.array([[i, q] for i in i_vals for q in q_vals])
ax.scatter(symbols_16qam[:, 0], symbols_16qam[:, 1], s=200, c=colors['danger'], alpha=0.7, edgecolors='black', linewidth=1.5)
ax.set_xlim([-4, 4])
ax.set_ylim([-4, 4])
ax.axhline(0, color='black', linewidth=0.5)
ax.axvline(0, color='black', linewidth=0.5)
ax.set_xlabel('I (In-phase)', fontsize=10, fontweight='bold')
ax.set_ylabel('Q (Quadrature)', fontsize=10, fontweight='bold')
ax.set_title('16-QAM: 4 bits/symbol', fontweight='bold')
ax.grid(True, alpha=0.3)
ax.set_aspect('equal')

# 64-QAM
ax = axes[1, 1]
i_vals = np.linspace(-7, 7, 8)
q_vals = np.linspace(-7, 7, 8)
symbols_64qam = np.array([[i, q] for i in i_vals for q in q_vals])
ax.scatter(symbols_64qam[:, 0], symbols_64qam[:, 1], s=100, c=colors['success'], alpha=0.7, edgecolors='black', linewidth=1)
ax.set_xlim([-8.5, 8.5])
ax.set_ylim([-8.5, 8.5])
ax.axhline(0, color='black', linewidth=0.5)
ax.axvline(0, color='black', linewidth=0.5)
ax.set_xlabel('I (In-phase)', fontsize=10, fontweight='bold')
ax.set_ylabel('Q (Quadrature)', fontsize=10, fontweight='bold')
ax.set_title('64-QAM: 6 bits/symbol', fontweight='bold')
ax.grid(True, alpha=0.3)
ax.set_aspect('equal')

plt.tight_layout()
plt.savefig('graphs/03_qam_constellations.png', dpi=300, bbox_inches='tight')
print("✓ 03_qam_constellations.png")
plt.close()

# ============================================================================
# 4. Orthogonality - Sin/Cos Integration
# ============================================================================

fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('Orthogonality: Why Sin and Cos Don\'t Interfere', fontsize=16, fontweight='bold')

t = np.linspace(0, 2*np.pi, 1000)
sin_signal = np.sin(t)
cos_signal = np.cos(t)

# Plot 1: Sine and Cosine (orthogonal basis)
ax1.plot(t, sin_signal, linewidth=2.5, label='sin(t)', color=colors['primary'])
ax1.plot(t, cos_signal, linewidth=2.5, label='cos(t)', color=colors['secondary'])
ax1.fill_between(t, sin_signal, alpha=0.2, color=colors['primary'])
ax1.fill_between(t, cos_signal, alpha=0.2, color=colors['secondary'])
ax1.set_xlabel('Time', fontsize=10, fontweight='bold')
ax1.set_ylabel('Amplitude', fontsize=10, fontweight='bold')
ax1.set_title('Orthogonal Basis Functions', fontweight='bold')
ax1.legend(fontsize=10)
ax1.grid(True, alpha=0.3)

# Plot 2: Product sin*cos
product = sin_signal * cos_signal
ax2.plot(t, product, linewidth=2.5, color=colors['danger'])
ax2.fill_between(t, product, alpha=0.3, color=colors['danger'])
ax2.axhline(0, color='black', linewidth=1)
ax2.set_xlabel('Time', fontsize=10, fontweight='bold')
ax2.set_ylabel('Amplitude', fontsize=10, fontweight='bold')
ax2.set_title('Product: sin(t)·cos(t)\n∫sin·cos dt = 0 (Orthogonal)', fontweight='bold')
ax2.grid(True, alpha=0.3)

# Plot 3: Cumulative integral of sin*cos
cumulative_integral = np.cumsum(product) * (t[1] - t[0])
ax3.plot(t, cumulative_integral, linewidth=2.5, color=colors['success'])
ax3.fill_between(t, cumulative_integral, alpha=0.3, color=colors['success'])
ax3.axhline(0, color='red', linestyle='--', linewidth=2, label='Zero integral → Orthogonal')
ax3.set_xlabel('Time', fontsize=10, fontweight='bold')
ax3.set_ylabel('Cumulative Integral', fontsize=10, fontweight='bold')
ax3.set_title('Cumulative Orthogonality Integral', fontweight='bold')
ax3.legend()
ax3.grid(True, alpha=0.3)

# Plot 4: QAM signals don't interfere
t_qam = np.linspace(0, 0.02, 1000)
carrier = 2 * np.pi * 100  # 100 Hz carrier
i_signal = np.cos(carrier * t_qam)
q_signal = 0.7 * np.sin(carrier * t_qam)
combined = i_signal + q_signal

ax4.plot(t_qam, i_signal, linewidth=2, label='I-component: cos', color=colors['primary'], alpha=0.8)
ax4.plot(t_qam, q_signal, linewidth=2, label='Q-component: sin', color=colors['secondary'], alpha=0.8)
ax4.plot(t_qam, combined, linewidth=2.5, label='Combined (no interference!)', color='black', linestyle='--')
ax4.set_xlabel('Time (s)', fontsize=10, fontweight='bold')
ax4.set_ylabel('Amplitude', fontsize=10, fontweight='bold')
ax4.set_title('QAM: Two Signals, One Frequency, No Interference', fontweight='bold')
ax4.legend(fontsize=9)
ax4.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('graphs/04_orthogonality.png', dpi=300, bbox_inches='tight')
print("✓ 04_orthogonality.png")
plt.close()

# ============================================================================
# 5. Bandwidth Efficiency - DSB-SC vs SSB vs VSB
# ============================================================================

fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('Bandwidth Efficiency: DSB-SC vs SSB vs VSB', fontsize=16, fontweight='bold')

# Frequency domain representation
f = np.linspace(-200, 200, 1000)
f_c = 100  # carrier frequency
B = 50     # baseband bandwidth

# Baseband spectrum
baseband = np.exp(-((f) / 30)**2)

# DSB-SC (both sidebands)
dsb_upper = 0.5 * np.exp(-((f - f_c) / 30)**2)
dsb_lower = 0.5 * np.exp(-((f + f_c) / 30)**2)

# SSB-USB (upper sideband only)
ssb_upper = np.exp(-((f - f_c) / 30)**2)

# VSB (partial lower sideband)
vsb_upper = np.exp(-((f - f_c) / 30)**2)
vsb_lower_partial = 0.3 * np.exp(-((f + f_c) / 30)**2)

# Plot baseband
ax1.fill_between(f, baseband, alpha=0.5, color=colors['primary'])
ax1.plot(f, baseband, linewidth=2, color=colors['primary'])
ax1.axvline(0, color='black', linestyle='--', linewidth=1, alpha=0.5)
ax1.set_xlim([-200, 200])
ax1.set_ylim([0, 1.1])
ax1.set_xlabel('Frequency (MHz)', fontsize=10, fontweight='bold')
ax1.set_ylabel('Magnitude', fontsize=10, fontweight='bold')
ax1.set_title('Baseband Signal: Bandwidth = B', fontweight='bold')
ax1.text(0, -0.15, 'BW = B', ha='center', transform=ax1.get_xaxis_transform(), fontsize=10, fontweight='bold', color=colors['primary'])
ax1.grid(True, alpha=0.3)

# Plot DSB-SC
ax2.fill_between(f, dsb_upper, alpha=0.5, color=colors['primary'], label='USB')
ax2.fill_between(f, dsb_lower, alpha=0.5, color=colors['secondary'], label='LSB')
ax2.plot(f, dsb_upper, linewidth=2, color=colors['primary'])
ax2.plot(f, dsb_lower, linewidth=2, color=colors['secondary'])
ax2.axvline(f_c, color='red', linestyle='--', linewidth=1, alpha=0.7)
ax2.axvline(-f_c, color='red', linestyle='--', linewidth=1, alpha=0.7)
ax2.set_xlim([-200, 200])
ax2.set_ylim([0, 1.1])
ax2.set_xlabel('Frequency (MHz)', fontsize=10, fontweight='bold')
ax2.set_ylabel('Magnitude', fontsize=10, fontweight='bold')
ax2.set_title('DSB-SC: Bandwidth = 2B (Both Sidebands)', fontweight='bold')
ax2.text(f_c, -0.15, 'BW = 2B', ha='center', fontsize=10, fontweight='bold', color=colors['primary'])
ax2.legend()
ax2.grid(True, alpha=0.3)

# Plot SSB-USB
ax3.fill_between(f, ssb_upper, alpha=0.5, color=colors['success'])
ax3.plot(f, ssb_upper, linewidth=2, color=colors['success'])
ax3.axvline(f_c, color='red', linestyle='--', linewidth=1, alpha=0.7)
ax3.set_xlim([-200, 200])
ax3.set_ylim([0, 1.1])
ax3.set_xlabel('Frequency (MHz)', fontsize=10, fontweight='bold')
ax3.set_ylabel('Magnitude', fontsize=10, fontweight='bold')
ax3.set_title('SSB-USB: Bandwidth = B (50% Savings!)', fontweight='bold')
ax3.text(f_c, -0.15, 'BW = B\n(50% saved)', ha='center', fontsize=10, fontweight='bold', color=colors['success'])
ax3.grid(True, alpha=0.3)

# Plot VSB
ax4.fill_between(f, vsb_upper, alpha=0.5, color=colors['danger'], label='Full USB')
ax4.fill_between(f, vsb_lower_partial, alpha=0.5, color=colors['secondary'], label='Vestigial LSB')
ax4.plot(f, vsb_upper, linewidth=2, color=colors['danger'])
ax4.plot(f, vsb_lower_partial, linewidth=2, color=colors['secondary'])
ax4.axvline(f_c, color='red', linestyle='--', linewidth=1, alpha=0.7)
ax4.set_xlim([-200, 200])
ax4.set_ylim([0, 1.1])
ax4.set_xlabel('Frequency (MHz)', fontsize=10, fontweight='bold')
ax4.set_ylabel('Magnitude', fontsize=10, fontweight='bold')
ax4.set_title('VSB: Bandwidth = B + ΔB (Practical Compromise)', fontweight='bold')
ax4.text(f_c, -0.15, 'BW ≈ 1.25B\n(TV broadcast)', ha='center', fontsize=10, fontweight='bold', color=colors['danger'])
ax4.legend()
ax4.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('graphs/05_bandwidth_efficiency.png', dpi=300, bbox_inches='tight')
print("✓ 05_bandwidth_efficiency.png")
plt.close()

# ============================================================================
# 6. PLL Dynamics - Lock and Pull-in Behavior
# ============================================================================

fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('Phase Locked Loop (PLL): Tracking and Lock Dynamics', fontsize=16, fontweight='bold')

# Phase error over time (acquisition to lock)
t_pll = np.linspace(0, 1, 1000)
phase_error_acq = np.pi * np.exp(-5*t_pll) * np.sin(10*t_pll)  # Damped oscillation
phase_error_track = 0.05 * np.sin(2*np.pi*t_pll)  # Residual noise after lock

ax1.plot(t_pll[:500], phase_error_acq[:500], linewidth=2.5, color=colors['danger'], label='Acquisition phase')
ax1.plot(t_pll[500:], phase_error_track[500:], linewidth=2.5, color=colors['success'], label='Locked phase (with noise)')
ax1.axhline(0, color='black', linewidth=1, linestyle='--', alpha=0.5)
ax1.axvline(0.5, color='gray', linewidth=1.5, linestyle=':', alpha=0.7, label='Lock point')
ax1.fill_between(t_pll[500:], -0.1, 0.1, alpha=0.2, color=colors['success'])
ax1.set_xlabel('Time (s)', fontsize=10, fontweight='bold')
ax1.set_ylabel('Phase Error (rad)', fontsize=10, fontweight='bold')
ax1.set_title('Phase Error: Acquisition → Lock', fontweight='bold')
ax1.set_ylim([-3.5, 3.5])
ax1.legend()
ax1.grid(True, alpha=0.3)

# VCO frequency correction
frequency_error = 1000 * (1 - np.exp(-3*t_pll))  # Hz
vco_correction = frequency_error * 0.1

ax2.plot(t_pll, frequency_error, linewidth=2.5, color=colors['primary'], label='Frequency error')
ax2.plot(t_pll, vco_correction, linewidth=2.5, color=colors['secondary'], label='VCO correction')
ax2.axhline(0, color='black', linewidth=1, linestyle='--', alpha=0.5)
ax2.set_xlabel('Time (s)', fontsize=10, fontweight='bold')
ax2.set_ylabel('Frequency (Hz)', fontsize=10, fontweight='bold')
ax2.set_title('VCO Frequency Correction Over Time', fontweight='bold')
ax2.legend()
ax2.grid(True, alpha=0.3)

# Phase detector characteristic
phase_range = np.linspace(-np.pi, np.pi, 500)
pd_output = np.sin(phase_range)

ax3.plot(phase_range, pd_output, linewidth=3, color=colors['primary'])
ax3.fill_between(phase_range, pd_output, alpha=0.3, color=colors['primary'])
ax3.axhline(0, color='black', linewidth=1)
ax3.axvline(0, color='red', linewidth=2, linestyle='--', alpha=0.7, label='Lock point (Δφ = 0)')
ax3.axvspan(-np.pi/2, np.pi/2, alpha=0.1, color=colors['success'], label='Lock range')
ax3.set_xlabel('Phase Error Δφ (rad)', fontsize=10, fontweight='bold')
ax3.set_ylabel('Phase Detector Output (V)', fontsize=10, fontweight='bold')
ax3.set_title('Phase Detector Characteristic: S-curve', fontweight='bold')
ax3.set_xticks([-np.pi, -np.pi/2, 0, np.pi/2, np.pi])
ax3.set_xticklabels(['-π', '-π/2', '0', 'π/2', 'π'])
ax3.legend()
ax3.grid(True, alpha=0.3)

# Loop bandwidth vs lock time trade-off
bandwidth = np.logspace(2, 5, 50)  # 100 Hz to 100 kHz
lock_time = 1000 / bandwidth  # Inverse relationship
noise_floor = 0.1 * np.sqrt(bandwidth)

ax4_twin = ax4.twinx()
line1 = ax4.loglog(bandwidth, lock_time, linewidth=3, color=colors['primary'], label='Lock time')
ax4.set_xlabel('Loop Bandwidth (Hz)', fontsize=10, fontweight='bold')
ax4.set_ylabel('Lock Time (ms)', fontsize=10, fontweight='bold', color=colors['primary'])
ax4.tick_params(axis='y', labelcolor=colors['primary'])

line2 = ax4_twin.loglog(bandwidth, noise_floor, linewidth=3, color=colors['danger'], label='Phase noise floor')
ax4_twin.set_ylabel('Phase Noise (rad)', fontsize=10, fontweight='bold', color=colors['danger'])
ax4_twin.tick_params(axis='y', labelcolor=colors['danger'])

ax4.set_title('PLL Design Trade-off: Bandwidth vs Performance', fontweight='bold')
ax4.grid(True, alpha=0.3, which='both')

# Combined legend
lines = [line1[0], line2[0]]
labels = [l.get_label() for l in lines]
ax4.legend(lines, labels, loc='center', fontsize=9)

plt.tight_layout()
plt.savefig('graphs/06_pll_dynamics.png', dpi=300, bbox_inches='tight')
print("✓ 06_pll_dynamics.png")
plt.close()

# ============================================================================
# 7. Spectral Efficiency Comparison
# ============================================================================

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
fig.suptitle('Spectral Efficiency: Modern vs Classical Modulation', fontsize=16, fontweight='bold')

# Bar chart of spectral efficiency
techniques_eff = ['BPSK\n(DSB-SC)', 'QPSK\n(DSB-SC)', '16-QAM\n(DSB-SC)', 'BPSK\n(SSB)', 'QPSK\n(SSB)', '16-QAM\n(SSB)', 'OFDM\n(WiFi)']
efficiencies = [0.5, 1.0, 2.0, 1.0, 2.0, 4.0, 3.0]
colors_eff = [colors['primary']]*3 + [colors['success']]*3 + [colors['secondary']]

bars = ax1.bar(range(len(techniques_eff)), efficiencies, color=colors_eff, alpha=0.7, edgecolor='black', linewidth=1.5)
ax1.set_ylabel('Spectral Efficiency (bits/Hz)', fontsize=11, fontweight='bold')
ax1.set_title('Spectral Efficiency Comparison', fontweight='bold')
ax1.set_xticks(range(len(techniques_eff)))
ax1.set_xticklabels(techniques_eff, fontsize=9)
ax1.set_ylim([0, 4.5])
ax1.grid(True, alpha=0.3, axis='y')

# Add value labels on bars
for i, (bar, eff) in enumerate(zip(bars, efficiencies)):
    ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1, f'{eff:.1f}', 
             ha='center', va='bottom', fontweight='bold', fontsize=9)

# Bandwidth vs Efficiency Trade-off
modulation_types = ['DSB-SC', 'SSB', 'VSB', 'QAM\n(Multiple)', 'OFDM']
bandwidth_factor = [2, 1, 1.25, 2, 2]
efficiency_array = [1, 2, 1.75, 4, 3]
sizes = [150, 200, 180, 300, 250]

scatter = ax2.scatter(bandwidth_factor, efficiency_array, s=sizes, alpha=0.6, 
                     c=range(len(modulation_types)), cmap='viridis', edgecolors='black', linewidth=2)
for i, txt in enumerate(modulation_types):
    ax2.annotate(txt, (bandwidth_factor[i], efficiency_array[i]), 
                ha='center', va='center', fontweight='bold', fontsize=9)

ax2.set_xlabel('Normalized Bandwidth (B = 1)', fontsize=11, fontweight='bold')
ax2.set_ylabel('Spectral Efficiency (bits/Hz)', fontsize=11, fontweight='bold')
ax2.set_title('Bandwidth-Efficiency Frontier', fontweight='bold')
ax2.set_xlim([0.8, 2.2])
ax2.set_ylim([0.5, 4.5])
ax2.grid(True, alpha=0.3)

# Add frontier line
bw_frontier = np.array([1, 1.25, 2])
eff_frontier = np.array([2, 1.75, 1])
ax2.plot(bw_frontier, eff_frontier, 'k--', linewidth=2, alpha=0.5, label='Pareto frontier')

plt.tight_layout()
plt.savefig('graphs/07_spectral_efficiency.png', dpi=300, bbox_inches='tight')
print("✓ 07_spectral_efficiency.png")
plt.close()

print("\n✅ All visualizations generated successfully!")
print("Generated files in: graphs/")
