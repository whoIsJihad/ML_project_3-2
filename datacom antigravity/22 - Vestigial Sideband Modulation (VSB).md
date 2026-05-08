# Vestigial Sideband Modulation (VSB)

> **Prerequisites**: [[20 - DSB-SC Modulation]], [[21 - Single Sideband Modulation (SSB)]]

---

## What Problem Does VSB Solve?

**DSB** takes too much bandwidth. **SSB** is perfectly efficient but requires impossibly sharp filters, making it terrible for signals that contain very low frequencies (like DC components in video signals).

**VSB (Vestigial Sideband)** is the perfect compromise. Instead of brutally cutting off one sideband perfectly at the carrier frequency, VSB allows a gradual filter roll-off. 
It transmits:
1. One complete sideband.
2. A "vestige" (a small, lingering piece) of the other sideband.

> **Real-world context**: VSB was the standard for analog Television broadcasting. Video signals have massive bandwidths (so DSB is too wide) and critical low-frequency/DC components (so SSB filters would destroy the picture).

---

## Math & Spectrum

![SSB and VSB Spectrum](/mnt/Data/3-2/datacom antigravity/diagrams/ssb_vsb_spectrum.png)

### Spectrum
In VSB, the transmission bandwidth is slightly larger than SSB but much smaller than DSB.
$$BW_{VSB} = f_m + f_v$$
Where $f_m$ is the message bandwidth and $f_v$ is the width of the vestigial sideband (typically around 25% of $f_m$).

### Filter Requirements
The key to VSB is the filter symmetry at the receiver. To perfectly reconstruct the original signal without distortion, the VSB shaping filter $H(f)$ must satisfy:
$$H(f - f_c) + H(f + f_c) = \text{Constant}$$
for $|f| \leq f_m$. This means whatever is cut off from the main sideband is exactly compensated for by the vestige of the other sideband.

---

## How to Modulate

VSB is typically generated using the **Filter Method**:
1. Generate a DSB-SC (or standard AM) signal using a standard modulator.
2. Pass it through a carefully designed **VSB Filter**.
3. This filter passes one sideband fully, and has a gradual, symmetric roll-off across the carrier frequency, leaving just a vestige of the second sideband.

---

## How to Demodulate

The demodulation method depends on how the VSB was transmitted.

### 1. Synchronous Demodulation (For VSB-SC)
If no carrier was transmitted (like DSB-SC/SSB), you must use a synchronous detector.
1. Multiply by local oscillator $\cos(2\pi f_c t)$.
2. Pass through a Low Pass Filter.
3. If the VSB filter at the transmitter (or receiver) satisfies the symmetry condition, the signal is recovered perfectly.

### 2. Envelope Detection (For VSB + Carrier)
If a large carrier is added to the VSB signal before transmission (like standard AM), you can use a cheap, simple **Envelope Detector**!
This is exactly why analog TV used it: the TV broadcaster transmits the complex VSB signal with a carrier, so millions of consumer TVs could use a 5-cent diode to demodulate the video instead of an expensive Phase Locked Loop.

---

## Summary Trade-offs

- **Bandwidth**: Slightly worse than SSB, vastly better than DSB.
- **Complexity**: Much easier to filter than SSB. Can use cheap envelope detectors if a carrier is added.
- **Application**: The absolute king of wideband analog signals with DC components (Television).
