# Answers to Theoretical Questions: Digital Communications

## Section 1: Bandwidth and Transmission Fundamentals

### 1. Why signal bandwidth must be ≤ channel bandwidth

For successful transmission, the channel must be able to pass all frequency components of the signal. If the signal contains frequencies outside the channel's range, those components will be severely attenuated or blocked entirely. This causes **distortion**—the received signal won't match the transmitted signal, leading to loss of information.

**Violation:** When signal BW > channel BW, higher (or lower) frequency components are cut off. For voice, this makes speech unintelligible. For data, it causes inter-symbol interference and bit errors.

---

### 2. Channel with 10 kHz bandwidth transmitting voice and music

**(a) Human voice:** **YES**. Voice bandwidth is approximately 3.1 kHz (300-3400 Hz). Since 3.1 kHz < 10 kHz, the channel can accommodate it with room to spare.

**(b) FM radio quality music:** **NO**. High-fidelity music requires bandwidth of approximately 15-20 kHz (20 Hz to 20 kHz). Since 20 kHz > 10 kHz, the channel cannot pass all frequency components. The music would sound muffled and lack high-frequency detail.

---

### 3. Signal bandwidth vs channel bandwidth

**Signal bandwidth:** An intrinsic property of the information being transmitted. It's determined by the frequency content of the signal itself (difference between highest and lowest frequencies in the signal).

**Channel bandwidth:** A physical property of the transmission medium. It's the range of frequencies that the channel can effectively transmit without significant loss.

**Analogy:** Signal bandwidth is the width of your car. Channel bandwidth is the width of the tunnel. The tunnel must be wider than the car for you to pass through without hitting the walls.

---

### 4. Why increasing signal bandwidth requires increasing channel bandwidth

Signals with higher bandwidth contain a wider range of frequency components. To preserve all these components during transmission, the channel must be capable of passing this entire frequency range.

**Practical implications:**
- Wider bandwidth channels are more expensive (copper wires, fiber optics, or radio spectrum allocation costs more)
- Bandwidth is a limited resource—spectrum must be shared among users
- System design involves tradeoffs: higher data rates need more bandwidth but cost more

---

### 5. Relationship between signal duration and bandwidth

**Time-frequency uncertainty principle:** A signal cannot be simultaneously narrow in both time and frequency. Mathematically, from the Fourier Transform scaling property: compressing in time expands in frequency.

**Explanation:** A short pulse (small time duration) requires many high-frequency components to create sharp transitions. A long, slowly varying signal requires only low frequencies.

**Example:** A 1 ms pulse needs approximately 1 kHz of bandwidth. A 1 μs pulse needs approximately 1 MHz of bandwidth.

---

## Section 2: Signal-to-Noise Ratio and System Performance

### 6. SNR definition and decibel expression

**SNR** = Ratio of signal power to noise power: $\text{SNR} = P_s / P_n$

**Why decibels?** SNR values span enormous ranges (0.001 to 1,000,000). Logarithmic scale compresses this into manageable numbers (−30 dB to 60 dB). Also, multiplication becomes addition in dB, simplifying cascaded system analysis.

$$\text{SNR}_{\text{dB}} = 10 \log_{10}(P_s/P_n)$$

---

### 7. SNR's effect on data rate (Shannon's formula)

$$C = B \log_2(1 + \text{SNR})$$

Higher SNR allows the receiver to distinguish between more signal levels, enabling encoding of more bits per symbol. This directly increases achievable data rate.

**Example:** At constant bandwidth B:
- SNR = 1 (0 dB): $C = B \log_2(2) = B$ bits/s
- SNR = 3 (4.77 dB): $C = B \log_2(4) = 2B$ bits/s
- SNR = 15 (11.76 dB): $C = B \log_2(16) = 4B$ bits/s

---

### 8. Strategies for reliable communication at low SNR

- **Increase signal power** if possible (limited by regulations and battery life)
- **Reduce data rate** to allow more energy per bit
- **Use powerful error-correcting codes** to overcome errors caused by noise
- **Increase transmission time** (spread spectrum techniques)
- **Use multiple antennas** (diversity techniques)
- **Reduce noise** through shielding or cooling (for receiver electronics)

---

### 9. Doubling bandwidth vs doubling SNR

**Doubling bandwidth:** $C_{\text{new}} = 2B \log_2(1 + \text{SNR})$ → Capacity approximately doubles

**Doubling SNR:** $C_{\text{new}} = B \log_2(1 + 2\text{SNR})$ → Capacity increases by less than 1 bit/Hz (logarithmic relationship)

**Conclusion:** **Doubling bandwidth has more dramatic effect** than doubling SNR, especially at high SNR values where logarithmic returns diminish.

---

### 10. Why increasing power improves noise immunity

