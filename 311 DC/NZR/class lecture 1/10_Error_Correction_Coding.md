# 10. Error Detection and Correction Coding (Channel Coding)

While source coding (compression) aims to *remove* redundancy to save space, **channel coding** does the opposite: it intelligently *adds* structured redundancy to a signal. This added information, called **parity bits** or **check bits**, allows the receiver to detect and, in some cases, correct errors that occur during transmission due to channel noise.

### 1. The Core Problem: Errors

When a digital signal (a stream of 1s and 0s) is transmitted over a noisy channel, some bits can be flipped (a 1 becomes a 0, or vice versa). This corrupts the data. Channel coding provides a way to make the data stream more robust and resilient to this noise.

### 2. Error Detection

Error detection codes allow the receiver to determine *if* an error has occurred. If an error is detected, the receiver typically requests a retransmission of the data. This is common in reliable protocols like TCP.

*   **Simple Parity Check:** The simplest form. A single parity bit is added to a block of data. For "even parity," the parity bit is set to 1 or 0 to ensure the total number of 1s in the block (including the parity bit) is even. If the receiver gets a block with an odd number of 1s, it knows an error occurred.
    *   *Limitation:* Cannot detect an even number of bit errors (e.g., two bits flipping).
*   **Cyclic Redundancy Check (CRC):** A much more powerful and common technique used in Ethernet, Wi-Fi, and many other protocols. It performs a polynomial division on the data block and uses the remainder as the "checksum." The receiver performs the same calculation. If the remainders don't match, an error is detected. CRC can detect a wide variety of common error patterns.

### 3. Error Correction

Error correction codes (also known as Forward Error Correction or FEC) are more advanced. They contain enough redundant information for the receiver to not only detect an error but also to identify which bit(s) flipped and correct them on the spot, without needing a retransmission.

*   **When to Use:** Essential for systems where retransmission is not feasible or would introduce unacceptable delay.
    *   **Real-time streaming** (VoIP, video conferencing)
    *   **Deep-space communications** (retransmission would take hours)
    *   **Data storage media** (CDs, DVDs, SSDs, where "retransmitting" isn't possible)
*   **Examples:**
    *   **Hamming Codes:** An early and elegant family of codes that can correct single-bit errors.
    *   **Reed-Solomon Codes:** Very powerful codes that work on blocks of bits (symbols). They are excellent at correcting "burst errors" (a sequence of consecutive bit errors). Used extensively in QR codes, CDs, and DVDs.
    *   **Convolutional Codes:** Operate on the data stream serially, bit by bit. Often used in conjunction with algorithms like the Viterbi decoder.
    *   **Turbo Codes & LDPC (Low-Density Parity-Check) Codes:** State-of-the-art codes that can achieve performance very close to the theoretical Shannon Limit. They are used in all modern high-speed communication standards, including 4G/5G, Wi-Fi (802.11n and later), and satellite communications.