# Mathematical Analysis: SNR Improvement of DPCM over PCM

According to your class notes (specifically Pages 6, 8, and 9), Differential Pulse Code Modulation (DPCM) improves the Signal-to-Noise Ratio (SNR) by exploiting the high correlation between consecutive samples to reduce the power of the signal being quantized.

## 1. The Core Principle: Reducing the Peak Amplitude ($m_p \rightarrow d_p$)
In standard PCM, the quantizer must handle the full dynamic range of the message signal $m(t)$, defined by its peak amplitude **$m_p$**. In DPCM, only the **prediction error** $d[k]$ is quantized.

* **Message Signal Peak:** $m_p$ (Large)
* **Difference Signal Peak:** $d_p = \text{Peak of } [m(k) - \hat{m}(k)]$ (Small)

Because adjacent samples are highly correlated, the difference between them is much smaller than the absolute values: **$d_p \ll m_p$**.

## 2. Quantization Step Size ($\Delta V$) Comparison
The quantization step size ($\Delta V$) is directly proportional to the peak amplitude of the signal entering the quantizer.

* **PCM Step Size:** $\Delta V_m = \frac{2 m_p}{L}$
* **DPCM Step Size:** $\Delta V_d = \frac{2 d_p}{L}$

For the same number of levels ($L$), the DPCM step size is significantly smaller: **$\Delta V_d < \Delta V_m$**.

## 3. Noise Power ($N_o$) Reduction
Quantization noise power is determined by the square of the step size:
$$N_o = \frac{(\Delta V)^2}{12}$$

Since $\Delta V_d < \Delta V_m$, the **Noise Power in DPCM is much lower** than in PCM ($N_{o, DPCM} < N_{o, PCM}$).

## 4. Resulting SNR Improvement
The SNR is defined as the ratio of signal power to noise power:
$$SNR = \frac{S_o}{N_o}$$

By keeping the signal power ($S_o$) constant but drastically reducing the noise power ($N_o$), DPCM achieves a higher SNR than PCM using the same number of bits. 

> **Note from Page 6:** Your notes explicitly state that DPCM is a solution to PCM's inefficiency because it allows for a "step size reduction" without increasing the bit rate.