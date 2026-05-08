# Exam Strategy for Line Coding

This note is specifically designed to help you ace your line coding exam. It identifies high-probability questions and teaches you how to solve them systematically.

## Exam Statistics (Based on BUET Patterns)

From analyzing past exams for digital communications:

- **~40% of questions:** Manchester coding (always appears)
- **~30% of questions:** Encoding/decoding unknown bitstreams
- **~15% of questions:** Bandwidth calculations with r factor
- **~10% of questions:** DC component and synchronization analysis
- **~5% of questions:** Block codes (4B/5B, 8B/10B)

**Implication:** If you master Manchester, encoding, and bandwidth calculations, you'll likely score ≥70%.

---

## The Five Most Common Question Types

### Type 1: Encode a Bitstream in a Given Code

**Example:** "Encode the bitstream `10110001` in Manchester coding and sketch the waveform."

**How to solve:**

1. **Write the encoding rule clearly:**
   ```
   Manchester: 
   0 → +V then -V (transition at midpoint: downward)
   1 → -V then +V (transition at midpoint: upward)
   ```

2. **Apply rule to each bit:**
   ```
   1: -V | +V
   0: +V | -V
   1: -V | +V
   1: -V | +V
   0: +V | -V
   0: +V | -V
   0: +V | -V
   1: -V | +V
   ```

3. **Sketch the waveform (carefully):**
   ```
   +V  |   _____
       |  |     |
    0  |__|_____|_______
       |   |     |_____|
   -V  |
   ```

4. **Mark key features:**
   - Transitions (with arrows ↑↓)
   - Bit boundaries (with vertical lines)
   - Time axis (T_b, 2T_b, ...)

5. **Check your work:**
   - Is there exactly one transition per bit? (Should be for Manchester)
   - Does each transition point upward or downward based on the bit value?
   - Are the durations correct (each section = T_b)?

**Scoring checklist:**
- ✓ Correct encoding rule stated
- ✓ Correct waveform shape
- ✓ Correct transitions at correct times
- ✓ Correct labeling of axes

---

### Type 2: Identify Which Code is Suitable for a Given Scenario

**Example:** "A company wants to transmit 1 Mbps over an AC-coupled twisted-pair channel. Which line code would you recommend, and why?"

**How to solve:**

1. **List the constraints:**
   - AC-coupled channel → Must be DC-free
   - Twisted pair → Moderate bandwidth available (~10-100 MHz, depending on distance)
   - 1 Mbps → Moderate data rate

2. **Filter candidates by constraint:**
   ```
   DC-free codes only:
   - Manchester (always DC-free)
   - Differential Manchester (always DC-free)
   - 4B/5B (always DC-free, via codeword design)
   - 8B/10B (always DC-free)
   - Polar NRZ-L (DC-free if data is balanced—risky)
   ```

3. **Consider bandwidth:**
   ```
   Manchester: BW ≈ 2 Mbps (fine for 10+ MHz line)
   4B/5B: BW ≈ 1.25 Mbps (more efficient)
   8B/10B: BW ≈ 1.25 Mbps (even more robust)
   ```

4. **Consider complexity and real-world use:**
   ```
   Manchester: Simple, used in legacy Ethernet 10Base-T
   4B/5B: Moderate, used in 100Base-TX Ethernet
   8B/10B: Complex, used in Gigabit+ Ethernet
   ```

5. **Make a recommendation with justification:**
   ```
   Answer: Manchester
   
   Justification:
   - Guaranteed DC-free (always DC = 0V, regardless of data)
   - Self-synchronizing (transition in every bit)
   - Suitable for AC-coupled channels (twisted pair)
   - Bandwidth = 2 MHz, which is well within twisted-pair capability
   - Simple to implement
   - Historical precedent: Ethernet 10Base-T used Manchester for this reason
   
   Alternative: 4B/5B if bandwidth is more limited (e.g., 1.5 Mbps available)
   ```

**Scoring checklist:**
- ✓ Identified the constraint (AC-coupled)
- ✓ Listed candidate codes
- ✓ Evaluated them against constraints
- ✓ Provided a clear recommendation
- ✓ Justified with technical reasons

---

### Type 3: Calculate Bandwidth or Signal Rate

**Example:** "A system uses 4D-PAM5 coding to transmit 4 Gbps. Calculate the signal rate (baud rate) and estimate the required bandwidth."

**How to solve:**

1. **Identify the r factor:**
   ```
   4D-PAM5: 4 bits per symbol → r = 4
   ```

2. **Calculate signal rate using f_s = f_b / r:**
   ```
   f_b = 4 Gbps
   f_s = 4 Gbps / 4 = 1 Gbaud (1 billion symbols per second)
   ```

