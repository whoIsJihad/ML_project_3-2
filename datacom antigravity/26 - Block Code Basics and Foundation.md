# Block Code Basics: The Strategy of Redundancy

> **The Problem**: You want to tell your friend "YES" or "NO" over a noisy radio. If you just say "YES," and a static pop happens, they might hear "ESS" or "Y-S" and be confused.
> **The Solution**: Use a bigger word. If you say "AFFIRMATIVE" and "NEGATIVE," a little static won't hide the intent. This is the first principle of Channel Coding.

---

## 1. The Intent: Structured Redundancy

In data communications, we don't just send raw bits. We add extra bits to protect the message.

-   **Unprotected**: `1` (1 bit)
-   **Protected**: `111` (3 bits)

If the middle bit flips in the protected version (`101`), you still know it was probably a `1`. You've used **redundancy** to fight **noise**.

---

## 2. The Vocabulary: (n, k) Notation

In every block code, we talk about two numbers:
-   **k**: The number of **Message bits** (the real information).
-   **n**: The number of **Codeword bits** (the total bits sent).
-   **r = n - k**: The **Redundancy** (the extra insurance bits).

![Codeword Structure](file:///mnt/Data/3-2/datacom%20antigravity/diagrams/codeword_structure.png)

> [!important] The Efficiency Trade-off
> **Code Rate (R) = k / n**
> -   If $R = 1$, you are very fast but have zero protection.
> -   If $R = 1/3$, you are 3x slower but very robust.

---

## 3. The Geography: Hamming Distance

How do we measure "how good" a code is? We use **Distance**.

### Hamming Distance ($d$)
The number of bits you have to flip to turn one string into another.
-   `101` and `100` $\to d = 1$ (1 bit differs).
-   `101` and `010` $\to d = 3$ (all bits differ).

### Minimum Distance ($d_{\min}$)
This is the "gap" between your valid codewords. If your valid codewords are `000` and `111`, the $d_{\min} = 3$. 

> [!tip] The First Principle of Correction
> If $d_{\min}$ is large, a small amount of noise won't be enough to "push" one valid codeword into looking like another valid codeword.

![Error Correction: The Sphere Packing Concept](file:///mnt/Data/3-2/datacom%20antigravity/diagrams/hamming_balls.png)

---

## 4. Error Detection vs. Correction

-   **To Detect $s$ errors**: You need $d_{\min} \ge s + 1$.
    -   *Logic*: The noise moves you away from a valid codeword, but not far enough to hit a different one.
-   **To Correct $t$ errors**: You need $d_{\min} \ge 2t + 1$.
    -   *Logic*: You are still "closer" to the original codeword than any other.

---

## 5. Primitive Examples

### 1. Parity Check (Detects 1 error)
Add one bit so the total number of 1s is even.
-   `101` $\to$ `1010`
-   If received `1011`, the total 1s are 3 (odd) $\to$ **Error!**

### 2. Repetition Code (Corrects 1 error)
Repeat each bit 3 times.
-   `1` $\to$ `111`
-   If received `101`, the **Majority Vote** says it's a `1`.

---

## Summary
1.  **Block Codes** group bits together.
2.  **Redundancy** ($n-k$) is the cost of reliability.
3.  **Hamming Distance** is the measure of how much noise a code can survive.

> **Next Step**: Basic parity is okay, but how do we build complex codes for 1000s of bits? We use matrices.
> **Next Note**: [[27 - Linear Block Codes]]
