# How to Analyze Any New Modulation

> **Prerequisites**: All previous notes — this is the synthesis.
> **This is your exam superpower.**

---

## The Framework

When you encounter a modulation scheme you've never seen, ask these seven questions **in order**:

---

### Question 1: What parameter(s) of the carrier are being varied?

```
Amplitude?  → AM family   (AM, ASK, PAM, QAM)
Frequency?  → FM family   (FM, FSK, MSK, OFDM subcarriers)
Phase?      → PM family   (PM, PSK, DPSK, QAM)
Multiple?   → Hybrid      (QAM = amplitude + phase)
```

**Why this matters**: The varied parameter determines the **noise sensitivity** and **demodulation** approach.

Reference: [[01 - Carrier Signals]], [[02 - Analog vs Digital Modulation]]

---

### Question 2: Is it analog or digital?

| Check | Analog | Digital |
|-------|--------|---------|
| Message signal | Continuous waveform | Discrete bits |
| Parameter variation | Smooth, continuous | Discrete steps/symbols |
| # of possible states | Infinite | Finite ($M$ states, $\log_2 M$ bits) |

If digital: **What is M?** (How many symbols?) This immediately gives you bits/symbol = $\log_2 M$.

Reference: [[02 - Analog vs Digital Modulation]]

---

### Question 3: How many bits per symbol?

$$b = \log_2 M$$

This number drives:
- **Spectral efficiency**: $\eta \leq b$ bits/s/Hz
- **Constellation complexity**: $M$ points in I/Q plane
- **SNR requirement**: roughly +4 dB per additional bit in QAM

Reference: [[11 - Bandwidth and Spectral Efficiency]]

---

### Question 4: What is the bandwidth?

Apply the relevant formula:

