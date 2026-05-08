# Backpropagation Through Time (BPTT)

## Definition

**Backpropagation Through Time** is the algorithm for training [[RNN]]
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

### Why gradients flow backward through multiple steps

$W_{hh}$ affects $h_t$ directly (through the $W_{hh} h_{t-1}$ term).

But $W_{hh}$ **also** affected $h_{t-1}$, which affected $h_t$. And it affected $h_{t-2}$ before that. And so on.

Think of it like dominoes: changing $W_{hh}$ changes $h_1$, which changes $h_2$, which changes $h_3$, etc. To know the total impact on the final loss, we must trace **all these paths**.

Full gradient must sum contributions from all paths:

$$\frac{\partial \mathcal{L}_t}{\partial W_{hh}} = \sum_{k=1}^{t} \frac{\partial \mathcal{L}_t}{\partial h_t} \frac{\partial h_t}{\partial h_k} \frac{\partial h_k}{\partial W_{hh}}$$

### Understanding the Jacobian

The term $\frac{\partial h_t}{\partial h_k}$ is called a **Jacobian matrix**. Don't be intimidated by the name—it just means: *"how much does $h_t$ change when we change $h_k$ by a tiny amount?"*

Mathematically:
- $h_t$ and $h_k$ are both **vectors** (e.g., 100-dimensional hidden states)
- The Jacobian is a **2D matrix** showing all pairs of derivatives
- Entry $(i,j)$ = how much does $h_t[i]$ change when $h_k[j]$ changes?

To compute how $h_t$ depends on $h_k$, we multiply multiple Jacobians together:
$$\frac{\partial h_t}{\partial h_k} = \frac{\partial h_t}{\partial h_{t-1}} \cdot \frac{\partial h_{t-1}}{\partial h_{t-2}} \cdot \ldots \cdot \frac{\partial h_{k+1}}{\partial h_k}$$

This is $(t-k)$ matrix multiplications—that's where the problem comes in (see next section).

### Why We Multiply Jacobians (Concrete Example)

**Chain rule in calculus**: If $y = f(u)$ and $u = g(x)$, then $\frac{dy}{dx} = \frac{dy}{du} \cdot \frac{du}{dx}$ (multiply the derivatives).

**Same idea with vectors**: If $h_3 = f(h_2)$ and $h_2 = f(h_1)$, then:
$$\frac{\partial h_3}{\partial h_1} = \frac{\partial h_3}{\partial h_2} \cdot \frac{\partial h_2}{\partial h_1}$$

