# Recurrent Neural Networks (RNNs)

## Definition

A **recurrent neural network** is a class of artificial neural networks designed to process sequences. 
It maintains hidden state across time steps. 
This state captures information from previous inputs.
The hidden state updates deterministically at each new input.

## Core Characteristic: Parameter Sharing Across Time

Standard feedforward networks have separate parameters for each layer.
RNNs reuse the same parameters across multiple time steps.

Consider processing a sequence: $x_1, x_2, x_3, ..., x_T$

Each element is processed by the **same set of weights and biases**.
This is fundamentally different from stacking $T$ separate networks.

**Why this matters**: Parameter sharing enables learning temporal dependencies with constant memory. 
A feedforward network needs $T \times n$ parameters to process sequences of length $T$ with $n$ hidden units.
An RNN needs only $n^2 + n$ parameters regardless of sequence length (approximately).

## The Hidden State

The hidden state $h_t$ summarizes all information from inputs $x_1$ through $x_t$.

$$h_t = f(h_{t-1}, x_t)$$

Where:
- $h_{t-1}$ is the previous hidden state (stores past information)
- $x_t$ is the current input
- $f$ is a function (typically nonlinear) that combines them
- $h_t$ is the new hidden state passed to the next time step

The hidden state is the **only mechanism for temporal information flow**.

## Basic RNN Equations

The simplest RNN uses these update rules:

$$h_t = \tanh(W_{hh} h_{t-1} + W_{xh} x_t + b_h)$$

$$y_t = W_{hy} h_t + b_y$$

Where:
- $W_{hh}$ connects previous hidden state to current hidden state (shape: $[n_h \times n_h]$)
- $W_{xh}$ connects input to hidden state (shape: $[n_x \times n_h]$)
- $W_{hy}$ connects hidden state to output (shape: $[n_h \times n_y]$)
- $b_h$, $b_y$ are biases
- $n_h$ = hidden dimension, $n_x$ = input dimension, $n_y$ = output dimension

## Numeric Example: Character-Level Processing

Process sequence "cat" one character at a time.

**Setup**: 
- Vocabulary size = 10 (characters mapped 0-9)
- Hidden dimension $n_h = 3$
- Input dimension $n_x = 10$ (one-hot encoded)
- Output dimension $n_y = 10$

**Initial state**: $h_0 = [0, 0, 0]^T$

**Input sequence**: 'c' → 'a' → 't'
- One-hot: $[0,0,1,0,...]$ → $[1,0,0,0,...]$ → $[0,0,0,1,...]$

**Step 1** (Process 'c'):
- $W_{xh} x_1 = \begin{bmatrix} -0.1 \\ 0.3 \\ 0.2 \end{bmatrix}$ (first 3 rows of $W_{xh}$)
- $W_{hh} h_0 = 0$ (since $h_0 = 0$)
- Pre-activation: $\begin{bmatrix} -0.1 \\ 0.3 \\ 0.2 \end{bmatrix} + b_h$
- After $\tanh$: $h_1 = \begin{bmatrix} -0.10 \\ 0.29 \\ 0.20 \end{bmatrix}$

**Step 2** (Process 'a'):
- $W_{xh} x_2 = \begin{bmatrix} 0.1 \\ -0.2 \\ 0.1 \end{bmatrix}$
- $W_{hh} h_1 = \begin{bmatrix} 0.05 \\ -0.08 \\ 0.12 \end{bmatrix}$ (different since $h_1 \neq 0$)
- Pre-activation: $\begin{bmatrix} 0.15 \\ -0.28 \\ 0.22 \end{bmatrix}$
- After $\tanh$: $h_2 = \begin{bmatrix} 0.15 \\ -0.27 \\ 0.22 \end{bmatrix}$

**Step 3** (Process 't'):
- Similar process, but uses $h_2$ as previous state
- Final hidden state $h_3$ contains information from all three characters

