# Single Sideband Modulation (SSB)

> **Prerequisites**: [[20 - DSB-SC Modulation]]
> **Related**: [[22 - Vestigial Sideband Modulation (VSB)]]

---

## What Problem Does SSB Solve?

DSB-SC solved the power inefficiency of AM by removing the carrier. However, it still transmits *both* the Upper Sideband (USB) and Lower Sideband (LSB). 
Because the USB and LSB are symmetric, they contain exactly the **same information**. Transmitting both is a waste of bandwidth.

**SSB** transmits only ONE sideband, cutting the bandwidth requirement perfectly in half.

---

## Math Derivation

![SSB and VSB Spectrum](/mnt/Data/3-2/datacom antigravity/diagrams/ssb_vsb_spectrum.png)

An SSB signal can be expressed mathematically using the **Hilbert Transform**, denoted as $\hat{m}(t)$. The Hilbert transform shifts the phase of all positive frequencies by $-90^\circ$.

The time-domain equation for an SSB signal is:

$$s_{SSB}(t) = \frac{A_c}{2} m(t) \cos(2\pi f_c t) \mp \frac{A_c}{2} \hat{m}(t) \sin(2\pi f_c t)$$

- Use the **minus ($-$)** sign for **Upper Sideband (USB)**.
- Use the **plus ($+$)** sign for **Lower Sideband (LSB)**.

**Bandwidth**: $BW = f_m$ (Exactly half of AM and DSB).
**Power Efficiency**: 100% (No carrier, no redundant sideband).

---

## How to Modulate (SSB Modulators)

Generating SSB is difficult because you need sharp filters or precise phase shifting.

### 1. Filter Method (Frequency Discrimination)
1. First, generate a DSB-SC signal using a balanced modulator.
2. Pass the DSB-SC signal through a highly selective Bandpass Filter.
3. The filter is designed with a very sharp cutoff to pass one sideband and completely block the other.
*Trade-off*: Requires very expensive, precise filters (like crystal or mechanical filters). Difficult if the message has very low-frequency components near DC.

### 2. Phase-Shift Method
This directly implements the time-domain equation $m(t)\cos(\omega_c t) \mp \hat{m}(t)\sin(\omega_c t)$.
1. Split the message $m(t)$ into two paths.
2. Path A multiplies $m(t)$ by $\cos(2\pi f_c t)$ using a balanced modulator.
3. Path B passes $m(t)$ through a $-90^\circ$ phase shifter (producing $\hat{m}(t)$) and multiplies it by $\sin(2\pi f_c t)$.
4. Add or subtract the two paths.
*Trade-off*: Designing a $-90^\circ$ wideband phase shifter for the audio signal is physically very difficult.

### 3. Weaver's Method (Third Method)
Uses two stages of mixing and low-pass filters to avoid the need for wideband phase shifters or sharp bandpass filters. It shifts the audio to a low intermediate frequency first.

---

## How to Demodulate (SSB Demodulators)

Like DSB-SC, SSB requires **Synchronous Detection** (a coherent local oscillator).

1. Multiply the received SSB signal by the local carrier $2 \cos(2\pi f_c t)$.
2. Pass the result through a Low Pass Filter (LPF).

$$v(t) = s_{SSB}(t) \times 2\cos(2\pi f_c t)$$
$$v(t) = [m(t)\cos(2\pi f_c t) - \hat{m}(t)\sin(2\pi f_c t)] \times 2\cos(2\pi f_c t)$$
$$v(t) = 2m(t)\cos^2(2\pi f_c t) - 2\hat{m}(t)\sin(2\pi f_c t)\cos(2\pi f_c t)$$
$$v(t) = m(t)[1 + \cos(4\pi f_c t)] - \hat{m}(t)\sin(4\pi f_c t)$$

After the LPF removes the high-frequency terms at $2f_c$, you are left perfectly with $m(t)$.

> **Frequency Error**: In SSB, if the local oscillator is slightly off frequency (e.g., $f_c + \Delta f$), the demodulated audio is pitch-shifted (like a "Donald Duck" voice).

---

## Summary Trade-offs

- **Pros**: Absolute best bandwidth efficiency for analog signals. 100% power efficient.
- **Cons**: Most complex to modulate and demodulate. Pitch shifting if not perfectly synchronized. Not suitable for signals with DC or very low frequencies (like video) because filters cannot be infinitely sharp.
