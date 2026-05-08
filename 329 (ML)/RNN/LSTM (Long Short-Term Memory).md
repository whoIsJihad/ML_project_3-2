# LSTM (Long Short-Term Memory)

## Problem Statement

Standard [[RNN (Recurrent Neural Network)]] cannot learn long-term dependencies.

After 50-100 time steps, gradients vanish (become too small).

The network forgets information from early in the sequence.

Example: predicting word in sentence "The bank manager opened the ___."
- "bank" appears 8 words earlier
- Standard RNN struggles to remember this
- LSTM solves this problem

## Core Innovation: Cell State vs Hidden State

Standard RNN: single state $h_t$.

LSTM: two states:
- **Cell state** $c_t$: long-term memory (barely modified, preserves information)
- **Hidden state** $h_t$: short-term output (changes each step)

The cell state is the key to solving vanishing gradients.

## LSTM Architecture

### Four Gates

LSTM uses four neural network layers (gates) that control information flow:

1. **Forget gate**: decide what information to remove from cell state
2. **Input gate**: decide what new information to add to cell state
3. **Cell gate**: compute candidate values to add
4. **Output gate**: decide what information to output as hidden state

Each gate is a sigmoid neuron (output between 0 and 1).

Multiplication by gate output = soft attention (0 = remove, 1 = keep).

### Equations

**Forget gate**:
$$f_t = \sigma(W_f h_{t-1} + U_f x_t + b_f)$$

**Input gate**:
$$i_t = \sigma(W_i h_{t-1} + U_i x_t + b_i)$$

**Cell candidate**:
$$\tilde{c}_t = \tanh(W_c h_{t-1} + U_c x_t + b_c)$$

**Cell state update**:
$$c_t = f_t \odot c_{t-1} + i_t \odot \tilde{c}_t$$

**Output gate**:
$$o_t = \sigma(W_o h_{t-1} + U_o x_t + b_o)$$

**Hidden state**:
$$h_t = o_t \odot \tanh(c_t)$$

Where:
- $\sigma$ is sigmoid (squashes to [0,1])
- $\tanh$ squashes to [-1,1]
- $\odot$ is element-wise multiplication
- $W_*$, $U_*$ are weight matrices
- $b_*$ are biases

## Why This Fixes Vanishing Gradients

### Analysis of Cell State Gradient

In standard RNN:
$$\frac{\partial h_t}{\partial h_{t-1}} \approx W_{hh} \cdot \tanh'(...) \quad \text{(small product)}$$

In LSTM:
$$\frac{\partial c_t}{\partial c_{t-1}} = f_t \quad \text{(just the forget gate value)}$$

The cell state gradient uses **addition** (not matrix multiplication):
$$c_t = f_t \odot c_{t-1} + i_t \odot \tilde{c}_t$$

Taking derivative w.r.t. $c_{t-1}$:
$$\frac{\partial c_t}{\partial c_{t-1}} = f_t$$

Since $f_t$ is a sigmoid output: $0 \leq f_t \leq 1$ (element-wise).

**Key difference**: 
- Standard RNN: gradient = product of many weight matrices
- LSTM: gradient flows through addition (preserves magnitude better)

Gradients don't vanish as easily over long sequences.

### Numeric Example: 50 Time Steps

**Standard RNN**:
- Gradient multiplied by $(0.9)^{50} \approx 0.005$ after 50 steps
- Gradient is 200× too small

**LSTM**:
- Forget gate values: $f_1 = 0.9, f_2 = 0.8, ..., f_{50} = 0.7$ (average $\approx 0.75$)
- Gradient multiplied by product: $0.9 \times 0.8 \times ... \times 0.7 \approx (0.75)^{50} \approx 5 \times 10^{-7}$

Wait, this is also small! Why does LSTM work?

**Answer**: The LSTM *learns* to keep forget gate close to 1 for important information.

If the network needs to remember something, it sets $f_t \approx 0.99$ at that step.

$(0.99)^{50} \approx 0.61$ — gradient is only 1.6× too small (much better).

Furthermore, the input and output gates add multiple paths for gradient flow.

**Practical behavior**:
- For important long-term information: forget gate $\approx 1.0$ (preserve cell state)
- For irrelevant information: forget gate $\approx 0.0$ (discard)
- The network **learns** when to remember and forget

## Simulation: LSTM Processing a Sequence

**Task**: Track whether parentheses are balanced in a sequence.

Sequence: `( x x ) x x x (`

Balanced pairs: (0,3), unmatched open at position 7.

### Step-by-Step Simulation

**Initial state**: $h_0 = 0$, $c_0 = 0$

