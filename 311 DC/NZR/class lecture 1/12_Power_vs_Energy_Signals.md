# 12. Power Signals vs. Energy Signals

In signal processing, signals are classified as either **power signals** or **energy signals** based on their behavior over an infinite time duration. This classification helps in using the correct mathematical tools for their analysis.

The classification depends on two key metrics:
1.  **Signal Energy ($E$):** The total energy dissipated by the signal over all time.
2.  **Signal Power ($P$):** The average power of the signal over all time.

A signal will be one of these two types; it cannot be both.

---

### 1. Energy Signal

An **energy signal** is a signal with **finite total energy**. For this to be true, the signal's amplitude must approach zero as time approaches infinity. These are typically signals that are time-limited or decay over time.

*   **Conditions:**
    *   Total Energy is finite: $0 < E < \infty$
    *   Average Power is zero: $P = 0$ (Because the finite energy is averaged over an infinite time).
*   **Conceptual Model:** A burst, a pulse, a transient event. It has a beginning and an end, and its influence is contained within a finite duration.
*   **Relevance:** Most real-world data communication signals are modeled as energy signals.
    *   A single data packet.
    *   A radar pulse.
    *   A human utterance.
    *   A flash of light.

---

### 2. Power Signal

A **power signal** is a signal with **infinite total energy** but a **finite average power**. These are signals that go on forever without their amplitude decaying to zero.

*   **Conditions:**
    *   Total Energy is infinite: $E = \infty$
    *   Average Power is finite and non-zero: $0 < P < \infty$
*   **Conceptual Model:** A persistent, ongoing, never-ending signal that has a steady intensity.
*   **Relevance:** Periodic signals are the classic example of power signals.
    *   An ideal sine wave or cosine wave that exists for all time.
    *   The carrier wave in a radio or TV broadcast system.
    *   A DC voltage source that is always on.

---

### Summary Table

| Property         | Energy Signal                    | Power Signal                     |
| ---------------- | -------------------------------- | -------------------------------- |
| **Total Energy** | Finite ($0 < E < \infty$)      | Infinite ($E = \infty$)          |
| **Avg. Power**   | Zero ($P=0$)                     | Finite ($0 < P < \infty$)        |
| **Duration**     | Typically time-limited or decaying | Typically persistent or periodic   |
| **Example**      | A single data packet             | A continuous sine wave (carrier) |

This distinction is crucial for theoretical analysis. For example, when analyzing the spectral content of an energy signal, we use the **Energy Spectral Density (ESD)**. For a power signal, we use the **Power Spectral Density (PSD)**.

### Next : [[13_Signal_Energy_and_Power_Formulas]]