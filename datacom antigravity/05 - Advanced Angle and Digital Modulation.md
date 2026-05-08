# Advanced Angle and Digital Modulation

> **Prerequisites**: [[04 - Angle Modulation (FM and PM)]]
> **Course**: CSE 311 — Data Communication (Md Asib Rahman)

This note serves as the definitive bridge. We begin by pushing analog Angle Modulation to its extreme mathematical limits (Narrowband vs. Wideband), exploring exactly how the hardware generates and demodulates these signals. Then, we pivot entirely: we leave the analog world behind and explore how these exact same principles (Amplitude, Frequency, and Phase) are used to transmit discrete digital bits in **ASK, FSK, and PSK**.

---

## PART 1: NARROWBAND FM (NBFM) — Spectrum Efficiency

In systems where bandwidth is heavily restricted (e.g., walkie-talkies, marine radio, emergency services), we can't afford the massive bandwidth of standard FM. We force the modulation index to be extremely small: $\beta \ll 1$.

### 1.1 The Mathematical Approximation
When $\beta$ is very small, we can use small-angle approximations:
$\sin(\beta \sin(\omega_m t)) \approx \beta \sin(\omega_m t)$
$\cos(\beta \sin(\omega_m t)) \approx 1$

This simplifies the complex FM equation into something that looks suspiciously like AM:
$$Y_{NBFM}(t) \approx V_C \cos(\omega_c t) + \frac{V_C \beta}{2} \cos((\omega_c + \omega_m)t) - \frac{V_C \beta}{2} \cos((\omega_c - \omega_m)t)$$

### 1.2 Characteristics
- **Bandwidth**: Exactly $2f_m$ (Identical to AM!).
- **Sidebands**: Only one significant pair (Upper and Lower).
- **Phase Relationship**: The Lower Sideband (LSB) is exactly **180° out of phase** with the Upper Sideband (USB). This phase inversion is the *only* mathematical difference between NBFM and standard AM.

### 1.3 NBFM Hardware Generation
Because the math looks like AM, we generate it like AM! 
1. We take an oscillator and shift it by $-90^\circ$.
2. We multiply it by the integrated message (producing a DSB-SC signal).
3. We add it back to the unshifted carrier.

