# Engineering Note: Binary Pulse Code Modulation (PCM)

## 1. Definition
Binary PCM is a digital modulation technique where an analog message signal is represented by a sequence of coded binary pulses (1s and 0s). Unlike analog pulse modulations (PAM, PWM), PCM is discrete in both **time** and **amplitude**.

## 2. The Three-Step Transformation Process
To convert an analog signal $m(t)$ into a binary stream, it must pass through three distinct stages:

### A. Sampling (Discrete in Time)
* **Action:** The signal is measured at uniform intervals $T_s$.
* **Constraint:** To avoid **aliasing**, we must follow the Nyquist Criterion ($f_s \ge 2B$), where $B$ is the signal bandwidth.
* **Output:** A Pulse Amplitude Modulated (PAM) signal.

### B. Quantization (Discrete in Amplitude)
* **Action:** The infinite range of analog amplitudes is rounded (mapped) to the nearest of $L$ discrete levels.
* **Step Size ($\Delta V$):** $\Delta V = \frac{2m_p}{L}$, where $m_p$ is the peak amplitude.
* **Error:** This rounding introduces "Quantization Noise," which can only be reduced by increasing the number of levels ($L$).

### C. Binary Encoding (Digital Representation)
* **Action:** Each of the $L$ quantized levels is assigned a unique **$n$-bit binary code**.
* **Relationship:** $L = 2^n$ (e.g., 8 bits provide 256 distinct levels).
* **Output:** A high-speed serial bitstream of 0s and 1s.

## 3. Key Performance Metrics
As a 3rd-year student, these are the calculations you'll likely see in your CTs:

* **Bit Rate ($R_b$):** The speed of the digital signal.
  $$R_b = n \times f_s \text{ bits/sec}$$
* **Transmission Bandwidth ($B_T$):** The minimum channel width required.
  $$B_T \ge \frac{R_b}{2} = nB$$
* **Signal-to-Noise Ratio (SNR):**

  $$SNR_{\mathrm{dB}} \approx 6.02n + 1.76 \, \mathrm{dB}$$
  *Every extra bit added to the code word improves the signal quality by roughly **6 dB**.*

## 4. Advantages & Trade-offs
| Feature | Benefit |
| :--- | :--- |
| **Noise Immunity** | Digital pulses can be perfectly reconstructed using Regenerative Repeaters, even if distorted by channel noise. |
| **Multiplexing** | Multiple binary PCM signals (like different phone calls) can be easily combined using Time Division Multiplexing (TDM). |
| **Bandwidth Penalty** | The main downside is that PCM requires significantly more bandwidth ($n$ times more) than the original analog signal. |