Noise has a relatively fixed power level (determined by thermal noise and environmental interference). Increasing signal power raises the signal level above the noise floor, making the signal more distinguishable.

**Physical reasoning:** With higher signal power, noise fluctuations become smaller relative to signal amplitude. The receiver can more reliably determine whether a "1" or "0" was transmitted because the decision threshold is further from the noise level.

---

## Section 3: Energy Signals vs Power Signals

### 11. Energy and power signal definitions; why not both

**Energy signal:** Finite total energy ($0 < E < \infty$), zero average power ($P = 0$)

**Power signal:** Infinite total energy ($E = \infty$), finite average power ($0 < P < \infty$)

**Why not both?** Power is energy per unit time averaged over infinite time. If energy is finite and you divide by infinite time, power → 0. If power is finite and non-zero over infinite time, total energy → ∞. Mathematically mutually exclusive.

---

### 12. Why periodic signals are power signals, pulses are energy signals

**Periodic signals** continue forever at constant amplitude. Over infinite time, they deliver infinite energy, but their average power (energy per cycle) remains finite and constant.

**Transient pulses** occur once and decay. Their energy is confined to a finite duration, giving finite total energy. Averaged over infinite time, power → 0.

---

### 13. Which type is more relevant for practical communication

**Energy signals** are more relevant. Real communication involves transmitting finite-duration signals (data packets, voice segments, pulses). These are modeled as energy signals.

Power signals are useful for modeling **carrier waves** and **theoretical analysis** of continuous transmissions, but actual information-bearing signals are energy signals.

---

### 14. Mathematical conditions for energy signals

An energy signal must satisfy:
$$E = \int_{-\infty}^{\infty} |x(t)|^2 \, dt < \infty$$

**Behavior at infinity:** The signal amplitude must approach zero as $t \to \pm\infty$ fast enough that the integral converges. Essentially, the signal must be time-limited or decay sufficiently.

---

### 15. Examples of energy and power signals

**Energy signals:**
1. A single data pulse in digital communication
2. A radar pulse
3. A decaying exponential: $e^{-|t|}$

**Power signals:**
1. A sinusoidal carrier wave: $\cos(2\pi f_0 t)$
2. A square wave repeating forever
3. A DC voltage source

---

## Section 4: Fourier Analysis Foundations

### 16. Transition from Fourier Series to Fourier Transform

**Key concept:** Treat aperiodic signal as periodic with infinite period ($T_0 \to \infty$).

**What happens to spectrum:**
- In Fourier Series: spectrum is **discrete** with spikes at $nf_0$ where $f_0 = 1/T_0$
- As $T_0 \to \infty$: fundamental frequency $f_0 \to 0$ (spacing between harmonics shrinks)
- In the limit: discrete spikes merge into a **continuous spectrum**
- The discrete sum becomes a continuous integral

---

### 17. Significance of Fourier Transform pair

The two equations provide a **bidirectional mapping** between time and frequency domains:

**Analysis equation:** Decomposes $x(t)$ into frequency components $X(f)$  
**Synthesis equation:** Reconstructs $x(t)$ from its frequency components

They represent the same information in different domains. Neither is "more fundamental"—they're equivalent descriptions of the same signal.

---

### 18. Dirichlet's conditions for FT existence

The signal must be **absolutely integrable:**
$$\int_{-\infty}^{\infty} |x(t)| \, dt < \infty$$

**Why necessary?** The Fourier integral must converge. For the integral to exist, the signal must have finite energy. Signals that don't decay or are infinite in extent (like DC forever) violate this condition and require generalized functions (impulses) in their transforms.

---

### 19. Why FS for periodic, FT for aperiodic

**Periodic signals** naturally decompose into discrete harmonic frequencies (integer multiples of $f_0$). Fourier Series captures this discrete spectrum efficiently.

**Aperiodic signals** contain a continuum of frequencies. Fourier Transform represents this continuous spectrum.

Additionally, most periodic signals are power signals (violate Dirichlet condition for FT), while aperiodic signals are typically energy signals (satisfy FT existence conditions).

---

### 20. "Harmonically related sinusoids" meaning

All frequency components are **integer multiples** of a fundamental frequency $f_0$: $f_0, 2f_0, 3f_0, \ldots$

**Why must they be harmonically related?** For the sum to be periodic with period $T_0$. A sinusoid at frequency $nf_0$ completes exactly $n$ cycles in time $T_0$, so it repeats with the same period. Non-harmonic frequencies would destroy periodicity.

---

## Section 5: Fourier Transform Properties

### 21. Time scaling property explained

$$x(at) \leftrightarrow \frac{1}{|a|} X(f/a)$$

**Compression in time ($a > 1$):** Signal changes faster, requiring higher frequencies → spectrum expands (stretches along frequency axis)

**Expansion in time ($0 < a < 1$):** Signal changes slower, using lower frequencies → spectrum compresses

