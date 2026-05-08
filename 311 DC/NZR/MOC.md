# Map of Content: Principles of Digital Communications

This document provides a centralized overview of all topics for the Digital Communications course (CSE 311).

---

### [[class lecture 1/MOC|Lecture 1: Introduction to Digital Communications]]
This lecture introduces the fundamental concepts of signals and the building blocks of a digital communication system.
- Signal Types (Continuous, Discrete, Analog, Digital)
- Analog-to-Digital Conversion Overview
- Bandwidth and Data Rate
- Signal-to-Noise Ratio (SNR) and Shannon Capacity
- Signal Properties (Periodicity, Power, Energy)

---

### [[class lecture 2,3/MOC|Lectures 2 & 3: Fourier Analysis]]
These lectures cover the mathematical tools used to analyze signals in the frequency domain.
- The Unit Impulse and Unit Step Functions
- **Fourier Series** (for periodic signals)
- **The Fourier Transform** (for aperiodic signals)
- Properties of the Fourier Transform (e.g., Duality)
- Existence Conditions

---

### Lecture 4: LTI Systems and Filtering
This lecture explores Linear Time-Invariant (LTI) systems, which are fundamental to signal processing and filtering.
- [[class lecture 4/Part One|LTI System Properties, Impulse Response, and Convolution]]
- [[class lecture 4/Part two|Ideal Lowpass, Highpass, and Bandpass Filters]]
- [[class lecture 4/Sampling theory|The Sampling Theorem and Signal Reconstruction]]

---

### [[class lecture 5/MOC|Lecture 5: Pulse Code Modulation (PCM)]]
This lecture details the most common method for digitizing an analog signal.
- The complete PCM System (Transmitter & Receiver)
- Uniform Quantization and Quantization Noise
- Signal-to-Noise Ratio in PCM
- Non-Uniform Quantization and Companding (μ-Law, A-Law)
- The 6-dB Rule

---

### [[class lecture 6,7/MOC|Lectures 6 & 7: Differential Pulse Code Modulation (DPCM)]]
These lectures cover a more efficient encoding scheme that exploits signal correlation.
- DPCM System Overview
- Linear Predictors and Prediction Error
- SNR Gains in DPCM

---

### [[class lecture 8/MOC|Lecture 8: Delta Modulation (DM)]]
This lecture presents a simplified, 1-bit version of DPCM.
- Delta Modulation System and Staircase Approximation
- Slope Overload Distortion
- Granular Noise
- Adaptive Delta Modulation (ADM)
