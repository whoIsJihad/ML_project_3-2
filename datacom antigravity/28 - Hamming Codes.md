# Hamming Codes: The GPS of Error Correction

> **Prerequisites**: [[27 - Linear Block Codes]]
> **The Problem**: Linear Block Codes can detect errors, but they don't always know *where* they are.
> **Hamming's Genius**: He realized that if we design the check matrix $\mathbf{H}$ perfectly, the syndrome won't just say "Error!", it will point to the exact bit index.

---

## 1. The Intent: Why Hamming Codes?

Recall the Parity Check Matrix $\mathbf{H}$ from the last note. It calculates the **Syndrome (S)**.

In a normal LBC, the syndrome is just a random non-zero pattern.
In a **Hamming Code**, the syndrome is the **binary address** of the error.

> [!important] The "Binary Pointer" Idea
> If bit 3 flips, the syndrome will be `011` (which is 3 in binary).
> If bit 7 flips, the syndrome will be `111` (which is 7 in binary).
> It's like having a GPS for every bit in your message.

---

## 2. The Math Constraint: The Hamming Bound

If we want to point to $n$ possible error locations (plus a "no error" state), we need $p$ parity bits such that:
$$2^p \ge n + 1$$

**Example**: For $n=7$ bits, we need $p=3$ parity bits because $2^3 = 8 \ge 7+1$.
This leaves $7 - 3 = 4$ bits for our actual data. This is the famous **Hamming(7,4)** code.

---

## 3. The Matrix Blueprint: Where do the bits go?

To make the matrix math work perfectly, we need a specific "blueprint" for where to place the parity bits. Hamming's rule is to place them at **powers of 2**:
-   Pos **1** ($2^0$)
-   Pos **2** ($2^1$)
-   Pos **4** ($2^2$)
-   Pos **8** ($2^3$)...

### How this Blueprint creates the Matrix:
1.  **Parity Bits**: Occupy the "Check" positions (1, 2, 4).
2.  **Data Bits**: Occupy all other positions (3, 5, 6, 7).
3.  **Coverage**: Each parity bit covers positions that "contain" its power of 2 in their binary address.
    -   $P_1$ (binary `001`) covers: 3, 5, 7.
    -   $P_2$ (binary `010`) covers: 3, 6, 7.
    -   $P_4$ (binary `100`) covers: 5, 6, 7.

> [!important] The Resulting Matrix
> These coverage rules are exactly what we use to fill the rows of $\mathbf{G}$ and the columns of $\mathbf{H}$. Once these matrices are built using this blueprint, we never have to think about "manual" coverage again—the matrix math handles it all automatically.

---

## 4. The Linear Perspective (G and H)

If you look at the Parity Check Matrix $\mathbf{H}$ for a Hamming(7,4) code, it looks incredibly simple. The columns are just the numbers 1 to 7 written in binary!

## 4. The Linear Matrices (G and H)

Since Hamming Codes are Linear Block Codes, they are defined by a **Generator Matrix (G)** and a **Parity Check Matrix (H)**.

### The Generator Matrix (G)
For Hamming(7,4) in systematic form, $\mathbf{G}$ is a $4 \times 7$ matrix. It takes your 4 data bits and creates the 7-bit codeword.
$$\mathbf{G} = \begin{bmatrix} 1&0&0&0 & \mid & 0&1&1 \\ 0&1&0&0 & \mid & 1&0&1 \\ 0&0&1&0 & \mid & 1&1&0 \\ 0&0&0&1 & \mid & 1&1&1 \end{bmatrix} \leftarrow [I_4 \mid P]$$

### The Parity Check Matrix (H)
The columns of $\mathbf{H}$ are the binary representations of the numbers 1 to 7. 
$$\mathbf{H} = \begin{bmatrix} 0&0&0&1&1&1&1 \\ 0&1&1&0&0&1&1 \\ 1&0&1&0&1&0&1 \end{bmatrix} \leftarrow \text{Binary values of indices 1-7}$$

> [!important] Why use the Matrix?
> You asked: "Why use $\mathbf{H}$ if I can just do manual XORs?"
> **Answer**: Because manual XORs become impossible for large codes (like Hamming(1023, 1013)). The matrix provides a **unified mathematical engine** that works for any code size. As you'll see in Phase 2 below, the manual checks are actually just the rows of $\mathbf{H}$ in action!

Let's walk through the entire lifecycle of a 4-bit message using the Hamming(7,4) code.