The hidden state accumulates information. Notice how $h_2$ differs from $h_1$ due to the recurrent connection $W_{hh}$.

## Three Core Architectures

### 1. Many-to-One
**Input**: Sequence of length $T$.
**Output**: Single prediction.

Example: sentiment analysis of a sentence.
- Input: word sequence
- Output: sentiment score (1 value)

Only the final hidden state $h_T$ is used for prediction.

### 2. One-to-Many
**Input**: Single element.
**Output**: Sequence of length $T$.

Example: image captioning.
- Input: image (encoded as vector)
- Output: sequence of words

The input sets initial state. Each step predicts next word.

### 3. Many-to-Many
**Input**: Sequence of length $T$.
**Output**: Sequence of length $T$ (or different length).

Example: machine translation.
- Input: sentence in language A
- Output: sentence in language B

Every hidden state produces an output. Most common in real applications.

## Why Standard RNNs Struggle: Vanishing Gradients

[[Backpropagation Through Time]] reveals a fundamental problem.

Gradients flow backward through time steps.
To update $W_{hh}$, we compute derivatives through many applications of $\tanh(W_{hh} h_{t-1} + ...)$.

Each $\tanh$ application compresses gradients (derivative bounded by 1).
After many time steps, gradients become exponentially small.

**Numeric illustration**:
- Gradient at step $t$: $\nabla_{W_{hh}} \mathcal{L}_t$
- This depends on product of derivatives: $\prod_{i=1}^{t} \frac{\partial h_i}{\partial h_{i-1}}$
- Each factor ≤ 1 (for $\tanh$)
- Product of 50 factors each = 0.9: $(0.9)^{50} \approx 0.005$
- Gradient is 200× smaller than it should be

This makes learning long-range dependencies nearly impossible.

**Result**: RNNs cannot effectively learn patterns spanning >10-20 time steps.

## Solutions to Vanishing Gradients

Two main architectural improvements:

1. **[[LSTM (Long Short-Term Memory)]]**: Introduces gating mechanisms and separate cell state. Allows gradients to flow unchanged through time steps.

2. **[[GRU (Gated Recurrent Unit)]]**: Simplified gating mechanism. Fewer parameters than LSTM.

Both fundamentally solve the vanishing gradient problem through architectural design, not just parameter initialization.

## Applications

- **Language modeling**: Predict next character/word given history
- **Machine translation**: [[Sequence-to-Sequence Models]]
- **Time series prediction**: Stock prices, weather forecasting
- **Video understanding**: Process frames sequentially
- **Speech recognition**: Convert audio sequences to text
- **Named entity recognition**: Tag words in sequences

## Key Disadvantages

1. **Computational expense**: Cannot parallelize across time steps easily (must process sequentially)
2. **Training difficulty**: Vanishing/exploding gradients require careful tuning
3. **Limited memory**: Standard RNN hidden state often insufficient for very long sequences
4. **Slow inference**: Processing sequences one step at a time

## Related Concepts

- [[Backpropagation Through Time]] - How RNNs are trained
- [[LSTM (Long Short-Term Memory)]] - Most successful RNN variant
- [[GRU (Gated Recurrent Unit)]] - Simpler alternative to LSTM
- [[Sequence-to-Sequence Models]] - RNNs for translation tasks
- [[Attention Mechanism]] - Modern alternative to pure RNNs
- [[Transformers]] - State-of-the-art sequence model (non-recurrent)
- [[Neural Networks Basics]] - Prerequisite: standard feedforward networks
- [[Backpropagation]] - Prerequisite: how neural networks learn
- [[Calculus for Neural Networks]] - Prerequisite: derivatives and chain rule

## Next Steps

To understand RNNs deeply:
1. Review [[Neural Networks Basics]] if feedforward networks are unfamiliar
2. Study [[Backpropagation Through Time]] to understand training
3. Learn [[LSTM (Long Short-Term Memory)]] for practical implementations
4. Explore [[Sequence-to-Sequence Models]] for real applications
