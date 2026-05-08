# Amplitude Modulation Study Guide (CSE 311)

## 📚 Complete Study Materials

A comprehensive, first-principles exploration of amplitude modulation and related communications concepts. **All materials are exam-ready with visual diagrams, mathematical proofs, and real-world applications.**

---

## 📖 Study Modules

### 1. [The Antenna Problem](01_antenna_problem.md) – Why Modulation is Necessary
- **Key Concepts:** Wavelength-frequency relationship, antenna size scaling, multiplexing advantages
- **Mathematical Focus:** $\lambda = c/f$, half-wave dipole requirements
- **Visualizations:** Antenna size vs frequency curves, bandwidth comparison
- **Real Example:** 50 km antenna → 150 m with modulation (333× reduction!)

### 2. [DSB-SC vs Conventional AM](02_dsb_sc_vs_am.md) – Power vs Complexity Trade-off
- **Key Concepts:** Power efficiency analysis, coherent vs envelope detection
- **Mathematical Focus:** Power decomposition, modulation index, efficiency formula
- **Visualizations:** Power distribution pie charts, efficiency curves, SNR performance
- **Real Example:** AM achieves only 33% maximum efficiency (vs 100% for DSB-SC)

### 3. [QAM & Orthogonality](03_qam_orthogonality.md) – Two Signals, One Frequency
- **Key Concepts:** Orthogonal basis functions, sin-cos independence, signal space
- **Mathematical Focus:** Inner products, Fourier decomposition, constellation diagrams
- **Visualizations:** BPSK/QPSK/16-QAM/64-QAM constellations, orthogonality proof
- **Real Example:** 16-QAM achieves 4 bits/symbol, no interference between I and Q

### 4. [Bandwidth Efficiency](04_bandwidth_efficiency.md) – DSB-SC, SSB, and VSB
- **Key Concepts:** Hilbert transform, sideband suppression, bandwidth savings
- **Mathematical Focus:** Analytic signals, $\int \sin \cos dt = 0$, VSB filtering
- **Visualizations:** Spectrum evolution (DSB → SSB → VSB), efficiency frontier
- **Real Example:** SSB saves 50% bandwidth (B vs 2B), used in aviation

### 5. [Phase Locked Loop (PLL)](05_phase_locked_loop.md) – Automatic Synchronization
- **Key Concepts:** Feedback control, phase detection, VCO tracking
- **Mathematical Focus:** Phase error dynamics, lock range, acquisition time
- **Visualizations:** PLL architecture diagram (Mermaid), lock behavior, trade-offs
- **Real Example:** FM radio tuning, satellite tracking, modern QAM demodulation

---

## 📊 Visual Resources

### Generated Graphs (High-Resolution, 300 DPI)

| File | Purpose | Use Case |
|------|---------|----------|
| `01_antenna_problem.png` | Antenna sizing across frequency bands | Understanding modulation necessity |
| `02_power_efficiency.png` | DSB-SC vs AM efficiency comparison | Power/complexity trade-offs |
| `03_qam_constellations.png` | BPSK/QPSK/16-QAM/64-QAM diagrams | Signal constellation reference |
| `04_orthogonality.png` | Sin-cos independence proof | Orthogonality visualization |
| `05_bandwidth_efficiency.png` | DSB-SC vs SSB vs VSB spectra | Bandwidth comparison |
| `06_pll_dynamics.png` | PLL lock behavior and phase error | PLL performance analysis |
| `07_spectral_efficiency.png` | Bits/Hz comparison chart | Modern modulation efficiency |
| `08_spectrum_evolution.png` | Signal transformation stages | Frequency domain evolution |
| `09_modulation_index_analysis.png` | AM modulation index effects | Envelope and efficiency |
| `10_demodulation_comparison.png` | Coherent vs envelope detection | Demodulation robustness |

### Mermaid Diagrams (Embedded in Markdown)

