# Manchester Coding

Manchester coding is the **gold standard** for self-synchronizing line codes. It's used in Ethernet, legacy token ring, and many industrial standards. Master this thoroughly — it's guaranteed on your exam.

## Definition

**Manchester encoding rule (IEEE 802.3 standard):**
- Bit 1 → Transition from -V to +V at the middle of the bit period
  - First half: -V
  - Second half: +V
  
- Bit 0 → Transition from +V to -V at the middle of the bit period
  - First half: +V
  - Second half: -V

**Key insight:** Every bit has exactly one transition in the middle. The direction of the transition encodes the bit value.

## Example: Encoding the Bit Stream `10110001`

Bit stream: 1 0 1 1 0 0 0 1

![[../manchester_10110001.png]]

## Signal Properties

| Property | Value |
|----------|-------|
| **Voltage levels** | 2 (-V and +V, symmetric) |
| **r factor** | 1 |
| **Signal rate (baud)** | = Bit rate (one symbol per bit) |
| **Bandwidth** | ~= 2 × Bit rate (due to mid-bit transitions) |
| **Transitions per bit** | Exactly 1 (guaranteed) |
| **Transitions per second** | 2 × Bit rate (minimum frequency) |
| **DC component** | Always 0V (perfectly balanced) |
| **Self-synchronization** | Excellent (transition every 0.5 T_b) |
| **Typical use** | Ethernet 10Base-T, 10Base-2, 10Base-5 |

## Critical Advantage: Built-in Synchronization

**Why Manchester is self-synchronizing:**

The encoding rule **forces** a transition in the middle of every bit period. There's no way to encode a Manchester bit without a transition.

Scenario: Long run of 1s

Bit sequence: 1 1 1 1 1 1 1 1

![[../manchester_long_ones.png]]

Transitions occur at every 0.5 bit period, without exception.
Receiver's PLL (Phase-Locked Loop) sees constant stream of edges.
Clock stays perfectly synchronized, regardless of data pattern.
No baseline wandering. No synchronization failure.

**Comparison to Polar NRZ-L:**

// Text diagrams removed; see above for waveform images and below for summary table.

## DC Component: Always Zero

**Proof:**

In each bit period $T_b$:
- First half ($T_b/2$): Voltage = either +V or -V
- Second half ($T_b/2$): Voltage = the opposite level

Over one complete bit period:
$$V_{DC} = \frac{1}{T_b} \left[ \frac{T_b}{2} \times (\text{level}_1) + \frac{T_b}{2} \times (\text{level}_2) \right]$$

where level_1 and level_2 are opposite: one is +V, one is -V.

$$V_{DC} = \frac{1}{T_b} \left[ \frac{T_b}{2} \times V + \frac{T_b}{2} \times (-V) \right] = \frac{1}{T_b} \times 0 = 0$$

**Guarantee:** No matter what the bit pattern is, Manchester always has DC = 0V. This is a major advantage over Polar NRZ-L.

## Bandwidth: Double the Basic NRZ

**Why is Manchester's bandwidth higher?**

The built-in mid-bit transitions increase the frequency content:

// Text diagrams removed; see table and images for visual reference.

**Trade-off:**
- **Advantage:** Perfect synchronization
- **Cost:** Requires 2× the bandwidth

For most channels, this trade-off is worthwhile.

## Encoding Algorithm

```
Algorithm: Manchester_Encode(bitstream, voltage_level_V)
  for each bit in bitstream:
    if bit == 1:
      output voltage = -V for duration T_b/2
      output voltage = +V for duration T_b/2
    else:
      output voltage = +V for duration T_b/2
      output voltage = -V for duration T_b/2
    
    // Net effect: always have one transition at T_b/2
```

## Decoding Algorithm

