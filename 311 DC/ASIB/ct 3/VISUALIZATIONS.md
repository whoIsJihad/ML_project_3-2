# Visual Study Guide Index

## 📊 All Generated Visualizations

### Module 1: The Antenna Problem
**File:** `graphs/01_antenna_problem.png`

Contains 4 subplots:
1. **Frequency vs Antenna Size** - Shows how antenna length scales inversely with frequency
2. **Wavelength Comparison** - Demonstrates $\lambda = c/f$ across communication bands
3. **Required Antenna Sizes** - Antenna impracticality at low frequencies
4. **Size Reduction Factor** - Shows orders of magnitude improvement through modulation

**Key Insight:** Modulation enables 333× smaller antenna for AM radio


---

### Module 2: DSB-SC vs Conventional AM
**File:** `graphs/02_power_efficiency.png`

Contains 4 subplots:
1. **AM Efficiency vs Modulation Index** - Shows maximum 33% efficiency at $\mu = 1$
2. **Power Distribution** - Carrier vs sideband power allocation
3. **SNR Performance** - Coherent detection outperforms envelope detection
4. **Efficiency vs Complexity Trade-off** - Plot showing DSB-SC is most efficient

**Key Insight:** DSB-SC is 3× more power-efficient than AM, but requires coherent detection


---

### Module 3: QAM & Orthogonality
**File:** `graphs/03_qam_constellations.png`

Contains 4 subplots (constellation diagrams):
1. **BPSK (2-QAM)** - 1 bit/symbol, 2 points on I-axis
2. **QPSK (4-QAM)** - 2 bits/symbol, 4 points at 45° angles
3. **16-QAM** - 4 bits/symbol, 4×4 grid
4. **64-QAM** - 6 bits/symbol, 8×8 grid

**Key Insight:** QAM uses orthogonal I-Q axes without interference


---

### Module 3: Orthogonality Proof
**File:** `graphs/04_orthogonality.png`

Contains 4 subplots:
1. **Sine and Cosine Signals** - Visual representation of orthogonal basis
2. **Product sin(t)·cos(t)** - Shows symmetric positive/negative areas
3. **Cumulative Integration** - Demonstrates integral ≈ 0 (orthogonality)
4. **QAM Combined Signal** - I and Q components without interference

**Key Insight:** Mathematical proof that $\langle \sin, \cos \rangle = 0$


---

### Module 4: Bandwidth Efficiency
**File:** `graphs/05_bandwidth_efficiency.png`

Contains 4 subplots (frequency domain):
1. **Baseband Signal** - Original message bandwidth = B
2. **DSB-SC Modulation** - Both sidebands present, BW = 2B
3. **SSB-USB** - Only upper sideband, BW = B (50% savings!)
4. **VSB Signal** - Partial lower sideband, BW ≈ 1.25B (practical TV)

**Key Insight:** SSB achieves 50% bandwidth savings via Hilbert Transform


---

### Module 5: PLL Dynamics
**File:** `graphs/06_pll_dynamics.png`

Contains 4 subplots:
1. **Phase Error Acquisition** - Lock transient followed by tracking
2. **VCO Frequency Correction** - How frequency error decays
3. **Phase Detector S-curve** - Non-linear characteristic $\sin(\Delta\phi)$
4. **Bandwidth-Noise Trade-off** - Higher bandwidth → faster lock, more noise

**Key Insight:** PLL design requires careful bandwidth selection


---

### Spectral Efficiency Comparison
**File:** `graphs/07_spectral_efficiency.png`

Contains 2 subplots:
1. **Bar Chart** - Spectral efficiency (bits/Hz) for BPSK through OFDM
2. **Efficiency Frontier** - Modulation techniques on Pareto frontier

**Key Insight:** Modern 16-QAM achieves 4 bits/Hz on DSB-SC (vs 0.5 for BPSK)


---

### Spectrum Evolution (Reference)
**File:** `graphs/08_spectrum_evolution.png`

Contains 6 subplots showing frequency domain at each stage:
1. **Baseband** - Original message
2. **DSB-SC** - Both sidebands
3. **Conventional AM** - With carrier component
4. **SSB-USB** - Single sideband
5. **VSB** - Vestigial sideband
6. **Filtered** - After bandpass filtering

**Use:** Reference for understanding spectrum transformation


---

### Modulation Index Analysis (Reference)
**File:** `graphs/09_modulation_index_analysis.png`

Contains 4 subplots:
1. **Envelope Diagrams** - Shows effect of different $\mu$ values
2. **Efficiency Curve** - $\eta = \frac{\mu^2}{2+\mu^2}$
3. **Power Distribution (Pie)** - Carrier vs message at $\mu = 1$
4. **Transmit Power Comparison** - DSB-SC vs AM power requirements

**Use:** Deep understanding of AM modulation mechanics


---

### Demodulation Comparison (Reference)
**File:** `graphs/10_demodulation_comparison.png`

Contains 2 subplots:
1. **Coherent Detection Phase Error Sensitivity** - Complete loss at 90° error
2. **Envelope Detection Robustness** - Immune to phase errors (optimal case)

**Use:** Understanding demodulation trade-offs


---

## 🎯 How to Use These Graphs in Study

### For Understanding Concepts
- **Visual learning:** First examine the graphs
- **Mathematical derivation:** Read the surrounding text
- **Practical application:** Check the real-world examples

### For Test Preparation
1. Cover the text and label the axes yourself
2. Derive the equations from first principles
3. Explain why each graph has its shape

### For Quick Reference
- All graphs are high-resolution (300 DPI)
- Suitable for printing as study aids
- Can be converted to slides for presentation


---

## 📊 Graph Statistics

| Metric | Value |
|--------|-------|
| Total Graphs | 10 |
| Total Subplots | 35+ |
| Resolution | 300 DPI (print-quality) |
| Format | PNG (compatible with all viewers) |
| Total Size | ~3.5 MB |
| Color Scheme | Professional (print-friendly) |

---

## 🔄 Regenerating Graphs

If you need to modify the graphs or regenerate them:

```bash
# Run main visualization script
python generate_graphs.py

# Run additional reference graphs
python generate_additional_graphs.py

# Both scripts write to graphs/ directory
```

### Python Dependencies
```
numpy
matplotlib
scipy
```

Install with:
```bash
pip install numpy matplotlib scipy
```

---

## 📋 Graph-to-Module Mapping

| Module | Main Graph | Reference Graphs |
|--------|-----------|------------------|
| 1. Antenna Problem | 01_antenna_problem.png | — |
| 2. DSB-SC vs AM | 02_power_efficiency.png | 09_modulation_index_analysis.png, 10_demodulation_comparison.png |
| 3. QAM | 03_qam_constellations.png | 04_orthogonality.png |
| 4. Bandwidth | 05_bandwidth_efficiency.png | 08_spectrum_evolution.png, 07_spectral_efficiency.png |
| 5. PLL | 06_pll_dynamics.png | — |

---

## ✅ Checklist for Using Visualizations

- [ ] Examine each graph before reading the text
- [ ] Identify what axes represent
- [ ] Predict behavior from math before checking graph
- [ ] Note numerical scale changes (log vs linear)
- [ ] Understand why each subplot is needed
- [ ] Connect graphs to real-world applications
- [ ] Use for exam review and quick reference
- [ ] Print high-quality versions if needed

---

**Last Updated:** February 16, 2026  
**Format:** High-quality PNG with matplotlib  
**Quality:** Print-ready (300 DPI)
