# Bipolar Line Coding (AMI and Pseudoternary)

Bipolar line coding is a clever **three-level** encoding scheme that improves upon Polar NRZ-L by enforcing **alternating voltage patterns**. The most common variant is **AMI (Alternate Mark Inversion)**, which is widely used in telecommunications.

## Overview: Why Bipolar?

Traditional two-level codes (like Polar NRZ-L) suffer from:
1. **DC component drift** when data is unbalanced
2. **Poor synchronization** on long runs of identical bits
3. **Baseline wandering** in AC-coupled channels

Bipolar coding solves these by using **three voltage levels** (-V, 0, +V) with an **alternating rule**: consecutive 1s must alternate between +V and -V.

## Definition: AMI (Alternate Mark Inversion)

**AMI encoding rule:**
- Bit 0 → Voltage = 0 V (for the entire bit period)
- Bit 1 → Alternates between +V and -V with each successive 1
  - First 1 → +V
  - Next 1 → -V
  - Next 1 → +V
  - And so on...

**Key principle:** Mark (1) inversion ensures no two consecutive 1s have the same polarity.

## Example: Encoding the Bit Stream `10110001`

![[images/note_ami_example.png]]

*(Figure: AMI encoding for `10110001` — 1s alternate polarity)*

**Observations:**
- All 0s produce 0V (no voltage)
- 1s alternate: +V, -V, +V, -V, ... (never repeats same polarity)
- Signal naturally oscillates, helping synchronization
- DC component is naturally balanced (equal +V and -V occurrences)

## Signal Properties

