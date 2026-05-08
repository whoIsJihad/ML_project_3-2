# AM Modulators and Demodulators

> **Prerequisites**: [[03 - Amplitude Modulation (AM)]]

This note covers the actual circuit implementations used to generate (modulate) and recover (demodulate) standard AM signals.

---

## Modulators (Generating AM)

To generate AM, we essentially need to multiply the message $m(t)$ by the carrier. Since perfectly linear multipliers are difficult to build, we often exploit **non-linear** components (like diodes or transistors) or **switching** behavior.

### 1. Square-Law Modulator
Uses a non-linear device like a diode or a FET operating in its non-linear region.
- **Concept**: The current-voltage characteristic is $i(t) = a_1 v(t) + a_2 v^2(t)$.
- **Process**: 
  1. Add the message and carrier: $v(t) = m(t) + c(t)$.
  2. Pass it through the non-linear device. The $v^2(t)$ term generates the product $2m(t)c(t)$, which is the necessary modulation term.
  3. Pass the output through a Bandpass Filter centered at $f_c$ to extract the standard AM signal and block unwanted frequencies.
- **Pros/Cons**: Simple, but highly inefficient and only works well for low modulation indices to avoid severe distortion.

### 2. Switching Modulator
Instead of a smooth non-linearity, we use a diode as a fast switch toggled by the high-power carrier.
- **Concept**: The strong carrier $c(t)$ turns a diode ON during positive half-cycles and OFF during negative half-cycles.
- **Process**:
  1. This is mathematically equivalent to multiplying $(m(t) + c(t))$ by a square wave switching at $f_c$.
  2. A Bandpass Filter then smooths out the square wave into a sine wave, extracting the fundamental frequency and yielding AM.
- **Pros/Cons**: Much more efficient than square-law. Commonly used in practical high-power transmitters.

---

## Demodulators (Recovering AM)

### 1. Square-Law Demodulator
Works on the exact same principle as the square-law modulator, but in reverse.
- The received AM signal $s(t)$ is squared.
- The squaring operation causes the envelope to be mixed down to baseband (audio frequencies).
- A Low Pass Filter extracts the audio.
- *Trade-off*: Suffers from distortion because squaring the envelope $(1 + m\cos\omega_m t)^2$ creates a $\cos^2$ term (second harmonic distortion of the audio).

### 2. Envelope Detector (The Industry Standard)
The most important, brilliant, and simple circuit in radio history.
- **Components**: Just a Diode, a Resistor, and a Capacitor in parallel.
- **Mechanism**:
  1. The diode acts as a half-wave rectifier, only letting the positive peaks of the AM signal through.
  2. The capacitor charges up quickly to the peak voltage of the carrier.
  3. When the carrier drops, the capacitor slowly discharges through the resistor.
  4. If the RC time constant is chosen perfectly, the capacitor voltage smoothly "traces" the outline (envelope) of the peaks, filtering out the high-frequency carrier completely.
- **The RC Trade-off**:
  - If RC is **too large**: Diagonal clipping. The capacitor discharges too slowly and misses the fast dips in the audio message.
  - If RC is **too small**: High-frequency ripple. The capacitor discharges too fast, and the audio signal becomes jagged with carrier noise.
- **Why it rules**: It is asynchronous. It does not need a local oscillator or a PLL. It is incredibly cheap.

### 3. Synchronous Detector
Used primarily for DSB-SC and SSB, but *can* be used for standard AM.
- Multiplies the incoming signal by a locally generated carrier that is perfectly phase-locked.
- Very expensive, but provides vastly superior noise performance compared to an envelope detector.
