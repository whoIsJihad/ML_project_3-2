# Double Sideband Suppressed Carrier (DSB-SC)

> **Prerequisites**: [[03 - Amplitude Modulation (AM)]]
> **Related**: [[21 - Single Sideband Modulation (SSB)]], [[23 - AM Modulators and Demodulators]]

---

## What Problem Does DSB-SC Solve?

Standard Amplitude Modulation (DSB-FC) is highly inefficient because it transmits the carrier signal, which contains **no information** but consumes at least 66.6% of the total transmitted power. 

**DSB-SC** (Double Sideband Suppressed Carrier) solves this by completely suppressing the carrier, transmitting *only* the two sidebands that contain the actual message.

---

## Math Derivation

![DSB-SC Waveform and Spectrum](/mnt/Data/3-2/datacom antigravity/diagrams/dsb_sc_waveform.png)

### Time Domain
In DSB-SC, the modulated signal $s(t)$ is simply the product of the message signal $m(t)$ and the carrier $c(t)$:

$$c(t) = A_c \cos(2\pi f_c t)$$
$$s(t) = m(t) c(t) = m(t) A_c \cos(2\pi f_c t)$$

Notice there is no $+ 1$ term like in standard AM ($[1 + m(t)] \cos(2\pi f_c t)$). The carrier is gone!

### Frequency Domain
Using the modulation property of the Fourier Transform:

$$S(f) = \frac{A_c}{2} [M(f - f_c) + M(f + f_c)]$$

This shows that the spectrum of the message $M(f)$ is shifted to $+f_c$ and $-f_c$. Unlike standard AM, there is no Dirac delta impulse $\delta(f-f_c)$ at the carrier frequency.

**Bandwidth**: $BW = 2f_m$ (Same as standard AM).
**Power Efficiency**: $100\%$ of transmitted power contains information.

---

## How to Modulate (DSB-SC Modulators)

To generate DSB-SC, we need circuits that perfectly multiply two signals. The most common are:

### 1. Balanced Modulator
Uses two standard AM modulators (like non-linear square-law modulators) arranged in a balanced configuration so that the carrier term cancels out.
- **Top branch**: Generates AM with $+m(t)$
- **Bottom branch**: Generates AM with $-m(t)$
- **Output**: Subtracting the two branches cancels the carrier, leaving only $2 m(t) A_c \cos(2\pi f_c t)$.

### 2. Ring Modulator
A very popular diode-based switching modulator. Four diodes are arranged in a ring. 
- The strong carrier signal turns the diodes ON and OFF like switches.
- It effectively multiplies the message $m(t)$ by a square wave at $f_c$.
- A bandpass filter then extracts the fundamental frequency component around $f_c$, yielding DSB-SC.

---

## How to Demodulate (DSB-SC Demodulators)

You **cannot** use a simple envelope detector for DSB-SC because the envelope does not trace the original message (it traces the absolute value $|m(t)|$, losing the phase/sign).

### Synchronous (Coherent) Detection
You must use a local oscillator at the receiver that is **perfectly matched** in frequency and phase to the original carrier.

1. Multiply the received signal $s(t)$ by a local carrier $\cos(2\pi f_c t)$.
$$v(t) = s(t) \cos(2\pi f_c t) = m(t) A_c \cos(2\pi f_c t) \cos(2\pi f_c t)$$
2. Use the trig identity $\cos^2(\theta) = \frac{1}{2} + \frac{1}{2}\cos(2\theta)$:
$$v(t) = \frac{A_c}{2} m(t) [1 + \cos(4\pi f_c t)]$$
$$v(t) = \frac{A_c}{2} m(t) + \frac{A_c}{2} m(t) \cos(4\pi f_c t)$$
3. **Low Pass Filter (LPF)**: The second term is centered at $2f_c$ (twice the carrier frequency). The LPF blocks it, leaving:
$$v_{out}(t) = \frac{A_c}{2} m(t)$$

> **The Phase Error Problem**: If the local oscillator has a phase error $\phi$, the output becomes $\frac{A_c}{2} m(t) \cos(\phi)$. If $\phi = 90^\circ$, the output is ZERO. This requires a **Phase Locked Loop (PLL)** to keep the receiver synchronized.

---

## Summary Trade-offs

- **Pros**: 100% power efficient.
- **Cons**: Requires complex, expensive synchronous receivers (PLLs) to demodulate. Still uses $2f_m$ bandwidth.