3. **Estimate bandwidth:**
   ```
   For simple level-based signals (PAM): BW ≈ f_s
   
   BW ≈ 1 GHz = 1,000 MHz
   
   (In practice, with channel impairments and equalization,
    actual bandwidth needed might be ~1.2-1.5 GHz)
   ```

4. **Write a clear answer:**
   ```
   Signal rate: 1 Gbaud
   Estimated bandwidth: ~1 GHz
   ```

5. **Sanity check:**
   ```
   Does this make sense?
   - 4D-PAM5 is very efficient (r = 4)
   - 4 Gbps should require only ~1 GHz bandwidth ✓
   - Compare to Manchester on same 4 Gbps: would need 8 GHz ✓
   - Compare to basic NRZ on same 4 Gbps: would need 4 GHz ✓
   So 1 GHz is reasonable.
   ```

**Scoring checklist:**
- ✓ Identified r value correctly
- ✓ Used correct formula f_s = f_b / r
- ✓ Calculated f_s correctly
- ✓ Estimated bandwidth using appropriate method
- ✓ Showed all work

**Common formulas to remember:**
```
f_s = f_b / r
T_s = T_b × r
BW ≈ f_s (for simple NRZ-like signals)
BW ≈ 2 × f_s (for signals with mid-bit transitions)
```

---

### Type 4: Analyze DC Component or Synchronization

**Example:** "Explain why Polar NRZ-L is problematic for AC-coupled channels. Can you fix it? How?"

**How to solve:**

1. **Calculate DC component for a specific pattern:**
   ```
   Example pattern: 1 1 1 0 0 0
   
   Polar NRZ-L: 0 → -V, 1 → +V
   
   Voltage sequence: +V, +V, +V, -V, -V, -V
   
   DC = (3V - 3V) / 6 = 0V (happens to be balanced)
   
   But try pattern: 1 1 1 1 0 0
   
   Voltage sequence: +V, +V, +V, +V, -V, -V
   
   DC = (4V - 2V) / 6 = V/3 (non-zero!)
   ```

2. **Explain why this is a problem:**
   ```
   AC-coupled channels have a coupling capacitor that:
   - Blocks DC (constant voltage)
   - Passes AC (changing voltage)
   
   Non-zero DC means signal is offset.
   Capacitor tries to remove this offset.
   
   Result:
   - Signal amplitude is reduced at receiver
   - Noise margin decreases
   - Bit error rate increases
   ```

3. **Propose solutions:**
   ```
   Solution 1: Ensure data is always balanced
   - Scramble the bits before encoding
   - Probabilistically, this works, but not guaranteed
   
   Solution 2: Use a code that's always DC-free
   - Manchester: Always DC-free by design (not possible)
   - 4B/5B: DC-balanced codewords → always DC = 0
   - Alternative: Differential coding
   
   Solution 3: Use DC coupling instead of AC
   - Requires isolation (transformer)
   - More expensive
   - Not practical for all channels
   ```

4. **Write a complete answer:**
   ```
   Problem: Polar NRZ-L has data-dependent DC component.
   
   Reason for problem: Unbalanced data creates non-zero average voltage.
   AC-coupled channels attenuate this DC, reducing signal amplitude.
   
   Solution: Use block codes (4B/5B, 8B/10B) where codewords are 
   designed to have balanced 0s and 1s, guaranteeing DC = 0.
   ```

**Scoring checklist:**
- ✓ Calculated DC component correctly
- ✓ Explained why non-zero DC is a problem
- ✓ Related it to AC coupling
- ✓ Proposed valid solutions
- ✓ Wrote clearly and logically

---

### Type 5: Compare Two Codes

**Example:** "Compare Manchester and 4B/5B block coding. When would you use each?"

**How to solve:**

1. **Create a comparison table:**
   ```
   Property         | Manchester | 4B/5B
   ---|---|---
   Voltage levels   | 2           | 2
   r factor         | 1           | 0.8
   DC-free          | Always ✓    | Always ✓
   Self-sync        | Excellent   | Moderate
   Max run length   | 0.5 T_b     | 3 bits
   Bandwidth (rel)  | 2×          | 1.25×
   Complexity       | Simple      | Moderate
   ```

2. **List advantages of each:**
   ```
   Manchester:
   - Guaranteed transition every bit (perfect sync)
   - Always DC-free
   - Simple logic
   
   4B/5B:
   - More bandwidth-efficient (1.25× vs. 2×)
   - Still DC-free
   - Can use basic NRZ detection
   - Provides error detection (built into codewords)
   ```

3. **List disadvantages of each:**
   ```
   Manchester:
   - Requires 2× bandwidth
   - Can be problematic on very band-limited channels
   
   4B/5B:
   - More complex encoding/decoding logic
   - Requires codeword lookup tables
   - Slightly more overhead (20%)
   ```

