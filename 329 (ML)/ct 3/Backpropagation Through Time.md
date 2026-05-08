# Backpropagation Through Time (BPTT)

## Definition

**Backpropagation Through Time** is the algorithm for training [[RNN (Recurrent Neural Network)]].
It extends standard [[Backpropagation]] to handle sequences.

The key insight: unroll the RNN across time steps, treating it as a deep feedforward network.
Then apply backpropagation normally.

## Why Standard Backpropagation Fails

Standard backpropagation updates parameters based on a single input-output pair.

RNNs process sequences. A parameter $W_{hh}$ affects **all time steps**.

The total loss is a sum over all time steps:

$$\mathcal{L} = \sum_{t=1}^{T} \mathcal{L}_t$$

Where $\mathcal{L}_t$ is the loss at time step $t$.

To compute $\frac{\partial \mathcal{L}}{\partial W_{hh}}$, we must sum contributions from all time steps:

$$\frac{\partial \mathcal{L}}{\partial W_{hh}} = \sum_{t=1}^{T} \frac{\partial \mathcal{L}_t}{\partial W_{hh}}$$

Each term $\frac{\partial \mathcal{L}_t}{\partial W_{hh}}$ requires derivatives flowing backward from step $t$ all the way to step 1.

## Unrolling the RNN

Unrolling means expanding the recurrence across time:

**Original RNN equations**:
$$h_t = \tanh(W_{hh} h_{t-1} + W_{xh} x_t + b_h)$$
$$y_t = W_{hy} h_t + b_y$$

**Unrolled (for $T=3$)**:

$$h_1 = \tanh(W_{hh} h_0 + W_{xh} x_1 + b_h)$$
$$h_2 = \tanh(W_{hh} h_1 + W_{xh} x_2 + b_h)$$
$$h_3 = \tanh(W_{hh} h_2 + W_{xh} x_3 + b_h)$$

$$y_1 = W_{hy} h_1 + b_y$$
$$y_2 = W_{hy} h_2 + b_y$$
$$y_3 = W_{hy} h_3 + b_y$$

Now it looks like a deep feedforward network with 3 layers (plus an input layer).

Each layer uses the **same weights** $W_{hh}$, $W_{xh}$, $W_{hy}$ (weight sharing).

## Computing Gradients: The Chain Rule Across Time

To find $\frac{\partial \mathcal{L}}{\partial W_{hh}}$, we apply the chain rule.

Consider the gradient of loss at step $t$ with respect to $W_{hh}$.

$W_{hh}$ affects $h_t$ directly (through the $W_{hh} h_{t-1}$ term).

But $W_{hh}$ also affected $h_{t-1}$, which affected $h_t$, and so on back to $h_1$.

Full gradient must trace **all these paths**:

$$\frac{\partial \mathcal{L}_t}{\partial W_{hh}} = \sum_{k=1}^{t} \frac{\partial \mathcal{L}_t}{\partial h_t} \frac{\partial h_t}{\partial h_k} \frac{\partial h_k}{\partial W_{hh}}$$

The product $\frac{\partial h_t}{\partial h_k}$ represents influence of $h_k$ on $h_t$.

This requires multiplying $(t-k)$ Jacobian matrices.

## Numeric Example: Gradient Through 3 Steps

**Setup**: 
- Sequence length $T = 3$
- Hidden dimension $n_h = 2$
- Assume $W_{hh} = \begin{bmatrix} 0.5 & 0.2 \\ 0.1 & 0.6 \end{bmatrix}$
- Assume $\tanh'(z) \approx 0.8$ at each step (approximate; actual value depends on $z$)

**Task**: Compute $\frac{\partial \mathcal{L}_3}{\partial W_{hh}}$

**Step 1**: Compute gradient at output (step 3).

Assume loss gradient: $\frac{\partial \mathcal{L}_3}{\partial y_3} = 1$ (scalar, for simplicity).

Backward through output layer:
$$\frac{\partial \mathcal{L}_3}{\partial h_3} = W_{hy}^T \frac{\partial \mathcal{L}_3}{\partial y_3} = W_{hy}^T$$

**Step 2**: Backward through hidden state at step 3.

$$\frac{\partial \mathcal{L}_3}{\partial h_3} \text{ is a vector. Call it } \delta_3$$

Gradient w.r.t. pre-activation (before $\tanh$):
$$\text{pre-activation gradient} = \delta_3 \odot \tanh'(\text{input to tanh at step 3})$$

Where $\odot$ is element-wise multiplication.

Approximate: $\delta_3 \approx [1, 1]$ (after all the matrix multiplications), and $\tanh'(z) \approx [0.8, 0.8]$.

$$\text{pre-activation gradient} \approx [0.8, 0.8]$$

Direct gradient w.r.t. $W_{hh}$:
$$\frac{\partial \mathcal{L}_3}{\partial W_{hh}} = [0.8, 0.8]^T h_2 = \begin{bmatrix} 0.8 \\ 0.8 \end{bmatrix} h_2^T$$

But we also need gradient from steps 1 and 2 flowing through $W_{hh}$ to step 3.

**Step 3**: Backward through $h_2$ (previous hidden state).

$$\frac{\partial \mathcal{L}_3}{\partial h_2} = W_{hh}^T \times \text{pre-activation gradient at step 3}$$