![NBFM Generation](file:///mnt/Data/3-2/datacom%20antigravity/diagrams/nbfm_block.png)

---

## PART 2: WIDEBAND FM (WBFM) — Noise Immunity

When $\beta > 5$, the small-angle approximation fails spectacularly. The math explodes into an infinite series of Bessel functions, $J_n(\beta)$. 

### 2.1 The Spectrum
Unlike NBFM which has only 2 sidebands, WBFM distributes the carrier's power across dozens of sidebands.

![NBFM vs WBFM Spectrum](file:///mnt/Data/3-2/datacom%20antigravity/diagrams/nbfm_vs_wbfm.png)

### 2.2 WBFM Hardware Generation
Generating WBFM directly using a Voltage-Controlled Oscillator (VCO) is unstable. The oscillator tends to drift over time. Instead, we use the **Armstrong Indirect Method**:
1. Use a highly stable crystal oscillator to generate a tiny, stable NBFM signal ($\beta = 0.2$).
2. Pass it through a **Frequency Multiplier** circuit (a non-linear diode).
3. The multiplier scales up *everything*: the center frequency, the deviation, and $\beta$.

![Frequency Multiplier](file:///mnt/Data/3-2/datacom%20antigravity/diagrams/freq_multiplier.png)

---

## PART 3: FM DEMODULATION

How does a receiver convert frequency changes back into audio?

### 3.1 The Differentiator Method (Slope Detection)
Pass the FM signal through a simple RC High-Pass Filter. 
Since the derivative of $\sin(\omega_i t)$ is $\omega_i \cos(\omega_i t)$, the output *amplitude* becomes directly proportional to the instantaneous frequency $\omega_i$. We then just use a standard AM Envelope Detector to extract the audio!

### 3.2 The Phase-Locked Loop (PLL)
Modern digital radios use PLLs. The PLL uses a Phase Detector to compare the incoming FM signal against its own internal VCO. The resulting error voltage (which tells the VCO to speed up or slow down to track the signal) is exactly identical to the original audio message.

![PLL Demodulator](file:///mnt/Data/3-2/datacom%20antigravity/diagrams/pll_block.png)

---

## PART 4: THE DIGITAL PIVOT

The analog era is ending. Modern systems (WiFi, 5G, Bluetooth) transmit discrete symbols (bits) rather than continuous audio waves. We take the three core parameters of a carrier—Amplitude, Frequency, and Phase—and **key** (switch) them between discrete states.

| Dimension | Technique | Robustness | Spectral Efficiency |
| :--- | :--- | :--- | :--- |
| **Amplitude** | ASK | Poor | Low |
| **Frequency** | FSK | Good | Very Low |
| **Phase** | PSK | Excellent | High |

---

## PART 5: AMPLITUDE SHIFT KEYING (ASK)

Also known as On-Off Keying (OOK) in its binary form.
- **Bit 1**: Carrier is ON ($V_C \cos(\omega_c t)$).
- **Bit 0**: Carrier is OFF ($0$).

**Pros**: Extremely simple receiver circuitry (just an envelope detector).
**Cons**: Horrifically susceptible to noise. Amplitude spikes easily flip a 0 to a 1.
**Use Case**: Cheap IR remotes, basic RFID tags.

---

## PART 6: FREQUENCY SHIFT KEYING (FSK)

Instead of turning the carrier off, we switch between two different frequencies.
- **Bit 1**: High frequency ($f_1$).
- **Bit 0**: Low frequency ($f_0$).

**Pros**: Constant amplitude! This means we can use limiters to completely ignore amplitude noise, just like analog FM.
**Cons**: Very poor spectral efficiency. It requires a wide bandwidth to transmit the two separate frequency tones without overlap.
**Use Case**: Legacy modems, Pagers, Bluetooth (GFSK).

---

## PART 7: PHASE SHIFT KEYING (PSK)

This is the undisputed king of digital modulation. We keep both amplitude and frequency perfectly constant, and encode data in sudden phase shifts.

### 7.1 Binary PSK (BPSK)
- **Bit 1**: $0^\circ$ phase.
- **Bit 0**: $180^\circ$ phase.

![BPSK Waveform](file:///mnt/Data/3-2/datacom%20antigravity/diagrams/bpsk_waveform.png)

### 7.2 Quadrature PSK (QPSK)
Why stop at 2 phases? By using 4 distinct phases (45°, 135°, 225°, 315°), we can encode **2 bits per symbol**. 
This is magic: QPSK transmits twice as much data as BPSK in the exact same bandwidth, without requiring any extra transmitter power.

### 7.3 Constellation Diagrams
We visualize digital modulation on an I/Q plane. The distance between points represents noise immunity.

![Constellations](file:///mnt/Data/3-2/datacom%20antigravity/diagrams/constellations.png)

---

## PART 8: DIFFERENTIAL PSK (DPSK)

Standard PSK has a major flaw: the receiver needs an absolutely perfect, phase-locked "reference" carrier to compare the incoming signal against (Coherent Detection). If the receiver's internal clock drifts by even a fraction of a degree, it might mistake a 0° for a 180°.

**The Solution**: DPSK.
Instead of encoding bits in the absolute phase, we encode data in **phase changes**.
- **Bit 0**: Do not change the phase from the previous symbol.
- **Bit 1**: Shift the phase by 180° from the previous symbol.

### 8.1 Delay-and-Multiply Demodulation
Because we only care about differences, the receiver simply delays the incoming signal by exactly one bit period ($T_b$) and multiplies it by the current signal. If they match, the output is positive (0). If they are inverted, the output is negative (1). No internal reference clock required!

![DPSK Logic](file:///mnt/Data/3-2/datacom%20antigravity/diagrams/dpsk_block.png)

---

## PART 9: THE ULTIMATE PERFORMANCE SYNTHESIS

How do we mathematically compare these digital schemes? We look at the **Symbol Error Rate (SER)** against the **Signal-to-Noise Ratio per Bit ($E_b/N_0$)**.

![SER vs SNR](file:///mnt/Data/3-2/datacom%20antigravity/diagrams/ser_snr.png)

### 9.1 Key Takeaways for the Exam
1. **BPSK and QPSK share the same curve**: This proves QPSK is fundamentally superior, giving double the data rate for free.
2. **ASK is the worst**: Notice how the ASK curve is shifted far to the right. It requires significantly more power to achieve the same error rate.
3. **FSK is a compromise**: Better than ASK, but worse than PSK. Used when receiver simplicity is prioritized over bandwidth.

---

## PART 10: WORKED EXAMPLES

### Example 1: NBFM vs WBFM Math
**Given**: $f_c = 100 \text{ MHz}$, $f_m = 5 \text{ kHz}$, $k_F = 1 \text{ kHz/V}$, $A_m = 1 \text{V}$.
**Find**: $\beta$ and Bandwidth.
1. $\Delta f = k_F \cdot A_m = 1 \text{ kHz}$.
2. $\beta = 1 / 5 = \mathbf{0.2}$. Since $0.2 < 1$, this is **NBFM**.
3. Bandwidth $= 2 \cdot f_m = \mathbf{10 \text{ kHz}}$.

### Example 2: BPSK Bandwidth
**Given**: A 10 Mbps data stream using BPSK with an ideal Nyquist filter (roll-off $r=0$).
**Find**: Minimum bandwidth.
1. For BPSK, 1 bit = 1 symbol. So $R_s = R_b = 10 \text{ MBaud}$.
2. Bandwidth $= R_s \cdot (1 + r) = 10 \cdot 1 = \mathbf{10 \text{ MHz}}$.
*(If we used QPSK instead, $R_s$ would drop to 5 MBaud, reducing bandwidth to 5 MHz!).*

---

> **Next Note**: The logical evolution of PSK is to combine Phase and Amplitude together to create incredibly dense data grids. → [[09 - Quadrature Amplitude Modulation (QAM)]]
