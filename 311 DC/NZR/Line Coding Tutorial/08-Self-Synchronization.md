# Self-Synchronization

**Self-synchronization** is the ability of a signal to carry its own **timing information**, allowing the receiver to extract a clock signal without a separate synchronization channel.

## The Core Problem: Clock Recovery

The receiver must know:
1. **When each bit starts** (bit boundary)
2. **When each bit ends** (next bit boundary)

```
Transmitter side:
Bit stream:     1    0    1    1    0    0    0    1
                |    |    |    |    |    |    |    |
+V |            ___      ___  __   __         ___
   |           |   |    |   ||  | |  |       |
0  |___________|___|____|___|__|_|__|_______|_|____
   |
-V |

Transmitter has a clock (shown as tick marks above)
Transmitter knows exactly when each bit period starts and ends.

Receiver side:
What arrives:    +V-V-V+V+V-V-V-V-V+V (a noisy, unsynchronized signal)
                  ?
Receiver must answer: When does each bit period start?
```

## The Synchronization Challenge

### Problem: No Self-Synchronization

```
Without built-in timing, the receiver must:
1. Assume a clock frequency (guess?)
2. Hope the phase aligns with the transmitter
3. As time passes, the two clocks drift (all oscillators drift!)
4. Eventually, the receiver is off by a full bit period
5. All subsequent bits are decoded incorrectly

Example with Unipolar NRZ and long 0s:
Bit stream:     0    0    0    0    0    0    0    0
                |    |    |    |    |    |    |    |
+V |
   |
0  |_____________________________
   |
-V |

For 8 bit periods, voltage = 0V (constant).

Receiver sees: A flat line. No transitions to indicate bit boundaries.
Receiver's clock drifts. By the time the next symbol (1) arrives,
the receiver is 0.5 bit periods off → misses the entire transition.
```

### Solution: Self-Synchronization

Embed **timing information** in the signal itself. Use signal **transitions** as the timing reference.

**Key insight:** Every time the signal transitions (changes voltage), it provides a "tick" for the receiver's clock to synchronize to.

## How Self-Synchronization Works

A self-synchronizing code ensures:

$$\text{Signal transitions occur frequently and regularly}$$

The receiver extracts the clock by:
1. Detecting edges (transitions) in the received signal
2. Locking a Phase-Locked Loop (PLL) to these edges
3. Using the recovered clock to sample the signal at the right moments

```mermaid
graph LR
    A["Received Signal<br/>(with transitions)"] --> B["Edge Detection"]
    B --> C["Phase-Locked Loop<br/>PLL"]
    C --> D["Recovered Clock"]
    D --> E["Sampling at<br/>Correct Times"]
    E --> F["Decoded Bits"]
    
    style A fill:#e1f5ff
    style D fill:#fff3e0
    style F fill:#c8e6c9
```

## Schemes with Self-Synchronization

### Manchester Coding (★ Best for Exam)

**Rule:** Every bit has exactly one transition

```
Bit 0: +V → -V (transition at middle of bit period)
Bit 1: -V → +V (transition at middle of bit period)

Bit stream: 0   1   0   1
            |   |   |   |
+V |    _       _
   |   | |     | |
0  |_  | |_   | |_____
   |   |_|   |_|
-V |

Minimum transition: One per bit period
Maximum run without transition: 0.5 bit periods

Receiver sees transitions at: 0.5T_b, T_b, 1.5T_b, 2T_b, 2.5T_b, ...
Clock easily recovers from these edges.
```

**Advantage:** Guaranteed transition every single bit → perfect self-sync

### Differential Manchester

**Rule:** 
- Start of each bit: Always transition
- Middle of bit: Transition if bit = 0, no transition if bit = 1 (or vice versa)

```
Bit 0: Transition at start AND middle
Bit 1: Transition at start, no transition at middle

Bit stream: 0    1    0    1
            |    |    |    |
+V |    _       _
   |   | |     | |
0  |_  | |_   | |_____
   |   |_|   |_|
-V |

Minimum transition: One per 0.5 bit periods (at bit boundaries)
Better synchronization than regular Manchester.
```

**Advantage:** Even more transitions; immunity to inversion

### Bipolar (AMI) – Partial Self-Sync

**Rule:** 
- Bit 0 → 0V (no transition within the bit)
- Bit 1 → alternating +V and -V (-V, +V, -V, +V, ... for consecutive 1s)

```
Bit stream: 1   1   1   0   0   1
            |   |   |   |   |   |
+V |     ___     ___
   |    |   \   |   \
0  |____|___|___| ___
   |        |   |_|   |
-V |                 ___

Transitions occur between consecutive 1s.
But long runs of 0s have NO transitions.
```

**Problem:** Not truly self-synchronizing (long 0-runs break sync)

**Solution:** Combine with scrambling (B8ZS, HDB3) to break up 0-runs.

## Quantifying Self-Synchronization

A useful metric is the **maximum time between transitions** (or equivalently, **maximum run length** MRL):