### Phase 1: Encoding (Sender side)

**Input Message**: $\mathbf{m} = [1, 0, 1, 1]$

**The Matrix Operation**: $\mathbf{C} = \mathbf{m} \cdot \mathbf{G}$
The codeword is the XOR sum of the rows of $\mathbf{G}$ where the message bits are `1`.
$$\mathbf{C} = 1 \cdot [1,0,0,0,0,1,1] \oplus 0 \cdot [0,1,0,0,1,0,1] \oplus 1 \cdot [0,0,1,0,1,1,0] \oplus 1 \cdot [0,0,0,1,1,1,1]$$

**Step-by-Step XOR**:
1.  Start: `1 0 0 0 0 1 1` (Row 1)
2.  Add Row 3: `1 0 1 0 1 0 1`
3.  Add Row 4: `1 0 1 1 0 1 0`

**Transmitted Codeword**: `1 0 1 1 0 1 0`

---

### Phase 2: Decoding with an Error (Receiver side)

**Situation**: The channel flips the **6th bit**.
**Received string ($\mathbf{r}$)**: `1 0 1 1 0 0 0` (originally `1`, now `0`)

**The Matrix Operation**: Syndrome $\mathbf{S} = \mathbf{r} \cdot \mathbf{H}^T$
The syndrome is the XOR sum of the **columns** of $\mathbf{H}$ where the received bits are `1`.
$$\mathbf{S} = 1 \cdot \text{Col}_1 \oplus 0 \cdot \text{Col}_2 \oplus 1 \cdot \text{Col}_3 \oplus 1 \cdot \text{Col}_4 \oplus 0 \cdot \text{Col}_5 \oplus 0 \cdot \text{Col}_6 \oplus 0 \cdot \text{Col}_7$$

**Step-by-Step XOR**:
1.  Start: `0 0 1` (Col 1)
2.  Add Col 3: `0 0 1` $\oplus$ `0 1 1` = `0 1 0`
3.  Add Col 4: `0 1 0` $\oplus$ `1 0 0` = `1 1 0`

**The GPS Syndrome**:
$\mathbf{S} = [1, 1, 0]$
Binary `110` = **Decimal 6**

**The GPS Syndrome**:
$S = [s_3, s_2, s_1] = [1, 1, 0]$
Binary `110` = **Decimal 6**

> [!tip] Matrix Connection
> Notice that $s_1, s_2, s_3$ are exactly what you get if you multiply $\mathbf{r} \cdot \mathbf{H}^T$.
> - $s_1$ is the XOR sum of bits where the **bottom row** of $H$ has a `1`.
> - $s_2$ is the XOR sum where the **middle row** of $H$ has a `1`.
> - $s_3$ is the XOR sum where the **top row** of $H$ has a `1`.
> The matrix $\mathbf{H}$ isn't "extra"—it's the **formal recipe** for the parity checks.

> [!tip] The Correction
> The syndrome points directly to **Position 6**.
> We take $r_6$ (which is 0) and flip it back to **1**.
> Valid Codeword recovered: `0 1 1 0 0 1 1`.

---

### Phase 3: The "All Good" Scenario

What if there was NO error?
**Received string ($r$)**: `0 1 1 0 0 1 1`

1.  $s_1 = 0 \oplus 1 \oplus 0 \oplus 1 = \mathbf{0}$
2.  $s_2 = 1 \oplus 1 \oplus 1 \oplus 1 = \mathbf{0}$
3.  $s_3 = 0 \oplus 0 \oplus 1 \oplus 1 = \mathbf{0}$

**Syndrome $S = [0, 0, 0]$**.
The receiver sees zero and knows the message is correct.

---

## 6. Summary: Efficiency vs. Protection

Hamming codes are **"Perfect Codes"**. They use the minimum possible number of parity bits to correct a single error.

-   **Hamming(7,4)**: 3 parity bits, corrects 1 error. Rate = 0.57.
-   **Hamming(15,11)**: 4 parity bits, corrects 1 error. Rate = 0.73.
-   **Hamming(31,26)**: 5 parity bits, corrects 1 error. Rate = 0.84.

As the block gets longer, the code becomes more efficient, but we are still only protected against **one single bit flip**. If 2 bits flip, the GPS gets "confused" and points to the wrong location.

---

> **Next Note**: [[29 - Cyclic Codes]] — How to make this math even faster using Polynomials.
