# Topic 7: Coherent Detection & Phase Errors – Why Synchronization Matters

## Part A: Introduction – The Sync Problem

In Module 2, we learned that **DSB-SC requires coherent detection** — you must multiply by a phase-synchronized replica of the carrier. 

But what happens when the synchronization **fails?** This module covers the mathematics of phase errors and why the system "vanishes" at 90° phase offset.

---

## Part B: Ideal Coherent Detection (Zero Phase Error)

### Perfect Scenario

Received signal: $r(t) = m(t) \cos(2\pi f_c t)$ (noise-free DSB-SC)

Local oscillator: $\text{LO}(t) = 2\cos(2\pi f_c t)$ (perfectly synchronized, gain factor of 2)

Multiplier output (before filtering):

$$y(t) = r(t) \cdot \text{LO}(t) = 2m(t) \cos^2(2\pi f_c t)$$

Using the identity $\cos^2 x = \frac{1}{2}[1 + \cos(2x)]$:

$$y(t) = 2m(t) \cdot \frac{1}{2}[1 + \cos(4\pi f_c t)]$$

$$= m(t) + m(t)\cos(4\pi f_c t)$$

**After lowpass filter** (removing the $\cos(4\pi f_c t)$ term at $2f_c$):

$$\hat{m}(t) = m(t)$$

**Perfect recovery!** ✓ No loss, no distortion.

---

## Part C: Phase Error Analysis

### Realistic Scenario

Now assume the local oscillator has a **phase error**:

$$\text{LO}(t) = 2\cos(2\pi f_c t + \phi)$$

where $\phi$ is the phase error (radians).

Multiplier output:

$$y(t) = r(t) \cdot \text{LO}(t) = m(t) \cos(2\pi f_c t) \cdot 2\cos(2\pi f_c t + \phi)$$

Using the product-to-sum identity $\cos A \cos B = \frac{1}{2}[\cos(A-B) + \cos(A+B)]$:

$$\cos(2\pi f_c t) \cdot \cos(2\pi f_c t + \phi) = \frac{1}{2}[\cos(-\phi) + \cos(4\pi f_c t + \phi)]$$

$$= \frac{1}{2}[\cos(\phi) + \cos(4\pi f_c t + \phi)]$$

Therefore:

$$y(t) = m(t) \cdot 2 \cdot \frac{1}{2}[\cos(\phi) + \cos(4\pi f_c t + \phi)]$$

$$= m(t)\cos(\phi) + m(t)\cos(4\pi f_c t + \phi)$$

**After lowpass filtering** (removing the $2f_c$ term):

$$\hat{m}(t) = m(t) \cos(\phi)$$

### Critical Finding: The Loss Factor

$$\boxed{\text{Recovered signal} = m(t) \cos(\phi)}$$

**The recovered message is scaled by $\cos(\phi)$:**

- $\phi = 0°$ → $\cos(0°) = 1$ → Full signal ✓
- $\phi = 30°$ → $\cos(30°) ≈ 0.866$ → 1.3 dB loss
- $\phi = 45°$ → $\cos(45°) ≈ 0.707$ → 3 dB loss
- $\phi = 60°$ → $\cos(60°) = 0.5$ → 6 dB loss
- $\phi = 90°$ → $\cos(90°) = 0$ → **Signal vanishes!** ✗

---

## Part D: The Vanishing Signal Problem

### Why Does the Signal Disappear at 90°?

At $\phi = 90°$:

$$\hat{m}(t) = m(t) \cos(90°) = 0$$

**Mathematically:** The local oscillator is **orthogonal** (90° out of phase) with the received signal. Their product averages to zero after filtering.

**Physically:** Imagine trying to hear a radio broadcast where your receiver's oscillator is 90° off:
- The original signal is $\cos(\omega t)$
- Your receiver reproduces $\sin(\omega t)$ (the 90° rotated version)
- $\cos(\omega t) \times \sin(\omega t)$ averages to zero → silence!

### Real Consequence

This creates a **critical failure mode** in communication systems:

- Small phase errors (< 45°) → graceful degradation (3 dB SNR penalty)
- Phase error near 90° → **complete loss** of signal
- This is called the **"quadrature null"** or **"phase ambiguity problem"**

---

## Part E: Frequency Offset (More Practical)

In reality, the frequency offset is often the bigger problem than phase offset.

### Scenario: Frequency Error

Local oscillator: $\text{LO}(t) = 2\cos(2\pi (f_c + \Delta f) t)$

Multiplier output:

$$y(t) = m(t) \cos(2\pi f_c t) \cdot 2\cos(2\pi (f_c + \Delta f) t)$$