**Physical insight:** Fast transitions need high frequencies. Slow transitions need only low frequencies. This is the mathematical expression of the uncertainty principle.

---

### 22. Convolution theorem and its importance

$$x(t) * y(t) \leftrightarrow X(f) \cdot Y(f)$$

**Why most important?** System analysis with LTI systems requires convolution in time domain:
$$y(t) = h(t) * x(t)$$

Convolution is mathematically complex (nested integrals). In frequency domain, this becomes simple multiplication:
$$Y(f) = H(f) \cdot X(f)$$

This transforms difficult integral calculus into simple algebra, making filtering analysis trivial.

---

### 23. Duality property and example

$$X(t) \leftrightarrow x(-f)$$

**Meaning:** Swap time and frequency domains, with frequency axis flipped.

**Example:** We know rectangular pulse in time transforms to sinc in frequency:
$$\text{rect}(t) \leftrightarrow \text{sinc}(f)$$

By duality:
$$\text{sinc}(t) \leftrightarrow \text{rect}(-f) = \text{rect}(f)$$

So sinc in time transforms to rectangle in frequency! This is how we derive the ideal lowpass filter impulse response without integration.

---

### 24. Time shift property explained

$$x(t - t_0) \leftrightarrow e^{-j2\pi f t_0} X(f)$$

The magnitude spectrum $|X(f)|$ remains unchanged. Only phase spectrum changes linearly: $\theta(f) = -2\pi f t_0$

**Why?** Time delay affects when frequency components arrive, not their amplitude. Energy content at each frequency is the same, just phase-shifted. For power/energy calculations (which depend on $|X(f)|^2$), time delays are invisible.

---

### 25. Multiplication theorem

$$x(t) \cdot y(t) \leftrightarrow X(f) * Y(f)$$

**Relationship to convolution theorem:** These are duals of each other:
- Time domain convolution → Frequency domain multiplication
- Time domain multiplication → Frequency domain convolution

**Use case:** Modulation (multiplying signal by carrier) causes frequency shifts. Windowing a signal (multiplication by time window) causes spectral spreading (convolution with window's spectrum).

---

## Section 6: Special Functions

### 26. Unit impulse function definition and nature

$$\delta(t) = \begin{cases} \infty & t = 0 \\ 0 & t \neq 0 \end{cases}$$
with $\int_{-\infty}^{\infty} \delta(t) \, dt = 1$

**Why not a "real" function?** No actual function can be zero everywhere except one point yet have non-zero integral. It's a **distribution** or **generalized function**—defined by its behavior under integration, not pointwise values. It's the limit of increasingly tall, narrow pulses.

---

### 27. Sampling property and its use

$$\int_{-\infty}^{\infty} x(t) \delta(t - T) \, dt = x(T)$$

The delta function "picks out" or "samples" the value of $x(t)$ at $t = T$.

**Use in sampling:** Sampling is mathematically modeled as multiplying signal by impulse train:
$$x_s(t) = x(t) \sum_n \delta(t - nT_s)$$

Each impulse extracts the signal value at that instant, creating the discrete samples.

---

### 28. Fourier Transform of delta function

$$\delta(t) \leftrightarrow 1$$

**Interpretation:** An impulse at $t = 0$ contains **all frequencies equally** with constant magnitude. This makes intuitive sense: an infinitely short pulse requires infinite bandwidth to represent (all frequencies needed for sharp transition).

**By duality:** $1 \leftrightarrow \delta(f)$ → A DC signal (constant for all time) has all its energy at frequency zero.

---

### 29. Sinc function definition and prevalence

$$\text{sinc}(x) = \frac{\sin(\pi x)}{\pi x}$$

**Why it appears everywhere:**
1. It's the Fourier Transform of a rectangular pulse (ideal time-limited signal)
2. It's the impulse response of an ideal lowpass filter (by duality)
3. It's the interpolation kernel in the sampling theorem
4. It naturally arises from the sharp cutoffs (rectangles) in either time or frequency domain

---

### 30. Ideal lowpass filter and sinc impulse response

An ideal lowpass filter has rectangular frequency response:
$$H(f) = \begin{cases} 1 & |f| \leq B \\ 0 & |f| > B \end{cases}$$

By inverse Fourier Transform (or duality):
$$h(t) = 2B \cdot \text{sinc}(2Bt)$$

**Why unrealizable?** The sinc function extends to $\pm\infty$ in time. To implement this filter, you'd need to wait for all future inputs (non-causal) and remember all past inputs forever. Physically impossible. Real filters approximate this with finite-length responses, accepting some passband ripple and gradual rolloff.

---

## Section 7: Sampling Theory

### 31. Sampling Theorem and Nyquist rate

**Theorem:** A band-limited signal with maximum frequency $B$ Hz can be perfectly reconstructed from samples taken at rate $f_s > 2B$ samples/second.

**Nyquist rate:** $f_N = 2B$ (minimum sampling rate for perfect reconstruction)

**Significance:** This is the bridge between analog and digital. It guarantees that sampling doesn't lose information if done correctly. Below Nyquist rate, information is irreversibly lost (aliasing).

---

### 32. Spectral replication explained

Sampling creates copies of the original spectrum shifted to every multiple of $f_s$:
$$X_s(f) = \frac{1}{T_s} \sum_{n=-\infty}^{\infty} X(f - nf_s)$$

**Why?** Mathematically, sampling is multiplication by impulse train. By the multiplication theorem, this causes convolution in frequency domain. Convolving with an impulse train replicates the spectrum at each impulse location.

**Physical interpretation:** Sampling introduces periodicity in time domain, which creates discrete copies in frequency domain.

---

### 33. Aliasing: definition and irreversibility

**Aliasing** occurs when $f_s < 2B$. Spectral copies overlap, causing high and low frequency components to mix indistinguishably.

**Why irreversible?** Once overlapped, you cannot separate the original spectrum from the copies. High frequencies "masquerade" as low frequencies. No post-processing can recover the original signal—information is permanently destroyed.

**Example:** A 9 kHz tone sampled at 8 kHz appears as a 1 kHz tone (9 − 8 = 1).

---

### 34. Interpolation formula and sinc's role

$$x(t) = \sum_{n=-\infty}^{\infty} x(nT_s) \text{sinc}\left(\frac{t - nT_s}{T_s}\right)$$

Each sample $x(nT_s)$ is weighted by a time-shifted sinc function. These sinc pulses:
- Equal 1 at their center ($t = nT_s$)
- Equal 0 at all other sample points
- Smoothly interpolate between samples

**Why sinc?** It's the impulse response of the ideal lowpass filter needed to extract the baseband spectrum from the sampled signal's replicated spectra.

---

### 35. Why sample above Nyquist rate in practice

**Reasons:**
1. **Real signals aren't perfectly band-limited** (they have some energy beyond $B$)
2. **Real filters aren't ideal** (can't perfectly separate overlapping spectra with brick-wall cutoff)
3. **Guard bands** prevent near-aliasing (marginal spectral separation)
4. **Easier reconstruction filtering** (less stringent filter requirements)

