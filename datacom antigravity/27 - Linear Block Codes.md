# Linear Block Codes (LBC): From First Principles

> **The Problem**: We want to add $r$ redundant bits to $k$ message bits. But how do we decide *which* bits to add so we can actually find errors later?
> **The Solution**: Linear Algebra.

---

## 1. The Intent: Why "Linear"?

Imagine you have a 2-bit message ($k=2$). There are 4 possible messages: `00, 01, 10, 11`.
You want to send 3-bit codewords ($n=3$). There are 8 possible 3-bit strings.

**The "Lookup Table" Approach (Bad)**:
You could just pick 4 random strings:
- `00` $\to$ `101`
- `01` $\to$ `011`
... This works, but for a 100-bit message, your table would need $2^{100}$ entries. Impossible.

**The "Linear" Approach (Good)**:
We want a **formula** (a mathematical engine) that takes any message and spits out a codeword.
Specifically, we want a formula where:
> If you add two messages, their codewords also add up. 
> **Message A + Message B = Codeword A + Codeword B**

This "Linearity" allows us to use **Matrices** instead of tables.

---

## 2. The Engine: The Generator Matrix (G)

Instead of a table, we pick $k$ "basis" codewords. Any other codeword is just a combination of these.

### How it works:
If your message is $\mathbf{m} = [m_1, m_2]$, your codeword is:
$$\mathbf{C} = m_1 \cdot (\text{Basis 1}) \oplus m_2 \cdot (\text{Basis 2})$$

We stack these basis codewords into a matrix $\mathbf{G}$:
$$\mathbf{C} = \mathbf{m} \cdot \mathbf{G} \pmod 2$$

> [!tip] First Principle Intuition
> $\mathbf{G}$ is like a **mixing console**. Each row of $\mathbf{G}$ is a "flavor" of codeword. Your message bits tell the console how much of each flavor to mix into the final output.

![LBC Encoding Pipeline|870](file:///mnt/Data/3-2/datacom%20antigravity/diagrams/lbc_pipeline.png)

---

## 3. The Systematic Form: Keeping it Simple

We usually want the original message to stay "visible" in the codeword.
To do this, we make the first part of $\mathbf{G}$ an **Identity Matrix** ($I$).

**Example (k=3, n=6)**:
$$\mathbf{G} = \underbrace{\begin{bmatrix} 1 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & 0 & 1 \end{bmatrix}}_{I \text{ (Message stays same)}} \mid \underbrace{\begin{bmatrix} 1 & 1 & 0 \\ 0 & 1 & 1 \\ 1 & 0 & 1 \end{bmatrix}}_{P \text{ (Parity bits recipe)}}$$

If your message is `1 0 1`, the first 3 bits of the codeword will be `1 0 1`. The rest are calculated by $P$.

---

## 4. The Gatekeeper: The Parity Check Matrix (H)

How does the receiver know if a received string $\mathbf{r}$ is a valid codeword?
They use a "check" matrix $\mathbf{H}$.

### The Orthogonality Principle
Every row in $\mathbf{G}$ is designed to be "orthogonal" to every row in $\mathbf{H}$.
This means:
$$\mathbf{G} \cdot \mathbf{H}^T = 0 \pmod 2$$

> [!important] The "Zero" Test
> If $\mathbf{r}$ is a valid codeword, then $\mathbf{r} \cdot \mathbf{H}^T$ **must be zero**.
> If it's NOT zero, the result is called the **Syndrome (S)**. The syndrome is your error alarm.

---

## 5. Worked Example: (6, 3) Code from Scratch

### Step 1: The Setup (Designer)
We choose a (6, 3) code. $k=3$ (data) and $n=6$ (total). Parity bits $r = 3$.
We pick a Generator Matrix in systematic form $\mathbf{G} = [\mathbf{I}_k \mid \mathbf{P}]$:
$$\mathbf{G} = \begin{bmatrix} 1&0&0 & \mid & 1&1&0 \\ 0&1&0 & \mid & 0&1&1 \\ 0&0&1 & \mid & 1&0&1 \end{bmatrix}$$

### Step 2: Create the Check Matrix (Receiver)
Using the rule $\mathbf{H} = [\mathbf{P}^T \mid \mathbf{I}_r]$:
$$\mathbf{H} = \begin{bmatrix} 1&0&1 & \mid & 1&0&0 \\ 1&1&0 & \mid & 0&1&0 \\ 0&1&1 & \mid & 0&0&1 \end{bmatrix}$$

---

### Step 3: Encoding (Sender)
**Input Message**: $\mathbf{m} = [1, 1, 0]$
**Calculation**: $\mathbf{C} = \mathbf{m} \cdot \mathbf{G}$
$C = 1 \cdot [\text{Row 1 of } G] \oplus 1 \cdot [\text{Row 2 of } G] \oplus 0 \cdot [\text{Row 3 of } G]$
$C = [1, 0, 0, 1, 1, 0] \oplus [0, 1, 0, 0, 1, 1] \oplus [0, 0, 0, 0, 0, 0]$
**Output Codeword**: `1 1 0 1 0 1` (Note: First 3 bits are our data!)

---

### Step 4: Decoding with an Error (Receiver)
**Situation**: The 4th bit flips ($1 \to 0$).
**Received**: $\mathbf{r} = [1, 1, 0, \mathbf{0}, 0, 1]$

**Calculation**: Syndrome $\mathbf{S} = \mathbf{r} \cdot \mathbf{H}^T$
(This is the same as XOR-ing the columns of $H$ where $r$ has a `1`)
$S = (\text{Col 1}) \oplus (\text{Col 2}) \oplus (\text{Col 6})$
$S = \begin{bmatrix} 1 \\ 1 \\ 0 \end{bmatrix} \oplus \begin{bmatrix} 0 \\ 1 \\ 1 \end{bmatrix} \oplus \begin{bmatrix} 0 \\ 0 \\ 1 \end{bmatrix}$
$S = \begin{bmatrix} 1 \oplus 0 \oplus 0 \\ 1 \oplus 1 \oplus 0 \\ 0 \oplus 1 \oplus 1 \end{bmatrix} = \begin{bmatrix} \mathbf{1} \\ \mathbf{0} \\ \mathbf{0} \end{bmatrix}$

**Decision**: Since $\mathbf{S} \ne 0$, the receiver knows an error occurred. In a standard LBC, they would now use a "Syndrome Table" to map `100` to the 4th bit position to fix it.

---

## Summary: The Workflow
1.  **System Designer**: Picks $\mathbf{G}$. Derives $\mathbf{H}$.
2.  **Sender**: Multiplies message by $\mathbf{G}$ to get Codeword.
3.  **Receiver**: Multiplies received bits by $\mathbf{H}^T$.
    -   If result is $0$: "Looks good to me!"
    -   If result is $\ne 0$: "Error detected! Here is the syndrome pattern."

> [!note] Why stop at detection?
> In the next note, we'll see how **Hamming Codes** use the syndrome not just as an alarm, but as a **GPS coordinate** to find and fix the exact bit that flipped.

> **Next Note**: [[28 - Hamming Codes]]