| Property | Value |
|----------|-------|
| **Voltage levels** | 3 (-V, 0, +V) |
| **r factor** | 1 |
| **Signal rate** | = Bit rate |
| **Bandwidth** | ~= Bit rate (same as Polar NRZ) |
| **DC component** | Always 0V (perfectly balanced) |
| **Self-synchronization** | Good (due to alternating pattern) |
| **Implementation** | Requires memory (must track last 1's polarity) |
| **Typical use** | T-carrier systems (T1, T2, T3), Digital subscriber line (DSL), ISDN |

## Advantages of AMI

### 1. Zero DC Component (Always)

Unlike Polar NRZ-L which requires balanced data, AMI **always produces zero DC** regardless of data pattern:

$$V_{DC} = \frac{N_{+V} \times V + N_{0} \times 0 + N_{-V} \times (-V)}{N_{+V} + N_0 + N_{-V}}$$

Since the alternating rule ensures $N_{+V} = N_{-V}$ (equal number of +V and -V):
$$V_{DC} = \frac{N_{+V} \times V - N_{+V} \times V}{N_{total}} = 0 \, \text{always}$$

**Benefit:** Perfect for AC-coupled channels. No baseline wandering, no power wasted on DC.

### 2. Built-in Error Detection

Because of the alternating rule, **consecutive 1s can never have the same polarity**. This provides a form of error detection:

- If the receiver detects two consecutive +V or two consecutive -V (from 1 bits), an error must have occurred
- Simple hardware can detect violations without complex algorithms

### 3. Reduced Synchronization Problems

The alternating pattern provides transitions regularly:

- Every 1 bit produces a level change (±V or back to 0V)
- Even for long runs of 0s (which produce no level change), the previous 1's alternation provides timing reference

Example: Sequence "1111"
```
Bit:      1   1   1   1
Voltage:  +V  -V  +V  -V
Transitions at: every bit boundary
```

This is much better than Polar NRZ-L where four consecutive 1s produce no transitions.

## Disadvantages

### 1. Three Voltage Levels Required

- More complex receiver circuitry (must distinguish three levels, not just two)
- More susceptible to noise (smaller spacing between levels means lower noise margin)
- Requires more stable power supply

### 2. Long Runs of Zeros Still Problematic

If many consecutive 0s occur (like "0000000000"), no transitions happen:

```
Bit stream:     0    0    0    0    0    0    0    0
Voltage:        0V   0V   0V   0V   0V   0V   0V   0V
No transitions ─────────────────────────────────────
```

Even though alternating rule helps with 1s, zeros don't contribute to synchronization.

**Partial solution:** Use block codes (like HDB3) that prevent long runs of zeros by inserting special patterns.

### 3. More Complex to Encode/Decode

Must maintain **state** (memory):
- "Which polarity should the next 1 have?"
- Requires a counter or flip-flop, not just combinational logic

## Comparison: AMI vs. Other Schemes

| Feature | Unipolar NRZ | Polar NRZ-L | **AMI** | Manchester |
|---------|--------------|-------------|---------|------------|
| **Levels** | 2 (0, +V) | 2 (-V, +V) | **3** | 2 |
| **DC component** | Large | Balanced data only | **Always 0** | Always 0 |
| **Synchronization** | Poor | Poor | **Good** | Excellent |
| **Bandwidth** | ~1× | ~1× | **~1×** | ~2× |
| **Error detection** | No | No | **Yes** | No |
| **Complexity** | Simplest | Simple | **Medium** | Higher |
| **Real-world use** | Historical | Disks | **Telecom** | Ethernet |

**Key insight:** AMI achieves Manchester-level synchronization **without doubling bandwidth**, making it efficient for long-distance telecommunications.

## Pseudoternary (The Opposite of AMI)

Some systems use **Pseudoternary**, the inverse of AMI:

**Pseudoternary encoding rule:**
- Bit 1 → Voltage = 0 V (no voltage)
- Bit 0 → Alternates between +V and -V with each successive 0
  - First 0 → +V
  - Next 0 → -V
  - Next 0 → +V
  - And so on...

**Example: Same bit stream `10110001`**
```
Bit:      1   0   1   1   0   0   0   1
Voltage:  0V  +V  0V  0V  -V  +V  -V  0V
```

### When to Use Pseudoternary?

- When the expected data has **more 1s than 0s**
- Then 0s (the minority) alternate, providing better synchronization
- Opposite strategy to AMI, which works better for **more 0s than 1s**

**Practical choice:** AMI is more common because in many communication systems (like voice), data has more silence (0s) than activity (1s).

## Detailed Analysis: Why Alternation Works

### The Problem It Solves

In Polar NRZ-L: Sequence "111111" → six +V pulses with no level change
```
Voltage:  +V  +V  +V  +V  +V  +V
Transitions: ─────────────────────  (none!)
Receiver clock drifts
```

### The AMI Solution

In AMI: Sequence "111111" → alternating ±V with transitions everywhere
```
Voltage:  +V  -V  +V  -V  +V  -V
Transitions: ↓   ↓   ↓   ↓   ↓   ↓ (every bit!)
Receiver locks to these transitions
```

### Error Detection Capability

If receiver sees: "+V +V -V" (two consecutive +V)
- This violates the alternating rule
- A 1-bit error likely occurred (a 0 was received as 1)
- Hardware can flag this immediately

## Encoding Algorithm (AMI)

```
Initialize: last_mark_polarity = +V

For each bit in the stream:
  if bit == 0:
    output 0V
  else:  // bit == 1
    if last_mark_polarity == +V:
      output -V
      last_mark_polarity = -V
    else:
      output +V
      last_mark_polarity = +V
```

**Time complexity:** O(n) for n bits  
**Space complexity:** O(1) (only need one bit of state)

## Decoding Algorithm (AMI)

```
For each voltage sample in the received signal:
  if voltage is approximately +V:
    output 1
    Remember: next 1 should be -V
  else if voltage is approximately -V:
    output 1
    Remember: next 1 should be +V
  else if voltage is approximately 0V:
    output 0
  else:
    ERROR (voltage outside expected range)
```

## Practical Applications

### 1. T-Carrier Systems (North America)

- **T1:** 1.544 Mbps, uses AMI encoding
- **T2:** 6.312 Mbps
- **T3:** 44.736 Mbps

All use AMI or variants (HDB3, B8ZS) for synchronization and error detection.

### 2. ISDN (Integrated Services Digital Network)

- AMI on copper phone lines
- DC-free signaling suitable for long distances
- Error detection catches transmission problems

### 3. DSL (Digital Subscriber Line)

- Variants of AMI used for high-speed data over phone lines
- Zero DC component critical for shared infrastructure

## Real-World Snapshot: Telephone System

When you make a phone call, your voice is:
1. Sampled 8,000 times/second (Nyquist for 4 kHz bandwidth)
2. Quantized to 8 bits per sample (256 levels)
3. Encoded in AMI for transmission
4. Multiplexed with other calls on a T1 line (24 channels, 1.544 Mbps total)

AMI ensures all 24 simultaneous calls have stable synchronization and zero DC drift, even if some callers stay silent (long runs of 0s) and others talk continuously (mixed 0s and 1s).

## Exam-Typical Questions

**Q1:** Encode "10110001" in both AMI and Pseudoternary. Compare the waveforms.

**A1:**

AMI image: ![[images/note_ami_example.png]]

Pseudoternary image: ![[images/note_pseudoternary_example.png]]

(AMI: 1s alternate polarity. Pseudoternary: 0s alternate polarity.)

**Q2:** A T1 carrier has received the AMI sequence: +V 0V -V +V 0V -V 0V **+V** -V

The marked bit is "**+V**" but the expected polarity is "-V". What does this indicate?

**A2:** 
An error has occurred. The alternation rule was violated. This likely means:
- A bit was corrupted
- Or a timing synchronization error occurred
- The receiver can trigger an alarm and request retransmission

**Q3:** Why is AMI better than Polar NRZ-L for telephone systems despite using more complex receivers?

**A3:**
- Telephone signals often have long periods of silence (0s) and activity (1s)
- Data is often unbalanced (more 0s than 1s)
- Polar NRZ-L suffers from DC drift on unbalanced data
- AMI guarantees zero DC regardless of balance
- AMI's alternating rule provides synchronization even with unbalanced data
- Error detection is a bonus feature for reliability

## Comparison: Synchronization Quality

```
Unipolar NRZ:    No transitions → Clock drifts badly
Polar NRZ-L:     Depends on data → Clock drifts on repeated bits
AMI:             Good transitions due to alternation → Clock stable
Manchester:      Transitions in every bit → Clock most stable (but double bandwidth)
```

## Related Concepts

- [[02-Line-Coding-Basics|Line Coding Basics]] — Why encoding is needed
- [[07-DC-Component|DC Component]] — Importance of zero DC
- [[08-Self-Synchronization|Self-Synchronization]] — How clocks lock onto patterns
- [[14-Manchester-Coding|Manchester Coding]] — Alternative self-synchronizing code
- [[22-Block-Coding|Block Coding (HDB3, B8ZS)]] — Solutions for long zero runs
- [[27-Comparison-Matrix|Comparison Matrix]] — All schemes ranked
- [[29-Exam-Strategy|Exam Strategy]] — Common question types

---

**Parent:** [[./MOC|Line Coding Complete Reference]]

**Last updated:** January 13, 2026