Typical practice: sample at $2.5B$ to $4B$.

---

### 36. Ideal lowpass filter for reconstruction

The sampled signal has spectral replicas at $\pm f_s, \pm 2f_s, \ldots$. To reconstruct, you must:
- Pass the baseband copy (centered at $f = 0$)
- Block all other copies

This requires an ideal lowpass filter with sharp cutoff at $f_s/2$ (Nyquist frequency).

**Challenge:** As explained in Q30, ideal filters are unrealizable (infinite impulse response, non-causal). Real reconstruction filters have gradual rolloff, requiring oversampling to prevent aliasing.

---

### 37. Sampling interval vs sampling frequency

**Sampling frequency:** $f_s$ = samples per second (Hz)  
**Sampling interval:** $T_s = 1/f_s$ = time between samples (seconds)

**Nyquist interval:** $T_N = 1/(2B)$ = maximum allowable time between samples

These are reciprocals. Higher frequency → shorter interval → more samples → better representation.

---

## Section 8: LTI Systems and Transfer Functions

### 38. Linearity and Time-Invariance definitions

**Linearity:** $ax_1(t) + bx_2(t) \to ay_1(t) + by_2(t)$  
Scaling and superposition are preserved.

**Time-Invariance:** $x(t - t_0) \to y(t - t_0)$  
Delaying input delays output by the same amount; system behavior doesn't change over time.

**Violations:**
- **Non-linear:** Squaring circuit ($y = x^2$), diode rectifier
- **Time-variant:** Amplitude modulation (multiplying by time-varying carrier), aging components

---

### 39. Why impulse response characterizes LTI system

Any input can be expressed as sum of shifted, scaled impulses:
$$x(t) = \int_{-\infty}^{\infty} x(\tau) \delta(t - \tau) \, d\tau$$

By linearity and time-invariance, the output is:
$$y(t) = \int_{-\infty}^{\infty} x(\tau) h(t - \tau) \, d\tau = x(t) * h(t)$$

where $h(t)$ is the response to $\delta(t)$. So knowing $h(t)$ lets you find output for ANY input using convolution.

---

### 40. Time vs frequency domain analysis comparison

**Time domain:** Requires convolution integral
$$y(t) = \int_{-\infty}^{\infty} x(\tau) h(t - \tau) \, d\tau$$
- Mathematically complex
- Nested integrals
- Difficult to visualize system effects

