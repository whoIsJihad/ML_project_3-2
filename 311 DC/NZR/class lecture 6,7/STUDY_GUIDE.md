# DPCM Study Guide & Practice Problems

## Study Path

### Step 1: Understand DPCM Concept (15 minutes)
- Read: [3.1 DPCM System Overview](3.1%20DPCM%20System%20Overview.md) - Introduction section
- Focus: Why DPCM works (signals are correlated)
- Visual: Study the three Mermaid diagrams
- Numerical example: Temperature/audio example showing 50% bit reduction

### Step 2: Learn Prediction (20 minutes)
- Read: [3.2 Prediction in DPCM](3.2%20Prediction%20in%20DPCM.md) - All sections
- Focus: Understand 1st, 2nd, and nth-order predictors
- Work through: Speech signal example with calculations
- Understand: Why use mq[k] not m[k]

### Step 3: Understand SNR Advantage (25 minutes)
- Read: [3.3 SNR in DPCM](3.3%20SNR%20in%20DPCM.md) - All sections
- Work through: Audio signal numerical example (PCM vs DPCM calculation)
- Key insight: 12 dB gain = 2 free bits!
- Study: Three real-world scenarios (speech, music, noise)

### Step 4: Quick Review (10 minutes)
- Review: [QUICK_REFERENCE.md](QUICK_REFERENCE.md)
- Test yourself: Can you explain all three concepts in simple terms?

**Total study time: ~70 minutes for complete understanding**

---

## Practice Problems

### Problem Set 1: DPCM System Overview

#### Problem 1.1: Compression Ratio
A signal sequence is [100, 103, 101, 105, 107, 104]. 

Using DPCM with 1st-order predictor (a₁=1) and 4-bit quantization for differences:
- PCM: Use 8 bits per sample
- DPCM: Use 8 bits for first sample, 4 bits for differences

**Calculate:** 
a) Total bits for PCM
b) Total bits for DPCM
c) Compression ratio (%)

**Answer:**
a) PCM: 6 × 8 = 48 bits
b) DPCM: 8 + 5×4 = 28 bits
c) Compression: (48-28)/48 = 20/48 = 41.7%

#### Problem 1.2: Understanding the Feedback Loop
Why is the feedback loop in DPCM critical? What would happen if the transmitter used the original sample m[k] instead of mq[k] in the predictor?

**Answer:** The receiver only has access to mq[k] (quantized values). If transmitter uses m[k], then:
- Transmitter's next prediction based on m[k]
- Receiver's next prediction based on mq[k]
- These diverge! Prediction error accumulates exponentially
- Using mq[k] at both sides keeps them synchronized

#### Problem 1.3: Block Diagram
Draw a simplified block diagram of DPCM transmitter with 3 blocks: Input, Predictor/Subtractor, Quantizer/Encoder. Show the feedback loop.

**Answer:** (See Mermaid diagram in 3.1 section)

---

### Problem Set 2: Prediction in DPCM

#### Problem 2.1: 1st-Order vs 2nd-Order Predictor
Signal sequence: [50, 52, 54, 56, 58] (perfect linear trend)

a) Calculate differences with **1st-order predictor** ($\hat{m}[k] = m_q[k-1]$)
b) Calculate differences with **2nd-order predictor** ($\hat{m}[k] = 1.5m_q[k-1] - 0.5m_q[k-2]$)
c) Which gives smaller differences?

**Answer:**

1st-order:
| k | m[k] | m̂[k] | d[k] |
|---|---|---|---|
| 0 | 50 | — | 50 |
| 1 | 52 | 50 | +2 |
| 2 | 54 | 52 | +2 |
| 3 | 56 | 54 | +2 |
| 4 | 58 | 56 | +2 |

2nd-order:
| k | m[k] | m̂[k] | d[k] |
|---|---|---|---|
| 0 | 50 | — | 50 |
| 1 | 52 | — | 52 |
| 2 | 54 | 1.5(52)-0.5(50)=73 | 54-73=-19 |
| 3 | 56 | 1.5(54)-0.5(52)=74 | 56-74=-18 |
| 4 | 58 | 1.5(56)-0.5(54)=75 | 58-75=-17 |

**Wait, 2nd-order coefficients were wrong!** For linear trend, optimal would be:
$\hat{m}[k] = 2m_q[k-1] - m_q[k-2]$ (extrapolation)

With correct coefficients:
| k | m[k] | m̂[k] = 2m_q[k-1]-m_q[k-2] | d[k] |
|---|---|---|---|
| 2 | 54 | 2(52)-50=54 | 0 |
| 3 | 56 | 2(54)-52=56 | 0 |
| 4 | 58 | 2(56)-54=58 | 0 |

**Winner: 2nd-order with correct coefficients** (perfect prediction on trend!)

#### Problem 2.2: Autocorrelation-Based Coefficient
A speech signal has autocorrelation:
- R[0] = 1000 (signal power)
- R[1] = 800 (1-sample correlation)

Calculate the optimal 1st-order coefficient a₁.

**Answer:**
$$a_1 = \frac{R[1]}{R[0]} = \frac{800}{1000} = 0.8$$

This means: Next sample is predicted to be 80% of the previous sample.

#### Problem 2.3: Compare Predictors
Three signals: A (constant), B (slowly varying), C (random)

Which predictor order (1st, 2nd, 3rd) would be optimal for each?

