# Cyclic Codes: Polynomial Magic

> **Prerequisites**: [[27 - Linear Block Codes]]
> **The Problem**: General Linear Block Codes use Matrix Multiplication. That's fine for software, but in hardware (chips), matrices are slow and use too many wires.
> **The Solution**: Treat bit-strings as **Polynomials**. This allows us to use simple "Shift Registers" to do all the math.

---

## 1. The Intent: Why "Cyclic" and why "Polynomials"?

In the last notes, we used **Matrices**. But matrices have a problem: to check a long codeword, you need a giant chip with thousands of wires. 

**The Cyclic Solution**: 
A code is **Cyclic** if every time you perform a **Cyclic Shift** (rotating the bits), you get another valid codeword.

> [!important] Cyclic Shift vs. Linear Shift
> - **Linear Shift (Padding)**: Shifting bits and filling the empty spot with a `0`. (`1101` $\to$ `11010`)
> - **Cyclic Shift (Wrapping)**: Shifting bits and taking the bit that "falls off" the end and putting it back at the start.
>   - Start: `1 1 0 1`
>   - Shift 1: `1 1 1 0` (The `1` from the end wrapped around to the front)
>   - Shift 2: `0 1 1 1`
>   - Shift 3: `1 0 1 1`

### Why does this property matter?
1.  **Memory Efficiency**: Because codewords are just rotations of each other, we don't need to store a giant $\mathbf{G}$ matrix. We only need to store **one single pattern** (the Generator).
2.  **Hardware Speed**: Rotating bits in a circle is extremely fast and uses very few wires.

---

## 2. The Bridge: From Bits to Polynomials

To do math with shifts, we represent a string like `1011` as a math equation:
-   Pos 0: `1` $\to 1 \cdot x^0 = 1$
-   Pos 1: `0` $\to 0 \cdot x^1 = 0$
-   Pos 2: `1` $\to 1 \cdot x^2 = x^2$
-   Pos 3: `1` $\to 1 \cdot x^3 = x^3$
-   **Polynomial**: $1 + x^2 + x^3$

> [!important] The First Principle
> -   **Adding** polynomials = XOR-ing bits. 
> -   **Multiplying by $x$** = A Linear Shift (padding a `0` at the end).
> -   **Modulo $(x^n + 1)$** = The "Wrapper". It takes any bit that exceeds length $n$ and puts it back at position 0. This creates the **Cyclic** effect.
> -   **Dividing** = Finding if a bit pattern "contains" the generator pattern.

---

## 3. The Engine: The Generator Polynomial g(x)

Instead of a Generator Matrix $\mathbf{G}$, we use a **Generator Polynomial** $g(x)$.

### How to Encode (The Intuition)
To encode a message $m(x)$, you just multiply it by $g(x)$:
$$C(x) = m(x) \cdot g(x)$$

**Example**:
Message $m = 101$ ($1 + x^2$)
Generator $g = 11$ ($1 + x$)
Codeword $C(x) = (1 + x^2)(1 + x) = 1 + x + x^2 + x^3$
Codeword = `1111`

---

## 4. Systematic Encoding: The Division Intuition

Usually, we want the message bits to stay at the front. To do this, we use **Polynomial Division**.

1.  **Shift the message**: Multiply $m(x)$ by $x^{n-k}$ (pads it with zeros).
2.  **Divide by g(x)**: The **remainder** of this division is your parity bits!

> [!important] The "Remainder" Logic
> Just like in normal math, $Dividend = Quotient \times Divisor + Remainder$.
> If we subtract (XOR) the remainder from the dividend, the result is **perfectly divisible** by the divisor. 
> This is exactly how we ensure the receiver can "check" the codeword!

---

## 5. Hardware: The Shift Register (LFSR)

This is the real reason cyclic codes are everywhere. You can implement polynomial division using a string of "Flip-Flops" and XOR gates.

![LFSR Encoder Circuit](file:///mnt/Data/3-2/datacom%20antigravity/diagrams/lfsr_encoder.png)

-   Each bit of the message is shifted in one by one.
-   The XOR gates (taps) represent the coefficients of $g(x)$.
-   After $k$ shifts, the bits left in the registers are your **CRC / Parity bits**.

---

## 6. Worked Example: (7,4) Cyclic Code

**Given**: $g(x) = x^3 + x + 1$ (Binary: `1011`).
**Message**: `1100` ($1 + x$).

### Step 1: Prepare the Dividend
We want a systematic codeword, so we shift the message by $n-k = 3$ positions.
- $m(x) \cdot x^3 = (1 + x) \cdot x^3 = x^3 + x^4$
- Binary Dividend: `1 1 0 0 | 0 0 0` (The zeros are placeholders for the CRC).

### Step 2: Binary Long Division (Modulo-2)
We divide the dividend by $g(x) = 1011$.

```text
            1111 (Quotient - ignored)
      __________
1011 | 1100000
       1011
       ----
       01110   (Shift down next bit)
        1011
        ----
        01010  (Shift down next bit)
         1011
         ----
         00010 (Shift down next bit)
          0000 (Divisor doesn't fit)
          ----
          0010 <- REMAINDER
```
*(Note: Every time the leading bit is 1, we XOR with the divisor. If it's 0, we just shift.)*

**Result**: Remainder = `010` ($x$).

### Step 3: Form the Codeword
Codeword = [Original Message] + [Remainder]
Codeword = `1 1 0 0` + `0 1 0` = **`1 1 0 0 0 1 0`**

---

## Summary
-   **Cyclic Codes** use Polynomial math.
-   **Encoding** is just multiplication or division.
-   **Hardware** is just a simple shift register (LFSR).
-   This efficiency is why they are used for almost all practical error detection (CRCs).

---

> **Next Note**: [[30 - Cyclic Redundancy Checks (CRC)]] — Putting cyclic codes to work in the real world.