**Frequency domain:** Simple multiplication
$$Y(f) = H(f) \cdot X(f)$$
- Algebraic operation
- Immediately see which frequencies are amplified/attenuated
- Easy to design and analyze

**Preference:** Frequency domain for analysis and design; time domain for understanding transient behavior.

---

### 41. Transfer function definition

$$H(f) = |H(f)| e^{j\theta(f)}$$

**Magnitude $|H(f)|$:** Gain at frequency $f$
- $|H(f)| > 1$: amplification
- $|H(f)| < 1$: attenuation
- $|H(f)| = 0$: complete blocking

**Phase $\theta(f)$:** Phase shift applied to frequency $f$
- Linear phase ($\theta = -2\pi f t_d$): pure delay, no distortion
- Non-linear phase: different frequencies delayed differently, causing distortion

---

### 42. How filtering becomes multiplication

By convolution theorem:
$$y(t) = h(t) * x(t) \quad \Rightarrow \quad Y(f) = H(f) \cdot X(f)$$

**Interpretation:** Each frequency component $X(f)$ is multiplied by the filter gain $H(f)$ at that frequency. Frequencies where $H(f) \approx 0$ are blocked. Frequencies where $H(f) \approx 1$ pass through.

This turns the complex operation of convolution into simple, frequency-by-frequency multiplication.

---

### 43. Lowpass, highpass, and bandpass filters

**Lowpass:** $|H(f)| \approx 1$ for $|f| < f_c$, $\approx 0$ for $|f| > f_c$  
Passes low frequencies, blocks high frequencies

**Highpass:** $|H(f)| \approx 0$ for $|f| < f_c$, $\approx 1$ for $|f| > f_c$  
Blocks low frequencies, passes high frequencies

**Bandpass:** $|H(f)| \approx 1$ for $f_1 < |f| < f_2$, $\approx 0$ elsewhere  
Passes only a specific frequency band

---

### 44. Linear phase response and desirability

**Linear phase:** $\theta(f) = -2\pi f t_d$ (straight line through origin)

This corresponds to pure time delay $t_d$ with no frequency-dependent distortion. All frequency components are delayed by the same time.

**Desirable because:** Non-linear phase causes **phase distortion**—different frequencies arrive at different times, smearing sharp edges and distorting waveform shape. Critical for applications like audio, video, and data communication where waveform shape carries information.

---

## Section 9: Shannon Capacity and Fundamental Limits

### 45. Shannon's Channel Capacity formula

$$C = B \log_2(1 + \text{SNR}) \text{ bits/second}$$

**Fundamental meaning:** The maximum rate at which information can be reliably transmitted through a noisy channel with bandwidth $B$ and signal-to-noise ratio SNR. No coding scheme, no matter how clever, can exceed this rate without errors.

---

### 46. Bandwidth-SNR tradeoff

Both increase capacity, but differently:
- **Bandwidth:** Linear contribution (doubling $B$ roughly doubles $C$)
- **SNR:** Logarithmic contribution (doubling SNR adds about 1 bit/Hz)

**Bandwidth-limited channels:** (e.g., telephone lines, fiber at moderate distances)  
Have high SNR but restricted $B$ → Increasing $B$ helps more

**Power-limited channels:** (e.g., deep space, satellite communications)  
Have wide $B$ but low SNR → Increasing power (SNR) helps more

---

### 47. Logarithmic relationship with SNR

$$C = B \log_2(1 + \text{SNR})$$

Logarithmic because of information theory: each doubling of SNR allows one more distinguishable level, adding 1 bit per sample.

**Practical implications:**
- **Diminishing returns:** At high SNR, huge power increases yield small capacity gains
- **Efficient at low SNR:** At low SNR, small power increases help significantly
- **Power is expensive:** Motivates use of efficient coding and larger bandwidth instead

---

### 48. Infinite bandwidth with fixed power

As $B \to \infty$ with fixed signal power $P_s$:
- Power spectral density spreads thinner
- Noise power increases proportionally with $B$
- SNR $\to 0$

Capacity approaches:
$$C_{\infty} = \frac{P_s}{N_0} \log_2 e \approx 1.44 \frac{P_s}{N_0}$$

where $N_0$ is noise power spectral density.

**Why finite?** Power per Hz becomes vanishingly small. Eventually, signal is buried in noise regardless of bandwidth. There's a fundamental limit based on energy per bit vs noise density.

---

### 49. Shannon Capacity as fundamental limit

Shannon proved this is the **information-theoretic limit**. It's derived from:
- Probability theory
- The definition of channel capacity (maximum mutual information)
- Fundamental physical constraints

**Can it be exceeded?** **No.** Any attempt to transmit faster will result in irreducible errors. You can approach it arbitrarily closely with sophisticated coding, but never exceed it. This is as fundamental as thermodynamic limits in physics.

---

## Section 10: Analog-to-Digital Conversion

