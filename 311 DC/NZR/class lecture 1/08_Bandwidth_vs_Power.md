# 8. Relationship Between Bandwidth and Power

In communication systems, **bandwidth** and **signal power** are the two primary, finite resources that engineers must manage to achieve a target data rate and reliability. The Shannon Capacity formula ($C = B \cdot \log_2(1 + \text{SNR})$) mathematically codifies their relationship.

This relationship is fundamentally a **trade-off**: to achieve a certain channel capacity (C), you can use:
*   A large amount of bandwidth (high `B`) with low signal power (which results in a low `SNR`).
*   A small amount of bandwidth (low `B`) with high signal power (to achieve a high `SNR`).

### 1. The Role of Bandwidth

Bandwidth ($B$) is the range of frequencies the channel can support. As seen in the Shannon formula, capacity is **linearly proportional** to bandwidth.

*   **Effect:** Doubling the bandwidth roughly doubles the maximum theoretical data rate.
*   **Use Case:** This is exploited in systems where bandwidth is plentiful. For example, **Ultra-Wideband (UWB)** communication uses an enormous bandwidth (e.g., > 500 MHz) to transmit data at high speeds using very low power, minimizing interference with other systems.

### 2. The Role of Power

Signal Power ($P_s$) is not directly in the Shannon formula, but it is the key component of the Signal-to-Noise Ratio ($\text{SNR} = P_s / P_n$). Increasing signal power increases the SNR. Capacity is **logarithmically proportional** to SNR.

*   **Effect:** Doubling the signal power does *not* double the capacity due to the $\log_2$ relationship. There are diminishing returns. A power increase from 1W to 2W has a much larger impact on capacity than an increase from 100W to 101W.
*   **Use Case:** This is critical in power-limited systems like satellites or mobile phones. Engineers must use the available power as efficiently as possible. It's also why systems in noisy environments (low SNR) require more power to maintain a clear connection.

### 3. The Trade-Off in Practice

Consider two scenarios aiming for the same data rate:

*   **Scenario A: Deep Space Probe:**
    *   **Constraint:** Extremely limited power due to solar panels and distance.
    *   **Resource:** Relatively large, dedicated bandwidth allocated by regulatory bodies.
    *   **Strategy:** Use a very wide bandwidth (`B` is large) to compensate for the very low SNR caused by a weak signal arriving at Earth.

*   **Scenario B: DSL Internet over Telephone Lines:**
    *   **Constraint:** Extremely limited bandwidth (~1 MHz) due to the physical properties of old copper wires.
    *   **Resource:** Abundant power available from the wall outlet.
    *   **Strategy:** Use sophisticated modulation techniques that pump a high amount of power into the signal, creating a very high SNR to maximize the capacity ($C$) within the narrow bandwidth ($B$).

In summary, every communication system operates at some point on this bandwidth-power spectrum, balancing the availability of one resource against the scarcity of the other to meet design goals for speed and reliability.

### Next : [[11_Periodic_vs_Aperiodic_Signals]]