- **PLL Architecture:** Block diagram with Phase Detector, LPF, VCO
- **Costas Loop:** QAM demodulation architecture
- (Additional ASCII/Mermaid diagrams in each module)

---

## 🎯 Study Recommendations

### For Exam Preparation

1. **Read in order:** Start with Topic 1 (antenna problem) to build physical intuition
2. **Study the math:** Each section includes proofs from first principles
3. **Review pitfalls:** ⚠️ marked sections highlight common exam mistakes
4. **Visualize:** Reference the generated graphs when studying each concept
5. **Practice:** Numerical examples provided for each topic

### Time Allocation

- **Topic 1 (Antenna):** 30 minutes – Fundamental motivation
- **Topic 2 (DSB-SC vs AM):** 45 minutes – Critical power analysis
- **Topic 3 (QAM):** 60 minutes – Orthogonality proof and constellations
- **Topic 4 (Bandwidth):** 60 minutes – Hilbert transform and VSB
- **Topic 5 (PLL):** 45 minutes – Synchronization dynamics
- **Review & Practice:** 60 minutes – Problems and exam preparation

### Key Formulas to Memorize

| Concept | Formula | Reference |
|---------|---------|-----------|
| Antenna size | $L = \frac{c}{2f}$ | Section 1.A |
| DSB-SC power | $P = \frac{1}{2}P_m$ | Section 2.A |
| AM efficiency | $\eta = \frac{\mu^2}{2+\mu^2}$ | Section 2.E |
| Modulation theorem | $\mathcal{F}[m(t)\cos(2\pi f_c t)] = \frac{1}{2}M(f \mp f_c)$ | Section 1.D |
| QAM demod | $m_I = \text{LPF}[2r(t)\cos(2\pi f_c t)]$ | Section 3.E |
| SSB bandwidth | $B$ (50% vs DSB-SC) | Section 4.C |
| VCO equation | $f_{\text{VCO}} = f_0 + K_v v_c$ | Section 5.B |

---

## 🔧 How to Use the Generated Graphs

### In VS Code

These markdown files use standard image syntax `![[path]]` that works in:
- VS Code with preview
- GitHub (renders as `![alt](path)`)
- Obsidian, Bear, and other markdown editors

### Python Scripts Included

- `generate_graphs.py` – Creates all 7 main visualizations
- `generate_additional_graphs.py` – Creates 3 reference graphs
- Both use matplotlib with high-quality output (300 DPI PNG)

To regenerate graphs:
```bash
python generate_graphs.py
python generate_additional_graphs.py
```

---

## 📋 Topic Checklist

### Topic 1: The Antenna Problem
- [ ] Understand $\lambda = c/f$ relationship
- [ ] Calculate antenna size for different frequencies
- [ ] Appreciate 333× antenna reduction with modulation
- [ ] Understand multiplexing advantage

### Topic 2: DSB-SC vs AM
- [ ] Know power distribution in AM
- [ ] Derive efficiency formula
- [ ] Compare coherent vs envelope detection
- [ ] Understand phase synchronization requirement

### Topic 3: QAM & Orthogonality
- [ ] Prove sin-cos orthogonality integral
- [ ] Understand constellation diagrams
- [ ] Visualize I-Q separation
- [ ] Know 16-QAM has 4 bits/symbol

### Topic 4: Bandwidth Efficiency
- [ ] Understand Hilbert transform role in SSB
- [ ] Compare DSB-SC (2B), SSB (B), VSB (1.25B)
- [ ] Know VSB used for TV broadcasts
- [ ] Understand spectrum efficiency metric

### Topic 5: Phase Locked Loop
- [ ] Know PLL components (PD, LPF, VCO)
- [ ] Understand phase error dynamics
- [ ] Know lock range is ±π
- [ ] Understand Costas loop for QAM

---

## 💡 Common Pitfalls to Avoid

