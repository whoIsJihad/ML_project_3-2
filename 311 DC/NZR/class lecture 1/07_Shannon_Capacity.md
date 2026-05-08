# 7. Shannon Capacity

The **Shannon-Hartley Theorem**, commonly known as **Shannon Capacity**, is a cornerstone of information theory. It defines the absolute, unbreakable upper limit on the rate at which information can be transmitted over a communication channel of a specified bandwidth in the presence of noise.

### 1. The Core Idea

Claude Shannon proved that for a given real-world channel (which always has some noise), there is a maximum rate of error-free communication.
*   **Below this rate:** It is theoretically possible to achieve error-free communication by using sufficiently advanced error-correction coding techniques.
*   **Above this rate:** Reliable (error-free) communication is impossible, regardless of the sophistication of the encoding scheme or the number of signal levels used.

The Shannon Capacity ($C$) gives us the "speed limit" of a communication channel.

### 2. The Formula

The formula is a concise and powerful expression of the factors that limit communication speed:

$$
C = B \cdot \log_2(1 + \text{SNR})
$$

Where:
*   `C` is the **channel capacity** in bits per second (bps). This is the theoretical maximum data rate.
*   `B` is the **channel bandwidth** in Hertz (Hz).
*   `SNR` is the **Signal-to-Noise Ratio**, which must be expressed as a linear power ratio (e.g., Signal Power / Noise Power), not in decibels (dB).

### 3. Implications of the Formula

The Shannon Capacity formula reveals the two fundamental resources we can leverage to increase the data rate of a channel:

1.  **Bandwidth (B):** The capacity is directly proportional to the bandwidth. If you double the bandwidth, you can potentially double the maximum data rate (all else being equal). This is why technologies like fiber optics (with enormous bandwidth) can achieve such high speeds compared to old telephone wires (with very narrow bandwidth).

2.  **Signal Power / Noise (SNR):** The capacity increases with the logarithm of the SNR. This means increasing signal power (or decreasing noise) increases the maximum data rate. However, the logarithmic relationship shows diminishing returns: doubling the signal power does *not* double the capacity. The first increases in power yield significant gains, but subsequent increases provide progressively smaller benefits.

Shannon's work tells us that bandwidth and power (relative to noise) are the ultimate currencies of communication. You can trade one for the other to achieve a desired performance level. For example, a low-power system (like a space probe) can still achieve a reasonable data rate if it uses a large amount of bandwidth. Conversely, a system with very limited bandwidth (like a telephone line) can increase its data rate by boosting the signal power to improve its SNR.

### Next : [[08_Bandwidth_vs_Power]]