### 50. Two steps of ADC

**1. Sampling:** Discretize the time axis (continuous time → discrete time)  
Governed by sampling theorem; must satisfy $f_s > 2B$

**2. Quantization:** Discretize the amplitude axis (continuous amplitude → discrete levels)  
Maps infinite continuous values to finite number of levels

**Why both necessary?** Digital systems process discrete-time, discrete-amplitude signals. Sampling alone gives discrete-time but continuous amplitude (not processable digitally). Quantization alone gives discrete amplitude but continuous time (infinite data). Both needed for finite digital representation.

---

### 51. Sampling vs quantization; which introduces error

**Sampling:** According to sampling theorem, if $f_s > 2B$, sampling is **theoretically lossless**—perfect reconstruction possible.

**Quantization:** **Irreversibly introduces error**. Continuous amplitude values are rounded to nearest discrete level. The difference (quantization error) cannot be recovered—information is permanently lost.

**Key distinction:** Sampling can be perfect; quantization cannot.

---

### 52. Why higher sampling rate improves fidelity

Higher $f_s$ means:
- Samples closer together in time
- Better capture of rapid signal variations
- Larger margin above Nyquist rate (easier anti-aliasing filtering)
- More sample points to interpolate between

Though theoretically perfect at $f_s = 2B$, practical factors (non-ideal filters, slight band-extension) make higher rates beneficial.

---

### 53. Quantization levels and bit relationship

With $n$ bits, you can represent $2^n$ discrete values:
$$L = 2^n$$

**Tradeoff:**
- **More bits** → More levels → Smaller quantization error → Higher quality
- **But** → More data to store/transmit → Higher bandwidth/storage requirements

**Example:** 8-bit audio has 256 levels; 16-bit has 65,536 levels (much better quality but double the data).

---

### 54. Why quantization error cannot be zero

Quantization maps a **continuous range** of amplitudes to a **single discrete level**. All values within a quantization interval get mapped to the same output.

**Example:** With levels at 0, 1, 2, 3, ..., any input between 0.5 and 1.5 might map to 1. A value of 1.4 has error of 0.4.

**Difference from sampling:** Sampling preserves amplitude perfectly at sample points (if Nyquist criterion met). Quantization fundamentally discards amplitude precision. The error is bounded by $\pm \Delta/2$ where $\Delta$ is the step size, but never zero.

---

## Section 11: Source Coding vs Channel Coding

### 55. Goal of source coding and example

**Goal:** Remove statistical redundancy to compress data, representing information with fewer bits.

**Example:** **Huffman coding** assigns short codes to frequent symbols, long codes to rare symbols. Text with frequent 'E' and rare 'Z' uses fewer bits than fixed-length encoding.

---

### 56. Goal of channel coding and apparent contradiction

**Goal:** Add structured redundancy to enable error detection and correction despite channel noise.

**Apparent contradiction:** Source coding removes redundancy; channel coding adds it. Seems contradictory!

**Resolution:** Different types of redundancy:
- Source coding removes **useless redundancy** (predictable patterns carrying no new information)
- Channel coding adds **protective redundancy** (carefully designed patterns that allow error recovery)

---

### 57. Redundancy in source vs channel coding

**Source coding redundancy:** Natural patterns in data (repeated sequences, predictable structure). Wasted space carrying no information. Should be removed.

**Channel coding redundancy:** Intentional extra bits (parity, checksums, error-correcting codes). Provides protection against errors. Should be added strategically.

---

### 58. Why use both in sequence

**Complete pipeline:**
1. **Source encode:** Compress to minimum bits (remove natural redundancy)
2. **Channel encode:** Add protective redundancy (error correction bits)
3. **Transmit** through noisy channel
4. **Channel decode:** Detect and correct errors using redundancy
5. **Source decode:** Decompress to original information

**Result:** Efficient use of bandwidth (compressed) with reliable delivery (error-protected). Best of both worlds.

---

## Section 12: Signal Properties and Transformations

### 59. Periodic signal definition and examples

**Definition:** $x(t) = x(t + T_0)$ for all $t$, where $T_0$ is the fundamental period.

**Examples:**
1. $\cos(2\pi f_0 t)$ with $T_0 = 1/f_0$
2. Square wave alternating between +1 and −1
3. Sawtooth wave

---

### 60. Time operations and order

**Time shifting:** $x(t) \to x(t - t_0)$ (shift right if $t_0 > 0$)  
**Time scaling:** $x(t) \to x(at)$ (compress if $a > 1$, expand if $a < 1$)  
**Inversion:** $x(t) \to x(-t)$ (flip around vertical axis)

**For $x(2t - 3)$:**  
Method 1: Shift then scale → $x(t - 3)$ then $x(2t - 3)$ (need to scale coordinate)  
Method 2: Rewrite as $x(2(t - 1.5))$ → Scale by 2, then shift right by 1.5