### Topic 1
- ❌ "Higher frequency = larger antenna" → ✅ "Higher frequency = smaller antenna" ($\propto 1/f$)

### Topic 2
- ❌ "AM is more efficient than DSB-SC" → ✅ "AM wastes 67% of power on unmodulated carrier"

### Topic 3
- ❌ "QAM uses double the bandwidth" → ✅ "QAM uses same bandwidth but sends 2× information"

### Topic 4
- ❌ "SSB saves power" → ✅ "SSB saves bandwidth, not power"

### Topic 5
- ❌ "PLL is always locked" → ✅ "PLL needs initial frequency tuning and has finite lock range"

---

## 📞 Quick Reference

### Bandwidth Summary Table
```
Technique      Bandwidth    Efficiency    Use Case
─────────────────────────────────────────────────
Baseband       B            100%          Impossible (antenna size)
DSB-SC         2B           100%          Professional radio
AM             2B           ≤33%          Broadcast (simple rx)
SSB            B            100%          Aviation, satellite
VSB            1.25B        75%           TV broadcast
QAM (16)       2B           200%          WiFi, LTE
OFDM           ~2B          300%          Modern wireless
```

### Detection Methods
```
Method              Phase Sync    Complexity    Performance
──────────────────────────────────────────────────────────
Coherent            Required      High          Best (no loss)
Envelope            Not needed    Very Low      Good (if μ < 1)
Costas Loop         Automatic     Medium        Excellent
```

---

## 🚀 Next Steps After This Guide

1. **Digital QAM:** 16-QAM, 64-QAM, 256-QAM in modern systems
2. **OFDM:** WiFi, LTE subcarrier multiplexing
3. **Frequency Division Multiplexing (FDM):** Multiple users in spectrum
4. **Noise Analysis:** SNR, BER calculations
5. **Channel Effects:** Fading, multipath, Doppler

---

## 📚 Files in This Directory

```
.
├── 01_antenna_problem.md              # Topic 1
├── 02_dsb_sc_vs_am.md                 # Topic 2
├── 03_qam_orthogonality.md            # Topic 3
├── 04_bandwidth_efficiency.md         # Topic 4
├── 05_phase_locked_loop.md            # Topic 5
├── generate_graphs.py                 # Graph generator
├── generate_additional_graphs.py       # Additional graphs
├── graphs/
│   ├── 01_antenna_problem.png
│   ├── 02_power_efficiency.png
│   ├── 03_qam_constellations.png
│   ├── 04_orthogonality.png
│   ├── 05_bandwidth_efficiency.png
│   ├── 06_pll_dynamics.png
│   ├── 07_spectral_efficiency.png
│   ├── 08_spectrum_evolution.png
│   ├── 09_modulation_index_analysis.png
│   └── 10_demodulation_comparison.png
├── context.md                         # (Original page outline)
└── README.md                          # This file
```

---

## 📖 Recommended Reading Order

1. **Start here:** [01_antenna_problem.md](01_antenna_problem.md)
   - Why modulation exists as a field
   - Physical intuition for everything that follows

2. **Then:** [02_dsb_sc_vs_am.md](02_dsb_sc_vs_am.md)
   - First practical trade-off (power vs complexity)
   - Foundation for understanding efficiency metrics

3. **Core concepts:** [03_qam_orthogonality.md](03_qam_orthogonality.md)
   - Mathematical beauty of communications
   - Why modern systems use QAM

4. **Advanced techniques:** [04_bandwidth_efficiency.md](04_bandwidth_efficiency.md)
   - How to squeeze more data into spectrum
   - Real-world compromises (TV uses VSB)

5. **Practical implementation:** [05_phase_locked_loop.md](05_phase_locked_loop.md)
   - How receivers actually work
   - Bridge between theory and practice

---

**Last Updated:** February 16, 2026  
**Format:** Markdown with embedded Mermaid diagrams and high-resolution PNG graphs  
**Target:** CSE 311 Exam Preparation
