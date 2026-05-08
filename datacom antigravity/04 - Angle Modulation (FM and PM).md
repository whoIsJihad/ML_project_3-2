# Angle Modulation: Frequency Modulation (FM) and Phase Modulation (PM)

> **Prerequisites**: [[03 - Amplitude Modulation (AM)]], [[06 - Pulse Amplitude Modulation (PAM)]]
> **Course**: CSE 311 — Data Communication (Md Asib Rahman)

This guide completely overhauls the concept of modulation. Instead of varying the height (amplitude) of a wave, what if we bury our data in the wave's rotation speed (frequency) or its starting angle (phase)?

---

## PART 1: WHY ANGLE MODULATION? (Context & Advantages)

### 1.1 The Fundamental Flaw of AM
In Amplitude Modulation (AM) and Pulse Amplitude Modulation (PAM), the information is encoded in the *height* (voltage level) of the signal. 
The problem? **Most channel noise is additive.** Lightning, motor interference, and static all add random voltage spikes to your signal. Because AM relies on voltage levels to carry data, this noise directly corrupts the information.

### 1.2 The Angle Modulation Concept
Consider a general carrier signal:
$$C(t) = V_C \cos(\omega_c t + \phi)$$

Instead of varying $V_C$, we keep it perfectly constant. We have two other parameters we can vary:
-   **Frequency Modulation (FM)**: We change $\omega$ (angular frequency) according to the message.
-   **Phase Modulation (PM)**: We change $\phi$ (phase) according to the message.
Both are considered "Angle Modulation" because they modulate the total angle of the cosine function.

