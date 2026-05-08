# Topic 4: Bandwidth Efficiency – DSB-SC, SSB, and VSB Compared

## Introduction: The Bandwidth-Efficiency Spectrum

All modulation schemes face a fundamental trade-off:

**Simplicity vs. Efficiency**

This section compares three major AM techniques, analyzes their bandwidth requirements, and explores the Hilbert Transform—the mathematical tool enabling SSB.

---

## Part A: Bandwidth Fundamentals

### Definition: Modulated Bandwidth

For a baseband signal $m(t)$ with frequency content from $0$ to $B$ Hz:

**Baseband bandwidth:** $B$ Hz

When modulated with carrier $\cos(2\pi f_c t)$, the modulated signal occupies:

**Modulated bandwidth:** Depends on technique (DSB-SC, SSB, VSB, etc.)

### The Modulation Theorem (Revisited)

$$\mathcal{F}[m(t) \cos(2\pi f_c t)] = \frac{1}{2}M(f - f_c) + \frac{1}{2}M(f + f_c)$$

**Two replicas** of $M(f)$ appear: one shifted by $+f_c$, one by $-f_c$.

Each replica occupies a **full copy** of the baseband spectrum width.

---

## Part B: DSB-SC (Double Sideband Suppressed Carrier)

### Definition

$$s_{\text{DSB-SC}}(t) = m(t) \cos(2\pi f_c t)$$

### Frequency Domain

From the modulation theorem:

$$S_{\text{DSB-SC}}(f) = \frac{1}{2}M(f - f_c) + \frac{1}{2}M(f + f_c)$$

### Bandwidth Calculation

If $M(f)$ occupies $[0, B]$:

**Upper sideband (USB):** $M(f - f_c)$ occupies $[f_c, f_c + B]$
**Lower sideband (LSB):** $M(f + f_c)$ occupies $[f_c - B, f_c]$

(Note: The LSB from negative frequency components actually reflects to positive frequencies)

**Total occupied bandwidth:**
$$\text{BW}_{\text{DSB-SC}} = (f_c + B) - (f_c - B) = 2B$$

**Spectrum visualization:**

```
Magnitude |S_DSB-SC(f)|
        |
        |   ╱╲              ╱╲
        |  ╱  ╲            ╱  ╲
        | ╱    ╲          ╱    ╲
    ____|╱______╲________╱______╲____
        0  f_c-B  f_c  f_c+B      f
        
        Lower SB   Upper SB
        <--- 2B --->
```

### Efficiency Metric

**Spectral efficiency** (for digital signals):

$$\eta_{\text{DSB-SC}} = \frac{\text{Information bits per symbol}}{\text{Bandwidth (Hz)}}$$

For binary symbols: $\eta = \frac{1 \text{ bit/symbol}}{2B} = \frac{1}{2B}$ bits/Hz.

### Observation