| Type | Bandwidth Formula |
|------|-------------------|
| AM (DSB) | $BW = 2f_m$ |
| AM (SSB) | $BW = f_m$ |
| FM | $BW \approx 2(\Delta f + f_m)$ (Carson's) |
| Digital (single-carrier) | $BW = (1+r) \cdot R_b / \log_2 M$ |
| OFDM | $BW = N \cdot \Delta f$ |

Reference: [[11 - Bandwidth and Spectral Efficiency]], [[04 - Frequency Modulation (FM)]]

---

### Question 5: What is the noise performance?

Key questions:
- **Constant envelope?** (Yes → can use limiter → better noise immunity)
- **What's the minimum distance $d_{min}$ between constellation points?** (Larger → better BER)
- **What Eb/N0 is needed for target BER?**

Rules of thumb:
- Constant envelope schemes (FSK, PSK) → noise-immune amplitude limiting possible
- Amplitude-varying schemes (ASK, QAM) → noise directly affects detection
- Higher M → closer points → worse BER at same SNR

Reference: [[12 - Noise and BER]]

---

### Question 6: What are the implementation trade-offs?

| Dimension | What to check |
|-----------|---------------|
| **Transmitter complexity** | Linear amp needed? (QAM: yes, PSK: no) |
| **Receiver complexity** | Coherent detection? Carrier recovery? Equalization? |
| **Power efficiency** | Constant envelope → efficient Class C amp |
| **Spectral efficiency** | bits/s/Hz — how efficiently does it use spectrum? |
| **Multipath handling** | Single-carrier → equalizer; OFDM → CP + FFT |

Reference: [[14 - Modulation Comparison Table]]

---

### Question 7: Where does it fit in the modulation family?

Find the **nearest relative** you already understand:

```
New scheme → Which known scheme is it most like?
           → What's different?
           → What trade-off does the difference address?
```

Examples:
- **APSK** (Amplitude + Phase Shift Keying) → Like QAM but points on concentric rings → better PAPR
- **GMSK** (Gaussian MSK) → MSK with Gaussian pulse shaping → narrower spectrum, used in GSM
- **SC-FDMA** → DFT-precoded OFDM → lower PAPR, used in LTE uplink
- **Chirp Spread Spectrum** → Frequency sweep → robust at extremely low SNR, used in LoRa

Reference: [[00 - Why Modulation Exists]], [[14 - Modulation Comparison Table]]

---

## Worked Example: Analyzing APSK (Unknown Scheme)

Let's say you encounter **32-APSK** on an exam.

1. **What's varied?** Amplitude AND phase → hybrid (like QAM)
2. **Analog or digital?** Digital — 32 discrete symbols
3. **Bits/symbol?** $\log_2 32 = 5$
4. **Bandwidth?** Same as 32-QAM: $BW = (1+r) \cdot R_b/5$
5. **Noise?** Points on concentric rings → more uniform peak power than 32-QAM → **better PAPR**
6. **Trade-offs?** Slightly less minimum distance than 32-QAM → marginally worse BER, but better for satellite (PAPR matters with satellite amplifiers)
7. **Family?** Modified QAM where points are arranged on rings instead of a grid. Used in DVB-S2 satellite broadcasting.

**You just analyzed a scheme you'd never seen before.** This is the end goal from [[00 - Why Modulation Exists]].

---

## The Universal Checklist (Print This)

```
┌─────────────────────────────────────────────────────┐
│          MODULATION ANALYSIS CHECKLIST               │
├─────────────────────────────────────────────────────┤
│                                                      │
│  1. Parameter varied: □ Amplitude □ Freq □ Phase     │
│  2. Type: □ Analog  □ Digital  (M = ___, b = ___)    │
│  3. Spectral efficiency: η = ___ bits/s/Hz           │
│  4. Bandwidth: BW = ___ Hz                           │
│  5. Eb/N0 needed: ___ dB (for BER = ___)             │
│  6. Constant envelope: □ Yes □ No                    │
│  7. Nearest known relative: _______________          │
│  8. Key advantage over alternatives: ___________     │
│  9. Key disadvantage: ________________________       │
│ 10. Typical application: _____________________       │
│                                                      │
└─────────────────────────────────────────────────────┘
```

---

## Connection Map (Full Knowledge Base)

```
[[00 - Why Modulation Exists]]
 └─→ [[01 - Carrier Signals]]
      └─→ [[02 - Analog vs Digital Modulation]]
           ├─→ ANALOG:
           │    ├─→ [[03 - Amplitude Modulation (AM)]]
           │    ├─→ [[04 - Frequency Modulation (FM)]]
           │    └─→ [[05 - Phase Modulation (PM)]]
           │
           └─→ DIGITAL:
                ├─→ [[06 - Pulse Amplitude Modulation (PAM)]]
                ├─→ [[07 - ASK and FSK]]
                ├─→ [[08 - Phase Shift Keying (PSK)]]
                ├─→ [[09 - Quadrature Amplitude Modulation (QAM)]]
                └─→ [[10 - OFDM]]
                     │
                     └─→ ANALYSIS:
                          ├─→ [[11 - Bandwidth and Spectral Efficiency]]
                          ├─→ [[12 - Noise and BER]]
                          ├─→ [[13 - Real World Systems]]
                          ├─→ [[14 - Modulation Comparison Table]]
                          └─→ [[15 - How to Analyze Any New Modulation]] ← YOU ARE HERE
```

---

## Final Exam Advice

1. **Don't memorize — understand the trade-offs.** If you understand WHY each scheme exists, you can derive its properties.
2. **Always start with the three knobs** (A, f, φ) — every scheme maps to these.
3. **Know your formulas**: Carson's rule, Nyquist, Shannon, BER for BPSK/QPSK/QAM.
4. **Practice the checklist** on schemes you know — then apply it to unknown ones.
5. **Draw constellation diagrams** — they make everything concrete.

> **You now have a complete framework for understanding modulation as a connected whole — not a menu of isolated techniques.**

---

*Good luck on finals.* 🎓
