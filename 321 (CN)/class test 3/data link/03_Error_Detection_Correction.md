# 3. Error Detection & Correction

> **[[00_DLL_Index|← Back to Index]]**

## The Reliability Problem

### Why Errors Happen

When data travels across physical wires (copper cables, fiber optics, wireless), it faces many threats:
- **Thermal noise**: Random electrical fluctuations from heat
- **Electromagnetic interference**: Radio signals, motors, power lines interfere with your signal
- **Crosstalk**: Other cables nearby leak signals into yours
- **Attenuation**: Signal gets weaker over distance, making it harder to distinguish 0 from 1

The result? Bits randomly flip from 0→1 or 1→0. Even a single bit error can corrupt an entire frame.

### The Core Challenge

The receiver faces a critical problem:
- It receives a bit pattern
- It doesn't know if any bits flipped during transmission
- It has **no way to compare** with the original (the sender can't send it twice!)

**Question**: How can the receiver **detect** (or even **correct**) errors without knowing what was sent?

### The Solution: Add Redundancy

The clever answer: **Include extra bits** that encode information about the original message. These redundant bits let the receiver:
1. **Detect**: Recognize that an error occurred (but not fix it)
2. **Correct**: Pinpoint which bit(s) flipped and restore them

**Trade-off**: You send more bits to gain error protection.

---

## Hamming Distance: The Foundation

### Definition

The **Hamming distance** between two bit strings is the **number of bit positions in which they differ**.

Think of it as: "How many flips would it take to turn one string into the other?"

**Examples**:
```
1010 vs 1011  → Hamming distance = 1 
  ↑ differ in position 4 only

1010 vs 0110  → Hamming distance = 2 
  ↑         ↑ differ in positions 1 and 3

1010 vs 1010  → Hamming distance = 0 
  (identical, no differences)

0000 vs 1111  → Hamming distance = 4
  ↑↑↑↑ all positions differ!
```

**Visual way to think about it**: Imagine the bit strings as points in space. Hamming distance = how many steps to get from one point to another.

### Minimum Distance of a Code

A **code** is a set of **valid codewords** — the only bit patterns we're allowed to send. The **minimum distance** ($d_{min}$) is the **smallest Hamming distance between ANY two valid codewords**.

**Why does this matter?** The minimum distance tells us how "spread out" our valid codewords are. The farther apart they are, the more errors we can tolerate.

**Example Code**:
```
Valid codewords: {0000, 1111}

Distances:
  d(0000, 1111) = 4  ← only one pair!
  
Minimum distance: d_min = 4
```

**Contrast**: A code with {0000, 0001, 1110, 1111} has:
```
  d(0000, 0001) = 1  ← too close!
  d(0000, 1110) = 3
  d(0000, 1111) = 4
  ...
Minimum distance: d_min = 1  ← weak code
```

The minimum is determined by the **worst pair** — the closest two valid codewords.

### Error Detection vs. Correction

#### Detection: Recognizing Something Went Wrong

To **detect up to $e$ bit errors**, we need:
$$d_{min} \geq e + 1$$

**Intuition**: If two valid codewords are far apart (distance ≥ e+1), then flipping e bits in one codeword can't turn it into another valid codeword. So the receiver can recognize "this is not a valid codeword → error!"

**Example: Detecting 1-bit errors with $d_{min} = 2$**
```
Valid codewords: {0000, 1111}  (distance between them = 4)
Minimum distance: d_min = 4  (so we can detect up to 3 errors)

Scenario 1: Send 0000, receive 0001
  - Check: Is 0001 a valid codeword? NO
  - Receiver: "Error detected!" ✓
  - (Can't correct it though — could have come from either codeword)

Scenario 2: Send 0000, receive 1000
  - Check: Is 1000 a valid codeword? NO
  - Receiver: "Error detected!" ✓
```

**Key insight**: Detection is **cheap** — you just need valid codewords far enough apart. You don't recover the original; you just ask the sender to retransmit.

---

#### Correction: Fixing the Error

To **correct up to $t$ bit errors**, we need:
$$d_{min} \geq 2t + 1$$

**Intuition**: If a valid codeword flips t bits, it moves "closer" toward some other codeword, but **not close enough to confuse them**. The receiver can decode: "The closest valid codeword is [X] → the original must have been X."

**Example: Correcting 1-bit errors with $d_{min} = 3$**
```
Valid codewords: {000, 111}  (distance = 3)

Scenario 1: Send 000, one bit flips in transmission → receive 001
  - Distance to 000: 1 ← very close
  - Distance to 111: 2
  - Receiver: "Closest valid codeword is 000" → Correct to 000 ✓

Scenario 2: Send 000, one different bit flips → receive 010
  - Distance to 000: 1
  - Distance to 111: 2
  - Receiver: "Closest valid codeword is 000" → Correct to 000 ✓

Scenario 3: Send 000, two bits flip → receive 011
  - Distance to 000: 2
  - Distance to 111: 1  ← closer now!
  - Receiver: "Closest valid codeword is 111" → Correct to 111 ✗ WRONG!
  - (That's why d_min = 3 only corrects 1 error, not 2)
```

**Key insight**: Correction is **expensive** — you need more redundancy to pinpoint errors. But it's essential when retransmission is impossible (satellites, broadcasts).

### Quick Comparison

| Goal | Required $d_{min}$ | Overhead | Real-World Example |
|------|----------|---------|---------------------|
| Detect 1 error | 2 | Small (1 parity bit) | Ethernet (CRC) |
| Detect 2 errors | 3 | Small | USB checksums |
| Correct 1 error | 3 | Medium (3 bits per 4 data bits) | Hamming(7,4) |
| Correct 2 errors | 5 | Larger | Deep space |

**Summary of the trade-off**:
- **Detection**: "Something is wrong" — cheap, but you must retransmit
- **Correction**: "Here's what's wrong and here's the fix" — expensive, but works offline

**Modern networks** prefer detection because links are reliable enough and retransmission is fast. **Unreliable or one-way channels** (wireless, space) use correction.

---

## Parity Bits: Simple Detection

### The Idea: Parity (Even or Odd)

The simplest error detection: Add **one extra bit** so that the total number of 1s in the frame is always **even** (even parity) or **odd** (odd parity).

**Why does this work?** If the transmission is clean, parity stays the same. If one bit flips, parity flips too — the receiver detects the change!

### Step-by-Step Example

**Sender's job** (using even parity):
```
Original data: 1 0 1 0 1
Count the 1s:  three 1s (odd) ← we want even
Add parity bit: 1        ← now we have four 1s (even)
Final frame:  1 0 1 0 1 1
              D D D D D P  (D=data, P=parity)
```

**Receiver receives cleanly**: `1 0 1 0 1 1`
```
Count: 1 + 1 + 1 + 1 = four 1s (even)
Check: Even parity? YES ✓
Conclusion: No error
```

**Receiver receives with ONE bit flip**: `1 0 1 1 1 1`
```
Count: 1 + 1 + 1 + 1 + 1 = five 1s (odd)
Check: Even parity? NO ✗
Conclusion: Error detected!
```

### The Problem: Not Enough Redundancy

**Hamming distance analysis**:
```
Valid codewords with even parity:
  0000 (zero 1s: even)
  0011 (two 1s: even)
  0101 (two 1s: even)
  0110 (two 1s: even)
  ...

Distance between any two: always 2 or more
Minimum distance: d_min = 2
```

**What it can do**:
- ✓ **Detects single-bit errors**: 1 error → parity flips, error caught
- ✗ **Cannot detect 2 errors**: 2 flips → parity flips twice → back to even, **error hidden!**
- ✗ **Cannot correct anything**: You know there's an error, but not where

**Example of missed 2-bit error**:
```
Sent:    1 0 1 0 1 1  (four 1s: even parity)
Transmit: bits 3 and 6 flip
Received: 1 0 0 0 1 0  (two 1s: even parity) ← looks fine!
Receiver: "Parity is even → no error" ✗ WRONG! Two bits flipped silently.
```

---

## Cyclic Redundancy Check (CRC): Better Detection

### The Big Picture

Parity bits are weak — they miss even-numbered errors. **CRC (Cyclic Redundancy Check)** is much stronger:
- Works like a "fingerprint" of the frame
- Catches single-bit errors, burst errors, and most random errors
- Still only **detects** (doesn't correct)
- Used widely: Ethernet, Wi-Fi, ZIP files

### How CRC Works: Polynomial Division

Instead of counting 1s, treat the frame as a **mathematical polynomial** and divide it by a special **generator polynomial**. The **remainder** is the check code.

**Don't worry about the math** — the key idea is:
```
CRC = Frame mod GeneratorPolynomial
```

The receiver computes the same remainder. If it matches, no error. If it differs, error detected.

### Polynomial Representation (Quick Overview)

Each bit string becomes a polynomial where position = power of x:

```
Bit string: 1 0 1 1 0
Index:      4 3 2 1 0  (from left to right)
Polynomial: 1·x^4 + 0·x^3 + 1·x^2 + 1·x^1 + 0·x^0
            = x^4 + x^2 + x
```

**Translation**:
- `1` → include the term
- `0` → skip the term

### CRC Calculation: The Algorithm

**Conceptually**:
1. Take your frame (data to send)
2. Append some zeros (how many? depends on generator length)
3. Divide by the generator polynomial (using XOR, not regular division)
4. The **remainder** is your CRC check code
5. Send: original frame + CRC
6. Receiver: Divide again. If remainder = 0, no error!

**In practice**: Specialized hardware/software does this super fast (not really doing polynomial math — it's optimized bit operations).

### Worked Example (Simplified)

Let's use a small, easy generator to see the pattern:

**Frame**: `1101011011`
**Generator**: `10011` (degree 4, so append 4 zeros)

**Step 1**: Append zeros
```
1101011011 → 11010110110000  (appended 4 zeros)
```

**Step 2**: Divide using XOR (like long division, but XOR instead of subtract)

```
Divisor (Generator): 10011

           1000...  ← quotient (we don't care about this)
         ───────────────────
10011 │ 11010110110000
        10011           ← XOR the first 5 bits
        ─────
        01001  ← result, bring down next bit
         1001x
        ─────
         ...
         ...          ← continue this process
        ────
        XXXX           ← remainder (4 bits) — this is the CRC!
```

**Result** (simplified for this example):
```
CRC remainder: 1110

Final transmitted frame: 1101011011 | 1110
                         (data)      (CRC)
```

**Receiver validation**:
```
Received: 11010110111110
Divide by same generator: 10011
Remainder: 0000 ← Perfect! No error.

If any bit flipped in transmission:
Remainder: non-zero ← Error detected!
```

### Why CRC Is Strong

**What CRC detects**:
- ✓ **All single-bit errors** — flipping one bit changes the remainder
- ✓ **All burst errors** (consecutive bits) up to the generator length — the generator "spans" the error
- ✓ **Most random multi-bit errors** — statistically, different errors give different remainders

**What CRC cannot do**:
- ✗ **Cannot correct** — you only know an error happened, not where
- ✗ **Cannot catch ALL errors** — theoretically 1 in $2^n$ undetectable (where n = CRC length)

### Common CRC Standards

| Name | Bit Length | Purpose | Where Used |
|------|-----------|---------|-----|
| CRC-8 | 8 bits check code | Small frames | I2C sensors |
| CRC-16 | 16 bits check code | Medium frames | Modbus, PPP |
| CRC-32 | 32 bits check code | Large frames | **Ethernet, Wi-Fi, ZIP files** |

**Why CRC-32 for Ethernet?** Protects 1500-byte frames (12,000 bits). Only 32 bits overhead (~0.3%), catches almost all realistic errors.

**Gut feeling**: The bigger your frame, the bigger your CRC generator should be. For internet packets, CRC-32 is the standard.

---

## Hamming Codes: Single-Error Correction

### When You REALLY Need Correction

Parity detects errors. CRC detects them better. But both say **"something is wrong — ask to retransmit."**

What if you **can't retransmit?**
- Sending data to space probes (year-long delays)
- Broadcasting to many receivers (can't ask all of them)
- Real-time systems that can't wait

Then you need **error correction** — fix the bits automatically.

**Hamming codes** are the elegant solution: Use parity bits smartly to **pinpoint exactly which bit flipped**.

### The Clever Trick: Parity at Power-of-2 Positions

Instead of one parity bit, use **multiple parity bits at special positions**: 1, 2, 4, 8, 16, ...

Each parity bit covers a **different subset** of the frame. By checking which parities fail, you can calculate the error position.

### Hamming(7,4): A Concrete Example

**What does it mean?**
- **7** = total bits in the codeword
- **4** = data bits (information you care about)
- **3** = parity bits (positions 1, 2, 4)

**Structure**:
```
Position: 1 2 3 4 5 6 7
Type:     P P D P D D D
          ↑ Positions 1,2,4 are parity
          Data in 3,5,6,7
```

**Coverage of each parity bit** (powers of 2 have special properties):
```
P1 (position 1): checks positions 1, 3, 5, 7
                 (positions with bit-0 = 1)
P2 (position 2): checks positions 2, 3, 6, 7  
                 (positions with bit-1 = 1)
P4 (position 4): checks positions 4, 5, 6, 7
                 (positions with bit-2 = 1)
```

**Why these subsets?** Binary representation:
```
Position 1 = 001  ← bit-0 set
Position 2 = 010  ← bit-1 set
Position 3 = 011  ← bit-0 AND bit-1 set
Position 4 = 100  ← bit-2 set
Position 5 = 101  ← bit-0 AND bit-2 set
Position 6 = 110  ← bit-1 AND bit-2 set
Position 7 = 111  ← all bits set

P1 checks all positions where bit-0=1: {1,3,5,7}
P2 checks all positions where bit-1=1: {2,3,6,7}
P4 checks all positions where bit-2=1: {4,5,6,7}
```

### Encoding Example: Adding Parity Bits

Let's encode the data `1011` into Hamming(7,4):

**Step 1: Place data bits**
```
Data: 1 0 1 1

Position: 1 2 3 4 5 6 7
Codeword: ? ? 1 ? 0 1 1
          ↑ P1  ↑ P2,P4 are parity (unknown yet)
```

**Step 2: Calculate each parity bit** (using even parity: total 1s in each group should be even)

**For P1** (position 1, checks positions 1, 3, 5, 7):
```
Positions: 1    3 5 7
Values:    P1   1 0 1  
Total 1s: P1 + 1 + 0 + 1 = P1 + 2

For even parity: P1 + 2 must be even
→ P1 = 0  (0 + 2 = 2, which is even ✓)
```

**For P2** (position 2, checks positions 2, 3, 6, 7):
```
Positions: 2    3 6 7
Values:    P2   1 1 1
Total 1s: P2 + 1 + 1 + 1 = P2 + 3

For even parity: P2 + 3 must be even
→ P2 = 1  (1 + 3 = 4, which is even ✓)
```

**For P4** (position 4, checks positions 4, 5, 6, 7):
```
Positions: 4    5 6 7
Values:    P4   0 1 1
Total 1s: P4 + 0 + 1 + 1 = P4 + 2

For even parity: P4 + 2 must be even
→ P4 = 0  (0 + 2 = 2, which is even ✓)
```

**Final codeword**:
```
Position: 1 2 3 4 5 6 7
Coded:    0 1 1 0 0 1 1
          P1 P2 D P4 D D D
```

So the data `1011` becomes `0110011` when encoded with Hamming(7,4).

### Decoding and Error Correction

When the receiver gets a codeword, it **checks each parity group**:

```
S1 = Check parity of positions {1, 3, 5, 7}
S2 = Check parity of positions {2, 3, 6, 7}
S4 = Check parity of positions {4, 5, 6, 7}
```

Each check returns:
- **0** = even (correct parity for that group)
- **1** = odd (error detected in that group)

Then, the **error position = $S_1 \cdot 1 + S_2 \cdot 2 + S_4 \cdot 4$** (binary to decimal)

### Decoding Example: Correcting a Bit Flip

**Sent**: `0 1 1 0 0 1 1` (from our earlier encoding)
**Received**: `0 1 1 0 1 1 1` (position 5 flipped: 0→1)

**Step 1: Check each parity group**

```
S1 (positions 1,3,5,7): 0, 1, 1, 1
  Count 1s: 3 (odd) → S1 = 1 ✗ Error in this group

S2 (positions 2,3,6,7): 1, 1, 1, 1
  Count 1s: 4 (even) → S2 = 0 ✓ No error in this group

S4 (positions 4,5,6,7): 0, 1, 1, 1
  Count 1s: 3 (odd) → S4 = 1 ✗ Error in this group
```

**Step 2: Calculate error position**
```
Error position = S1·1 + S2·2 + S4·4
               = 1·1 + 0·2 + 1·4
               = 1 + 0 + 4
               = 5
```

**Step 3: Flip the bit at position 5**
```
Before: 0 1 1 0 [1] 1 1
Flip pos 5: 0 1 1 0 [0] 1 1 ← corrected!
```

The receiver automatically fixed the error! ✓

### Why This Works

The syndrome bits ($S_1, S_2, S_4$) act like a **binary address**:
- If $S_1=1$, position 1's bit is set in the error address
- If $S_2=1$, position 2's bit is set
- If $S_4=1$, position 4's bit is set

So the syndrome **directly encodes** which position is wrong — clever!

### Efficiency: The Cost of Correction

**Hamming(7,4):**
```
Total bits: 7
Data bits: 4
Parity bits: 3
Efficiency: 4/7 ≈ 57%  (43% overhead for error correction)
```

Compare to parity bit (only 1 overhead but can't correct!):
```
Parity bit method:
Total: 5 bits
Data: 4
Parity: 1
Efficiency: 4/5 = 80%  (20% overhead, detection only)
```

**Scaling to bigger codes**: The formula is $\text{Hamming}(2^n - 1, 2^n - n - 1)$ with n parity bits:

| Code | Total Bits | Data Bits | Parity Bits | Efficiency |
|------|-----------|----------|-------------|------------|
| Hamming(7,4) | 7 | 4 | 3 | 57% |
| Hamming(15,11) | 15 | 11 | 4 | 73% |
| Hamming(31,26) | 31 | 26 | 5 | 84% |
| Hamming(63,57) | 63 | 57 | 6 | 90% |

**Key insight**: As you scale up, overhead becomes less painful. Hamming(63,57) only adds 6 bits per 57 data bits — that's cheaper than CRC-32!

### Burst Error Handling: Spread Out Your Codewords

Hamming codes shine at **single-bit errors**. But real-world errors often come in **bursts** — many consecutive bits flip (bad cable, electromagnetic pulse).

**Problem**: A 4-bit burst destroys an entire Hamming(7,4) codeword

**Solution**: **Interleave** multiple codewords so burst errors hit different codewords:

**Without interleaving** (vulnerable):
```
Codeword 1: c1 c2 c3 c4 c5 c6 c7
Codeword 2: c1 c2 c3 c4 c5 c6 c7
Codeword 3: c1 c2 c3 c4 c5 c6 c7

Burst error (4 bits): ← hits Codeword 2 directly
  Complete disaster! All 7 bits corrupted, Hamming can't fix it.
```

**With interleaving** (spread out):
```
Interleaved transmission:
c1(cw1) c1(cw2) c1(cw3) c2(cw1) c2(cw2) c2(cw3) c3(cw1) ...
  ↑       ↑       ↑
  From different codewords

Burst error (4 bits): ← hits bits from different codewords
  cw1: 1 bit flipped → can correct ✓
  cw2: 1 bit flipped → can correct ✓
  cw3: 1 bit flipped → can correct ✓
  cw1: 1 bit flipped → can correct ✓
  Each codeword gets only 1-bit error!
```

**Key takeaway**: Interleaving converts burst errors into scattered single-bit errors, which Hamming codes handle perfectly. This combo is used in wireless and satellite systems.

---

## Practical Choice: Detection vs. Correction

### Decision Tree

```
Can you retransmit if error detected?
  ├─ YES (Ethernet, Wi-Fi, Internet)
  │  → Use DETECTION (CRC)
  │     - Fast, low overhead
  │     - Just ask sender to resend
  │
  └─ NO (Satellite, one-way broadcast)
     → Use CORRECTION (Hamming or stronger codes)
        - Higher overhead
        - Fixes errors on the fly
```

### When to Use Detection (CRC)

**Scenario**: Sending data over **Ethernet within your home**
- ✓ Link is reliable (short distance, good cable)
- ✓ Retransmission is instant (both devices are right there)
- ✓ No latency penalty for requesting resend

**Tech**: CRC-32 (32-bit check code)
- **Overhead**: ~0.3% for typical 1500-byte frames
- **Speed**: Fast (hardware acceleration)
- **Result**: If error detected, frame is dropped; sender retransmits

**Real example**: Ethernet frames
```
Frame structure: [Header][Data (1500 bytes)][CRC-32 (4 bytes)]
Overhead: 4 bytes per 1500+ bytes ≈ 0.3%
```

### When to Use Correction (Hamming or Stronger)

**Scenario 1: Deep space probe**
- ✗ Retransmission takes 20 minutes (spacecraft is far away)
- ✗ Retransmission eats power/bandwidth budget
- ✓ Must fix errors locally
- → Use Hamming codes + convolutional codes (FEC)

**Scenario 2: Wireless sensor network**
- ✗ Many transmission errors (RF interference, obstacles)
- ✗ Re-transmission wastes battery
- ✓ Need errors fixed immediately
- → Use Hamming or Reed-Solomon codes

**Scenario 3: Broadcast (TV, radio)**
- ✗ Cannot ask millions of receivers to request retransmission
- ✓ Must work for everyone receiving it once
- → Use strong forward error correction (FEC)

**Real example**: Space probe encoding
```
Raw data: 26 bits
After Hamming(31,26): 31 bits (+19% overhead)
After Convolutional: up to 100+ bits (very strong)
Result: Can correct multiple bit errors in short messages
```

---

## Key Takeaways

1. **Hamming distance** is the foundation:
   - $d_{min} \geq e + 1$ needed to **detect** e errors
   - $d_{min} \geq 2t + 1$ needed to **correct** t errors
   - Larger distance = stronger error handling (but more overhead)

2. **Parity bits** — The simplest detector:
   - 1 extra bit detects 1-bit errors
   - Cannot detect even-numbered errors (limitation!)
   - Cannot correct anything
   - Use when: You'll retransmit anyway

3. **CRC** — Industrial-strength detection:
   - Catches single-bit errors, burst errors, most random errors
   - Used everywhere: Ethernet, Wi-Fi, ZIP, Modbus
   - CRC-32 is standard (32-bit check code)
   - Cannot correct — just detect
   - Use when: Link is reliable and retransmission is fast

4. **Hamming codes** — Automatic error correction:
   - Pinpoint and fix single-bit errors
   - Hamming(7,4) = 3 parity bits, 4 data bits, 57% efficiency
   - Scales well: Hamming(31,26) = 84% efficiency
   - Handle burst errors via interleaving
   - Use when: Cannot retransmit (space, broadcast, real-time)

5. **The design philosophy**:
   - **Modern reliable networks**: Detection + retransmission (cheaper)
   - **Unreliable/one-way channels**: Correction codes (necessary)
   - **Trade-off**: Simpler detection vs. expensive correction

---

> **Next**: [[04_Evolution_DLL_Protocols|4. Evolution of DLL Protocols]] — How do we combine error handling with flow control and sequencing?

