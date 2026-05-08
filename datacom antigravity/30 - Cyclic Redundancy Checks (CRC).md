# Cyclic Redundancy Checks (CRC): Digital Fingerprints

> **Prerequisites**: [[29 - Cyclic Codes]]
> **The Objective**: We don't want to fix errors (that's too expensive/slow for high-speed networks). We just want to know *if* an error happened so we can throw the packet away and ask for a new one.
> **The Tool**: The "Remainder" from a long division.

---

## 1. The Intent: Why a Remainder?

Imagine you have a long number like `12345`. You want to send it to a friend. 
You decide on a "Secret Divisor," say `7`. 

1.  You divide `12345` by `7`. The remainder is `4`.
2.  You send your friend the number `12345` AND the remainder `4`.
3.  Your friend divides `12345` by `7`. If they get a remainder of `4`, they assume the number is correct.

> [!important] The CRC Philosophy
> A CRC is just a **mathematical remainder** that acts as a fingerprint for your data. If even one bit changes, the "division" will result in a completely different remainder.

---

## 2. The Algorithm: Long Division (Binary Style)

In computers, we don't use regular numbers; we use bit-strings (Polynomials). And we don't use regular subtraction; we use **XOR**.

### Steps to generate a CRC:
1.  **Padding**: Append $L-1$ zeros to your data (where $L$ is the length of your divisor).
2.  **XOR Division**: Perform long division.
3.  **Transmission**: Send the [Data + Remainder].

![CRC Division Visual](file:///mnt/Data/3-2/datacom%20antigravity/diagrams/crc_division.png)

---

## 4. Worked Example: Step-by-Step

**Data**: `101101` (6 bits)
**Generator ($G$)**: `1101` (4 bits)

1.  **Padding**: Append $4-1=3$ zeros $\to$ `101101 000`
2.  **XOR Division**:

```text
            110001 (Quotient)
      ____________
1101 | 101101000
       1101
       ----
       01100      (Shift down)
        1101
        ----
        00011     (Shift down - doesn't fit)
         0000
         ----
         00110    (Shift down - doesn't fit)
          0000
          ----
          01100   (Shift down)
           1101
           ----
           00010  <- REMAINDER
```

3.  **Resulting CRC**: `010`
4.  **Final Transmitted Codeword**: `101101` + `010` = **`101101010`**

### Verification (At Receiver)
The receiver divides `101101010` by `1101`. 
If the math is correct, the remainder will be exactly **`000`**.

---

## 4. Hardware Implementation

Because CRC is just polynomial division, we use the **LFSR** (Linear Feedback Shift Register) we saw in [[29 - Cyclic Codes]].

-   Network cards (Ethernet) do this at **gigabit speeds**. 
-   It takes zero CPU power because it's built into the hardware chips.

---

## 5. Why is CRC so good?

Standard "Checksums" (just adding bits) can be fooled if two bits flip in opposite directions.
**CRC is much smarter**:
-   Detects **all** single-bit errors.
-   Detects **all** double-bit errors.
-   Detects **all** burst errors (clumps of noise) shorter than the CRC itself.

| Standard | Divisor Size | Best For |
| :--- | :--- | :--- |
| **CRC-16** | 16 bits | USB, Modbus |
| **CRC-32** | 32 bits | **Ethernet**, Gzip, PNG images |

---

## Summary
-   **CRC** is about detection, not correction.
-   It uses **XOR division**.
-   The **remainder** is the only thing that matters.
-   It is the **global standard** for data reliability on the internet.

---

> **Next Note**: [[31 - ECC Comparison and Synthesis]] — The final overview of all coding types.