Using product-to-sum:

$$y(t) = m(t) \cos(2\pi \Delta f \cdot t) + m(t) \cos(2\pi (2f_c + \Delta f) t)$$

After lowpass filtering:

$$\hat{m}(t) = m(t) \cos(2\pi \Delta f \cdot t)$$

### Interpretation

The recovered message is **multiplied by a slowly varying cosine** at the offset frequency.

- If $\Delta f = 0$ (perfect frequency match) → $\cos(0) = 1$ → ideal ✓
- If $\Delta f = 10\text{ Hz}$ and message bandwidth = 5 kHz → **severe beat pattern** (the signal appears to fade in/out at 10 Hz)
- If $\Delta f > B$ (offset larger than message bandwidth) → signal occupies different frequency bands → complete distortion

### Frequency Lock Range

The PLL must lock within a **frequency lock range**:

$$|\Delta f| < f_{\text{lock}}$$

Typically, $f_{\text{lock}}$ is 1–10% of $f_c$ (depends on PLL design).

---

## Part F: Combined Phase & Frequency Error

### Realistic Receiver Model

The local oscillator typically has **both** errors:

$$\text{LO}(t) = 2\cos(2\pi (f_c + \Delta f) t + \phi)$$

**Result after demodulation (before filter):**

$$y(t) = m(t)\cos(\phi) \cos(2\pi \Delta f \cdot t) + \text{(high-frequency terms)}$$

**After filtering:**

$$\hat{m}(t) = m(t) \cos(\phi) \cos(2\pi \Delta f \cdot t)$$

**Three ways the signal degrades:**

1. **Phase error $\phi$:** Steady attenuation by $\cos(\phi)$
2. **Frequency offset $\Delta f$:** Time-varying scaling $\cos(2\pi \Delta f \cdot t)$ (beat pattern)
3. **Combined:** Worst case — message drowns in distortion

---

## Part G: How the PLL Solves This Problem

The **Phase Locked Loop (PLL)** automatically **minimizes phase and frequency error**.

### PLL Feedback Loop

```
Received r(t) ──→ [Phase Detector] ──→ ε(t) (phase error voltage)
  (DSB-SC)          ↑                     │
                    │                     ↓
                    └──── [VCO] ←── [LPF] ←── ε(t)
                    LO feedback
```

**How it works:**

1. **Phase Detector:** Compares phase of $r(t)$ and VCO output → generates error voltage $\epsilon(t)$
2. **LPF:** Smooths the error (removes high-frequency noise)
3. **VCO:** Adjusts frequency based on smoothed error
4. **Feedback:** Continuous adjustment until error → 0

**Result:** Automatic phase/frequency tracking.

### Lock Condition

When the PLL is "locked," the VCO frequency equals (or closely tracks) the incoming carrier:

$$f_{\text{VCO}} \approx f_c, \quad \phi \approx 0$$

The receiver then demodulates at nearly perfect synchronization.

---

## Part H: Phase Detector Types

### Type 1: Multiplier Phase Detector (Analog)

```
r(t) ──→ [×] ──→ LPF ──→ ε(t)
         ↑
VCO(t) ──┘
```

**Output:** $\epsilon(t) = K_d \sin(\phi)$ 

where $K_d$ is the phase detector gain.

**Characteristic:** S-shaped, zero-crossing at $\phi = 0$ (stable lock point).

### Type 2: XOR Gate (Digital)

For binary signals (1 or 0), the **XOR gate** acts as a phase detector:

```
Bit stream 1 ──→ [XOR] ──→ LPF ──→ ε(t)
                ↑
Bit stream 2 ──┘
(from VCO clock recovery)
```

**Output:** Proportional to phase error.

---

## Part I: Complete Coherent Receiver Architecture

```
┌─────────────────────────────────────────────────────┐
│                    RECEIVER FRONT-END               │
│                                                     │
│  Antenna ──→ [LNA] ──→ [BPF] ──→ [Mixer] ────────┐ │
│  (RF)      (amp)   (narrow)    (×)               │ │
│                                  ↑                │ │
│                                  │ LO             │ │
│                                  │ (from PLL)     │ │
│                              [Local Osc]         │ │
│                              (VCO + Phase Det)   │ │
│                                                     │ │
└─────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────┐
│              BASEBAND DEMODULATION                   │
│                                                     │
│  Mixer output ──→ [LPF] ──→ [ADC] ──→ DSP         │
│                 (2B BW)   (quantize) (decode)     │
│                                                     │
└─────────────────────────────────────────────────────┘
```

**Key stages:**

