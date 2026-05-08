# Complete Comparison Matrix

Use this matrix to quickly evaluate and compare all line coding schemes. Organize your knowledge here.

## Full Comparison Table

| Scheme | Levels | r | DC-Free | Self-Sync | Max Run | BW / Bit Rate | Use Case | Rating |
|--------|--------|---|---------|-----------|---------|---|---|---|
| **Unipolar NRZ** | 2 (0, +V) | 1 | No | No | ∞ | 1× | Teaching only | ❌ Poor |
| **Polar NRZ-L** | 2 (-V, +V) | 1 | Yes* | No | ∞ | 1× | Disk storage | ⚠ Fair |
| **Polar NRZ-I** | 2 (-V, +V) | 1 | Yes* | No | ∞ | 1× | Satellite | ⚠ Fair |
| **Polar RZ** | 2 (-V, +V) | 1 | Yes* | Moderate | ∞ | 2× | Legacy systems | ⚠ Fair |
| **Manchester** | 2 (-V, +V) | 1 | Yes | Yes | 0.5T_b | 2× | Ethernet legacy | ✅ Excellent |
| **Diff. Manchester** | 2 (-V, +V) | 1 | Yes | Yes | 0.5T_b | 2× | Token Ring | ✅ Excellent |
| **AMI** | 3 (-V, 0, +V) | 1 | Yes* | No | ∞ (0s only) | 1× | T-carrier base | ⚠ Fair |
| **Pseudoternary** | 3 (-V, 0, +V) | 1 | Yes* | No | ∞ (1s only) | 1× | Variant of AMI | ⚠ Fair |
| **2B1Q** | 4 levels | 2 | Depends | No | ∞ | 0.5× | ISDN, DSL (old) | ✅ Good |
| **8B6T** | 3 (ternary) | 1.33 | Yes | Depends | Limited | ~0.75× | Gigabit Ethernet | ✅ Good |
| **4D-PAM5** | 5 levels | 4 | Depends | No | ∞ | 0.8× | Gigabit Ethernet | ✅ Good |
| **4B/5B** | 2 (-V, +V) | 0.8 | Yes | Depends** | 3 | 1.25× | 100Base-TX | ✅ Excellent |
| **8B/10B** | 2 (-V, +V) | 0.8 | Yes | Depends** | 8 | 1.25× | 10G, USB, FC | ✅ Excellent |
| **B8ZS** | 2 (-V, 0, +V) | 1 | Yes | Moderate | 2 | 1× | T1 carrier | ✅ Good |
| **HDB3** | 2 (-V, 0, +V) | 1 | Yes | Moderate | 3 | 1× | E1 carrier | ✅ Good |

**Key:**
- **Levels:** How many distinct voltage levels
- **r:** Data bits per signal element (higher = more efficient)
- **DC-Free:** Can transmit over AC-coupled channels?
  - Yes: Always
  - Yes*: Only if data is balanced
  - Depends: Depends on data pattern
- **Self-Sync:** Can receiver recover clock from signal?
- **Max Run:** Maximum consecutive identical bits (indicator of sync reliability)
- **BW / Bit Rate:** Approximate bandwidth as multiple of bit rate
- **Use Case:** Real-world application
- **Rating:** How good is this scheme overall?

---

## Quick Selection Guide

### If you need **robust self-synchronization on any data:**
→ Use **Manchester** or **Differential Manchester**

```
Why: Forced transition in every bit
Trade-off: Requires 2× bandwidth
Applications: Ethernet 10Base-T, legacy protocols
```

### If you need **DC-free for AC-coupled channels** without extra bandwidth:
→ Use **4B/5B** or **8B/10B**

```
Why: Codewords designed for balance and run-length limits
Trade-off: 20-25% bandwidth overhead, more complex
Applications: Modern Ethernet (100Base-TX, 1Gbps+), USB, storage
```

### If you need **maximum data rate on limited bandwidth:**
→ Use **multilevel codes: 2B1Q or 4D-PAM5**

```
Why: Multiple bits per symbol
Trade-off: More signal levels, harder detection, requires equalization
Applications: DSL, early modems, high-speed access
```

### If you need **fix long 0-runs in AMI systems:**
→ Use **B8ZS** or **HDB3**

