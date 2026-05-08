# Unipolar NRZ (Non-Return-to-Zero)

Unipolar NRZ is the **simplest** line code. It's also the **worst** for real channels. Understanding why it fails teaches you why good line codes are necessary.

## Definition

**Unipolar NRZ encoding rule:**
- Bit 0 → Voltage = 0 V (for the entire bit period)
- Bit 1 → Voltage = +V (for the entire bit period)

**"Non-Return-to-Zero"** means: Once the signal reaches a voltage level, it stays there for the entire bit period. It doesn't return to zero mid-bit.

## Example: Encoding the Bit Stream `10110001`

```
Bit stream:     1    0    1    1    0    0    0    1
                |    |    |    |    |    |    |    |


Observations:
- Bit 1: +V for one bit period
- Bit 0: 0V for one bit period
- Transitions only occur when the bit pattern changes (1→0 or 0→1)
- Long runs of the same bit have NO transitions
```
![[note_10.png]]

## Signal Properties

| Property | Value |
|----------|-------|
| **Voltage levels** | 2 (0V and +V) |
| **r factor** | 1 |
| **Signal rate** | = Bit rate |
| **Bandwidth** | ~= Bit rate |
| **DC component** | Depends on data; ranges from 0V (if 0s = 1s) to +V (if all 1s) |
| **Self-synchronization** | Poor (no forced transitions) |
| **Implementation** | Very simple |

## Detailed Analysis

### Voltage Levels: Limited to Non-Negative

Notice: The signal uses only **0V and +V**, never goes negative.

This is called **unipolar** because both levels are on the same side of zero (both ≥ 0V).

**Consequence:** Unlike bipolar codes, there's no symmetry. The signal is "biased" towards positive voltage.

### DC Component: Data-Dependent

For a bit sequence with $N_1$ ones and $N_0$ zeros (total $N = N_1 + N_0$):

$$V_{DC} = \frac{N_1 \times V + N_0 \times 0}{N} = \frac{N_1}{N} \times V$$

**Examples:**
- All 1s: $V_{DC} = V$ (maximum)
- All 0s: $V_{DC} = 0$ (minimum)
- Equal 0s and 1s: $V_{DC} = V/2$ (middle)
- Random data (statistically): $V_{DC} \approx V/2$

**Problem:** A non-zero DC component makes the signal unsuitable for AC-coupled channels (which block DC). The receiver sees reduced amplitude.

```
Example: Data with more 1s than 0s (e.g., "1111000")
DC = 4V / 7 ≈ 0.57V (positive offset)

In an AC-coupled receiver:
Original:    +V at time t → DC level = 0.57V
Received:    (+V - 0.57V) = 0.43V (reduced amplitude!)

Signal-to-noise ratio (SNR) degrades.
```

### Baseline Wandering: Critical Issue

Long runs of the same bit cause **baseline wandering** (discussed in [[06-Baseline-Wandering|Baseline Wandering]]):

```
Scenario: 10 consecutive 0s

Bit stream:  0 0 0 0 0 0 0 0 0 0
             |_________________|

Voltage:
+V  |
    |
 0  |____________________________
    |
-V  |

For 10T_b, the voltage is constant at 0V.

In an AC-coupled receiver:
- The coupling capacitor "sees" a constant voltage
- Capacitor charges/discharges, reducing output amplitude
- Receiver's baseline reference drifts
- When the next 1 arrives, the receiver may not recognize it
- Synchronization fails
```

### Self-Synchronization: Non-Existent

There are NO guaranteed transitions. Transitions depend entirely on the data:

- Data `10101010` (alternating): Many transitions, receiver stays synchronized ✓
- Data `11110000` (long runs): Few transitions, receiver loses sync ✗
- Data `00000000` (all zeros): Zero transitions, receiver completely lost ✗✗

**Real systems can't rely on the data being alternating.** So Unipolar NRZ is fundamentally unreliable for synchronization.

## Frequency Spectrum

In signal processing, every signal (like your Unipolar NRZ waveform) can be thought of as a combination of sine waves at different frequencies. Each frequency "component" has an **amplitude** (how tall the wave is) and contributes to the signal's overall energy.

"Power" at a frequency means the **energy contribution** from that specific frequency component. It's calculated as the amplitude squared (since power = voltage²/resistance, but simplified here).

- **High power** at a frequency: That frequency is a big part of the signal—lots of energy there. The signal "uses" that frequency strongly.
- **Low/no power**: That frequency contributes little or nothing; the signal ignores it.

For example:
- In Unipolar NRZ, **0 Hz (DC)** has power because the signal has a constant average voltage (offset), like a flat line. This is a 0 Hz sine wave with amplitude.
- Higher frequencies have power from transitions (bit changes), like ripples on the signal.

