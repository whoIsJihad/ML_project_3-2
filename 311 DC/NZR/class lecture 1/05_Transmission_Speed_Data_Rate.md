# 5. Transmission Speed (Data Rate)

**Transmission Speed**, more commonly known as **Data Rate** (or Bit Rate), refers to the number of bits of information that are transmitted across a communication channel per second. Its unit is **bits per second (bps)**, often scaled up to kilobits per second (kbps), megabits per second (Mbps), and so on.

It's crucial to differentiate data rate from bandwidth:
*   **Bandwidth** (measured in Hertz) refers to the *range of frequencies* a channel can carry – the "width" of the communication highway.
*   **Data Rate** (measured in bps) refers to the *amount of information* that can be sent over that highway in a given time – how many "cars" (bits) can pass in a second.

A wider bandwidth generally *enables* a higher data rate, but they are distinct concepts. The actual achievable data rate depends on several factors, including bandwidth, the number of signal levels used, and the amount of noise present in the channel.

Two fundamental theorems establish the theoretical limits of data rate for a given channel:

---

### 1. Nyquist Bit Rate: The Limit for a NOISELESS Channel

Developed by Harry Nyquist, this formula defines the maximum bit rate achievable over a perfect, noiseless channel. It primarily addresses **intersymbol interference**, ensuring that symbols sent too rapidly don't bleed into one another.

*   **Concept:** For a given bandwidth, there's a maximum rate at which distinct symbols can be sent without them becoming indistinguishable. This maximum symbol rate is $2 \cdot B$. The total bit rate then scales with how many bits each unique symbol can represent.
*   **Formula:**
    $$
    \text{BitRate} = 2 \cdot B \cdot \log_2(L)
    $$
    Where:
    *   `B` is the channel bandwidth in Hertz (Hz).
    *   `L` is the number of discrete signal levels (or symbols) used to encode data.
*   **Explanation:**
    *   If a signal uses `L` distinct voltage levels (e.g., different amplitudes), each level can represent $\log_2(L)$ bits. For example, if `L=2` (two levels, like `0` and `1`), then $\log_2(2) = 1$ bit per level. If `L=4` (four levels), then $\log_2(4) = 2$ bits per level.
    *   This theorem suggests that to increase the bit rate in a noiseless scenario, one can either increase the channel's bandwidth or increase the number of distinct signal levels used.

---

### 2. Shannon Capacity: The Ultimate Limit for a NOISY Channel

Claude Shannon's groundbreaking work provides the theoretical maximum error-free data rate for a channel that *does* experience noise – a much more realistic scenario. This limit is known as the **Shannon Capacity**.

*   **Concept:** Shannon's theorem states that for a channel with a given bandwidth and a certain amount of noise, there is an absolute maximum rate at which information can be transmitted reliably (i.e., with an arbitrarily small error rate). No matter how sophisticated the encoding or modulation scheme, this limit cannot be surpassed.
*   **Formula:**
    $$
    C = B \cdot \log_2(1 + \text{SNR})
    $$
    Where:
    *   `C` is the channel capacity in bits per second (bps).
    *   `B` is the channel bandwidth in Hertz (Hz).
    *   `SNR` is the Signal-to-Noise Ratio, expressed as a linear power ratio (not in decibels). This is calculated as `Signal Power / Noise Power`.
*   **Implication:** This formula reveals that the fundamental resources limiting the speed of communication are the channel's **bandwidth** and the **quality of the signal relative to the noise**. To increase capacity, you must either expand the bandwidth or improve the SNR (e.g., by increasing signal power or reducing noise). Shannon's formula implicitly accounts for the fact that in a noisy channel, trying to squeeze too many signal levels (as suggested by Nyquist) will make them indistinguishable, leading to errors.

In real-world systems, achieved data rates are always below the theoretical Shannon Capacity due to practical limitations, but the formula provides an invaluable benchmark and design target.

### Next : [[06_Signal_to_Noise_Ratio_SNR]]