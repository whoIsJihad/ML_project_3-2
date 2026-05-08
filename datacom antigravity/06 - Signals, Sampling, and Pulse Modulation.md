# Signals, Sampling, and Line Coding

> **Prerequisites**: [[00 - Why Modulation Exists]], [[02 - Analog vs Digital Modulation]]
> **Course**: CSE 311 — Data Communication (Niaz Sir's Module)

This comprehensive guide covers the foundational physics of signals, the mathematics of sampling, and the critical transitional techniques that bridge raw analog data (like a voice) into discrete digital bits suitable for transmission.

![Digital-to-Digital Conversion Pipeline](file:///mnt/Data/3-2/datacom%20antigravity/diagrams/niaz_pipeline.png)

---

## PART 1: SIGNAL BASICS & SHANNON'S LIMIT

### 1.1 Signal Classification
- **Continuous vs. Discrete**: Analog signals are continuous in both time and amplitude. Digital signals exist only at discrete values.
- **Periodic vs. Aperiodic**: Periodic signals repeat a specific pattern exactly. Aperiodic signals never repeat.
- **Deterministic vs. Random**: Deterministic signals are perfectly predictable via math. Random signals contain unpredictable noise or information.
- **Energy vs. Power**: Energy signals decay to zero (finite energy, zero power). Power signals go on forever (infinite energy, finite periodic power).

### 1.2 Signal Transformations in Time
Given a signal $x(t)$:
- **Time Shifting**: $x(t - t_0)$ delays the signal. $x(t + t_0)$ advances it.
- **Time Scaling**: $x(\alpha t)$. If $\alpha > 1$, the signal is compressed. If $\alpha < 1$, it is expanded.
- **Time Inversion**: $x(-t)$ flips the signal along the vertical Y-axis.

### 1.3 Shannon's Channel Capacity Theorem (Crucial)
This is the fundamental limit of the universe for communication.
$$C = B \log_2(1 + \text{SNR})$$
Where:
- $C$ = Absolute maximum channel capacity in bits per second (bps).
- $B$ = Bandwidth of the channel in Hertz (Hz).
- $\text{SNR}$ = Signal-to-Noise Ratio (Linear scale, not dB).

> [!important] The Bandwidth-SNR Trade-off
> To increase your data rate, you must either buy more bandwidth $B$ or pump more power to improve your $\text{SNR}$. Modern modulation schemes try to balance this trade-off.

![Shannon Capacity Curve](file:///mnt/Data/3-2/datacom%20antigravity/diagrams/niaz_shannon.png)

---

## PART 2: FOURIER ANALYSIS FUNDAMENTALS

### 2.1 The Unit Impulse (Dirac Delta)
The Dirac delta function $\delta(t)$ is infinitely tall at $t=0$, infinitely narrow, and has an exact area of 1.
**The Sifting Property**:
If you multiply a continuous signal by a shifted impulse and integrate, it "sifts" out the exact value of the signal at that instant.
$$\int_{-\infty}^{\infty} x(t) \delta(t - t_0) dt = x(t_0)$$

### 2.2 Periodic Signals and Fourier Series
*Any* periodic signal can be broken down into a sum of pure sine and cosine waves (harmonics).
$$x(t) = \frac{a_0}{2} + \sum_{n=1}^{\infty} \left[ a_n \cos(n\omega_0 t) + b_n \sin(n\omega_0 t) \right]$$

For example, a square wave is just a fundamental sine wave stacked with its 3rd harmonic, 5th harmonic, 7th harmonic, etc.

![Fourier Series Decomposition](file:///mnt/Data/3-2/datacom%20antigravity/diagrams/niaz_fourier.png)

### 2.3 The Fourier Transform (Aperiodic Signals)
If a signal doesn't repeat, its period is mathematically infinite. The discrete harmonics blur together into a continuous spectrum.
**Forward Transform (Time to Freq)**: $X(f) = \int_{-\infty}^{\infty} x(t) e^{-j2\pi ft} dt$
**Inverse Transform (Freq to Time)**: $x(t) = \int_{-\infty}^{\infty} X(f) e^{j2\pi ft} df$

**Crucial Transform Properties**:
- **Time Shifting**: Shifting in time only affects phase, not the frequency magnitude.
- **Modulation**: Multiplying by a carrier $e^{j2\pi f_c t}$ shifts the spectrum up to $f_c$.
- **Time Scaling**: Compressing a signal in time expands it in frequency. (Short pulses require massive bandwidth).

---

## PART 3: SAMPLING THEOREM & RECONSTRUCTION

Before we can convert analog to digital, we must take snapshots (samples) of it. How fast do we need to snap photos to not lose the shape of the wave?

### 3.1 The Nyquist-Shannon Theorem
> A bandlimited signal with maximum frequency $f_m$ can be perfectly reconstructed if the sampling rate $f_s$ satisfies:
> $$f_s \geq 2f_m$$

**The Nyquist Rate**: $f_N = 2f_m$ (The absolute minimum speed).

### 3.2 The Frequency Domain View (Aliasing)
When you sample a signal, its frequency spectrum duplicates itself infinitely at multiples of the sampling rate ($\pm f_s, \pm 2f_s, \dots$).
- **If $f_s > 2f_m$**: The copies do not overlap. You can use a Low-Pass Filter to extract the original perfectly.
- **If $f_s < 2f_m$**: The copies smash into each other. High frequencies bleed into low frequencies. This catastrophic data loss is called **Aliasing**.

![Sampling in Frequency Domain](file:///mnt/Data/3-2/datacom%20antigravity/diagrams/niaz_sampling.png)

### 3.3 Reconstruction (Sinc Interpolation)
To rebuild the continuous analog wave from discrete dots, we use an Ideal Low-Pass filter. In the time domain, the impulse response of an ideal filter is a **sinc function**. 
Every sample drops a sinc function, and adding them all together perfectly traces the original analog wave!

![Sinc Reconstruction](file:///mnt/Data/3-2/datacom%20antigravity/diagrams/niaz_sinc_pam.png)

---

## PART 4: PULSE MODULATION (ANALOG TO PULSE)

Now that we know how to sample, how do we transmit those samples?

### 4.1 Pulse Amplitude Modulation (PAM)
We hold the amplitude of each sample to define the height of a rectangular pulse. This is the simplest method, but like AM, it is heavily susceptible to noise destroying the pulse height.

### 4.2 Pulse Time Modulation (PWM and PPM)
Instead of varying the height (which noise corrupts), we vary the timing!
- **Pulse Width Modulation (PWM)**: A louder signal makes a *wider* pulse.
- **Pulse Position Modulation (PPM)**: A louder signal pushes the pulse *later* in the time slot. 
**Advantage**: Pulse heights are constant, so we can use limiters to completely reject amplitude noise.

![PWM vs PPM](file:///mnt/Data/3-2/datacom%20antigravity/diagrams/niaz_pwm_ppm.png)

### 4.3 Pulse Code Modulation (PCM)
This is the true bridge to the digital world. We don't just transmit the pulse; we **quantize** it to the nearest binary value.
1. **Sample**: at $f_s \geq 2f_m$.
2. **Quantize**: Round to the nearest level. ($n$ bits = $2^n$ levels).
3. **Encode**: Spit out the binary string.

![PCM Process](file:///mnt/Data/3-2/datacom%20antigravity/diagrams/niaz_pcm.png)

> [!example] PCM Bit Rate Calculation
> A voice channel ($f_m = 4$ kHz) is sampled at $8$ kHz. We use 8 bits per sample.
> Bit Rate $R_b = 8000 \text{ samples/sec} \times 8 \text{ bits/sample} = \mathbf{64 \text{ kbps}}$.

### 4.4 Delta Modulation (DM)
Instead of transmitting the full 8-bit value of the sample, what if we just transmit the *difference* between the current sample and the last one? 
If the wave goes up, send a `1`. If it goes down, send a `0`.
- **Pro**: Extremely simple, low bit rate.
- **Con**: Suffers from **Slope Overload** (it can't keep up if the signal jumps violently).

---

## PART 5: DIGITAL-TO-DIGITAL (LINE CODING)

You have a string of 1s and 0s from your PCM encoder. How do you physically put them on a copper wire? You need a **Line Code**.

### 5.1 Common Line Codes

![Line Coding Comparison](file:///mnt/Data/3-2/datacom%20antigravity/diagrams/niaz_line_codes.png)

- **Unipolar NRZ**: $1 \rightarrow +V$, $0 \rightarrow 0V$. Terrible DC offset.
- **Bipolar NRZ**: $1 \rightarrow +V$, $0 \rightarrow -V$. Fixes DC offset, but long strings of 0s cause loss of clock synchronization.
- **Return to Zero (RZ)**: Pulses return to $0V$ in the middle of the bit. Excellent clock sync, but uses double the bandwidth.
- **Manchester**: $1$ is a high-to-low transition. $0$ is a low-to-high transition. Perfect clock sync and DC balance, heavily used in Ethernet.
- **AMI (Alternate Mark Inversion)**: $0 \rightarrow 0V$. But for $1$, it alternates between $+V$ and $-V$. Zero DC offset and lower bandwidth.

### 5.2 Block Coding (4B5B)
If AMI or NRZ encounters a long string of zeros (e.g., `00000000`), the receiver loses the clock because the voltage never changes.
**Solution**: 4B5B. We map every 4 bits of data into a 5-bit code that is *mathematically guaranteed* to never have more than three consecutive zeros.
- Example: `0000` is mapped to `11110`. 

### 5.3 Scrambling
For high-speed links (like 10G Ethernet), we XOR the data with a pseudo-random sequence. This naturally destroys long runs of 0s or 1s, balancing the DC offset without needing the 25% overhead of 4B5B.

---

## PART 6: SYNTHESIS & COMPLETE FLOW

Let's trace a voice call from a microphone to a router.

1. **Anti-Aliasing Filter**: A Low-Pass filter cuts off the microphone at 4 kHz.
2. **Sampler**: An ADC samples the wave at 8 kHz (satisfying Nyquist).
3. **Quantizer (PCM)**: The sample is rounded to one of 256 voltage levels.
4. **Encoder**: The level is converted to an 8-bit binary word.
5. **Line Coder**: The bits are converted into a Manchester voltage waveform to maintain clock sync down the wire.
6. **Modulator**: The Manchester wave is fed into a QPSK modulator to be blasted over WiFi to the router.

---

> **Next Note**: To understand how the Modulator in Step 6 actually works, see the advanced transitional guide at [[05 - Advanced Angle and Digital Modulation]].