Each Jacobian matrix $\frac{\partial h_t}{\partial h_{t-1}}$ is approximately:
$$J_t \approx \text{diag}(\tanh'(z_t)) \cdot W_{hh}$$

Where $\text{diag}(\tanh'(z_t))$ is the derivative of the activation function (element-wise).

**The key insight**: when $W_{hh}$ has small eigenvalues (like 0.6), each matrix multiplication **shrinks** the result. Multiply enough times, and you get nearly zero.

## Numeric Example: Gradient Through 3 Steps

**Setup**: 
- Sequence length $T = 3$
- Hidden dimension $n_h = 2$
- Assume $W_{hh} = \begin{bmatrix} 0.5 & 0.2 \\ 0.1 & 0.6 \end{bmatrix}$
- Assume $\tanh'(z) \approx 0.8$ at each step (approximate; actual value depends on $z$)

**Key idea**: At each backward step, we multiply by $W_{hh}$ again. Watch what happens to the numbers:

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

To find how the loss depends on $h_2$, we multiply by $W_{hh}^T$ (this is what the chain rule requires):

$$\frac{\partial \mathcal{L}_3}{\partial h_2} = W_{hh}^T \times \text{pre-activation gradient at step 3}$$

$$\frac{\partial \mathcal{L}_3}{\partial h_2} = \begin{bmatrix} 0.5 & 0.1 \\ 0.2 & 0.6 \end{bmatrix} \begin{bmatrix} 0.8 \\ 0.8 \end{bmatrix} = \begin{bmatrix} 0.48 \\ 0.56 \end{bmatrix}$$

**Notice**: The gradient is still reasonably sized ($0.48$ and $0.56$ are close to $0.8$). This is because our weights are small (0.5, 0.6).

**Step 4**: Process step 2.

Again, multiply by $W_{hh}$ as we go backward:

Gradient through $\tanh$: $\begin{bmatrix} 0.48 \\ 0.56 \end{bmatrix} \odot [0.8, 0.8] \approx \begin{bmatrix} 0.384 \\ 0.448 \end{bmatrix}$

**Watch the numbers shrink**: Compare $[0.8, 0.8] \to [0.48, 0.56] \to [0.384, 0.448]$. They're getting smaller!

This is because we keep multiplying by $W_{hh}$ which has small values (0.5, 0.6).

Gradient w.r.t. $W_{hh}$ from step 2's loss flowing through steps 2 and 3:
$$\text{Contribution from step 2} = \begin{bmatrix} 0.384 \\ 0.448 \end{bmatrix}^T h_1$$

**Step 5**: Process step 1.

Backward through $h_1$ — multiply by $W_{hh}$ **one more time**:
$$\frac{\partial \mathcal{L}_3}{\partial h_1} = W_{hh}^T \begin{bmatrix} 0.384 \\ 0.448 \end{bmatrix}$$

$$\approx \begin{bmatrix} 0.5 & 0.1 \\ 0.2 & 0.6 \end{bmatrix} \begin{bmatrix} 0.384 \\ 0.448 \end{bmatrix} = \begin{bmatrix} 0.237 \\ 0.345 \end{bmatrix}$$

**See the pattern?** $[0.8, 0.8] \to [0.48, 0.56] \to [0.384, 0.448] \to [0.237, 0.345]$

Each step multiplies by roughly 0.6. This is the **multiplication chain**.

Gradient through $\tanh$: $\approx \begin{bmatrix} 0.190 \\ 0.276 \end{bmatrix}$

Contribution from step 1:
$$\begin{bmatrix} 0.190 \\ 0.276 \end{bmatrix}^T h_0$$

**Total gradient**:
$$\frac{\partial \mathcal{L}_3}{\partial W_{hh}} = \begin{bmatrix} 0.8 \\ 0.8 \end{bmatrix} h_2^T + \begin{bmatrix} 0.384 \\ 0.448 \end{bmatrix} h_1^T + \begin{bmatrix} 0.190 \\ 0.276 \end{bmatrix} h_0^T$$

### Why this matters: The vanishing gradient problem

Each backward step multiplies by $W_{hh}$ (and $\tanh'(z)$).

Let's trace how the gradient shrinks:
- Step 3 gradient: $[0.8, 0.8]$ 
- Step 2 gradient: $[0.8, 0.8] \times 0.6 \approx [0.48, 0.48]$ (roughly)
- Step 1 gradient: $[0.48, 0.48] \times 0.6 \approx [0.29, 0.29]$ (roughly)

After 3 steps: gradient is about $(0.6)^3 \approx 0.22$ times smaller.

After 50 steps: gradient is about $(0.6)^{50} \approx 10^{-11}$ times smaller—essentially **zero**!

This is the **vanishing gradient problem**. The network cannot learn from distant past steps.

## Vanishing and Exploding Gradients

### Understanding Eigenvalues (Intuition First)

**What's an eigenvalue?** Think of a matrix $W_{hh}$ as a transformation. An eigenvalue tells you: "by how much does this matrix scale things when applied?" 

More precisely:
- If you have a vector $v$ and $W_{hh} \cdot v = \lambda v$, then $\lambda$ is the eigenvalue
- If $\lambda = 0.8$, the matrix shrinks things by 20%
- If $\lambda = 1.2$, the matrix grows things by 20%
- The **largest eigenvalue** $\lambda_{\max}$ tells you: when I multiply by $W_{hh}$, things typically shrink/grow by this factor

Why does this matter? Because when we go backward through time, we keep multiplying by $W_{hh}$:

$$\text{gradient at step } t-k \approx \text{gradient at step } t \times (\lambda_{\max})^k$$

### Vanishing Gradients

When eigenvalues of $W_{hh}$ are **less than 1** (like 0.6, 0.9), gradients shrink exponentially.

**Mechanism**: Each backward step multiplies by values < 1, so:
- After 1 step: $\times 0.9$
- After 2 steps: $\times 0.9^2 = 0.81$
- After 3 steps: $\times 0.9^3 = 0.73$
- After 50 steps: $\times 0.9^{50} \approx 0.005$ (200× smaller!)

**Formula**: After $t$ time steps, gradient magnitude is roughly $\times (\lambda_{\max})^t$, where $\lambda_{\max}$ is the largest eigenvalue of $W_{hh}$.

**Example**: If $\lambda_{\max} = 0.9$ and $t = 50$: $(0.9)^{50} \approx 0.005$. Gradients become 200× too small.

**Result**: RNN cannot learn dependencies spanning many time steps. The network "forgets" about errors from the distant past.

### Exploding Gradients

When eigenvalues are **greater than 1** (like 1.1, 1.5), gradients grow exponentially.

**Mechanism**: Each backward step multiplies by values > 1, so:
- After 1 step: $\times 1.1$
- After 2 steps: $\times 1.1^2 = 1.21$
- After 50 steps: $\times 1.1^{50} \approx 117$ (117× larger!)

**Result**: Gradients become huge, causing unstable training, wild weight updates, and often NaN ("not a number") values that break the model.

## Gradient Clipping (Practical Solution for Exploding Gradients)\n\n**Problem it solves**: Exploding gradients (when $\\lambda_{\\max} > 1$). Doesn't fix vanishing gradients.\n\n**Idea**: If your gradient gets too large, shrink it proportionally (like turning down the volume on a speaker without changing the \"direction\" of the sound).\n\n**Formula**: \n$$\\text{if } \\|\\nabla\\| > \\text{threshold}: \\quad \\nabla \\leftarrow \\frac{\\text{threshold}}{\\|\\nabla\\|} \\nabla$$\n\nThis rescales the gradient to fit within the threshold while keeping its direction.\n\n**Numeric example**:\n- Computed gradient: $\\nabla = [100, 50]$ (very large!)\n- Norm (\"magnitude\"): $\\|\\nabla\\| = \\sqrt{100^2 + 50^2} = \\sqrt{12500} \\approx 111.8$\n- Threshold: $1.0$\n- **Scale factor**: $\\frac{1.0}{111.8} \\approx 0.0089$\n- Clipped: $\\nabla' = 0.0089 \\times [100, 50] = [0.89, 0.45]$\n\nNotice: The direction $[100, 50]$ is preserved, but magnitude is capped at $1.0$.\n\n**Important caveat**: Clipping prevents *exploding* gradients but **does not fix** vanishing gradients. It's a band-aid, not a cure.

## Why [[LSTM (Long Short-Term Memory)]] and [[GRU (Gated Recurrent Unit)]] Work

### The Problem With Standard RNNs (Review)

In standard RNNs, the backward gradient is:
$$\text{gradient} \propto W_{hh}^T \times W_{hh}^T \times \ldots \times W_{hh}^T \text{ (repeated } t \text{ times)}$$

So after $t$ steps: gradient $\approx (\lambda_{\max}(W_{hh}))^t \times \text{base gradient}$

If $\lambda_{\max} < 1$, the gradient vanishes. If $\lambda_{\max} > 1$, it explodes. No middle ground.

### How LSTMs and GRUs Fix This

LSTMs use a **different operation**: addition instead of multiplication.

**Standard RNN recurrence**:
$$h_t = f(W_{hh} h_{t-1} + W_{xh} x_t)$$

The gradient with respect to $h_{t-1}$ requires multiplying by $W_{hh}$ repeatedly.

**LSTM recurrence** (simplified):
$$c_t = c_{t-1} + \text{(gated update)}$$

Notice: **addition**, not multiplication!

When we backpropagate through addition:
$$\frac{\partial \mathcal{L}}{\partial c_{t-1}} = \frac{\partial \mathcal{L}}{\partial c_t} + \text{other terms}$$

There's **no matrix multiplication** in the main path. The gradient can flow backward without exponential shrinking/growth.

### Intuition

- **Multiplication**: $a \times 0.9 \times 0.9 \times 0.9 \ldots$ shrinks exponentially
- **Addition**: $a + b + c + d \ldots$ doesn't shrink exponentially

LSTMs replace the problematic multiplication chain with addition, allowing gradients to flow reliably through long sequences.

## Truncated BPTT

Full BPTT through all $T$ time steps is expensive for long sequences.

**Truncated BPTT**: Only backpropagate through last $k$ time steps (e.g., $k=20$).

**Trade-off**:
- Faster computation (avoids computing $(0.9)^{200}$ terms)
- Loses information from very distant steps
- Works well in practice for most applications

Most frameworks use truncated BPTT with $k \approx 20-100$.

## Implementation Considerations

### Practical Guidelines

1. **Initialize $W_{hh}$ carefully**
   - Goal: eigenvalues near 1.0 for stability
   - Why: Eigenvalues determine whether gradients shrink or grow
   - How: Use \"orthogonal initialization\" (many libraries have this built-in)

2. **Use gradient clipping**
   - Goal: Prevent exploding gradients
   - How: Set a threshold (e.g., 1.0) and rescale if norm exceeds it
   - Note: Doesn't fix vanishing gradients, only explosive ones

3. **Monitor gradient norms during training**
   - What to look for: 
     - Gradient norm decreasing to near-zero = vanishing gradients
     - Gradient norm suddenly spiking to millions = exploding gradients
   - Action: If vanishing, switch to LSTM/GRU. If exploding, use gradient clipping.

4. **Truncate long sequences or use LSTMs/GRUs**
   - Standard RNN + long sequences = vanishing gradients
   - LSTMs/GRUs can handle longer sequences (up to several hundred steps)
   - Truncated BPTT: compromise between speed and gradient flow

5. **Batch sequences of similar length**
   - Efficiency: Process many sequences in parallel
   - Stability: Avoid extreme length variations in a batch

## Summary: The Big Picture

### What happens in BPTT

1. **Unroll the RNN**: Expand across all time steps, treating it like a deep feedforward network
2. **Apply backpropagation**: Compute gradients by multiplying Jacobians backward through time
3. **Gradients depend on eigenvalues**: The largest eigenvalue of $W_{hh}$ controls whether gradients shrink or grow

### The Core Problem

When we backpropagate through $T$ time steps:
$$\text{gradient} \propto (\lambda_{\max})^T$$

If $\lambda_{\max} < 1$: gradient vanishes exponentially (can't learn long-term dependencies)  
If $\lambda_{\max} > 1$: gradient explodes exponentially (unstable training)

### Three Solutions

1. **Gradient Clipping** (band-aid): Prevents exploding gradients, doesn't fix vanishing
2. **Truncated BPTT** (speed-up): Only backpropagate through last $k$ steps, not all $T$ steps
3. **LSTMs/GRUs** (fundamental fix): Replace multiplication with addition, so gradients don't vanish or explode

### Why This Matters

Standard RNNs struggle with long sequences (anything beyond ~20-30 steps). LSTMs can handle hundreds of steps. This is why LSTMs are the default choice for sequence modeling in practice.