The spectrum plot shows this distribution: peaks mean strong frequencies, flat areas mean weak ones. In the Unipolar NRZ plot, power starts high at DC and drops, meaning the signal is mostly "slow-changing" (low freq), which is bad for AC channels that filter out low freq/DC. If a frequency has zero power, it's not in the signal at all.

The frequency content of unipolar NRZ depends on the data pattern:

```
Random data spectrum:
              ↑ Power
              | ___
              ||   \___
              ||       \___
              ||           \___
       DC→   ||_______________\____→ Frequency
        0Hz       |   |
                Bit rate

Most energy between 0 (DC) and about 2× bit rate.

Key observation: 
- DC component (0 Hz) carries power
- AC-coupled channels block this DC
- Signal is weakened
```
![[note_10_spectrum.png]]
For alternating data:
- Most energy at the bit rate frequency (one transition per bit period)
- Minimal DC component

For bursty data (long runs):
- Significant DC component
- Energy concentrated at very low frequencies (< bit rate / 10)
- Hard for AC-coupled channels to pass

## Advantages

✓ **Extremely simple** — easiest to implement  
✓ **Minimal circuitry** — just assign voltage levels  
✓ **For DC-coupled channels** — works fine if channel allows DC

## Disadvantages

❌ **DC component** — unsuitable for AC-coupled channels (the standard)  
❌ **No self-sync** — receiver can't maintain clock from the signal alone  
❌ **Baseline wandering** — loses synchronization on long runs  
❌ **Spectrum occupies DC** — wasted power at 0 Hz  

## Real-World: Where Unipolar NRZ is Used

**Almost nowhere in modern systems.** It's a theoretical baseline and teaching tool.

Rare exceptions:
- **Fiber-optic to free-space optical:** Direct intensity modulation (fiber 0→off, 1→on light)
- **LED/light pulses:** Simple on/off encoding
- **Simple digital logic tests:** Laboratory equipment with DC-coupled signals

## Comparison to Other Schemes

See [[27-Comparison-Matrix|Comparison Matrix]] for systematic comparison.

Quick preview:

| Aspect | Unipolar NRZ | Polar NRZ-L | Manchester |
|--------|-------------|------------|-----------|
| Levels | 2 (0, +V) | 2 (-V, +V) | 2 (-V, +V) |
| DC-free? | No | Yes* | Yes |
| Self-sync? | No | No | Yes |
| Bandwidth | 1× | 1× | 2× |
| Practical use | Rare | Common | Ethernet |

*Polar NRZ-L is DC-free only for balanced data.

## Design Question: How Would You Fix Unipolar NRZ?

To make it suitable for AC-coupled channels:

1. **Use both voltage levels (polar instead of unipolar)** → Reduces/eliminates DC
   - Example: Polar NRZ-L
   
2. **Ensure frequent transitions** → Maintains synchronization
   - Example: Manchester, RZ
   
3. **Limit long runs** → Combination of both benefits
   - Example: Block codes (4B/5B), Scrambling (B8ZS)

All of these approaches are explored in later notes.

## Encoding/Decoding Algorithm

### Encoding (Bit → Voltage)

```
Algorithm: Unipolar_NRZ_Encode(bitstream, voltage_level_V)
  for each bit in bitstream:
    if bit == 1:
      output voltage = V
    else:
      output voltage = 0
    hold voltage for duration T_b
```

### Decoding (Voltage → Bit)

```
Algorithm: Unipolar_NRZ_Decode(received_signal, threshold)
  threshold = V / 2  (midpoint)
  for each bit period T_b:
    sample_voltage = signal at T_b/2 (mid-point of bit)
    if sample_voltage >= threshold:
      output bit = 1
    else:
      output bit = 0
```

**Problem with decoding:** Determining the correct threshold is hard if DC offset is unknown!

## Exam Tip

Unipolar NRZ frequently appears on exams as:
1. A **baseline for comparison** — "NRZ requires X bandwidth, Manchester requires 2X"
2. A **negative example** — "Why is Unipolar NRZ unsuitable? Answer: DC component and no sync"
3. A **calculation exercise** — "Given a bitstream, encode it in Unipolar NRZ and sketch the waveform"

**For exams:** Know it well enough to critique it, not well enough to use it in practice!

## Related Concepts

- [[01-Digital-Signal-Fundamentals|Digital Signal Fundamentals]] — Voltage levels and bit periods
- [[02-Line-Coding-Basics|Line Coding Basics]] — The problem it embodies
- [[03-Data-Elements-vs-Signal-Elements|Data Elements vs. Signal Elements]] — r = 1 example
- [[06-Baseline-Wandering|Baseline Wandering]] — Why it fails on long runs
- [[07-DC-Component|DC Component]] — Why it's unsuitable for AC channels
- [[08-Self-Synchronization|Self-Synchronization]] — Why it has poor sync
- [[11-Polar-NRZ-L|Polar NRZ-L]] — An immediate improvement
- [[13-Polar-RZ|Polar RZ]] — Another improvement