![General Framework](file:///mnt/Data/3-2/datacom%20antigravity/diagrams/angle_mod_framework.png)

### 1.3 The Superpowers of Angle Modulation

#### Advantage 1: Noise Immunity (The Limiter)
Because the amplitude $V_C$ contains no information, the receiver can pass the incoming signal through a **Limiter** circuit. This clips the tops and bottoms off the wave, completely erasing any amplitude noise before demodulation even begins.

![Limiter Concept](file:///mnt/Data/3-2/datacom%20antigravity/diagrams/limiter_concept.png)

#### Advantage 2: Constant Amplitude (Efficiency)
A constant amplitude means we can use highly non-linear, Class-C amplifiers in the transmitter. These amplifiers are incredibly power-efficient. AM requires linear amplifiers, which waste a massive amount of power as heat.

#### Advantage 3: The Capture Effect
When two AM signals overlap on the same frequency, you hear a garbled mix of both. When two FM signals overlap, the receiver's limiter completely "captures" the stronger signal and entirely suppresses the weaker one. This allows tighter reuse of frequencies in cellular and radio networks.

#### The Trade-off: Disadvantages
-   FM and PM require significantly **more bandwidth** than AM.
-   The receiver circuits (demodulators) are mathematically and physically more complex.

---

## PART 2: FOUNDATIONAL CONCEPTS (Before the Math)

### 2.1 Instantaneous Angular Frequency
If frequency is changing constantly, the concept of $f = 1/T$ breaks down. We need calculus.
Let the total angle inside the cosine be the **instantaneous phase**, $\theta(t)$.
The **instantaneous angular frequency** $\omega_i(t)$ is simply how fast that phase is changing:
$$\omega_i(t) = \frac{d\theta(t)}{dt}$$

> [!tip] Intuition
> Think of $\omega_i(t)$ as the speedometer of the wave. It tells you exactly how fast the wave is oscillating at this exact microsecond.

### 2.2 Frequency Deviation ($\Delta f$)
This is the maximum "swing" away from the center carrier frequency.
-   **FM**: $\Delta f = k_F \cdot A_m$ (where $k_F$ is the frequency sensitivity in Hz/Volt).
-   **PM**: Phase deviation is $\Delta \phi = k_P \cdot A_m$.

### 2.3 The Modulation Index ($\beta$)
This is the most critical parameter for determining bandwidth.
-   **For FM**: $\beta = \frac{\Delta f}{f_m}$ (Ratio of maximum frequency swing to the speed at which it swings).
-   **For PM**: $\beta = \Delta \phi$ (Maximum phase swing in radians).

| Value of $\beta$ | Classification | Resulting Bandwidth |
| :--- | :--- | :--- |
| $\beta < 0.5$ | Narrowband (NBFM) | Small (Comparable to AM) |
| $\beta > 5$ | Wideband (WBFM) | Very Large (High fidelity) |

---

## PART 3: FREQUENCY MODULATION (FM) DETAILED

### 3.1 The Core Equation
In FM, the frequency changes proportionally with the message $m(t)$:
$$\omega_i(t) = \omega_c + 2\pi k_F m(t)$$

Since we need the phase $\theta(t)$ to put inside our cosine, we must **integrate** the frequency:
$$\theta(t) = \int \omega_i(t) dt = \omega_c t + 2\pi k_F \int m(t) dt$$

$$Y_{FM}(t) = V_C \cos\left(\omega_c t + 2\pi k_F \int m(t) dt\right)$$

### 3.2 Single-Tone FM Spectrum (Bessel Functions)
If $m(t)$ is a sine wave, the resulting FM wave requires complex math to find its frequencies. We use **Bessel functions of the first kind**, $J_n(\beta)$.

$$Y_{FM}(t) = V_C \sum_{n=-\infty}^{\infty} J_n(\beta) \cos((\omega_c + n\omega_m)t)$$

![Bessel Functions](file:///mnt/Data/3-2/datacom%20antigravity/diagrams/bessel_plot.png)

> [!important] What this means:
> Unlike AM which has exactly 2 sidebands, FM has an **infinite** number of sidebands spaced at intervals of $f_m$. 
> The amplitude of the $n$-th sideband is determined by the Bessel curve $J_n(\beta)$.

![FM Spectra](file:///mnt/Data/3-2/datacom%20antigravity/diagrams/fm_spectra.png)

### 3.3 Carson's Rule (Bandwidth)
While there are infinite sidebands, most of them have near-zero power. **Carson's Rule** gives the practical bandwidth containing ~98% of the signal power:
$$BW = 2(\Delta f + f_m) = 2f_m(\beta + 1)$$

---

## PART 4: PHASE MODULATION (PM) DETAILED

### 4.1 The Core Equation
In PM, the phase changes directly with the message:
$$\phi(t) = k_P m(t)$$
$$Y_{PM}(t) = V_C \cos(\omega_c t + k_P m(t))$$

What happens to the frequency? We take the derivative!
$$\omega_i(t) = \frac{d}{dt}(\omega_c t + k_P m(t)) = \omega_c + k_P \frac{dm(t)}{dt}$$

> [!tip] The Big Difference
> - **FM's** frequency depends directly on the message.
> - **PM's** frequency depends on the **derivative** of the message.

### 4.2 FM vs PM: The Frequency Response
Because PM's instantaneous frequency depends on the derivative, higher frequency messages cause a more violent frequency swing.

![FM vs PM Frequency Response](file:///mnt/Data/3-2/datacom%20antigravity/diagrams/fm_pm_freq_response.png)

**Practical Consequence**: FM is better for analog audio because human voices have more power at lower frequencies. PM is superior for digital data (PSK, QAM) because discrete bit transitions provide sharp derivatives.

---

## PART 5: SIGNAL GENERATION (ENCODERS)

Because FM requires integration and PM requires differentiation, their circuits are closely related.
-   **To make FM**: Integrate the message, then feed it to a Phase Modulator.
-   **To make PM**: Differentiate the message, then feed it to a Frequency Modulator (like a VCO).

![Encoders](file:///mnt/Data/3-2/datacom%20antigravity/diagrams/fm_pm_encoders.png)

---

## PART 6: PHASE WRAPPING AMBIGUITY

A major challenge with Phase Modulation is that phase is periodic ($2\pi$). 
If your message causes a phase swing of $3\pi$, the receiver sees it as $\pi$ (because $3\pi \mod 2\pi = \pi$). 
The receiver loses track of how many full rotations occurred. 
-   **Solution**: Differential coding (encode data in phase *changes* rather than absolute phase) or using Phase-Locked Loops (PLLs) to track continuous phase.

---

## PART 7: POWER ANALYSIS

**The greatest trick of Angle Modulation:**
$$P_{total} = \frac{V_C^2}{2R}$$

The power is **100% constant**. It doesn't matter what $\beta$ is, or what the message is doing. All the modulation index does is take the carrier's power and distribute it among the sidebands. 
In AM, transmitting louder audio requires physically more wattage from the power supply. In FM, transmitting louder audio just spreads the existing wattage wider across the frequency spectrum.

---

## PART 8: WORKED EXAMPLES

### Example 1: Standard FM Radio
**Given**: Carrier $f_c = 100$ MHz, $V_C = 10$V. Message $f_m = 15$ kHz (max audio), $A_m = 1$V. Frequency sensitivity $k_F = 75$ kHz/V.
**Find**: $\Delta f$, $\beta$, Bandwidth, and Power in $50\Omega$.

1.  **Deviation**: $\Delta f = k_F \cdot A_m = 75 \times 1 = \mathbf{75 \text{ kHz}}$ (This is the max allowed in commercial FM).
2.  **Modulation Index**: $\beta = \Delta f / f_m = 75 / 15 = \mathbf{5}$ (Wideband FM).
3.  **Bandwidth (Carson)**: $BW = 2(75 + 15) = \mathbf{180 \text{ kHz}}$. (Channels are spaced 200 kHz apart in the real world).
4.  **Power**: $P = (10^2) / (2 \times 50) = \mathbf{1 \text{ Watt}}$. Constant.

### Example 2: Interpreting an Equation
**Given**: $Y(t) = 5 \cos(2\pi \cdot 10^6 t + 4 \sin(2000\pi t))$ Volts.
**Identify**: Is it FM or PM? What is $\beta$? What is the bandwidth?

1.  We can't technically know if it's FM or PM just by looking at it (since an integrated cosine is a sine). Let's assume standard FM form.
2.  $\beta = \mathbf{4}$ (The coefficient of the inner sine wave).
3.  $f_m = 2000\pi / 2\pi = \mathbf{1000 \text{ Hz}}$.
4.  $\Delta f = \beta \cdot f_m = 4 \times 1000 = \mathbf{4000 \text{ Hz}}$.
5.  $BW = 2(4000 + 1000) = \mathbf{10 \text{ kHz}}$.

---

## PART 9: REAL WORLD SYSTEMS

1.  **FM Radio Broadcasting (88 - 108 MHz)**: Uses Wideband FM ($\beta = 5$). Trades massive bandwidth (200 kHz per channel) for crystal-clear, noise-free audio.
2.  **Police / Fire Two-Way Radios**: Uses Narrowband FM (NBFM). $\beta \approx 1$. Bandwidth is only 12-15 kHz. Audio quality is worse, but it fits far more channels into the spectrum while keeping the constant-amplitude amplifier efficiency.
3.  **Wi-Fi / 5G**: Uses digital variants of Phase Modulation (PSK, QAM).

---

## PART 10: SYNTHESIS SUMMARY

| Feature | Frequency Modulation (FM) | Phase Modulation (PM) |
| :--- | :--- | :--- |
| **Angle Equation $\theta(t)$**| $\omega_c t + 2\pi k_F \int m(t) dt$ | $\omega_c t + k_P m(t)$ |
| **Instantaneous Freq** | $\omega_c + 2\pi k_F m(t)$ | $\omega_c + k_P \frac{dm(t)}{dt}$ |
| **Modulation Index $\beta$**| $\frac{k_F A_m}{f_m}$ (Decreases with $f_m$) | $k_P A_m$ (Constant) |
| **Primary Use** | Analog Audio Broadcasting | Deep Space, Digital Comms |

---

> **Next Note**: [[07 - ASK and FSK]] — Taking these analog concepts into the digital domain.
