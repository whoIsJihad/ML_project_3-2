# Polar NRZ-L (Polar Non-Return-to-Zero, Level Encoding)

Polar NRZ-L is a simple but significant improvement over Unipolar NRZ. It addresses the DC component problem by using **both positive and negative voltage levels**.

## Definition

**Polar NRZ-L encoding rule (standard convention):**
- Bit 1 → Voltage = +V (for the entire bit period)
- Bit 0 → Voltage = -V (for the entire bit period)

The terms "NRZ" and "L" mean:
- **NRZ (Non-Return-to-Zero):** Voltage stays constant throughout the bit period
- **L (Level):** Bit value is encoded by the voltage *level*, not transitions

## Example: Encoding the Bit Stream `10110001`

Bit stream: 1 0 1 1 0 0 0 1

![[note_11.png]]

## Signal Properties

| Property | Value |
|----------|-------|
| **Voltage levels** | 2 (-V and +V, symmetric) |
| **r factor** | 1 |
| **Signal rate** | = Bit rate |
| **Bandwidth** | ~= Bit rate |
| **DC component** | 0V for balanced data (equal 0s and 1s); non-zero otherwise |
| **Self-synchronization** | Poor (transitions depend on data pattern) |
| **Implementation** | Simple |
| **Typical use** | Magnetic disk recording, satellite transmission |

## Advantages over Unipolar NRZ

### 1. DC-Free (for Balanced Data)

For a bit stream with equal number of 1s and 0s:
$$V_{DC} = \frac{N_1 \times V + N_0 \times (-V)}{N_1 + N_0} = \frac{(N_1 - N_0) V}{N_1 + N_0}$$

If $N_1 = N_0$ (balanced data):
$$V_{DC} = 0$$

**Advantage:** No DC component means:
- Signal is more suitable for AC-coupled channels
- Power is not wasted on DC
- Baseline doesn't drift as much

**Limitation:** Only works if data is statistically balanced. Random data or intentional patterns might have unequal 0s and 1s, causing non-zero DC.

### 2. Symmetric Voltage Levels

```
Unipolar:     0V  ─────────────  +V
              (asymmetric)

Polar:   -V  ─────────────  0  ─────────────  +V
         (symmetric, centered at 0V)
```

**Consequence:** Signal is naturally "balanced" around zero voltage, making it suitable for transformers and AC coupling.

## Disadvantages: Still Poor Synchronization

Long runs of the same bit create synchronization problems:

Scenario: Bit sequence "11110000"

![[note_11_disadvantages.png]]

For 4 bit periods: voltage = +V (constant)
For next 4 bit periods: voltage = -V (constant)

Only 1 transition in 8 bit periods!

Receiver's Phase-Locked Loop (PLL) tries to lock to transitions,
but with such long constant periods, it drifts.
By the time the next 1 arrives, phase error has accumulated.

**Conclusion:** Polar NRZ-L is NOT self-synchronizing. It still suffers from baseline wandering on long runs.

## DC Component: Detailed Analysis

### Case 1: Balanced Data (N_1 = N_0)

Example: "1010"

![[note_11_dc1.png]]

Average = (2V - 2V) / 4 = 0V

DC-free ✓

### Case 2: Unbalanced Data (More 1s than 0s)

Example: "1111000"

![[note_11_dc2.png]]

Count: 4 ones (+V) and 3 zeros (-V)
Average = (4V - 3V) / 7 = V/7 ≈ 0.143V

Not DC-free ✗

### Case 3: Worst Case (All 1s or All 0s)

Example: "1111111"

![[note_11_dc3.png]]

All ones: Average = V (maximum positive DC)
All zeros: Average = -V (maximum negative DC)

DC-free? No ✗

**Practical Solution:** In real systems, either:
1. **Assume data is random** and average to ~0V (works with probability)
2. **Use scrambling** to randomize the bit pattern (done in protocols)
3. **Use block codes** that guarantee balance (4B/5B, 8B/10B)
4. **Pre-code the data** before encoding (differential encoding)

