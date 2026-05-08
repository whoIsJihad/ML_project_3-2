# 6. Signal-to-Noise Ratio (SNR)

**Signal-to-Noise Ratio (SNR)** is one of the most important metrics in communications, quantifying the quality of a signal. It measures the level of a desired signal's power relative to the level of background noise.

### 1. The Concept of SNR

Every communication channel is affected by noise—random, unwanted electrical energy that degrades the signal. SNR tells us exactly how much stronger our signal is than this noise.

*   A **high SNR** means the signal is clean and easily distinguishable from the noise. This leads to reliable communication with a low error rate.
*   A **low SNR** means the noise is strong relative to the signal, making it difficult for the receiver to extract the original information. This causes a high number of errors.

### 2. SNR as a Linear Ratio

In its most direct form, SNR is the ratio of signal power ($P_s$) to noise power ($P_n$). 

$$ 
\text{SNR}_{\text{linear}} = \frac{\text{Power}_{\text{signal}}}{\text{Power}_{\text{noise}}} = \frac{P_s}{P_n} 
$$ 

An SNR of 100 means the signal is 100 times more powerful than the noise. An SNR of 1 means the signal and noise have equal power.

### 3. The Decibel (dB) Scale

Because the linear SNR can span an enormous range of values (from less than 1 to many millions), it is more commonly expressed on a logarithmic scale in **decibels (dB)**. This makes the numbers more manageable and is often more intuitive in signal analysis.

*   **Formula:**
    $$ 
    \text{SNR}_{\text{dB}} = 10 \cdot \log_{10}\left(\frac{P_s}{P_n}\right) = 10 \cdot \log_{10}(\text{SNR}_{\text{linear}}) 
    $$ 
*   **Key Benchmarks:**
    *   If $P_s = P_n$, then $\text{SNR}_{\text{linear}} = 1$, and $\text{SNR}_{\text{dB}} = 10 \cdot \log_{10}(1) = \mathbf{0} \text{ dB}$. (Signal and noise are equal).
    *   If $P_s$ is 10 times $P_n$, then $\text{SNR}_{\text{linear}} = 10$, and $\text{SNR}_{\text{dB}} = 10 \cdot \log_{10}(10) = \mathbf{10} \text{ dB}$.
    *   If $P_s$ is 100 times $P_n$, then $\text{SNR}_{\text{linear}} = 100$, and $\text{SNR}_{\text{dB}} = 10 \cdot \log_{10}(100) = \mathbf{20} \text{ dB}$.

### 4. Impact on Data Rate

As established by the **Shannon Capacity formula**, SNR is a fundamental limiter of a channel's maximum data rate.

$$ C = B \cdot \log_2(1 + \text{SNR}) $$ 

A higher SNR allows a receiver to distinguish between more finely-grained signal levels, which in turn enables more bits to be encoded per symbol, leading directly to a higher achievable data rate. If SNR is very low, the channel capacity drops dramatically, regardless of the available bandwidth.

### Next : [[07_Shannon_Capacity]]