1. **LNA:** Low-Noise Amplifier (minimize added noise)
2. **BPF:** Bandpass filter (reject out-of-band interference)
3. **Mixer:** Multiply by LO (downconvert to baseband)
4. **LPF:** Lowpass filter (extract baseband message)
5. **ADC:** Convert to digital (for DSP)
6. **PLL:** In feedback loop (automatic sync)

---

## Part J: Phase Error Impact on SNR

In the presence of **noise**, phase error degrades signal-to-noise ratio:

### Ideal Case ($\phi = 0$)

SNR after demodulation:

$$\text{SNR}_{\text{out}} = \text{SNR}_{\text{in}}$$

(No loss, assuming linear receiver)

### Phase Error Case

$$\text{SNR}_{\text{out}} = \cos^2(\phi) \cdot \text{SNR}_{\text{in}}$$

**Example:** If $\phi = 30°$ and input SNR = 10 dB (10 linear):

$$\text{SNR}_{\text{out}} = \cos^2(30°) \times 10 = 0.866^2 \times 10 ≈ 7.5$$

**Loss:** 1.25 dB

At $\phi = 45°$:

$$\text{SNR}_{\text{out}} = 0.707^2 \times 10 ≈ 5$$

**Loss:** 3 dB (significant!)

---

## Part K: Exam-Critical Pitfalls

### ⚠️ Pitfall 1: Confusing Phase Error with Frequency Error

**Wrong:** "A 10 Hz frequency offset and a 30° phase error are the same."

**Correct:** 
- Phase error: static attenuation by $\cos(\phi)$
- Frequency error: **time-varying** attenuation $\cos(2\pi \Delta f \cdot t)$ (much worse!)

### ⚠️ Pitfall 2: The 90° Myth

**Question:** "What happens at exactly 90° phase error?"

**Answer:** The signal **completely vanishes** ($\cos(90°) = 0$).

**This is real!** No DSP trickery can recover a quadrature null.

### ⚠️ Pitfall 3: Forgetting About Lock-Up

**Wrong:** "The PLL adjusts phase perfectly in 1 nanosecond."

**Correct:** The PLL has an **acquisition time** (typically milliseconds) before it achieves lock. During lock-up, phase error exists.

### ⚠️ Pitfall 4: Assuming LO Noise is Negligible

VCO phase noise degrades performance (Wiener process model). Modern receivers use **low-phase-noise oscillators** (e.g., oven-controlled, atomic clocks).

---

## Part L: Real-World Example – DVB-T (Digital TV)

**Scenario:** Receiving a DVB-T signal at 600 MHz carrier, 8 MHz bandwidth.

**Phase Lock Requirements:**

- Carrier frequency accuracy: better than ±5 kHz (0.00833 ppm)
- Phase jitter: < 5° RMS
- Acquisition time: < 200 ms

**Receiver PLL design:**

- **Phase detector:** Multiplier type (S-curve)
- **Loop filter:** 2nd-order (proportional + integrator)
- **VCO:** VCXO (Voltage Controlled Crystal Oscillator) for stability
- **Bandwidth:** 10 kHz (stiff lock, fast acquisition)

**Performance:**

- Phase error after lock: < 2° (< 1% attenuation loss)
- SNR penalty: < 0.1 dB

---

## Part M: Summary Table – Phase Error Effects

| Phase Error | $\cos(\phi)$ | Attenuation | SNR Loss | Practical Impact |
|---|---|---|---|---|
| 0° | 1.0 | 0 dB | 0 dB | Ideal |
| 15° | 0.966 | 0.3 dB | 0.3 dB | Excellent |
| 30° | 0.866 | 1.3 dB | 1.3 dB | Good |
| 45° | 0.707 | 3 dB | 3 dB | Acceptable |
| 60° | 0.5 | 6 dB | 6 dB | Poor |
| 75° | 0.259 | 12 dB | 12 dB | Severe |
| 90° | 0 | **∞** | **∞** | **Complete loss** |

---

## Conclusion

**Phase and frequency errors in coherent detection cause:**

1. **Steady attenuation** (by $\cos(\phi)$ for phase error)
2. **Time-varying distortion** (beat patterns for frequency error)
3. **SNR degradation** (logarithmic loss in dB)
4. **Catastrophic failure** at 90° (quadrature null)

**The PLL automatically corrects these errors**, making modern coherent communication systems practical.

---

## Next Steps
- [Module 5: Phase Locked Loop](05_phase_locked_loop.md) — Deep dive into PLL design and stability
- [Module 6: Modulators & Practical Implementation](06_modulators_practical.md) — Transmitter side
- Summary: Review all modules for exam preparation