| Scheme | Max Time Between Transitions | Self-Sync? |
|--------|------------------------------|-----------|
| **Manchester** | 0.5 × T_b | ✅ Excellent |
| **Diff. Manchester** | 0.5 × T_b | ✅ Excellent |
| **Polar RZ** | 0.5 × T_b | ✅ Good (mid-bit return) |
| **AMI (with B8ZS)** | ~2 × T_b | ✅ Moderate |
| **Unipolar NRZ** | Unlimited | ❌ Poor |
| **Polar NRZ** | Unlimited | ❌ Poor |

**Rule:** If max time between transitions > 2-3 × T_b, self-synchronization becomes difficult.

## Why Transitions Matter: PLL Behavior

The receiver uses a Phase-Locked Loop (PLL) to track the transmitter's clock:

```
PLL behavior:

1. Sees a transition (edge) in the signal
2. Adjusts its internal oscillator to align with the edge
3. "Locks" to that frequency
4. Continues running until the next edge
5. If the next edge occurs soon, fine-tunes the phase
6. If the next edge is delayed, PLL drifts

Example with Manchester (good):
Signal edges:  |--|--|--|--|--|--|--|--| (frequent, regular)
PLL locks easily, drifts minimally

Example with Unipolar NRZ of 0 0 0 0:
Signal edges:  |         (then long silence)
PLL loses lock, drifts, phase error grows
```

## Practical Snapshot: Compare Two Scenarios

### Scenario A: Unipolar NRZ with Data Pattern `10110000`

```
Bit:        1    0    1    1    0    0    0    0
            |    |    |    |    |    |    |    |
+V  |  ___     ___  __
    | |   |   |   ||  |
0   |_|___|___|___|__|_____________
    |
-V  |

Transitions occur at: T_b, 2T_b, 3T_b, 4T_b (then silence)
For the next 4 bit periods (from 4T_b to 8T_b), NO transitions.
PLL loses track of phase.
When the first bit after the 0-run arrives, the receiver may sample at the wrong time.

Result: Bit errors after long 0-runs
```

### Scenario B: Manchester with Same Data `10110000`

```
Bit:        1    0    1    1    0    0    0    0
            |    |    |    |    |    |    |    |
+V  |    _      _
    |   | |    | |
0   |__ | |__ | |___
    |   |_|   |_|
-V  |

Transitions occur at: 0.5T_b, T_b, 1.5T_b, 2T_b, 2.5T_b, 3T_b, 3.5T_b, 4T_b,
                      4.5T_b, 5T_b, 5.5T_b, 6T_b, 6.5T_b, 7T_b, 7.5T_b, 8T_b

(every 0.5 bit periods, without fail)

PLL sees constant stream of edges. Stays locked. Phase remains accurate.
When sampling time arrives, receiver always samples at the correct moment.

Result: No bit errors due to synchronization issues ✓
```

## Examining the Problem Deeply

**Why does Manchester have a built-in transition?**

Because the **encoding rule itself forces it**:

- **Bit 0:** Always goes from +V to -V during the bit period → 1 transition
- **Bit 1:** Always goes from -V to +V during the bit period → 1 transition

There's **no way** to encode a Manchester bit without a transition. The code is designed such that the signal *must* change.

By contrast, Unipolar NRZ:
- **Bit 0:** Always stays at 0V → 0 transitions
- **Bit 1:** Always stays at +V → 0 transitions

The signal can remain constant for arbitrarily long periods.

## Self-Synchronization vs. Other Criteria

Self-synchronization affects:
- ✅ Clock recovery at the receiver
- ✅ Robustness to phase drift
- ✅ Tolerance for oscillator drift
- ✓ (Partially) baseline wandering

Self-synchronization does NOT directly affect:
- ❌ Bandwidth (though schemes with frequent transitions may have wider bandwidth)
- ❌ DC component (though forced transitions help with DC)
- ❌ Noise immunity (though it helps indirectly)

## Design Trade-offs

To achieve self-synchronization:
- **Forced transitions (Manchester):** High bandwidth cost, but excellent sync
- **Limited run length (4B/5B):** Small bandwidth cost, good sync, redundancy overhead
- **Scrambling (B8ZS):** Minimal bandwidth cost, targeted fixing of problem patterns

## Exam Checklist

✓ Understand why synchronization is needed (receiver must know bit boundaries)
✓ Understand how transitions provide timing information
✓ Know which schemes are self-synchronizing (Manchester, Diff. Manchester, block codes with run-length limits)
✓ Know which schemes are NOT (Unipolar, basic Polar)
✓ Be able to analyze a bit pattern and determine if sync is maintained
✓ Understand the trade-off: More transitions = Better sync, but usually higher bandwidth

## Related Concepts

- [[01-Digital-Signal-Fundamentals|Digital Signal Fundamentals]] — Synchronization need
- [[06-Baseline-Wandering|Baseline Wandering]] — Related (baseline drift without sync)
- [[14-Manchester-Coding|Manchester Coding]] — Premier self-synchronizing scheme
- [[15-Differential-Manchester|Differential Manchester]] — Improved variant
- [[22-Block-Coding|Block Coding]] — Self-sync via run-length limits
- [[26-B8ZS-HDB3|B8ZS and HDB3]] — Scrambling maintains run-length limits