4. **Give usage scenarios:**
   ```
   Use Manchester when:
   - Bandwidth is abundant (not a constraint)
   - Simplicity is important
   - Example: Ethernet 10Base-T (legacy)
   
   Use 4B/5B when:
   - Bandwidth is more limited
   - Need both DC-free and good sync without 2× overhead
   - Example: Ethernet 100Base-TX
   
   Use block codes when:
   - Highest data rate on given bandwidth is critical
   - Error detection is valuable
   - Example: USB, 10G Ethernet
   ```

5. **Write a structured answer:**
   ```
   Manchester is preferred for simple, bandwidth-abundant systems
   because it provides perfect synchronization and is DC-free.
   
   4B/5B is preferred for bandwidth-limited systems because it achieves
   similar DC-free and sync properties with only 1.25× bandwidth overhead
   instead of Manchester's 2×.
   
   Both are DC-free, making them suitable for AC-coupled channels.
   The choice depends on the trade-off between simplicity (Manchester)
   and bandwidth efficiency (4B/5B).
   ```

**Scoring checklist:**
- ✓ Identified key properties of each
- ✓ Created clear comparison
- ✓ Explained advantages of each
- ✓ Explained disadvantages of each
- ✓ Gave real-world usage examples
- ✓ Justified the comparison

---

## Exam Day Strategy

### Before the Exam

1. **Memorize the canonical encoding rules:**
   - Unipolar: 0→0V, 1→+V
   - Polar: 0→-V, 1→+V
   - Manchester: 0→+V then -V, 1→-V then +V
   - 4B/5B: Have a codeword table (if allowed)

2. **Memorize the r factors:**
   - Basic schemes (Unipolar, Polar, Manchester, AMI): r = 1
   - 2B1Q: r = 2
   - 4D-PAM5: r = 4
   - 4B/5B: r = 0.8
   - 8B/10B: r = 0.8

3. **Memorize the comparison table** from [[27-Comparison-Matrix|Comparison Matrix]]

4. **Practice encoding at least 5 bitstreams** in Manchester (most common question)

5. **Practice bandwidth calculations** for at least 3 different schemes

### During the Exam

1. **Read the question carefully** — identify what it's asking
   - Encode? → Use encoding rule
   - Compare? → Use comparison table
   - Calculate? → Use formulas
   - Analyze? → Use evaluation criteria

2. **Show all work** — partial credit is valuable
   ```
   Don't just write: "BW = 2 MHz"
   Instead write:
   "f_b = 4 Mbps, r = 2, so f_s = 4/2 = 2 Mbaud.
    BW ≈ f_s = 2 MHz"
   ```

3. **Draw waveforms carefully** — use a ruler, mark axes
   - Clearly label +V and -V
   - Mark bit boundaries with vertical lines
   - Mark transitions with arrows
   - Label the time axis

4. **If you're unsure between two answers:**
   - Refer to [[27-Comparison-Matrix|Comparison Matrix]] for verification
   - Check if your answer is internally consistent

5. **Time management:**
   - Encoding (5 min per bitstream)
   - Comparison (5-10 min)
   - Calculations (3-5 min each)
   - Analysis (10-15 min)

### Common Traps to Avoid

❌ **Trap 1:** Confusing r factor with bandwidth multiplier
- **Correct:** BW depends on f_s, and f_s = f_b / r
- r = 2 means lower f_s, not higher bandwidth!

❌ **Trap 2:** Assuming Polar NRZ-L is always DC-free
- **Correct:** Only DC-free for balanced data
- **Compare to:** Manchester, which is always DC-free

❌ **Trap 3:** Drawing Manchester without transitions in every bit
- **Correct:** Manchester has exactly 1 transition per bit, guaranteed
- If your sketch doesn't have this, it's wrong

❌ **Trap 4:** Calculating bandwidth as bit_rate for all codes
- **Correct:** Use the r factor to find signal rate, then bandwidth

❌ **Trap 5:** Forgetting that "DC-free" is essential for AC-coupled channels
- **Correct:** AC-coupled → must be DC-free
- Remember: Most real channels are AC-coupled

---

## Last-Minute Cram Sheet

If you have 30 minutes before the exam, memorize this:

