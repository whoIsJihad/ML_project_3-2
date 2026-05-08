# Digital Signal Fundamentals

Before understanding line coding, you must be precise about what constitutes a "digital signal."

## Definition: What is a Digital Signal?

A **digital signal** is a physical representation of discrete data (typically binary: 0s and 1s) using **voltage levels** that change over time at specific **time intervals**.

Key distinction:
- **Data (logical level):** The abstract bit: 0 or 1
- **Signal (physical level):** The actual voltage on a wire at a specific time

A digital signal is a time-domain function:
$$s(t) = \text{voltage level at time } t$$

## Voltage Levels: The Physical Foundation

In most digital systems, two voltage levels represent the two logical states:

| Logical State | Voltage Level | Common Example |
|---------------|--------------|-----------------|
| 0 (space) | Lower voltage | 0 V (or -V) |
| 1 (mark) | Higher voltage | +V (or +5 V) |

**Example:** In RS-232 (serial communication):
- Logic 1 (mark): -3 to -15 V
- Logic 0 (space): +3 to +15 V

**Important:** The *choice* of voltage levels depends on the channel, the equipment, and historical standards. The line coding scheme determines how bits map to these levels.

## The Bit Interval (Bit Period)

A **bit** occupies a fixed time duration called the **bit interval** or **bit period**:
$$T_b = \frac{1}{f_b}$$

where:
- $T_b$ = bit interval (seconds)
- $f_b$ = bit rate (bits per second, bps)

**Example:** If the bit rate is 1000 bps, then:
$$T_b = \frac{1}{1000} = 1 \text{ ms}$$

Each bit "lives" for exactly 1 ms.

## Signal Transitions and Edges

Within each bit interval, the voltage can:

1. **Stay constant** (level encoding) — the voltage represents the entire bit
2. **Transition** (transition encoding) — the change in voltage carries information
3. **Return to baseline** (return-to-zero) — a mid-bit change brings the signal back

```
Constant Level (NRZ):
+V |     ___________       ___________
   |    |           |     |
 0 |____|___________|_____|___________|____
   |                       
-V |                         
    t=0  T_b  2T_b  3T_b  4T_b

Transition at Midpoint (RZ):
+V |     ___     ___
   |    |   |   |   |
 0 |____|   |___|   |___
   |
-V |
    t=0  T_b  2T_b  3T_b  4T_b
```

## Signal Elements vs. The Signal

A **signal element** is a voltage waveform that occupies a specific time interval. The "shape" of this waveform is determined by the **line coding scheme**.

**Example:** In Manchester coding (discussed later), each data bit is represented by a signal element that always contains a transition — but the *direction* of the transition indicates the bit value.

## Frequency Content (Bandwidth)

Any signal with voltage transitions contains frequency components. The **frequency content** (or **spectrum**) of a digital signal is crucial because:

1. **Different channels have bandwidth limits** — you can't send a 1 MHz signal over a twisted pair rated for 100 kHz
2. **AC-coupled channels can't send DC** — low-frequency components (nearly constant voltage) are attenuated
3. **The choice of line code affects the bandwidth** — this is why some schemes are more efficient than others

**Intuition:** Faster transitions (sharper edges) = higher frequency content = wider bandwidth needed.

A transition from 0 V to +V in time $\Delta t$ requires frequencies up to roughly $\frac{1}{\Delta t}$.

## Synchronization Problem (Preview)

The receiver must know:
1. **When each bit starts and ends** (clock synchronization)
2. **What the baseline voltage is** (especially if the signal drifts)

If the signal has long periods of constant voltage (like many 0s or 1s in a row), the receiver can "lose sync" because there are no transitions to lock onto.

**This is the core motivation for line coding schemes** — to ensure transitions occur frequently enough to maintain synchronization.

## Related Concepts

- [[02-Line-Coding-Basics|Line Coding Basics]] — How we solve these synchronization and bandwidth problems
- [[03-Data-Elements-vs-Signal-Elements|Data Elements vs. Signal Elements]] — Formal terminology
- [[05-Data-Rate-and-Signal-Rate|Data Rate and Signal Rate]] — Relating bit rate to bandwidth
