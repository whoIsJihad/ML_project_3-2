# Line Coding Schemes - Quick Reference Guide

**Purpose:** Fast revision for exams. Use this table to compare all schemes at a glance.

## Quick Comparison Table

| **Scheme** | **Setup** | **Pros** | **Cons** | **r Value** | **Bandwidth** | **DC-Free** | **Sync** |
|---|---|---|---|---|---|---|---|
| **Unipolar NRZ** | 1 → +V, 0 → 0V | Simplest | Long 0s drift clock, DC drift | 1 | ~B | ❌ | Poor |
| **Polar NRZ-L** | 1 → +V, 0 → -V | Better than unipolar | Long runs no transitions, need balanced data | 1 | ~B | ⚠️ (balanced) | Poor |
| **Polar NRZ-I** | Invert if 0, hold if 1 | Immune to line inversion | Still poor sync on long runs | 1 | ~B | ⚠️ | Poor |
| **Polar RZ** | 1 → +V→0V, 0 → 0V | Sync better (transitions) | Double bandwidth | 0.5 | ~2B | ✅ | Good |
| **Manchester** | 0 → +V then -V, 1 → -V then +V | Excellent sync (every bit), DC-free | Double bandwidth | 0.5 | ~2B | ✅ | Excellent |
| **Diff Manchester** | Invert at start if 0, always transition | Immune to phase inversion + sync | Even more complex | 0.5 | ~2B | ✅ | Excellent |
| **AMI (Bipolar)** | 0 → 0V, 1 → ±V alternating | Always DC-free, error detection | 3-level complexity, long 0s | 1 | ~B | ✅ | Good |
| **Pseudoternary** | 1 → 0V, 0 → ±V alternating | Best for data-heavy patterns | For different data profile | 1 | ~B | ✅ | Good |
| **2B1Q** | 2 bits → 4 levels (-3, -1, +1, +3) | Bandwidth efficient (0.5r) | Noise sensitivity (4-level) | 0.5 | ~B/2 | ❌ | ⚠️ |
| **8B6T** | 8 bits → 6 ternary symbols | Good bandwidth (0.75r), DC-free | Complex encoding tables | 0.75 | 3B/4 | ✅ | Fair |
| **4B/5B** | 4 bits → 5-bit code, prevents long runs | Solves long-zero problem, NRZ efficient | Overhead (20% extra) | 0.8 | 1.25B | ⚠️ (with 8B/10B) | Good |
| **8B/10B** | 8 bits → 10-bit code (running disparity) | Excellent DC balance, 128 patterns | More overhead (25%) | 0.8 | 1.25B | ✅ | Excellent |

## Legend

- **r value** = data elements / signal elements = bit rate / baud rate
- **B** = original signal bandwidth
- **DC-Free** = ✅ always, ⚠️ conditional, ❌ not guaranteed
- **Sync** = self-synchronization quality

## Encoding Rules (One-Liner)

| Scheme | Rule |
|---|---|
| **Unipolar NRZ** | 1=+V, 0=0V |
| **Polar NRZ-L** | 1=+V, 0=-V |
| **Polar NRZ-I** | Invert on 0, hold on 1 |
| **Polar RZ** | 1=+V then 0, 0=0V (always return to zero mid-bit) |
| **Manchester** | 0=↑↓, 1=↓↑ (always transition at midpoint) |
| **Diff Manchester** | Transition always, invert if 0 |
| **AMI** | 0=0V, 1=±V (alternate polarity) |
| **Pseudoternary** | 1=0V, 0=±V (alternate polarity) |
| **2B1Q** | 00=-3, 01=-1, 10=+1, 11=+3 |
| **4B/5B** | Fixed lookup table (5-bit output for each 4-bit input) |
| **8B/10B** | Complex table balancing DC component |

## When to Use (Exam Decision Tree)

### Question: "Which scheme should I use?"

1. **Need DC-free?** → Manchester, AMI, 8B/10B, Poly RZ
2. **Need bandwidth efficient?** → 2B1Q (0.5r), 4B/5B (0.8r)
3. **Need perfect synchronization?** → Manchester or 8B/10B
4. **Need simplicity?** → Unipolar/Polar NRZ
5. **Telecom (T-carrier)?** → AMI (or HDB3 variant)
6. **Ethernet?** → 8B/10B
7. **Need error detection?** → AMI (alternation violation) or 8B/10B (disparity)

## Key Takeaways

| Concept | Quick Fact |
|---|---|
| **r factor** | Lower r = higher bandwidth efficiency; 1 means bit rate = baud rate |
| **DC drift** | Caused by unbalanced 0s and 1s; solved by alternating (AMI, Manchester) or using RZ |
| **Synchronization** | Needs frequent transitions; achieved by Manchester (every bit) or alternating schemes |
| **Bandwidth penalty** | Manchester costs 2× but guarantees sync; Block codes cost 20-25% overhead; Multilevel (2B1Q) saves bandwidth but risk noise |
| **Error detection** | AMI detects alternation violations; 8B/10B detects disparity violations |

## Quick Calculation Formulas

$$\text{Bit rate } (R_b) = \text{baud rate} \times \text{bits per symbol}$$
$$\text{Baud rate} = \text{bit rate} / r \text{ value}$$
$$\text{Bandwidth} \approx \text{baud rate} \times \text{scaling factor}$$
$$\text{Scaling factor} = 1 \text{ (for NRZ), } 2 \text{ (for RZ/Manchester)}$$

**Example:** 1000 bps in Manchester (r=0.5)
- Baud rate = 1000 / 0.5 = 2000 baud
- Bandwidth ≈ 2000 × 2 = 4000 Hz

## Exam Tips

- **Always check:** r value, DC, and synchronization quality
- **Manchester is king:** Appears in 40% of questions—memorize it!
- **Block codes = run-length limitation:** They prevent long sequences of 0s
- **Multilevel = noise trade-off:** More bits per symbol saves bandwidth but needs cleaner channel
- **T1/ISDN = AMI:** Default for telecom systems
- **Ethernet = 8B/10B:** Industry standard for high speed

## Related Full Notes

- [[02-Line-Coding-Basics|Basics]] 
- [[10-Unipolar-NRZ|Unipolar NRZ]]
- [[11-Polar-NRZ-L|Polar NRZ-L]]
- [[14-Manchester-Coding|Manchester]]
- [[16-Bipolar-Line-Coding|AMI/Pseudoternary]]
- [[22-Block-Coding|Block Codes]]

---

**Last updated:** January 13, 2026  
**For:** Quick exam revision