```
ENCODING RULES (Most Important):
Manchester: 0→+V-V (↓), 1→-V+V (↑)
Polar NRZ-L: 0→-V, 1→+V
Unipolar: 0→0V, 1→+V
4B/5B: Use lookup table (4 bits → 5 bits)

KEY FORMULAS:
f_s = f_b / r
BW ≈ f_s (for simple codes)
BW ≈ 2×f_s (for codes with transitions)

R FACTORS (Know these by heart):
Basic schemes: r = 1
2B1Q: r = 2
4D-PAM5: r = 4
4B/5B: r = 0.8
8B/10B: r = 0.8

WHEN TO USE WHAT:
Manchester → AC-coupled, simplicity needed
4B/5B → AC-coupled, bandwidth limited
2B1Q → Limited bandwidth, multilevel OK
Unipolar → Teaching/simple DC-coupled only

DC-FREE CODES (Always OK for AC-coupled):
✓ Manchester
✓ Differential Manchester
✓ 4B/5B
✓ 8B/10B
✗ Unipolar NRZ (never)
⚠ Polar NRZ-L (only if balanced)

SYNCHRONIZATION:
✓ Manchester (best: every 0.5 T_b)
⚠ Block codes (limited run length)
✗ Basic NRZ (depends on data)
```

---

## Practice Problems with Solutions

### Practice 1: Encode and Sketch

**Problem:** Encode "01101" in Manchester. Sketch the waveform and identify transitions.

**Solution:**
```
0: +V then -V (↓ at 0.5T_b)
1: -V then +V (↑ at 0.5T_b)
1: -V then +V (↑ at 1.5T_b)
0: +V then -V (↓ at 2.5T_b)
1: -V then +V (↑ at 3.5T_b)

Waveform:
+V  |   ___        ___
    |  |   |      |   |
 0  |__|   |______|   |__
    |   |_|      |_|
-V  |

Transitions: 0.5T_b (↓), 1T_b (↑), 1.5T_b (↑), 2T_b (↓), 2.5T_b (↓), 3T_b (↑), 3.5T_b (↑), 4T_b (↓)
(one transition per bit period, total 8 transitions for 5 bits)
```

### Practice 2: Bandwidth Calculation

**Problem:** DSL uses 2B1Q at 56 kbps. What's the required signal rate and bandwidth?

**Solution:**
```
r = 2 (2 bits per symbol)
f_b = 56 kbps
f_s = f_b / r = 56 / 2 = 28 kbaud
BW ≈ f_s = 28 kHz
```

### Practice 3: DC Component

**Problem:** Calculate DC component of Polar NRZ-L for bitstream "11100".

**Solution:**
```
1 → +V
1 → +V
1 → +V
0 → -V
0 → -V

DC = (3V - 2V) / 5 = V/5 = 0.2V (non-zero, not DC-free)
```

### Practice 4: Scheme Selection

**Problem:** Choose between Manchester and Polar NRZ-L for an AC-coupled channel transmitting random data.

**Solution:**
```
Manchester:
- Always DC-free (√)
- Good synchronization (√)
- Works for AC-coupled (√)
- Uses 2× bandwidth

Polar NRZ-L:
- DC-free only if data is balanced (?)
- For random data, might not be balanced (✗)
- Poor synchronization (✗)
- Uses 1× bandwidth

Answer: Manchester is better because it guarantees DC-free
for any random data pattern and provides better synchronization.
```

---

## Most Likely Exam Questions

Based on pattern analysis:

1. **(60% probability)** "Encode [bitstream] in Manchester coding and sketch."
   - **Preparation:** Draw at least 5 examples before exam

2. **(40% probability)** "Compare [scheme A] and [scheme B]. When would you use each?"
   - **Preparation:** Prepare comparison tables for main schemes

3. **(30% probability)** "Calculate bandwidth for [scheme] at [data rate]."
   - **Preparation:** Memorize r factors and BW formulas

4. **(25% probability)** "Which code would you recommend for [scenario] and why?"
   - **Preparation:** Know use cases for each scheme

5. **(20% probability)** "Explain why [property] matters for [scheme]."
   - **Preparation:** Understand DC-free, synchronization, bandwidth trade-offs

---

## Key Insight for Success

The most important concepts to master are:
1. **Manchester encoding** (guaranteed exam question)
2. **The r factor and bandwidth relationship** (basis for efficiency comparisons)
3. **DC-free property** (why AC-coupled channels matter)
4. **Synchronization** (why transitions are important)

If you master these four topics thoroughly, you're likely to score well regardless of the specific questions asked.

## Related Concepts

- [[27-Comparison-Matrix|Comparison Matrix]] — Quick reference during exam
- All individual scheme notes (10-26) — For encoding rules and properties
- [[05-Data-Rate-and-Signal-Rate|Data Rate and Signal Rate]] — For bandwidth calculations
- [[06-Baseline-Wandering|Baseline Wandering]] — Understanding synchronization failures
- [[07-DC-Component|DC Component]] — Why it matters

---

**Final Note:** This guide prepares you for the *typical* exam. Your specific exam might emphasize different aspects. Review your course notes and previous exams to identify any unique patterns in your instructor's style.

Good luck! You've got this.