**Both sidebands contain the same information** (they're mirror images). The lower sideband is mathematically redundant.

---

## Part C: SSB (Single Sideband) – Eliminating Redundancy

### The Key Insight

Since the lower and upper sidebands are **redundant**, we can transmit only one and recover the message completely.

**SSB signal:**
$$s_{\text{SSB}}(t) = m(t) \cos(2\pi f_c t) \pm \hat{m}(t) \sin(2\pi f_c t)$$

where $\hat{m}(t)$ is the **Hilbert transform** of $m(t)$, and $\pm$ determines USB or LSB.

### Frequency Domain of SSB

For Upper Sideband (USB):
$$S_{\text{SSB-USB}}(f) = \frac{1}{2}M(f - f_c) \quad \text{for } f > f_c$$

**Only the upper sideband is present!**

**Total occupied bandwidth:**
$$\text{BW}_{\text{SSB}} = B$$

**50% bandwidth savings** compared to DSB-SC! ✓

**Spectrum visualization:**

```
Magnitude |S_SSB(f)|
        |
        |              ╱╲
        |             ╱  ╲
        |            ╱    ╲
    ____|____________╱______╲____
        0            f_c  f_c+B   f
        
        Upper Sideband ONLY
        <--- B --->
```

---

## Part D: The Hilbert Transform – Theory and Practice

### Definition

The **Hilbert transform** of $m(t)$ is:

$$\hat{m}(t) = \frac{1}{\pi} \int_{-\infty}^{\infty} \frac{m(\tau)}{t - \tau} \, d\tau$$

This integral operator **shifts all frequency components by 90°** (phase shift).

### Frequency Domain Representation

$$\mathcal{F}[\hat{m}(t)] = \begin{cases}
-j M(f) & \text{if } f > 0 \\
+j M(f) & \text{if } f < 0
\end{cases}$$

In other words: $\hat{M}(f) = -j \cdot \text{sgn}(f) \cdot M(f)$

where $\text{sgn}(f)$ is the sign function.

### Physical Interpretation

The Hilbert transform is equivalent to **filtering through a 90° phase shifter**:
- All positive frequencies get a $-90°$ phase shift
- All negative frequencies get a $+90°$ phase shift

---

## Part E: Why Hilbert Transform Enables SSB

### Mathematical Construction of SSB

Consider the **analytic signal**:

$$s_a(t) = m(t) + j\hat{m}(t)$$

In the frequency domain:
$$S_a(f) = M(f) + j(-j \text{sgn}(f) M(f)) = M(f)[1 + \text{sgn}(f)]$$

For $f > 0$:
$$S_a(f) = M(f) \cdot 2 = 2M(f)$$

For $f < 0$:
$$S_a(f) = M(f) \cdot 0 = 0$$

**The analytic signal contains only positive frequencies!**

### Modulation to Create SSB

To shift this to carrier frequency, we use complex modulation:

$$s_{\text{SSB}}(t) = \text{Re}[s_a(t) \cdot e^{j 2\pi f_c t}]$$

$$= \text{Re}[(m(t) + j\hat{m}(t)) \cdot e^{j 2\pi f_c t}]$$

$$= \text{Re}[m(t) e^{j 2\pi f_c t} + j\hat{m}(t) e^{j 2\pi f_c t}]$$

Using $e^{j\theta} = \cos(\theta) + j\sin(\theta)$:

$$= m(t) \cos(2\pi f_c t) - \hat{m}(t) \sin(2\pi f_c t)$$

(The imaginary parts cancel, leaving only the real part)

### Frequency Domain Result

$$S_{\text{SSB}}(f) = \frac{1}{2}M(f - f_c)$$

Only the **upper sideband** appears. The lower sideband is completely eliminated. ✓

---

## Part F: Demodulation of SSB

### Coherent Detection for SSB

SSB is still a form of DSB-SC (no carrier component), so it requires **coherent (synchronous) detection**.

**Recovery process:**

1. Multiply by $2\cos(2\pi f_c t)$:
$$r(t) \cdot 2\cos(2\pi f_c t) = [m(t) \cos(2\pi f_c t) - \hat{m}(t) \sin(2\pi f_c t)] \cdot 2\cos(2\pi f_c t)$$

2. Expand:
$$= 2m(t) \cos^2(2\pi f_c t) - 2\hat{m}(t) \sin(2\pi f_c t) \cos(2\pi f_c t)$$
$$= m(t)[1 + \cos(4\pi f_c t)] - \hat{m}(t) \sin(4\pi f_c t)$$

3. Low-pass filter (remove terms at $2f_c$):
$$m(t)$$

**Recovered perfectly!** ✓

---

## Part G: VSB (Vestigial Sideband) – The Practical Compromise

### The Problem with SSB

**Disadvantage:** SSB requires:
- Complex Hilbert Transform implementation
- Precise phase synchronization
- Difficulty with signals containing DC components

**Advantage of DSB-SC:**
- Simpler implementation
- Robust to phase errors

**Advantage of Conventional AM:**
- Simple envelope detection (no phase sync needed)
- Robust

### The VSB Solution

VSB **partially suppresses one sideband** while keeping most of the other. It's a compromise:

$$s_{\text{VSB}}(t) = m(t) \cos(2\pi f_c t) + m_{\text{partial}}(t) \sin(2\pi f_c t)$$

where $m_{\text{partial}}(t)$ represents a **filtered version** of $\hat{m}(t)$.

In frequency domain:

$$S_{\text{VSB}}(f) = M(f - f_c) + \text{partial replica at } (f + f_c)$$

### Bandwidth of VSB

One sideband is **fully transmitted**, one is **partially vestigial**:

$$\text{BW}_{\text{VSB}} = B + \Delta B$$

where $\Delta B$ is the "vestigial" portion (typically 10-25% of $B$).

**Savings:** 10-50% compared to DSB-SC, depending on filter design.

**Spectrum visualization:**

![[graphs/05_bandwidth_efficiency.png]]

### VSB Applications

**Television:** Analog TV uses VSB because:
1. Saves spectrum (critical for broadcast)
2. Envelope detection possible with special VSB filter
3. Good trade-off between complexity and efficiency

---

## Part H: Comprehensive Bandwidth Comparison

### Table of Bandwidth Requirements

| Technique | Signal | Bandwidth | Savings vs. DSB-SC |
|-----------|--------|-----------|------------------|
| **Baseband** | $m(t)$ | $B$ | N/A |
| **DSB-SC** | $m(t) \cos(2\pi f_c t)$ | $2B$ | — (baseline) |
| **DSB with pilot** | $m(t) \cos(2\pi f_c t) + A \cos(2\pi f_c t)$ | $2B$ | — (same) |
| **Conventional AM** | $[A + m(t)] \cos(2\pi f_c t)$ | $2B$ | — (same) |
| **SSB-USB** | $m(t) \cos(2\pi f_c t) - \hat{m}(t) \sin(2\pi f_c t)$ | $B$ | **50%** |
| **VSB (TV)** | Partial SSB | $B + 0.25B$ | **37.5%** |

---

## Part I: Demodulation Complexity Comparison

### Demodulator Requirements

| Technique | Phase Sync | Amplitude Ref | Devices | Cost |
|-----------|-----------|---------------|---------|------|
| **DSB-SC** | Required | Yes | Multiplier, LPF | Medium |
| **Conventional AM** | Not required | No | Diode, RC circuit | Low |
| **SSB** | Required (tight) | Yes | Multiplier, Hilbert, LPF | High |
| **VSB** | Partial | Possible | Multiplier, VSB filter, LPF | Medium |

### Key Trade-off

**Efficiency vs. Complexity:**

$$\text{Bandwidth Savings} \propto \text{Receiver Complexity}$$

- **DSB-SC:** 0% savings, moderate complexity
- **SSB:** 50% savings, high complexity
- **VSB:** 37.5% savings, medium-high complexity

---

## Part J: The Hilbert Transform – Practical Implementation

### Why Direct Integration Is Impractical

The Hilbert transform integral:
$$\hat{m}(t) = \frac{1}{\pi} \int_{-\infty}^{\infty} \frac{m(\tau)}{t - \tau} \, d\tau$$

is **improper** (infinite limits, singularity at $t = \tau$).

### Practical Approach: Frequency Domain

In digital/discrete implementations:

1. Compute FFT of $m(t)$: $M(f)$
2. Multiply by the Hilbert transform filter: $H(f) = -j \cdot \text{sgn}(f)$
3. Inverse FFT to get $\hat{m}(t)$

**Frequency domain multiplication is efficient and numerically stable.**

### FIR Filter Approximation

For practical systems, approximate the Hilbert transform with an FIR filter:

$$\hat{m}(t) \approx \sum_{n} h(n) \cdot m(t - nT_s)$$

where $h(n)$ is the impulse response designed to approximate $-j \cdot \text{sgn}(f)$ over the signal bandwidth.

---

## Part K: Real-World Examples

### AM Radio (DSB-SC with Envelope Detection)

**Frequency:** 540 kHz – 1.7 MHz
**Channel spacing:** 10 kHz (5 kHz audio)
**Bandwidth per channel:** 10 kHz (DSB)
**Channels:** 116

If SSB were used:
**Bandwidth per channel:** 5 kHz
**Channels:** 232 (double the stations!)

**Reason SSB not used:** Cost and complexity of consumer SSB receivers.

### Aviation VHF (SSB)

**Frequency:** 118 – 137 MHz
**Channel spacing:** 25 kHz (SSB)
**Message bandwidth:** ~3 kHz (voice)
**Bandwidth saved:** 50% vs. DSB-SC

**Reason SSB used:** Spectrum is congested. Aircraft need reliable sync (pilot communication).

### Analog Television (VSB)

**Video bandwidth:** 4.5 MHz
**Vestigial portion:** 0.25 MHz
**Total bandwidth:** 5.25 MHz
**Savings vs. DSB:** 38% (full sideband would need 9 MHz!)

**Reason VSB used:** TV broadcasts need spectrum efficiency AND relatively simple receivers (envelope detector with VSB filter).

---

## Part L: Spectral Efficiency Numbers

### Definition

$$\eta = \frac{\text{Bits per second}}{\text{Bandwidth (Hz)}}$$

### Comparison for Digital QAM Signals

| Modulation | Bits/Symbol | Bandwidth | Efficiency (bits/Hz) |
|------------|-------------|-----------|---------------------|
| DSB-SC (BPSK) | 1 | $2B$ | 0.5 |
| DSB-SC (QPSK) | 2 | $2B$ | 1.0 |
| DSB-SC (16-QAM) | 4 | $2B$ | 2.0 |
| SSB (BPSK) | 1 | $B$ | 1.0 |
| SSB (QPSK) | 2 | $B$ | 2.0 |
| SSB (16-QAM) | 4 | $B$ | 4.0 |

**SSB with 16-QAM achieves 8× the efficiency of DSB-SC with BPSK!**

---

## Part M: Common Pitfalls (Exam Critical!)

### ⚠️ Pitfall 1: Assuming Bandwidth is Always $2B$

**Wrong:** "All modulated signals need $2B$ bandwidth."
**Correct:** DSB-SC and AM need $2B$. SSB needs only $B$. VSB needs $B + \Delta B$.

### ⚠️ Pitfall 2: Confusing "Sidebands" with "Bandwidth"

**Wrong:** "SSB saves bandwidth by removing one sideband."
**Correct:** Both DSB-SC and SSB have **two sidebands** (at positive and negative frequencies). SSB removes the **negative frequency** component entirely using the Hilbert transform.

### ⚠️ Pitfall 3: Forgetting Hilbert Transform Properties

**Important:** The Hilbert transform:
- Does NOT change amplitude (energy preserved)
- Shifts **all** frequency components by 90° phase
- Creates an analytic signal (no negative frequencies)

**Not important:** Hilbert transform is not a filter that "selects" frequencies.

### ⚠️ Pitfall 4: Thinking SSB Saves Power

**Wrong:** "SSB saves power because it uses less bandwidth."
**Correct:** SSB saves **bandwidth**, not power. Transmitted power depends on signal amplitude and modulation method, not bandwidth alone.

### ⚠️ Pitfall 5: Ignoring the Phase Sync Requirement

**Critical for SSB:** Even though SSB saves bandwidth, it **requires tight phase synchronization** at the receiver. Any phase error $\phi$ causes:

$$m_{\text{received}} = m(t) \cos(2\phi)$$

At $\phi = 45°$: 30% signal loss.
At $\phi = 90°$: Complete signal loss (quadrature null).

This makes SSB harder to implement than DSB-SC in practice.

---

## Part N: Advanced Consideration – OFDM and Multi-Carrier SSB

### Why SSB Matters for Broadband

Modern broadband systems (LTE, WiFi) use thousands of narrow-band subcarriers via OFDM.

Each subcarrier can use SSB-like efficiency:
- Each 20 MHz WiFi channel contains ~50 subcarriers
- Each is approximately "single-sideband" in behavior
- Total efficiency approaches SSB limits

This is why modern wireless achieves **spectral efficiencies of 2-6 bits/Hz**.

---

## Part O: Summary and Efficiency Frontier

### The Modulation Landscape

```
Bandwidth
   2B  ┌─────────────────────────────────────────
       │  DSB-SC, AM, Conventional
       │  Simple but wasteful
       │
1.25B  │                    VSB
       │               (TV broadcast)
       │
    B  │                                   SSB
       │                          (Aviation, Professional)
       │
    0  └─────────────────────────────────────────
       Simple         Complexity        Complex
       
       Trade-off: Bandwidth vs. Receiver Complexity
```

![[graphs/07_spectral_efficiency.png]]

---

## Conclusion

**Bandwidth efficiency is a design choice:**

1. **DSB-SC/AM:** Simplest receiver, wastes 50% bandwidth (two sidebands).
2. **VSB:** Compromise—saves 25-50% bandwidth with moderate complexity. Used for TV.
3. **SSB:** Maximum bandwidth efficiency, but requires complex Hilbert transform and tight phase sync. Used where spectrum is scarce (aviation).

**The Hilbert transform** is the mathematical tool enabling SSB:
- Converts real signals to analytic signals (only positive frequencies)
- Enables perfect removal of one sideband
- Achieves 50% bandwidth savings

Understanding this trade-off is crucial for practical communications engineering.

---

## Next Steps
- Deep dive into **Phase Locked Loops (PLL)** for synchronization
- Understanding **Frequency Division Multiplexing (FDM)** with these techniques
- Exploring **Digital QAM** and modern spectral efficiency