$$\frac{\partial \mathcal{L}_3}{\partial h_2} = \begin{bmatrix} 0.5 & 0.1 \\ 0.2 & 0.6 \end{bmatrix} \begin{bmatrix} 0.8 \\ 0.8 \end{bmatrix} = \begin{bmatrix} 0.48 \\ 0.56 \end{bmatrix}$$

**Step 4**: Process step 2.

Gradient through $\tanh$: $\begin{bmatrix} 0.48 \\ 0.56 \end{bmatrix} \odot [0.8, 0.8] \approx \begin{bmatrix} 0.384 \\ 0.448 \end{bmatrix}$

Gradient w.r.t. $W_{hh}$ from step 2's loss flowing through steps 2 and 3:
$$\text{Contribution from step 2} = \begin{bmatrix} 0.384 \\ 0.448 \end{bmatrix}^T h_1$$

**Step 5**: Process step 1.

Backward through $h_1$:
$$\frac{\partial \mathcal{L}_3}{\partial h_1} = W_{hh}^T \begin{bmatrix} 0.384 \\ 0.448 \end{bmatrix}$$

$$\approx \begin{bmatrix} 0.5 & 0.1 \\ 0.2 & 0.6 \end{bmatrix} \begin{bmatrix} 0.384 \\ 0.448 \end{bmatrix} = \begin{bmatrix} 0.237 \\ 0.345 \end{bmatrix}$$

Gradient through $\tanh$: $\approx \begin{bmatrix} 0.190 \\ 0.276 \end{bmatrix}$

Contribution from step 1:
$$\begin{bmatrix} 0.190 \\ 0.276 \end{bmatrix}^T h_0$$

**Total gradient**:
$$\frac{\partial \mathcal{L}_3}{\partial W_{hh}} = \begin{bmatrix} 0.8 \\ 0.8 \end{bmatrix} h_2^T + \begin{bmatrix} 0.384 \\ 0.448 \end{bmatrix} h_1^T + \begin{bmatrix} 0.190 \\ 0.276 \end{bmatrix} h_0^T$$

**Key observation**: Each backward step multiplies by $W_{hh}$ (and $\tanh'$).

After 3 steps: gradient multiplied by $(0.5)^3 + (0.6)^3 + \text{cross terms} \approx 0.35$

After 50 steps: gradient multiplied by roughly $(0.6)^{50} \approx 10^{-11}$

This is the **vanishing gradient problem**.

## Vanishing and Exploding Gradients

### Vanishing Gradients

Eigenvalues of $W_{hh}$ < 1 cause gradients to shrink exponentially.

**Formula**: After $t$ time steps, gradient magnitude roughly $\times (\lambda_{\max})^t$, where $\lambda_{\max}$ is largest eigenvalue of $W_{hh}$.

If $\lambda_{\max} = 0.9$ and $t = 50$: $(0.9)^{50} \approx 0.005$

Gradients become 200× too small for effective learning.

**Result**: RNN cannot learn dependencies spanning many time steps.

### Exploding Gradients

If $\lambda_{\max} > 1$, gradients grow exponentially.

$(1.1)^{50} \approx 117$: gradients become 117× too large.

**Result**: Unstable training, diverging loss, NaN values.

## Gradient Clipping (Practical Solution)

To prevent exploding gradients, clip gradient norm:

$$\text{if } \|\nabla\| > \text{threshold}: \quad \nabla \leftarrow \frac{\text{threshold}}{\|\nabla\|} \nabla$$

This keeps gradients bounded without changing direction.

**Numeric example**:
- Computed gradient: $\nabla = [100, 50]$
- Norm: $\|\nabla\| = \sqrt{100^2 + 50^2} = \sqrt{12500} \approx 111.8$
- Threshold: $1.0$
- Clipped: $\nabla' = \frac{1.0}{111.8} [100, 50] = [0.89, 0.45]$

Clipping helps, but doesn't solve the underlying problem (vanishing gradients still happen).

## Why [[LSTM (Long Short-Term Memory)]] and [[GRU (Gated Recurrent Unit)]] Work

Both architectures modify how gradients flow backward.

Instead of multiplying by $W_{hh}$ at each step, they use **addition operations** (gating).

Addition preserves gradient magnitude better than multiplication.

Gradient flow: $\frac{\partial h_t}{\partial h_{t-1}} \approx 1$ (instead of $< 1$ or $> 1$).

This prevents exponential decay or explosion.

## Truncated BPTT

Full BPTT through all $T$ time steps is expensive for long sequences.

**Truncated BPTT**: Only backpropagate through last $k$ time steps (e.g., $k=20$).

**Trade-off**:
- Faster computation (avoids computing $(0.9)^{200}$ terms)
- Loses information from very distant steps
- Works well in practice for most applications

Most frameworks use truncated BPTT with $k \approx 20-100$.

## Implementation Considerations

1. **Initialize $W_{hh}$ carefully**: eigenvalues near 1.0 help stability
2. **Use gradient clipping**: prevent exploding gradients
3. **Monitor gradient norms**: large norms indicate instability
4. **Truncate or use LSTMs**: avoid very long sequences with standard RNNs
5. **Batch sequences**: process many sequences in parallel for efficiency

## Summary

BPTT is backpropagation applied to unrolled RNNs.

Gradients must flow through many time steps.

This causes exponential shrinking (vanishing) or growth (exploding).

Solutions include gradient clipping (short-term) or architectural changes like LSTMs (fundamental fix).