**Easier approach:** Factor out the scaling: $x(a(t - b/a))$ means scale by $a$ then shift by $b/a$.

---

### 61. Continuous/discrete time and amplitude

**Time axis:**
- **Continuous-time:** Defined at every instant (smooth curve)
- **Discrete-time:** Defined only at specific instants (sample points)

**Amplitude axis:**
- **Continuous-amplitude:** Can take any value in a range
- **Discrete-amplitude:** Can only take specific levels

---

### 62. Analog vs digital signals

**Analog signal:** Continuous in both time and amplitude  
(Real-world signals like temperature, sound pressure)

**Digital signal:** Discrete in amplitude; time may be continuous or discrete  
(Binary signals: 0 or 1; computer data after ADC)

---

## Section 13: Unit Step Function

### 63. Unit step function and relationship with impulse

**Definition:**
$$u(t) = \begin{cases} 1 & t \geq 0 \\ 0 & t < 0 \end{cases}$$

**Relationship:** Step is the integral of impulse; impulse is the derivative of step:
$$u(t) = \int_{-\infty}^{t} \delta(\tau) \, d\tau$$
$$\delta(t) = \frac{du(t)}{dt}$$

---

### 64. Step as integral of impulse

$$u(t) = \int_{-\infty}^{t} \delta(\tau) \, d\tau$$

For $t < 0$: integral doesn't include the impulse at $\tau = 0$ → result is 0  
For $t \geq 0$: integral includes the impulse → result is 1 (area of impulse)

This expresses that the step "accumulates" the impulse.

---

### 65. Derivative of step function

$$\frac{du(t)}{dt} = \delta(t)$$

The step has a discontinuity (jump) at $t = 0$. The derivative of a discontinuity is an impulse. This formalizes the intuition that an instantaneous jump represents infinite rate of change.

**Useful for:** Expressing derivatives of piecewise functions using impulse and step functions.

---

## Section 14: Advanced Properties and Concepts

### 66. Parseval's Theorem

$$\int_{-\infty}^{\infty} |x(t)|^2 \, dt = \int_{-\infty}^{\infty} |X(f)|^2 \, df$$

**Meaning:** Total signal energy is the same whether computed in time domain or frequency domain. Energy is conserved by the Fourier Transform.

**Significance:** You can analyze energy distribution across frequencies ($|X(f)|^2$ is energy spectral density). Validates that time and frequency are equivalent representations.

---

### 67. Conjugate symmetry and applicability

$$X(-f) = X^*(f)$$

**Meaning:** For real-valued signals, negative frequency components are complex conjugates of positive frequency components.

**When it applies:** Only for **real** signals ($x(t)$ has no imaginary part). Complex signals don't have this symmetry.

**Implication:** For real signals, negative frequencies carry redundant information (fully determined by positive frequencies).

---

### 68. Differentiation property and high-pass effect

$$\frac{dx(t)}{dt} \leftrightarrow j2\pi f \cdot X(f)$$

Multiplying by $f$ in frequency domain amplifies high frequencies (large $f$) and suppresses low frequencies (small $f$).

**Why high-pass?** Differentiation emphasizes rapid changes (high frequencies) and suppresses slow variations (low frequencies). Mathematically, the $j2\pi f$ factor grows with frequency.

---

### 69. Integration property and low-pass effect

$$\int_{-\infty}^{t} x(\tau) \, d\tau \leftrightarrow \frac{X(f)}{j2\pi f} + \frac{X(0)}{2} \delta(f)$$

Dividing by $f$ in frequency domain suppresses high frequencies and emphasizes low frequencies.

**Why low-pass?** Integration smooths out rapid changes (high frequencies) and accumulates slow variations (low frequencies). The $1/f$ factor attenuates as frequency increases.

---

### 70. Frequency shift (modulation) property

$$x(t) e^{j2\pi f_0 t} \leftrightarrow X(f - f_0)$$

Multiplying by a complex exponential (frequency $f_0$) shifts the spectrum by $f_0$.

**Use in communication:** Modulation moves baseband signals (near 0 Hz) to high carrier frequencies for transmission. AM/FM radio, WiFi, cellular all use this principle to allocate different channels at different frequencies without interference.

---

## Section 15: Conceptual Integration Questions

### 71. Bandwidth, SNR, and Shannon Capacity relationship

**Complete chain:**

1. **Bandwidth $B$:** Determines the range of frequencies the channel can pass
2. **SNR:** Quantifies signal quality (power relative to noise)
3. **Shannon Capacity:** Combines both to give maximum data rate:
   $$C = B \log_2(1 + \text{SNR})$$

**Integration:** Wider bandwidth allows more frequency components (more information carrying capacity). Higher SNR allows distinguishing more signal levels per frequency (more bits per symbol). Together they determine the fundamental limit on how fast you can communicate reliably.

