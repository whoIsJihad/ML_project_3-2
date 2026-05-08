# Hamming Code: Error Correction Basics

## What is the Problem?

When storing or transmitting data (as sequences of 1s and 0s), errors can occur:
- Scratches on CDs/DVDs
- Bit flips during transmission
- Read errors on storage devices

**Key Challenge:** How can we detect AND correct errors while using minimal extra space?

| Approach | Redundancy | Advantages | Disadvantages |
|----------|-----------|-----------|----------------|
| **Triple Copy** | 200% extra | Simple to understand | Can't fix 2+ errors; wastes space |
| **Hamming Code (16-bit)** | 25% extra | Detects & corrects 1-bit errors; Scalable | More complex |
| **Hamming Code (256-bit)** | 3% extra | Highly efficient | Requires special setup |

## Background: Richard Hamming (1940s)

Hamming worked at Bell Labs with limited computer access. Frustrated by frequent bit-read errors, he invented the first error correction code.

## Part 1: Understanding Parity Checks

### Simple Parity Check

**Idea:** Use one special "parity bit" to track if the total number of 1s is even or odd.

| Step | Count of 1s | Parity Status | Action |
|------|------------|---------------|--------|
| Original message | 7 | Odd | Set parity bit = 1 |
| After parity bit set | 8 | Even | Ready to send |

### How It Works:

- **Sender:** Sets the parity bit so total 1s = even
- **Receiver:** Counts all 1s
  - If odd → Error detected!
  - If even → No error (or even number of errors)

### Limitations:

- Detects errors but **cannot locate or fix** them
- Cannot distinguish between 1, 3, or 5 errors
- Cannot detect 2, 4, or 6 errors (even number of flips keeps parity even)

---

## Part 2: Hamming Code (16-bit Block)

### Overview

The Hamming code uses 4 parity checks to pinpoint exactly WHERE an error occurred.

| Component | Details |
|-----------|---------|
| **Block size** | 16 bits (positions 0-15) |
| **Parity bits** | Positions 0, 1, 2, 4, 8 (powers of 2) |
| **Data bits** | Remaining 11 positions |
| **Result** | Called "15-11 Hamming code" (after excluding position 0) |

### The 4 Parity Checks

Each parity check monitors a specific subset of bit positions:

| Check # | Controls Position | Monitors | Pattern |
|---------|------------------|----------|---------|
| 1 | 1 | Odd-numbered positions | 1,3,5,7,9,11,13,15 |
| 2 | 2 | Right half of grid | 2,3,6,7,10,11,14,15 |
| 3 | 4 | Odd rows | 4,5,6,7,12,13,14,15 |
| 4 | 8 | Bottom half | 8,9,10,11,12,13,14,15 |

### Key Insight: Binary Connection

Each position's binary number shows which parity checks it belongs to:

| Position | Binary | Check 1 | Check 2 | Check 3 | Check 4 |
|----------|--------|--------|--------|--------|---------|
| 3 | 0011 | ✓ | ✓ | ✗ | ✗ |
| 5 | 0101 | ✓ | ✗ | ✓ | ✗ |
| 10 | 1010 | ✗ | ✓ | ✗ | ✓ |
| 15 | 1111 | ✓ | ✓ | ✓ | ✓ |

---

## Part 3: Error Detection & Correction

### Receiver's Process

The receiver performs 4 parity checks and gets a 4-bit result:

| Check | Result = 0 | Result = 1 |
|-------|-----------|-----------|
| Check 1 (odd positions) | Even parity | Odd parity |
| Check 2 (right half) | Even parity | Odd parity |
| Check 3 (odd rows) | Even parity | Odd parity |
| Check 4 (bottom half) | Even parity | Odd parity |

**The 4-bit result is the position of the error!**

### Example:

If checks return: 1, 0, 1, 0 → Error at position 0101₂ = 5₁₀

| Check Result | Binary | Position | Action |
|-------------|--------|----------|--------|
| 0,0,0,0 | 0000 | No error | Accept message |
| 1,0,0,0 | 0001 | Position 1 | Flip bit 1 |
| 0,1,0,1 | 1010 | Position 10 | Flip bit 10 |

---

## Part 4: Extended Hamming Code (Detecting 2 Errors)

### The Problem with Position 0

- 4 parity checks give 16 outcomes
- Need 17 outcomes (1 for "no error" + 16 for each position)
- Solution: Use position 0 as an **overall parity bit**

### Extended Hamming Process

| Step | Action |
|------|--------|
| 1 | Set parity bits 1, 2, 4, 8 (as before) |
| 2 | Set position 0 to make **entire block** have even parity |
| 3 | On reception, check all 5 parity bits |

### Detection Ability:

| Error Count | Parity Check Result | Overall Parity | Receiver Knows |
|-------------|-------------------|-----------------|-----------------|
| 0 | All 0s | Even | No error ✓ |
| 1 | Non-zero | Odd | 1 error—can fix ✓ |
| 2 | Non-zero | Even | 2+ errors exist—cannot fix |

**This is called "Extended Hamming Code"**

---

## Part 5: Efficiency & Scaling

### Comparison of Different Block Sizes

| Block Size | Parity Bits | Data Bits | Efficiency |
|-----------|------------|-----------|-----------|
| 4-bit (2²) | 2 | 2 | 50% |
| 16-bit (2⁴) | 5 | 11 | 69% |
| 256-bit (2⁸) | 9 | 247 | 96% |

**Key:** Only log₂(N) parity bits needed for N-bit block!

---

## Quick Reference: Hamming Code Steps

### For Sender (Encoding):

1. Place data bits in non-power-of-2 positions
2. For each parity bit position (1, 2, 4, 8...):
   - Count 1s in its monitored subset
   - Set bit = 0 if even, = 1 if odd
3. (Extended only) Set position 0 to make total parity even

### For Receiver (Decoding):

1. Perform 4 parity checks (or more for larger blocks)
2. Record results as a binary number
3. If result = 0: No error
4. If result ≠ 0: Flip bit at that position
5. Extract data bits from non-power-of-2 positions

---

## Summary

| Concept | Definition |
|---------|-----------|
| **Parity** | Whether total count of 1s is even or odd |
| **Hamming Code** | Error correction using strategic parity checks |
| **Efficiency** | Can correct 1-bit errors with only log₂(N) overhead |
| **Elegance** | The error position emerges naturally from check results |