```
Why: Targeted scrambling of problem patterns
Trade-off: Slightly more complex encoding/decoding
Applications: T1 (B8ZS) and E1 (HDB3) carrier systems
```

### If you need **simplicity with acceptable performance:**
→ Use **Polar NRZ-L**

```
Why: Simple encoding, works for DC-coupled channels
Trade-off: Requires balanced data or external sync
Applications: Magnetic disk recording, some satellite systems
```

---

## Detailed Property Comparison

### DC Component: Which are Always DC-Free?

**Always DC-free (no caveats):**
- Manchester ✅
- Differential Manchester ✅
- 4B/5B ✅
- 8B/10B ✅
- B8ZS ✅
- HDB3 ✅

**DC-free only with balanced data:**
- Polar NRZ-L* 
- Polar NRZ-I*
- Polar RZ*
- AMI*
- Pseudoternary*

**Never DC-free:**
- Unipolar NRZ ❌

**Depends heavily on data:**
- 2B1Q
- 4D-PAM5

### Self-Synchronization: Which Maintain Sync?

**Excellent (transition every 0.5 T_b):**
- Manchester
- Differential Manchester

**Moderate (limited run length prevents sync loss):**
- 4B/5B (run-length ≤ 3)
- 8B/10B (run-length ≤ 8)
- B8ZS (run-length ≤ 2)
- HDB3 (run-length ≤ 3)

**Poor (depend on data):**
- Unipolar NRZ
- Polar NRZ-L
- Polar NRZ-I
- Polar RZ
- AMI
- Pseudoternary
- 2B1Q
- 4D-PAM5

### Bandwidth Efficiency

**Most efficient (lowest bandwidth needed):**
1. 4D-PAM5 (0.8× baseline)
2. 2B1Q (0.5× baseline)
3. 8B6T (0.75× baseline)
4. Unipolar/Polar/AMI (1× baseline)
5. 4B/5B, 8B/10B (1.25× baseline)
6. Manchester, RZ (2× baseline)

**Trade-off:** More efficient codes require more signal levels, making them harder to detect in noise.

### Practical Implementation

**Easiest to implement:**
1. Unipolar NRZ (simple)
2. Polar NRZ-L (simple + symmetric)
3. Manchester (straightforward logic)

**Moderately complex:**
- Differential Manchester
- Polar RZ
- AMI
- 2B1Q

**Most complex (require lookup tables and logic):**
- 4B/5B
- 8B/10B
- 4D-PAM5 (also needs equalization)
- B8ZS (needs run-length detection)
- HDB3 (needs run-length detection)

---

## By Application Domain

### **Ethernet Standards**

| Speed | Standard | Coding | Medium |
|-------|----------|--------|--------|
| 10 Mbps | 10Base-T | Manchester | Twisted pair |
| 10 Mbps | 10Base-2 | Manchester | Coaxial cable |
| 100 Mbps | 100Base-TX | 4B/5B + NRZ | Twisted pair |
| 1 Gbps | 1000Base-T | 4D-PAM5 + 8B/10B | Twisted pair |
| 10 Gbps | 10GBase-T | Multiple PAM | Twisted pair |

### **Telephone/Carrier Systems**

| Standard | Line Rate | Coding | Purpose |
|----------|-----------|--------|---------|
| T1 | 1.544 Mbps | B8ZS | Digital telephone trunk |
| E1 | 2.048 Mbps | HDB3 | European digital trunk |
| DSL | ~50 kbps-15 Mbps | 2B1Q, 4D-PAM5 | Broadband over copper |

### **Storage Systems**

| Medium | Typical Coding | Reason |
|--------|---|---|
| Magnetic disk | NRZI, Polar NRZ-L | Simple, DC-coupled, no sync needed |
| Optical disk | EFM modulation | Specialized (not covered in this course) |
| Tape | Manchester, 2B1Q | Varies by standard |

### **Wireless & Satellite**

| Application | Coding | Reason |
|---|---|---|
| Satellite telemetry | Polar NRZ | High power efficiency |
| Wireless digital | QPSK, QAM | (Advanced, beyond this course) |

---

## Symbol Count for Different Schemes

**Given:** Transmit 1,000,000 bits per second

