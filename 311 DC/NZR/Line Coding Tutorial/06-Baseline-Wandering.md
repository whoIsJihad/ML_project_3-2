# Baseline Wandering

**Baseline wandering** is the receiver's loss of ability to distinguish "signal present" from "signal absent." It's one of the primary evaluation criteria for line codes.

## The Problem: Illustrated

When a long sequence of the same bit (many 0s or many 1s) is transmitted without transitions, the receiver loses track of the average (baseline) voltage.

### Example: Long Sequence of 0s

```
Bit sequence: 0 0 0 0 0 0 0 0 (eight zeros)

Unipolar NRZ encoding:
+V  |
    |
 0  |_____________________________
    |
-V  |

For the entire duration, the voltage = 0 V (constant).

The receiver sees:
- No transitions
- Cannot distinguish this from "no signal" or "broken channel"
- The receiver's timing circuits lose synchronization
- The receiver's baseline reference (0 V) drifts
```

### What Happens Next: Baseline Drift

```
In an AC-coupled channel (capacitor-coupled):

1. The capacitor eventually charges to match the constant 0 V
2. When a transition finally occurs (say, to +V), the capacitor voltage overshoots
3. The receiver misinterprets the signal amplitude
4. Bits are decoded incorrectly

Example waveform at receiver input (AC-coupled):
+V  |        (constant)     (transition causes overshoot)
    |_______________         /⎺⎺⎺⎺
 0  |               \       /
    |                \_____(overshoot distorts signal)
    |
-V  |
```

## Formal Definition

**Baseline wandering** occurs when:

1. **The receiver lacks frequent transitions** to lock its timing circuits
2. **The signal drifts towards a DC component** (constant offset)
3. **The receiver cannot maintain a stable voltage reference** for distinguishing 0 and 1

**Metric:** A signal that suffers from baseline wandering needs:
- Frequent transitions in the bit stream
- Or an encoding that **guarantees transitions** regardless of the data

## Baseline Wandering: Visual Snapshot
![[Pasted image 20260503222131.png|695]]

SCENARIO 1: Unipolar NRZ with alternating bits
Bit stream: 1 0 1 0 1 0 1 0


Receiver sees frequent transitions. Baseline stays steady at 0 V. ✓ Good.


SCENARIO 2: Unipolar NRZ with long 0s, then long 1s
Bit stream: 0 0 0 0 1 1 1 1


Long period at 0 V, then long period at +V.
Receiver baseline drifts. Cannot distinguish reliably. ✗ Bad.

---

SCENARIO 3: Manchester with the same bit sequence
Bit stream: 0 0 0 0 1 1 1 1


Every bit has a transition (from + to - or vice versa).
Receiver always has a timing edge. Baseline stays stable. ✓ Good.



## Why This Happens: AC-Coupled Channels

Most transmission channels use **AC coupling** (capacitors in the signal path) to:
- Block DC power supply voltages
- Remove low-frequency noise
- Protect equipment from DC faults

But AC coupling introduces a problem:

```
Channel model:
Data ---[Encoder]---[AC Coupling (C)]---[Receiver]---[Decoder]---Data
                         |
                    (blocks DC,
                     passes AC)

The capacitor has a time constant τ = RC.

If the signal is constant (DC), the capacitor voltage approaches the signal voltage,
and the effective signal at the receiver drops toward zero.

If the signal has frequent transitions (AC component), the capacitor can maintain
a voltage that represents the signal amplitude.
```

## How Line Codes Mitigate Baseline Wandering

### Strategy 1: Ensure Frequent Transitions (Self-Synchronization)

**Example: Manchester Coding**
- Rule: Every bit contains exactly one transition
- Result: Transitions occur at least twice per bit period
- Benefit: Receiver never loses sync, baseline is stable

**Example: Differential Manchester**
- Rule: Every bit starts with a transition; bit value determines mid-bit transition
- Result: Guaranteed transitions every half bit period
- Benefit: Even better sync than Manchester

### Strategy 2: Limit Run Length (Length of Consecutive 0s or 1s)

**Example: Block Coding (4B/5B, 8B/10B)**
- Rule: Map data bits to codewords that avoid long runs of 0s or 1s
- Result: No more than 3 consecutive 0s (in 4B/5B) or 8 consecutive 0s (in 8B/10B)
- Benefit: Transitions occur frequently enough to prevent baseline drift

**Example: Scrambling (B8ZS, HDB3)**
- Rule: Identify long runs of 0s and replace with special patterns
- Result: Long runs are broken up with transitions or "violations"
- Benefit: Similar to block coding, but without overhead

## Quantitative Metric: Maximum Run Length

A useful metric is the **maximum run length** (MRL):
$$\text{MRL} = \text{Maximum number of consecutive identical bits}$$

| Scheme | MRL | Baseline Wandering Risk |
|--------|-----|------------------------|
| Unipolar NRZ | Unlimited | Very high |
| Polar NRZ-L | Unlimited | Very high |
| Polar RZ | Unlimited | Very high |
| Manchester | 1 (forced transition every bit) | None |
| Diff. Manchester | 1 | None |
| AMI | Unlimited (only 0s, not 1s) | High |
| Pseudoternary | Unlimited (only 1s, not 0s) | High |
| 4B/5B | 3 (guaranteed by mapping) | Low |
| 8B/10B | 8 (guaranteed by mapping) | Very low |
| B8ZS | 2 (by design) | Very low |
| HDB3 | 3 (by design) | Very low |

**Rule:** Baseline wandering is a serious concern if MRL > 5.

## Exam-Style Problem

**Q:** A channel uses Unipolar NRZ. A data pattern consists of 50 consecutive 0s. Explain why baseline wandering will occur and what happens when the signal transitions to a 1.

**A:**

*Baseline wandering occurs because:*
1. 50 consecutive 0s means the voltage is 0 V for a long duration
2. In an AC-coupled receiver, the coupling capacitor charges to 0 V
3. The receiver's baseline reference (the "midpoint" between 0 and 1) drifts toward -V (the negative rail)
4. When the bit finally transitions to 1 (+V), the capacitor must discharge
5. Due to finite time constant, the capacitor voltage can't change instantaneously
6. The receiver sees the 1 as a partial voltage rise, not a full +V
7. Signal amplitude is reduced; noise margin is lost; bit errors become likely

*Solution:* Use a line code that prevents long 0-runs, such as:
- Manchester (forces transitions)
- 4B/5B (limits runs to 3 zeros)
- AMI with scrambling (B8ZS breaks up long 0-runs)

## Key Takeaway

Baseline wandering is essentially a **synchronization failure** caused by lack of signal transitions. It's why simple schemes like Unipolar NRZ are unsuitable for real channels. Every practical encoding either:
- Forces frequent transitions (Manchester, RZ)
- Limits run length (block codes)
- Combines strategies (B8ZS, HDB3)

## Related Concepts

- [[01-Digital-Signal-Fundamentals|Digital Signal Fundamentals]] — AC-coupled channels
- [[08-Self-Synchronization|Self-Synchronization]] — The solution to baseline wandering
- [[10-Unipolar-NRZ|Unipolar NRZ]] — An example of a scheme with baseline wandering issues
- [[14-Manchester-Coding|Manchester Coding]] — A solution (forces transitions)
- [[22-Block-Coding|Block Coding]] — Another solution (limits run length)
