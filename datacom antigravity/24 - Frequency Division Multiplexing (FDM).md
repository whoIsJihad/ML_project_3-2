# Frequency Division Multiplexing (FDM)

> **Prerequisites**: [[03 - Amplitude Modulation (AM)]], [[11 - Bandwidth and Spectral Efficiency]]

---

## What Problem Does FDM Solve?

A single physical channel (like a coax cable, fiber optic, or the open air) has a massive amount of available bandwidth. A single message (like a voice call) only takes up a tiny fraction of that bandwidth (e.g., 4 kHz).

If we only sent one signal per cable, we would waste 99% of the cable's capacity. 
**Frequency Division Multiplexing (FDM)** solves this by stacking multiple, separate signals into different frequency "slots" and sending them all simultaneously over the exact same medium.

> **Real-world analogy**: Radio broadcasting. The air is the medium. 90.1 FM, 92.5 FM, and 101.3 FM are all transmitted at the exact same time through the same air. Your car radio uses a bandpass filter to "tune in" to just one frequency slot at a time.

---

## How It Works (The Process)

![FDM Spectrum](/mnt/Data/3-2/datacom antigravity/diagrams/fdm_spectrum.png)

### 1. Multiplexing (At the Transmitter)
1. You have $N$ different baseband signals (e.g., $m_1(t), m_2(t), m_3(t)$), all occupying the same low-frequency band (e.g., 0-4 kHz).
2. Each signal is passed into its own modulator.
3. Each modulator uses a **different carrier frequency** ($f_1, f_2, f_3$). 
   - $m_1(t)$ is shifted to $f_1$
   - $m_2(t)$ is shifted to $f_2$
   - $m_3(t)$ is shifted to $f_3$
4. The spacing between $f_1, f_2, f_3$ must be wide enough so the modulated signals' bandwidths do not overlap.
5. All the modulated signals are added together into one massive composite signal and transmitted.

### 2. Guard Bands
Real-world filters are not perfect brick walls. If we stack channels perfectly back-to-back, a filter trying to extract Ch1 might accidentally let in some of Ch2 (this is called **Crosstalk**).
To prevent this, we insert **Guard Bands** — empty, unused frequency space between adjacent channels.

$$BW_{Total} = N \times BW_{channel} + (N-1) \times BW_{guard}$$

### 3. Demultiplexing (At the Receiver)
1. The receiver gets the massive composite signal.
2. It uses a bank of parallel **Bandpass Filters (BPF)**.
3. BPF 1 is tuned to $f_1$, extracting only the first modulated signal.
4. BPF 2 is tuned to $f_2$, etc.
5. Each isolated signal is then sent to its own demodulator to recover the original baseband messages $m_1, m_2, m_3$.

---

## SSB in FDM
Because FDM stacks signals, bandwidth is precious. For this reason, **Single Sideband (SSB)** modulation was historically the standard for analog telephone networks using FDM. By using SSB, telecom companies could pack exactly twice as many phone calls into a single transatlantic cable compared to standard AM or DSB.

---

## Summary
- **Dimension**: Divides the frequency spectrum.
- **Requirement**: Orthogonal (non-overlapping) frequency bands.
- **Limitation**: Crosstalk if filters are poor; requires guard bands which waste some spectrum.