```
Algorithm: Manchester_Decode(received_signal)
  for each bit period T_b:
    // Sample at two points: beginning and middle
    sample_start = signal at T_b/4
    sample_mid = signal at 3T_b/4
    
    if (sample_start < 0) and (sample_mid > 0):
      // -V to +V transition (upward)
      output bit = 1
    else if (sample_start > 0) and (sample_mid < 0):
      // +V to -V transition (downward)
      output bit = 0
    else:
      // Error: no transition detected (corrupted signal)
      flag_error()
```

**Advantage of this decoder:** The transition itself carries the information. Clock recovery is inherent in detecting the transition.

## Actual Snapshot: Ethernet 10Base-T

```
Ethernet uses Manchester coding on twisted pair wires.

Link speed: 10 Mbps

Encoded bit rate: 20 Mbaud (20 million symbols per second)

Why 20 Mbaud? Because each bit contains one transition,
and transitions occur every 0.5 bit period.

Bandwidth needed: ~20 MHz

Physical layer:
- Twisted pair can handle ~10-20 MHz bandwidth (legacy)
- Manchester fits with room to spare
- Self-synchronization allows simple phase-locked loop
- No baseline wandering issues
- Perfect for office environments
```

## Comparison: Manchester vs. Alternatives

| Aspect | Manchester | Polar NRZ-L | Unipolar NRZ |
|--------|-----------|------------|-------------|
| Transitions per bit | 1 (guaranteed) | 0-1 (depends) | 0-1 (depends) |
| Self-sync? | Excellent ✓ | Poor ✗ | Poor ✗ |
| DC-free? | Always ✓ | Balanced only | Never ✗ |
| Bandwidth | 2× baseline | 1× baseline | 1× baseline |
| AC-coupled OK? | Yes ✓ | Yes* | No ✗ |
| Sync on long runs? | Perfect | Fails | Fails |

*Polar NRZ-L is AC-OK only if data is balanced.

## Exam-Critical Practice

**Q1:** Encode "1010" in Manchester and sketch the waveform.

**A1:**
1: -V then +V
0: +V then -V
1: -V then +V
0: +V then -V


![[../manchester_1010.png]]

*Note: The above image shows the Manchester encoded waveform for the bit stream '1010', with each bit's transition clearly visible at the midpoint of the bit period.*

Transitions at: 0.5T_b, T_b, 1.5T_b, 2T_b, 2.5T_b, 3T_b, 3.5T_b, 4T_b (every 0.5 bit period)

**Q2:** A channel has 1 MHz bandwidth. What bit rate can Manchester support?

**A2:**
Manchester requires BW ≈ 2 × bit_rate.
So: 1 MHz = 2 × bit_rate
bit_rate = 500 kbps

**Q3:** Why is Manchester suitable for AC-coupled channels while Polar NRZ-L isn't always?

**A3:**
- Polar NRZ-L has zero DC only if data is balanced (50% 0s, 50% 1s)
- Random data may have unequal 0s and 1s, creating DC offset
- Manchester always has zero DC, regardless of data pattern
- For AC-coupled channels that block DC, Manchester is always safe

## Historical Note: Why "Manchester"?

The coding scheme was invented at Manchester University (UK) in the 1960s. The naming is purely geographic, not descriptive!

## Key Insight for Design

Manchester's brilliant insight is to **move the clock information into the signal itself** by encoding it as transitions. This solves the synchronization problem at the cost of bandwidth.

Many modern codes (Differential Manchester, NRZI, 8B/10B) follow similar philosophies.

## Related Concepts

- [[02-Line-Coding-Basics|Line Coding Basics]] — Why encoding is needed
- [[08-Self-Synchronization|Self-Synchronization]] — Detailed theory of sync
- [[07-DC-Component|DC Component]] — Why DC-free is valuable
- [[15-Differential-Manchester|Differential Manchester]] — Enhanced variant
- [[27-Comparison-Matrix|Comparison Matrix]] — How it ranks among all schemes
- [[29-Exam-Strategy|Exam Strategy]] — Manchester appears on almost every exam