**Answer:**
- A (constant): Any 1st-order with a₁≈1 works (no change)
- B (slowly varying): 2nd-order captures trend well
- C (random): Even 10th-order won't help (no correlation)

---

### Problem Set 3: SNR in DPCM

#### Problem 3.1: SNR Calculation
Given:
- Signal: peak amplitude m_p = 256, power = 4096
- Quantization levels: L = 16 (so 4 bits)
- DPCM achieves difference peak: d_p = 64

Calculate:
a) PCM SNR (in ratio)
b) DPCM SNR (in ratio)
c) Processing gain (in ratio and dB)

**Answer:**

a) PCM SNR:
$$SNR_{PCM} = 3L^2 \frac{\overline{m^2}}{m_p^2} = 3 \times 16^2 \times \frac{4096}{256^2} = 768 \times \frac{4096}{65536} = 768 \times 0.0625 = 48$$

b) DPCM SNR:
$$SNR_{DPCM} = 3L^2 \frac{\overline{m^2}}{d_p^2} = 3 \times 16^2 \times \frac{4096}{64^2} = 768 \times \frac{4096}{4096} = 768$$

c) Processing Gain:
$$G_p = \frac{SNR_{DPCM}}{SNR_{PCM}} = \frac{768}{48} = 16$$
$$G_p(dB) = 10\log_{10}(16) = 12.04 \text{ dB}$$

#### Problem 3.2: Bit Savings
From Problem 3.1, we have 12 dB processing gain.

Using the 6-dB rule (1 bit = 6 dB):
- How many equivalent bits are saved?
- What PCM bit-depth would give same SNR as 4-bit DPCM?

**Answer:**
- 12 dB ÷ 6 dB/bit = **2 bits saved**
- 4-bit DPCM ≈ (4+2)-bit PCM = **6-bit PCM**

#### Problem 3.3: Predictor Quality Impact
A system uses 4-bit DPCM (L=16) with signal peak m_p=100 and power=2000.

Compare SNR for three predictor qualities:
- **Good predictor:** d_p = 20
- **OK predictor:** d_p = 50
- **Bad predictor:** d_p = 90

Calculate SNR for each in dB.

**Answer:**

Good: $SNR_{DPCM} = 3×256×\frac{2000}{400} = 3840$ → 35.8 dB
OK: $SNR_{DPCM} = 3×256×\frac{2000}{2500} = 614.4$ → 27.9 dB
Bad: $SNR_{DPCM} = 3×256×\frac{2000}{8100} = 188.1$ → 22.7 dB

**Insight:** Better predictor = dramatically better SNR!

#### Problem 3.4: When DPCM Fails
A white noise signal has no correlation (random values).

What would be the difference peak d_p compared to signal peak m_p?

**Answer:**
Since there's no predictability, the difference d[k] = m[k] - m̂[k] would be approximately as large as m[k] itself or larger!

Therefore: d_p ≈ m_p (or worse)

Processing gain: $G_p \approx 1$ (0 dB) - **No advantage!**

**Conclusion:** Use PCM for random signals, not DPCM.

---

## Challenge Problems

### Challenge 1: Design a DPCM System
Design a DPCM system for a speech signal with specifications:
- Sampling rate: 8 kHz
- Signal amplitude range: 0-256
- Target bit rate: 32 kbps
- Target SNR: > 25 dB

Determine:
a) Number of bits per sample for DPCM quantizer
b) Suggested predictor order
c) Expected processing gain

**Hint:** 32 kbps / 8000 samples/sec = 4 bits per sample

### Challenge 2: Comparison Analysis
Create a comparison table for PCM, DPCM, and Delta Modulation covering:
- Bits per sample
- Predictor type
- Data rate
- SNR gain
- Complexity
- Best use case

### Challenge 3: Real-World Application
A video codec needs to compress image data.
- Images are 512×512 pixels, 8-bit grayscale
- Processing power is limited (can use 2nd-order predictor max)
- Goal: Reduce file size by at least 30%

Design a DPCM-based compression approach. What challenges might arise?

---

## Answer Key Summary

Most answers are provided above. For Challenge Problems:
- Work through them with the notes
- Discuss with classmates
- Compare results with instructor

## Self-Assessment Checklist

After completing this study guide, can you:

- [ ] Explain why DPCM uses less data than PCM
- [ ] Draw DPCM transmitter and receiver block diagrams
- [ ] Understand the importance of the feedback loop
- [ ] Calculate predictions for 1st, 2nd, and Nth-order predictors
- [ ] Explain why to use mq[k] not m[k] in predictor
- [ ] Calculate SNR for both PCM and DPCM systems
- [ ] Understand processing gain and its relationship to bits saved
- [ ] Know when DPCM works (correlated signals) vs when it fails (random)
- [ ] Compare different predictor qualities and their impact
- [ ] Apply 6-dB rule to convert dB gains to bit savings

**If you checked all boxes:** Ready for exam! 🎓

---

**Study Resources:**
- Main notes: See the three main files
- Quick reference: QUICK_REFERENCE.md
- Visual diagrams: In each section of main notes
- Numerical examples: Throughout all files

**Time estimates:**
- Problem Set 1: 15 minutes
- Problem Set 2: 20 minutes
- Problem Set 3: 20 minutes
- Challenge problems: 30-45 minutes

**Total practice time: ~90 minutes**
