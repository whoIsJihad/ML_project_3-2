# Topic 0: Introduction & Recap – Fourier Foundations

## Part A: Why This Course Matters

Amplitude Modulation is the foundational language of radio, satellite, and wireless communications. Before we dive into **why** we modulate, you need to understand the mathematical tools that make everything work.

This module recaps the critical Fourier properties and sets up the framework for the entire course.

---

## Part B: Critical Fourier Transform Properties

### Property 1: Linearity

$$\mathcal{F}[a \cdot f(t) + b \cdot g(t)] = a \cdot F(f) + b \cdot G(f)$$

**Implication:** Modulation is a linear operation. If you know how the baseband and carrier behave separately, you can predict the combined result.

### Property 2: Time Shift (Delay)

$$\mathcal{F}[f(t - t_0)] = e^{-j2\pi f t_0} \cdot F(f)$$

**Implication:** Delaying a signal adds a phase shift in frequency domain. Phase errors (e.g., in PLL synchronization) translate to time delays.

### Property 3: Frequency Shift (Modulation Theorem)

$$\mathcal{F}[f(t) \cos(2\pi f_c t)] = \frac{1}{2}[F(f - f_c) + F(f + f_c)]$$

**This is the core of AM.** Multiplying by a carrier shifts the spectrum.

### Property 4: Product in Time = Convolution in Frequency

$$\mathcal{F}[f(t) \cdot g(t)] = F(f) * G(f)$$

*(Convolution symbol: $*$)*

**Why it matters:** Modulation (multiplication in time) becomes convolution in frequency. This is why filtering is critical after modulation.

### Property 5: Convolution in Time = Product in Frequency

$$\mathcal{F}[f(t) * g(t)] = F(f) \cdot G(f)$$

**Implication:** If you convolve the modulated signal with a filter impulse response, the result is simply the product of spectra. This is how VSB (Vestigial Sideband) works.

### Property 6: Parseval's Theorem (Energy Conservation)

$$\int_{-\infty}^{\infty} |f(t)|^2 \, dt = \int_{-\infty}^{\infty} |F(f)|^2 \, df$$

**Implication:** Energy in time domain equals energy in frequency domain. Power is conserved—you can't create energy by modulating.

---

## Part C: The Course Roadmap

### Module Flow

1. **Module 0 (this file):** Fourier foundations and why they matter.
2. **Module 1:** The Antenna Problem — why modulation is necessary.
3. **Module 2:** DSB-SC vs. Conventional AM — the power/complexity trade-off.
4. **Module 3:** QAM & Orthogonality — sending two messages simultaneously.
5. **Module 4:** Bandwidth Efficiency — SSB, VSB, and the Hilbert Transform.
6. **Module 5:** Phase Locked Loop — automatic carrier synchronization.
7. **Module 6:** Modulators & Practical Implementation — how to build a modulator.
8. **Module 7:** Coherent Detection & Phase Errors — why synchronization fails and how to fix it.

### The Bigger Picture

Communication systems follow this pipeline:

```
Message m(t) → Modulate → Transmit → Channel → Receive → Demodulate → Recovered m(t)
   (baseband)   (shift to f_c)                           (shift back)
```

**Key question at each stage:** How does the spectrum change?

---

## Part D: Trigonometric Identities You'll Use All Semester

### Sum-to-Product

$$\cos A + \cos B = 2 \cos\left(\frac{A+B}{2}\right) \cos\left(\frac{A-B}{2}\right)$$

$$\sin A + \sin B = 2 \sin\left(\frac{A+B}{2}\right) \cos\left(\frac{A-B}{2}\right)$$

### Product-to-Sum

$$\cos A \cos B = \frac{1}{2}[\cos(A-B) + \cos(A+B)]$$

$$\sin A \sin B = \frac{1}{2}[\cos(A-B) - \cos(A+B)]$$

$$\sin A \cos B = \frac{1}{2}[\sin(A+B) + \sin(A-B)]$$

### Power Reduction

$$\cos^2 x = \frac{1}{2}[1 + \cos(2x)]$$

$$\sin^2 x = \frac{1}{2}[1 - \cos(2x)]$$

**Exam Critical:** The factor of $\frac{1}{2}$ in power reduction appears everywhere—DSB-SC power, AM efficiency calculations, demodulator gain.

---

## Part E: Common Student Mistakes (Already!)

### ⚠️ Mistake 1: Forgetting the 1/2 Factor in Frequency Shift

**Wrong:** $\mathcal{F}[m(t) \cos(2\pi f_c t)] = M(f - f_c) + M(f + f_c)$

**Correct:** $\mathcal{F}[m(t) \cos(2\pi f_c t)] = \frac{1}{2}[M(f - f_c) + M(f + f_c)]$