## Frequency Spectrum

The spectrum depends on the data pattern (like Unipolar):

```
For balanced random data:
- Minimal DC component (0 Hz)
- Energy centered around bit_rate / 2
- Suitable for AC-coupled channels

For unbalanced data:
- Non-zero DC component
- Lower frequency components emphasized
- Potential issues with AC coupling
```
![[note_11_spectrum.png]]

## Relationship to [[12-Polar-NRZ-I|Polar NRZ-I]]

**Polar NRZ-I** is a variant that uses **differential encoding** instead of level encoding:
- Transition present → 1
- No transition → 0 (or vice versa)

Polar NRZ-I addresses some clock recovery challenges but still isn't self-synchronizing.

## Encoding Algorithm

```
Algorithm: Polar_NRZ_L_Encode(bitstream, voltage_level_V)
  for each bit in bitstream:
    if bit == 1:
      output voltage = +V
    else:
      output voltage = -V
    hold voltage for duration T_b
```

## Decoding Algorithm

```
Algorithm: Polar_NRZ_L_Decode(received_signal)
  threshold = 0V (midpoint)
  for each bit period T_b:
    sample_voltage = signal at T_b/2 (mid-point of bit)
    if sample_voltage >= threshold:
      output bit = 1
    else:
      output bit = 0
```

**Advantage over Unipolar decoding:** Threshold is fixed at 0V (the true midpoint), not guessed or estimated.

## Practical Use Cases

### Magnetic Disk Recording

```
Hard drives store data in magnetic domains:
- Magnetic domain pointing "up" → Bit 1 (+V)
- Magnetic domain pointing "down" → Bit 0 (-V)

Why Polar NRZ-L works here:
- Symmetric levels (natural for magnetic domains)
- Simple to implement
- No AC coupling needed (direct magnetic sensing)
```

### Satellite Communication

```
Modulation schemes often use:
- Signal phase = +90° → Bit 1
- Signal phase = -90° → Bit 0

This is conceptually similar to Polar NRZ-L.
Symmetric levels provide balanced power transmission.
```

## Comparison: Unipolar vs. Polar NRZ-L

```
Aspect                | Unipolar NRZ | Polar NRZ-L
----------------------|--------------|------------
Voltage levels        | 0V, +V       | -V, +V
DC component          | High (≥0)    | Low (if balanced)
Suitable for AC?      | No           | Yes*
Self-sync?            | No           | No
Bandwidth             | ~1× bit rate | ~1× bit rate
Implementation        | Simplest     | Simple
Real-world use        | Rare         | Moderate

*Only for balanced data
```

## Exam-Typical Questions

**Q1:** Encode the bitstream "110010" in Polar NRZ-L and sketch the waveform.

**A1:**
1: +V
1: +V
0: -V
0: -V
1: +V
0: -V

![[note_11_exam.png]]

**Q2:** Calculate the DC component for "111000".

**A2:**
- 3 ones at +V, 3 zeros at -V
- DC = (3V - 3V) / 6 = 0V (balanced!)

**Q3:** Why is Polar NRZ-L better than Unipolar for AC-coupled channels?

**A3:**
- Unipolar has DC component between 0V and +V (data-dependent)
- AC coupling attenuates DC and low frequencies
- Polar NRZ-L has zero DC (for balanced data), so less attenuation
- Received signal amplitude is closer to transmitted amplitude

## Related Concepts

- [[10-Unipolar-NRZ|Unipolar NRZ]] — Predecessor (lacks symmetric levels)
- [[12-Polar-NRZ-I|Polar NRZ-I]] — Variant using differential encoding
- [[13-Polar-RZ|Polar RZ]] — Another variant with mid-bit return
- [[07-DC-Component|DC Component]] — Why DC-free matters
- [[06-Baseline-Wandering|Baseline Wandering]] — Why transitions matter
- [[27-Comparison-Matrix|Comparison Matrix]] — How it compares to other schemes
