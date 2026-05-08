# Convolutional Codes: Foundations and Encoding

> **Prerequisites**: [[26 - Block Code Basics and Foundation]]
> **Course**: CSE 311 — Data Communication (Md Asib Rahman)

---

## PART 1: Why Convolutional Codes?

### 1.1 Block Codes vs. Convolutional Codes
So far, we've looked at **Block Codes** (Hamming, Cyclic, CRC). These process data in fixed-size chunks:
-   **Block Codes**: Take $k$ bits, add $r$ bits, spit out $n$ bits. No memory.
-   **Convolutional Codes**: Process a **continuous stream** of bits. The output for the current bit depends on the current input **AND** previous inputs stored in memory.

| Feature        | Block Codes            | Convolutional Codes             |
| :------------- | :--------------------- | :------------------------------ |
| **Input**      | Fixed blocks ($k$)     | Continuous stream               |
| **Memory**     | No memory (stateless)  | Memory-based (state machine)    |
| **Redundancy** | Spatial (within block) | Temporal (over time)            |
| **Best For**   | Bursty data / Packets  | Streaming / Real-time / Low SNR |

### 1.2 Real-World Use
Convolutional codes are the "workhorses" of wireless communication because they handle noise much better than block codes at low signal levels.
-   **NASA Deep Space**: Voyager and Pioneer probes.
-   **Cellular Networks**: 3G and early LTE control channels.
-   **Satellite TV**: DVB standards.

---

## PART 2: The Encoder Structure

### 2.1 How it Works: The Shift Register
The heart of a convolutional encoder is a **Shift Register**. As each new bit enters, the old bits move one step to the right.

-   **Constraint Length ($K$)**: The total number of bits that influence the output (current bit + memory).
-   **Generator Sequences ($g$ strips)**: These define which "taps" (stages of the register) are XORed together to produce each output bit.

![Convolutional Encoder Structure](file:///mnt/Data/3-2/datacom%20antigravity/diagrams/conv_encoder.png)

### 2.2 Parameters & Notation (n, k, K)
-   **$n$**: Output bits produced per input cycle.
-   **$k$**: Input bits per cycle (usually $1$).
-   **$K$**: Constraint length.
-   **Code Rate ($R$)**: $k/n$. (Commonly $1/2$ or $1/3$).

> [!important] The "State"
> The **State** of the encoder is defined by the bits currently in the memory stages. 
> For a $K=3$ encoder, there are $K-1 = 2$ bits of memory, leading to $2^2 = 4$ possible states: `00, 10, 01, 11`.

---

## PART 3: Visualizing the Encoder

### 3.1 State Diagram
The encoder is a finite state machine. Each input bit causes a transition from the current state to a new state and produces specific output bits.

![Convolutional State Diagram](file:///mnt/Data/3-2/datacom%20antigravity/diagrams/conv_state_diagram.png)

### 3.2 Trellis Diagram
The Trellis is the most important visualization for decoding. It expands the state diagram over **time**.
-   **Vertical**: Possible states.
-   **Horizontal**: Time steps (one per input bit).

![Convolutional Trellis Diagram](file:///mnt/Data/3-2/datacom%20antigravity/diagrams/conv_trellis.png)

---

## PART 4: Worked Example: Encoding [1, 1, 0]

Let's use a **Rate 1/2, K=3** encoder with:
-   $g_1 = [1, 1, 1]$ (Taps all stages)
-   $g_2 = [1, 0, 1]$ (Taps current and last stage)

**Initial State**: `00`

1.  **Input 1**:
    -   Register: `[1, 0, 0]`
    -   $X_1 = 1 \oplus 0 \oplus 0 = 1$
    -   $X_2 = 1 \oplus 0 = 1$
    -   **Output**: `11`, **New State**: `10`
2.  **Input 1**:
    -   Register: `[1, 1, 0]`
    -   $X_1 = 1 \oplus 1 \oplus 0 = 0$
    -   $X_2 = 1 \oplus 0 = 1$
    -   **Output**: `01`, **New State**: `11`
3.  **Input 0**:
    -   Register: `[0, 1, 1]`
    -   $X_1 = 0 \oplus 1 \oplus 1 = 0$
    -   $X_2 = 0 \oplus 1 = 1$
    -   **Output**: `01`, **New State**: `01`

**Final Codeword**: `11 01 01`

---

## PART 5: Tail Bits (The "Flush")

To make decoding easier, we usually add $K-1$ zeros at the end of our data. 
-   **Intent**: This "flushes" the memory and forces the encoder back to the `00` state.
-   **Benefit**: The receiver knows exactly where the message ends, which improves accuracy at the final steps.

---

> **Next Note**: [[33 - The Viterbi Algorithm]] — How we undo this "convolution" to recover the message from noise.