---

### 72. Complete analog-to-digital transmission chain

1. **Sampling:** Discretize time at rate $f_s > 2B$ (sampling theorem)
2. **Quantization:** Map continuous amplitudes to $2^n$ discrete levels
3. **Source coding:** Compress (remove redundancy)
4. **Channel coding:** Add error-correction redundancy
5. **Transmission:** Through bandwidth-limited ($B$), noisy (SNR) channel
6. **Channel decoding:** Detect and correct errors
7. **Source decoding:** Decompress
8. **Reconstruction:** Interpolate using sinc functions to recover continuous signal

**Key constraints:**
- Data rate must not exceed Shannon limit: $R < B \log_2(1 + \text{SNR})$
- Signal bandwidth must fit channel: Signal BW $\leq B$

---

### 73. Why Fourier analysis is fundamental

**Unification:**

1. **Bandwidth:** Signal's frequency content revealed by Fourier Transform ($X(f)$ shows which frequencies present)
2. **Filtering:** LTI systems analyzed via multiplication in frequency domain ($Y(f) = H(f) X(f)$)
3. **Sampling:** Spectral replication understood through Fourier domain (copies at $\pm nf_s$)
4. **Channel capacity:** Depends on available frequency range (bandwidth in frequency domain)

**Bottom line:** Fourier Transform converts time-domain problems into frequency-domain problems where:
- Convolution → Multiplication (easier)
- System effects → Visual (frequency response)
- Bandwidth → Directly measurable (spectrum width)

---

### 74. Interconnection: energy signals, FT, and sampling

**Energy signals:**
- Have finite energy → Satisfy Dirichlet condition
- Can be Fourier Transformed

**Fourier Transform:**
- Reveals frequency content → Shows bandwidth $B$
- Determines sampling requirements

**Sampling Theorem:**
- Requires $f_s > 2B$ where $B$ from Fourier Transform
- Applies to energy signals (actual transmitted pulses)

**Chain:** Energy signal → Has finite FT → FT reveals bandwidth → Bandwidth determines Nyquist rate → Governs sampling strategy

---

### 75. Sinc function connecting filtering and reconstruction

**In frequency domain (filtering):**
- Ideal lowpass filter: rectangular $H(f)$
- Passes $|f| < B$, blocks $|f| > B$

**In time domain (impulse response):**
- By inverse FT: $h(t) = 2B \cdot \text{sinc}(2Bt)$

**In reconstruction:**
- Ideal lowpass filter extracts baseband from sampled signal's replicated spectrum
- Its output is convolution with sinc
- This gives interpolation formula: sum of sinc functions

**Connection:** The sinc function is the fundamental link because:
1. It's the FT of a rectangle (ideal filter)
2. It's the impulse response used for reconstruction
3. It provides perfect interpolation between samples

All three aspects are the same mathematical object viewed differently.

---

## Section 16: Formulas and Key Equations

### 76. Signal-to-Noise Ratio formulas

**Linear:**
$$\text{SNR} = \frac{P_{\text{signal}}}{P_{\text{noise}}} = \frac{P_s}{P_n}$$

**Decibels:**
$$\text{SNR}_{\text{dB}} = 10 \log_{10}\left(\frac{P_s}{P_n}\right)$$

---

### 77. Fourier Transform pair

**Analysis (Forward Transform):**
$$X(f) = \int_{-\infty}^{\infty} x(t) e^{-j2\pi f t} \, dt$$

**Synthesis (Inverse Transform):**
$$x(t) = \int_{-\infty}^{\infty} X(f) e^{j2\pi f t} \, df$$

---

### 78. Shannon Capacity formula

$$C = B \log_2(1 + \text{SNR}) \quad \text{[bits per second]}$$

Where:
- $C$ = channel capacity (maximum reliable data rate)
- $B$ = bandwidth (Hz)
- $\text{SNR}$ = signal-to-noise ratio (linear, not dB)

---

### 79. Signal energy and power formulas

**Energy:**
$$E = \int_{-\infty}^{\infty} |x(t)|^2 \, dt$$

**Power:**
$$P = \lim_{T \to \infty} \frac{1}{T} \int_{-T/2}^{T/2} |x(t)|^2 \, dt$$

---

### 80. Sampling theorem and Nyquist rate

**Theorem inequality:**
$$f_s > 2B$$

Where:
- $f_s$ = sampling frequency
- $B$ = maximum frequency in signal (bandwidth)

**Nyquist rate:**
$$f_N = 2B \quad \text{(minimum sampling rate)}$$

**Nyquist interval:**
$$T_N = \frac{1}{2B} \quad \text{(maximum sampling period)}$$

---

This completes all 80 theoretical questions with comprehensive answers.