**Why:** The $\frac{1}{2}$ is buried in the modulation theorem. It comes from the identity $\cos x = \frac{1}{2}(e^{jx} + e^{-jx})$.

### ⚠️ Mistake 2: Confusing Convolution with Multiplication

If you filter a modulated signal:

**Correct way (frequency domain):** $S_{\text{filtered}}(f) = S(f) \cdot H(f)$

**Incorrect way:** $S_{\text{filtered}}(f) = S(f) * H(f)$ (this is backwards!)

Filtering is **multiplication** in frequency, **convolution** in time.

### ⚠️ Mistake 3: Assuming All Signals Are Real

Complex exponentials $e^{j\omega t}$ are mathematical conveniences, but **transmitted signals are always real**. When you write a spectrum, remember:
- The spectrum is symmetric: $X(-f) = X^*(f)$ (conjugate symmetry)
- One-sided power spectral densities are often used in practice (scaling the positive frequencies by 2)

---

## Part F: Notation & Conventions

### Time-Domain Signal Representation

- **$m(t)$** = message (baseband, usually real, zero mean)
- **$c(t) = \cos(2\pi f_c t)$** = carrier (real, high frequency)
- **$s(t)$** = modulated signal (transmitted)
- **$r(t)$** = received signal (may include noise, channel effects)

### Frequency-Domain Representation

- **$M(f)$** = Fourier transform of $m(t)$ (typically real and symmetric if $m(t)$ is real)
- **$C(f)$** = Fourier transform of carrier (delta functions at $\pm f_c$)
- **$S(f)$** = Fourier transform of $s(t)$ (shifted version of $M(f)$)

### Power & Energy

- **$P_m$** = average power of message: $P_m = \mathbb{E}[m^2(t)]$ (time average)
- **$P_s$** = average power of modulated signal
- **$\eta$** = efficiency = useful power / total power (expressed as %)

### Phase & Frequency

- **$\phi(t)$** = instantaneous phase
- **$\theta(t)$** = phase error (deviation from perfect carrier sync)
- **$\Delta f$** = frequency offset (receiver VCO off from true $f_c$)

---

## Part G: The Modulation Landscape (Quick Reference)

| Scheme | Transmit Signal | Bandwidth | Demod | Efficiency | Real-world |
|--------|---|---|---|---|---|
| **DSB-SC** | $m(t)\cos(2\pi f_c t)$ | $2B$ | Coherent | 100% | Satellite, QAM |
| **Conventional AM** | $[A+m(t)]\cos(2\pi f_c t)$ | $2B$ | Envelope | ≤33% | AM radio |
| **SSB** | $m(t)\cos(2\pi f_c t) \pm \hat{m}(t)\sin(2\pi f_c t)$ | $B$ | Coherent | 100% | Phone, 3G/4G |
| **VSB** | Filtered compromise | $1.25B$ | Hybrid | ~75% | TV broadcast |
| **QAM** | $m_I(t)\cos(...) + m_Q(t)\sin(...)$ | $2B$ | Coherent | 100%+ | WiFi, LTE, 5G |

*(More details on each in later modules.)*

---

## Part H: Study Strategy for This Course

### Approach 1: Frequency-Domain First
- Understand the spectrum at each stage (baseband → modulated → filtered → demodulated)
- This is **the easiest way** to understand AM

### Approach 2: Time-Domain Derivation
- Work through the math step-by-step (multiply out formulas, apply identities)
- Builds deeper intuition but takes longer

### Approach 3: Circuit-Level Implementation
- Understand practical modulators and demodulators (diodes, multipliers, PLLs)
- Critical for exam questions on "how do you build this?"

**Recommended:** Start with Approach 1 (frequency-domain), then supplement with Approach 2 for rigor.

---

## Part I: What You Should Know by the End of This Course

✓ How to sketch AM spectra (baseband, DSB-SC, AM, SSB, QAM)

✓ Why DSB-SC is 3× more efficient than conventional AM

✓ How to recover a message from modulated signals (both coherent and envelope detection)

✓ The role of the PLL in automatic synchronization

✓ How modulators and demodulators work (practical circuits)

✓ The trade-offs between bandwidth, power, and complexity

✓ Why phase errors cause signal degradation (and vanishing at 90°)

---

## Conclusion

Amplitude Modulation is ultimately about **spectral engineering**: taking a baseband message, shifting it to a higher frequency for transmission, and shifting it back at the receiver. The Fourier Transform is your lens for understanding this process.

**Go forth and modulate! 📡**

---

## Next Steps
- [Module 1: The Antenna Problem](01_antenna_problem.md)
- [Module 2: DSB-SC vs. Conventional AM](02_dsb_sc_vs_am.md)
