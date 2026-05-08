# The Viterbi Algorithm: Decoding and Trellis Math

> **Prerequisites**: [[32 - Convolutional Codes: Foundations and Encoding]]
> **Course**: CSE 311 — Data Communication (Md Asib Rahman)

---

## PART 1: The Decoding Problem

In Convolutional coding, we don't just "calculate" the answer. Because the code has memory, a single bit error in the received stream could make the whole sequence look invalid.

**The Goal**: Find the path through the Trellis that is "closest" to the received sequence. This is called **Maximum Likelihood Decoding**.

---

## PART 2: The Viterbi Algorithm (Intuition)

Instead of checking every possible path (which grows exponentially), the Viterbi algorithm uses **Dynamic Programming**.

> [!tip] The "Survivor" Principle
> If two paths reach the same state at the same time, we only keep the one with the best "score" (smallest error count). We discard the other because it can never be part of the optimal overall path.

---

## PART 3: The ACS Process (Add-Compare-Select)

This is the core "heartbeat" of the Viterbi decoder. At every time step, for every state:

1.  **ADD**: Add the branch metric (error count for this transition) to the existing path metric.
2.  **COMPARE**: Look at the two paths entering the current state.
3.  **SELECT**: Keep the one with the lower total metric (the "Survivor"). Store which previous state it came from (the "Back-pointer").

![Viterbi ACS Operation](file:///mnt/Data/3-2/datacom%20antigravity/diagrams/viterbi_acs.png)

---

## PART 4: Worked Example: Decoding [01 10 11 00 00]

Let's decode 5 received pairs using a $K=3$ Trellis.

### 1. The Metric: Hamming Distance
We count how many bits differ between what we **received** and what the encoder **would have sent** on that branch.

### 2. The Walkthrough
-   **Step 1 ($t=1$)**: Received `01`. 
    -   From `00` to `00` (expects `00`) $\to$ Metric 1.
    -   From `00` to `10` (expects `11`) $\to$ Metric 1.
-   **Step 2 ($t=2$)**: Received `10`.
    -   Path `00->00->00` $\to$ Cumulative Metric: $1 + (\text{dist between } 10, 00) = 1+1 = 2$.
    -   Path `00->10->01` $\to$ Cumulative Metric: $1 + (\text{dist between } 10, 10) = 1+0 = 1$.
-   **Continuing...**: We repeat this for all 5 steps, always discarding the "loser" when two paths meet in a state.

### 3. Traceback
Once we reach the end ($t=5$), we find the state with the **lowest total metric**. We then follow our "back-pointers" to find the sequence of input bits that produced that path.

---

## PART 5: Key Performance Metrics

### 1. Free Distance ($d_{free}$)
The minimum Hamming distance between any two distinct codewords in the code.
-   Just like $d_{\min}$ in block codes, $d_{free}$ determines how many errors we can correct.
-   For a standard $K=3, R=1/2$ code, $d_{free} = 5$.

### 2. Hard vs. Soft Decisions
-   **Hard Decision**: You decide if a bit is `0` or `1` before decoding (uses Hamming distance).
-   **Soft Decision**: You pass the raw voltage levels to the Viterbi algorithm (uses Euclidean distance).
    -   *Soft decision Viterbi is ~2dB more powerful than hard decision.*

---

## PART 6: Summary Comparison

| Metric | Block Codes (Note 26) | Viterbi (Convolutional) |
| :--- | :--- | :--- |
| **Search Space** | Fixed codewords | Trellis paths |
| **Logic** | Syndrome lookup/math | Dynamic programming |
| **Latency** | Wait for whole block | High (Traceback depth) |
| **Efficiency** | Excellent for detection | Excellent for correction |

---

> **Next Note**: [[31 - ECC Comparison and Synthesis]] — Updated with Convolutional details.
