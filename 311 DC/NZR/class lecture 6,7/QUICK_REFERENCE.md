# DPCM Quick Reference Guide

## One-Page Summary

### DPCM vs PCM at a Glance

| Aspect | PCM | DPCM |
|--------|-----|------|
| **Encodes** | Absolute sample value | Difference (sample - prediction) |
| **Formula** | Quantize m[k] directly | Quantize d[k] = m[k] - m̂[k] |
| **Bits Needed** | More | 30-50% fewer! |
| **Quality (SNR)** | Baseline | 6-12 dB better |
| **Complexity** | Simple | Medium (needs predictor) |
| **Works Best For** | Uncorrelated signals | Correlated signals (audio, images) |

## The Three Core Concepts

### 1. DPCM System
**Key Idea:** Send differences, not absolute values
- Transmitter: Sample → Predict → Find difference → Quantize → Send
- Receiver: Receive → Decode → Reconstruct = Prediction + Difference
- **Critical:** Use quantized feedback, not original samples (prevents error buildup)

### 2. Prediction  
**Key Idea:** Guess the current sample from past samples
$$\hat{m}[k] = a_1 \cdot m_q[k-1] + a_2 \cdot m_q[k-2] + ...$$
- 1st-order (simplest): $\hat{m}[k] = m_q[k-1]$ (just previous sample)
- 2nd-order: Uses 2 previous samples (captures trends)
- Nth-order: Uses N previous samples (better predictions, more complex)
- **Quality predictor** = small differences = high compression

### 3. SNR Improvement
**Key Idea:** Quantizing small differences gives better quality than quantizing large values
$$SNR_{DPCM} = 3L^2 \frac{\overline{m^2}}{d_p^2} \quad \text{vs} \quad SNR_{PCM} = 3L^2 \frac{\overline{m^2}}{m_p^2}$$

Processing Gain:
$$G_p = \frac{m_p^2}{d_p^2}$$

**Examples:**
- Amplitude reduced 4×: 16× gain = 12 dB = **2 free bits!**
- 4-bit DPCM = 6-bit PCM quality
- Great for correlated signals (speech, audio, images)

## Numerical Example Walkthrough

**Input sequence:** [50, 52, 51, 55, 58]

**1st-order predictor:** $\hat{m}[k] = m_q[k-1]$

| k | Sample | Prediction | Difference | Bits (4-bit) |
|---|--------|-----------|-----------|---------|
| 0 | 50 | — | 50 | 8 bits |
| 1 | 52 | 50 | +2 | 0010 |
| 2 | 51 | 52 | -1 | 1111 |
| 3 | 55 | 51 | +4 | 0100 |
| 4 | 58 | 55 | +3 | 0011 |

- **PCM:** 5 × 8 = 40 bits
- **DPCM:** 8 + 4 × 4 = 24 bits
- **Saving:** 40% reduction!

## Block Diagram Summary

### Transmitter
```
Input m[k] ──┐
             ├──[−]──→ d[k] ──[Quantize]──→ dq[k] ──[Encode]──→ Send
       Predictor ├─[−]
             │
[Feedback] ←─┘─[+]──→ mq[k] (used for next prediction)
```

### Receiver
```
Receive ──[Decode]──→ dq[k] ──┐
                              ├──[+]──→ mq[k] (reconstructed)
       Predictor ─────────────┤
                              │
                    [Feedback]┘
```

## Key Formulas

### Predictor Design
- **1st-order optimal:** $a_1 = \frac{R[1]}{R[0]}$ (autocorrelation-based)
- **Nth-order:** Wiener-Hopf equations (minimize prediction error variance)

### SNR Calculations
- **PCM SNR (dB):** $10\log_{10}\left(3L^2 \frac{\overline{m^2}}{m_p^2}\right)$
- **DPCM SNR (dB):** $10\log_{10}\left(3L^2 \frac{\overline{m^2}}{d_p^2}\right)$
- **Processing Gain (dB):** $20\log_{10}\left(\frac{m_p}{d_p}\right)$

### 6-dB Rule Connection
- 1 bit = 6 dB improvement in SNR
- 12 dB gain = 2 bits saved
- 18 dB gain = 3 bits saved

## When to Use DPCM

### ✓ Use DPCM When:
- Signal is correlated (adjacent samples are similar)
- Examples: Speech, audio, images, video
- Data rate is critical (need compression)
- Quality is important (want good SNR with few bits)

### ✗ Use PCM Instead When:
- Signal is random/uncorrelated (white noise)
- Simplicity is needed
- Predictor design is impractical
- No correlation between samples

## Common Mistakes to Avoid

❌ Using original sample m[k] in predictor feedback (causes error buildup)
✓ Always use quantized sample mq[k]

❌ Expecting DPCM to work equally on all signals
✓ Good predictor design is critical; depends on signal type

❌ Over-complicating the predictor (N=100 for tiny gain)
✓ N=1 to 3 usually optimal; 6 dB → 1 bit saved rule

❌ Forgetting the feedback loop is part of the quantizer
✓ Feedback reconstruction ensures transmitter ≈ receiver

## Next: Delta Modulation

DPCM with:
- 1-bit quantizer (only +1 or -1)
- 1st-order predictor with a₁=1
- Simplest form of DPCM

See: [[../class lecture 8/4.1 Delta Modulation System Overview|Delta Modulation]]

---

**Master the Big Picture:**
1. Different signal → Different prediction → Different efficiency
2. Good predictor → Small differences → Few bits → High compression
3. Quality maintained through quantized feedback loop
4. SNR gain from reducing what we quantize, not how we quantize
