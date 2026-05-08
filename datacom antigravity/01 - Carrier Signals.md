# Carrier Signals

> **Prerequisites**: [[00 - Why Modulation Exists]]
> **Next**: [[02 - Analog vs Digital Modulation]]

---

## What Is a Carrier?

A carrier is a **pure sinusoidal wave** at a known, fixed frequency — the "blank canvas" onto which you paint your message.

$$c(t) = A_c \cdot \cos(2\pi f_c \cdot t + \phi)$$

Three parameters define this wave completely:

| Parameter | Symbol | What It Controls | Unit |
|-----------|--------|------------------|------|
| **Amplitude** | $A_c$ | Height of the wave | Volts |
| **Frequency** | $f_c$ | How fast it oscillates | Hz |
| **Phase** | $\phi$ | Where in the cycle it starts | Radians |

> **Key Insight**: These three parameters are the **only** knobs you can turn. Every modulation technique — from the simplest AM to the most complex 256-QAM — works by **varying one or more of these three**.

---

## Why a Sinusoid?

Not just any waveform — specifically a **sinusoid**. Why?

1. **Fourier's Theorem**: Any signal can be decomposed into sinusoids. A sinusoid is the **atomic unit** of frequency.
2. **Narrowband**: A perfect sinusoid occupies **exactly one frequency** — zero bandwidth. This is the tightest possible spectral footprint.
3. **Linear Systems**: Sinusoids pass through linear systems (filters, amplifiers, channels) and come out as sinusoids — only A, f, φ may change.
4. **Mathematical Convenience**: Differentiation and integration of sinusoids produce sinusoids. This makes the math tractable.

$$\frac{d}{dt}[\cos(\omega t)] = -\omega \sin(\omega t) \quad \text{(still a sinusoid)}$$

---

## The Three Knobs — Visualized

Think of the carrier as a **spinning wheel** viewed from the side:

```
         Q (Quadrature)
         ↑
         │    ╭─────╮
         │   ╱   •   ╲     ← The dot traces out the sinusoid
         │  │    ↗    │     
         │   ╲  A_c  ╱        A_c = radius (amplitude)
         │    ╰─────╯         φ = starting angle  
    ─────┼─────────────→ I (In-phase)
         │                    f_c = rotation speed
         │
```

| Modulation Type | What Changes | Wheel Analogy |
|----------------|--------------|---------------|
| **AM** — [[03 - Amplitude Modulation (AM)]] | $A_c$ varies | Wheel **grows/shrinks** |
| **FM** — [[04 - Frequency Modulation (FM)]] | $f_c$ varies | Wheel **speeds up/slows down** |
| **PM** — [[05 - Phase Modulation (PM)]] | $\phi$ varies | Wheel **jumps ahead/behind** |

---

## Carrier in the Frequency Domain

A pure carrier at frequency $f_c$ appears as a **single spike** (Dirac delta) in the spectrum:

```
    |S(f)|
    ↑
    │           ↑ 
    │           │  ← carrier at f_c
    │           │
    ┼───────────┼──────────→ f
    0          f_c
```

When you modulate, you **spread** energy around this spike:
- **AM**: sidebands appear at $f_c \pm f_m$ → see [[03 - Amplitude Modulation (AM)]]
- **FM**: many sidebands (Bessel functions) → see [[04 - Frequency Modulation (FM)]]
- **Digital**: bandwidth depends on symbol rate → see [[11 - Bandwidth and Spectral Efficiency]]

---

## I/Q Representation

This is **critical** for understanding [[09 - Quadrature Amplitude Modulation (QAM)]] and [[08 - Phase Shift Keying (PSK)]].

Any modulated signal can be expressed as:

$$s(t) = I(t) \cdot \cos(2\pi f_c t) - Q(t) \cdot \sin(2\pi f_c t)$$

Where:
- $I(t)$ = **In-phase** component (cosine axis)
- $Q(t)$ = **Quadrature** component (sine axis)

This is equivalent to varying amplitude and phase simultaneously:

$$A(t) = \sqrt{I^2(t) + Q^2(t)}, \qquad \phi(t) = \arctan\left(\frac{Q(t)}{I(t)}\right)$$

> **Why This Matters**: The I/Q framework is the **universal representation** for digital modulation. Every constellation diagram ([[08 - Phase Shift Keying (PSK)]], [[09 - Quadrature Amplitude Modulation (QAM)]]) is plotted on I/Q axes.

---

## Connection Map

- Comes from: [[00 - Why Modulation Exists]] — we need a carrier to shift baseband signals up
- Leads to: [[02 - Analog vs Digital Modulation]] — how we choose to vary the carrier
- The three knobs map directly to: [[03 - Amplitude Modulation (AM)]], [[04 - Frequency Modulation (FM)]], [[05 - Phase Modulation (PM)]]
- The I/Q framework is essential for: [[08 - Phase Shift Keying (PSK)]], [[09 - Quadrature Amplitude Modulation (QAM)]]

---

## Exam-Style Questions

1. **Write the general equation for a carrier signal and identify its three tunable parameters.**
2. **Why do we use sinusoidal carriers instead of square waves or triangular waves?** *(Fourier, narrowband, linear system invariance)*
3. **Express a carrier in I/Q form. What do I(t) and Q(t) represent geometrically?**
4. **If a carrier at 100 MHz is amplitude-modulated by a 5 kHz tone, where do the sidebands appear?** *(95 kHz and 105 kHz from carrier → 99.995 MHz and 100.005 MHz)*

---

> **Next Step**: Now you know the carrier and its knobs. The next question is: do we vary them **continuously** or in **discrete steps**? → [[02 - Analog vs Digital Modulation]]