**Step 1** (input = '('):
- Forget gate: $f_1 = \sigma(W_f h_0 + ...) = 0.1$ (start fresh, forget little)
- Input gate: $i_1 = \sigma(W_i h_0 + ...) = 0.8$ (accept new info)
- Cell candidate: $\tilde{c}_1 = \tanh(...) = 0.7$ (encode '(')
- Cell update: $c_1 = 0.1 \times 0 + 0.8 \times 0.7 = 0.56$ (store info about '(')
- Output gate: $o_1 = \sigma(...) = 0.3$ (don't output everything yet)
- Hidden state: $h_1 = 0.3 \times \tanh(0.56) = 0.3 \times 0.5 = 0.15$

**Step 2** (input = 'x'):
- Forget gate: $f_2 = 0.95$ (keep memory, 'x' is not special)
- Input gate: $i_2 = 0.2$ (don't add much new info)
- Cell candidate: $\tilde{c}_2 = 0.1$
- Cell update: $c_2 = 0.95 \times 0.56 + 0.2 \times 0.1 = 0.532 + 0.02 = 0.552$ (cell state barely changes)
- Output gate: $o_2 = 0.3$
- Hidden state: $h_2 \approx 0.15$

**Steps 3-6**: Similar to step 2. Cell state remains $\approx 0.56$.

**Step 7** (input = ')'):
- Forget gate: $f_7 = 0.8$ (keep some history)
- Input gate: $i_7 = 0.9$ (accept this important symbol)
- Cell candidate: $\tilde{c}_7 = -0.6$ (encode ')' with opposite sign to '(')
- Cell update: $c_7 = 0.8 \times 0.55 + 0.9 \times (-0.6) = 0.44 - 0.54 = -0.1$ (cell state shifts, indicating pair)
- Output gate: $o_7 = 0.9$ (output the decision)
- Hidden state: $h_7 = 0.9 \times \tanh(-0.1) = 0.9 \times (-0.1) = -0.09$ (signal: pair found)

**Step 8** (input = '('):
- Forget gate: $f_8 = 0.1$ (clear for new '(' because previous was closed)
- Input gate: $i_8 = 0.8$
- Cell candidate: $\tilde{c}_8 = 0.7$ (encode '(' again)
- Cell update: $c_8 = 0.1 \times (-0.1) + 0.8 \times 0.7 = 0 + 0.56 = 0.56$ (back to '(' state)
- Output gate: $o_8 = 0.3$
- Hidden state: $h_8 = 0.3 \times \tanh(0.56) = 0.15$ (same as after first '(')

**Result**: The LSTM tracked the balanced pair and detected the unmatched open paren.

The cell state preserved information across 4 irrelevant 'x' tokens (steps 2-5).

### Key Observations

1. **Forget gate stayed high (0.95)** during irrelevant symbols. Cell state didn't decay.
2. **Cell state value** ($c_t$) changed significantly only for meaningful symbols ('(' and ')').
3. **Output gate controlled** what information to expose as $h_t$.
4. The network learned these gate values through training.

## LSTM Variants

### Peephole Connections

Allow gates to access cell state directly:

$$f_t = \sigma(W_f h_{t-1} + U_f x_t + V_f c_{t-1} + b_f)$$

(Similar for other gates)

Helps timing-dependent tasks. Rarely used in modern code.

### Coupled Input-Forget Gates

Instead of separate $i_t$ and $f_t$, use:
$$i_t = 1 - f_t$$

Simpler, fewer parameters. Works similarly in practice.

### Bidirectional LSTMs (BiLSTM)

Process sequence in both directions:
- Forward LSTM: $\overrightarrow{h}_1, \overrightarrow{h}_2, ..., \overrightarrow{h}_T$ (left to right)
- Backward LSTM: $\overleftarrow{h}_T, ..., \overleftarrow{h}_1$ (right to left)

Output: $h_t = [\overrightarrow{h}_t; \overleftarrow{h}_t]$ (concatenate)

Allows using future context. Cannot be used for real-time prediction.

Example: part-of-speech tagging looks at words before and after target word.

## Computational Complexity

**Parameters per LSTM unit**: $4 \times (n_h^2 + n_x \times n_h + n_h) \approx 4 n_h (n_h + n_x)$

For comparison, standard RNN: $n_h(n_h + n_x)$

**LSTM is 4× more parameters** than RNN.

For $n_h = 512, n_x = 100$:
- RNN: $512 \times (512 + 100) = 312,832$ parameters
- LSTM: $4 \times 512 \times 612 = 1,251,328$ parameters

**Computation per step**: ~4× more than RNN per time step.

But quality improvement is often 10-100×.

## When to Use LSTM

✓ Long sequences (>50 steps)
✓ Dependencies spanning many time steps
✓ Language modeling, machine translation
✓ Any task where standard RNN fails to learn

✗ Very short sequences (< 20 steps) — overhead not worth it
✗ Real-time, low-latency applications — computational cost high
✗ Very long sequences with modern hardware (Transformers often better)

## Comparison with [[GRU (Gated Recurrent Unit)]]

| Aspect | LSTM | GRU |
|--------|------|-----|
| Parameters | 4× RNN | 3× RNN |
| Hidden states | 2 (cell + hidden) | 1 (hidden) |
| Gates | 4 (forget, input, cell, output) | 2 (reset, update) |
| Performance | Slightly better on long sequences | Faster, similar for most tasks |
| Interpretability | More transparent | Simpler |

In practice, GRU often performs similarly with fewer parameters.

## Summary

LSTM solves vanishing gradients through gating mechanism.

Cell state flows through addition (not matrix mult), preserving gradient magnitude.

Network learns when to remember and forget through gate values.

Works well for sequences up to 100-1000 steps.

Beyond that, use Transformers or [[Attention Mechanism]].
