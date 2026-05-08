# Phase Locked Loop (PLL)

> **Prerequisites**: [[04 - Frequency Modulation (FM)]], [[20 - DSB-SC Modulation]]

---

## What Problem Does a PLL Solve?

For synchronous demodulation (used in DSB-SC, SSB, and digital schemes like QAM/PSK), the receiver needs a local oscillator that matches the transmitter's carrier **perfectly** in both frequency and phase.
If the frequency drifts by even 1 Hz, or the phase shifts, the demodulated signal is corrupted.

A **Phase Locked Loop (PLL)** is an automatic control system (a feedback loop) that adjusts a local oscillator to perfectly track the phase and frequency of an incoming signal. 

Additionally, PLLs are the standard mechanism for **demodulating FM signals**.

---

## The Three Core Components

![PLL Tracking](/mnt/Data/3-2/datacom antigravity/diagrams/pll_tracking.png)

A PLL is a classic negative feedback loop consisting of three blocks:

### 1. Phase Detector (PD) / Multiplier
- **Inputs**: The received signal (e.g., $A \sin(\omega_c t + \theta_{in})$) and the local oscillator signal (e.g., $B \cos(\omega_c t + \theta_{out})$).
- **Operation**: It multiplies them together. Mathematically, multiplying a sine and cosine yields sum and difference frequencies:
  - High frequency term: $\sin(2\omega_c t + ...)$
  - Low frequency term: $\sin(\theta_{in} - \theta_{out})$
- **Output**: An error voltage proportional to the phase difference $\Delta\theta$ between the two inputs.

### 2. Loop Filter (Low Pass Filter)
- Takes the raw output of the Phase Detector.
- Blocks the high-frequency term ($2\omega_c$).
- Smooths out the error voltage into a clean DC (or slowly varying) control voltage $v_c(t)$.
- **Critical role**: Determines the dynamic response of the loop (how fast it locks, how well it rejects noise).

### 3. Voltage Controlled Oscillator (VCO)
- An oscillator whose frequency is controlled by an input voltage.
- When $v_c(t) = 0$, it outputs its "free-running" center frequency.
- When $v_c(t)$ is positive or negative, it shifts its frequency up or down proportionally.
- The output of the VCO is fed back into the Phase Detector.

---

## How It Works (The Loop in Action)

1. **Free-running**: Initially, the VCO generates a frequency close to, but not exactly matching, the incoming signal.
2. **Error Generation**: The Phase Detector compares them and generates an error voltage.
3. **Correction**: The Loop Filter smooths this voltage and feeds it to the VCO.
4. **Locking**: The voltage forces the VCO to speed up or slow down until its phase *exactly* matches the incoming signal.
5. **Locked State**: Once locked, $\theta_{in} \approx \theta_{out}$, the error voltage stabilizes, and the VCO tracks the incoming signal continuously.

---

## Applications

### 1. Synchronous Carrier Recovery
Used in DSB-SC/SSB/QAM receivers. A small "pilot carrier" is transmitted alongside the data. The receiver's PLL locks onto this pilot, creating a flawless local carrier for coherent demodulation.

### 2. FM Demodulation
This is the most brilliant use of a PLL.
- The incoming signal is Frequency Modulated (its frequency swings up and down based on the audio message).
- The PLL locks onto this incoming signal.
- For the VCO to perfectly track the swinging frequency of the FM signal, the control voltage $v_c(t)$ entering the VCO *must* be swinging up and down in the exact same pattern!
- Therefore, **the control voltage $v_c(t)$ IS the demodulated audio message**. You just tap the wire between the filter and the VCO, and you have your audio.