| Scheme | r | Signal Elements/sec | Comments |
|--------|---|---|---|
| Unipolar NRZ | 1 | 1,000,000 | 1 bit per symbol |
| Manchester | 1 | 1,000,000 | 1 bit per symbol, but 2 transitions |
| 2B1Q | 2 | 500,000 | 2 bits per symbol |
| 4B/5B | 0.8 | 1,250,000 | Less bits per symbol (redundancy) |
| 4D-PAM5 | 4 | 250,000 | 4 bits per symbol |

---

## Quick Reference: Encoding Rules

### Level-Based (voltage indicates bit value)
- **Unipolar NRZ:** 0→0V, 1→+V
- **Polar NRZ-L:** 0→-V, 1→+V

### Transition-Based (transition indicates bit value)
- **Manchester:** 0→+V→-V, 1→-V→+V
- **Differential Manchester:** Start with transition, mid-bit transition = 0, no mid-bit = 1
- **Polar NRZ-I:** Transition→1, No transition→0

### Multilevel (multiple bits per symbol)
- **2B1Q:** 00→-3V, 01→-V, 10→+V, 11→+3V
- **AMI:** 0→0V, 1→alternating ±V

### Block Coded (groups of bits mapped to special codewords)
- **4B/5B:** 16 possible 4-bit patterns → 32 valid 5-bit codewords
- **8B/10B:** 256 possible 8-bit patterns → 1024 valid 10-bit codewords

---

## Visual Comparison: Same Bit Pattern Across Schemes

**Bit stream:** `1 1 0 0 1`

```
Unipolar NRZ:
+V |  ___   ___
   | |   | |   |
0  |_|___|_|___|___
   |
-V |

Polar NRZ-L:
+V | ___   ___
   ||   | |   |
0  |_|   | |
   |     | |___
-V |     |_|   |

Manchester:
+V |  -\ +/      -\
   |    \|  \   /  \
0  |_____\   X     ___
   |        \|  \ /
-V |         +\  -/

2B1Q (grouping: 11, 00, 1X):
+3|      ___
+1|  ___|   |___
0 |_|       |   |___
-1|   |_____     ___
-3|

(Note: Last bit needs padding)
```

**Key observation:** Same data, completely different waveforms depending on the code!

---

## How to Use This Matrix on Exams

### If asked "Which code is best for X?"

1. **Identify the constraint:** (AC-coupled channel, limited bandwidth, ease of sync, etc.)
2. **Cross-reference the matrix:** Find which codes satisfy the constraint
3. **Rank the candidates:** Use the trade-offs to eliminate poor choices
4. **Justify the answer:** Cite the property that makes it suitable

### If asked to compare two codes:

1. **Find both codes in the table**
2. **Compare properties row by row**
3. **Highlight where they differ**
4. **Explain implications of differences**

### If asked to calculate something:

1. **Find the r value** in the matrix
2. **Use the formulas:** $f_s = f_b / r$, $\text{BW} \approx k \times f_s$
3. **Verify your answer makes sense** by comparing to similar codes

---

## Common Exam Patterns

**Pattern 1:** "Name two codes suitable for AC-coupled channels."  
**Answer:** Manchester and 4B/5B (both always DC-free)

**Pattern 2:** "Why does Manchester require more bandwidth?"  
**Answer:** Built-in transitions double the signal rate complexity

**Pattern 3:** "Encode `101` in [scheme] and sketch."  
**Answer:** Apply the encoding rule step-by-step (see individual scheme notes)

**Pattern 4:** "Compare efficiency of scheme A and scheme B for transmitting 1 Mbps."  
**Answer:** Calculate baud rates using r, compare bandwidths

**Pattern 5:** "Which code would you use for a DSL system and why?"  
**Answer:** 2B1Q or 4D-PAM5 (r > 1 for efficiency on bandwidth-limited line)

## Related Concepts

- Individual scheme notes (10-26)
- [[05-Data-Rate-and-Signal-Rate|Data Rate and Signal Rate]] — For calculations
- [[06-Baseline-Wandering|Baseline Wandering]] — Understand why max run length matters
- [[07-DC-Component|DC Component]] — Why DC-free is important
- [[08-Self-Synchronization|Self-Synchronization]] — Understanding sync properties
- [[09-Bandwidth-Efficiency|Bandwidth Efficiency]] — How bandwidth is calculated
