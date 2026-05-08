# Vanishing Gradients and Exploding Gradients

## Problem Definition

During [[Backpropagation]], gradients flow backward through many layers or time steps.

Each multiplication shrinks or grows the gradient.

After many steps, gradient becomes too small (vanishes) or too large (explodes).

Result: Cannot learn long-range dependencies.

## Vanishing Gradients: Mathematical Analysis

### Chain Rule Multiplication

Gradient at layer $k$ (counting backward from output):

$$\frac{\partial L}{\partial W^{[k]}} = \frac{\partial L}{\partial h^{[k]}} \cdot \frac{\partial h^{[k]}}{\partial W^{[k]}}$$

But to influence later layers:

$$\frac{\partial L}{\partial h^{[k]}} = \frac{\partial L}{\partial h^{[k+1]}} \cdot \frac{\partial h^{[k+1]}}{\partial h^{[k]}}$$

Expanding fully (layer $L$ is output):

$$\frac{\partial L}{\partial W^{[k]}} = \frac{\partial L}{\partial h^{[L]}} \prod_{i=k}^{L-1} \frac{\partial h^{[i+1]}}{\partial h^{[i]}} \cdot \frac{\partial h^{[k]}}{\partial W^{[k]}}$$

Each Jacobian term $\frac{\partial h^{[i+1]}}{\partial h^{[i]}}$ is a matrix multiplication.

### RNN Time Steps: Repeated Matrix Multiplication

For [[RNN]] processing sequence of length $T$:

$$\frac{\partial L}{\partial W_{hh}} \propto \prod_{t=1}^{T} \frac{\partial h_t}{\partial h_{t-1}}$$

This product has $T$ terms.

Each term is a Jacobian of activation function + weight matrix multiplication.

For sigmoid/tanh: $\frac{\partial a}{\partial z} \leq 0.25$ (maximum).

For standard RNN: $\frac{\partial h_t}{\partial h_{t-1}} = W_{hh}^T \text{diag}(\tanh'(...))$

Spectral norm (largest eigenvalue) of $W_{hh}$: typically < 1.

**Product of many terms < 1**: $(0.9)^{50} \approx 0.005$

Gradient shrinks exponentially with sequence length.

### Numeric Demonstration

**Setup**:
- Standard RNN with hidden dimension 128
- Eigenvalues of $W_{hh}$: largest = 0.95
- Sequence length $T = 100$

**Gradient magnitude**:

After 10 steps: $(0.95)^{10} \approx 0.60$ (40% reduction)
After 50 steps: $(0.95)^{50} \approx 0.007$ (99.3% reduction)
After 100 steps: $(0.95)^{100} \approx 0.00006$ (99.99% reduction)

**Practical consequence**: Weight updates at early time steps are 10000× too small.

Network cannot learn to correlate early input with late output.

## Symptoms of Vanishing Gradients

### In Training

1. **Loss stops decreasing**: Gradient updates too small
2. **Early time steps ignored**: Network forgets past inputs
3. **Model learns recency bias**: Only responds to recent inputs
4. **Poor long-sequence performance**: Accuracy drops for long inputs

### Example: Language Model

Task: Predict next character given sequence.

Input: "The quick brown fox jumped over the lazy dog."

Vanishing gradient model:
- Predicts based on last 5 words (recent context)
- Forgets "The" from beginning
- Poor at long-range coherence

### Validation Signal

- Training loss: decreasing normally
- Validation loss: plateaus, doesn't improve with longer sequences
- Validation accuracy on sequences > 20 tokens: < 10%

## Exploding Gradients: Mathematical Analysis

### When Eigenvalues > 1

If largest eigenvalue of $W_{hh}$ > 1:

$(1.1)^{50} \approx 117$: Gradients grow exponentially.

Each multiplication amplifies the gradient.

### Numeric Example

Same setup as before, but largest eigenvalue = 1.05:

After 10 steps: $(1.05)^{10} \approx 1.63$ (63% larger)
After 50 steps: $(1.05)^{50} \approx 11.5$ (1050% larger)
After 100 steps: $(1.05)^{100} \approx 131$ (13000% larger)

Gradients become huge.

## Symptoms of Exploding Gradients

### In Training

1. **Loss becomes NaN**: Numerical overflow
2. **Weights diverge**: Parameters become huge
3. **Training crashes abruptly**: Often after 5-20 epochs
4. **Gradient norms exploding**: $\|\nabla\| > 10^{10}$ suddenly

### Example: NaN at Training Step

```
Epoch 1, Step 100: Loss = 2.34
Epoch 1, Step 200: Loss = 2.15
Epoch 1, Step 300: Loss = 2.11
Epoch 1, Step 400: Loss = NaN  ← Exploded
```

### Debug Signal

Print gradient norm:
```python
grad_norm = torch.norm(gradients)
if grad_norm > 1000:
    print(f"Warning: gradient norm = {grad_norm}")
```

If gradient norm suddenly jumps from 1.0 to 1,000,000, you have exploding gradients.

## Solution 1: Gradient Clipping

**Idea**: Clip gradient magnitude to prevent explosion.

**Algorithm**:

```
computed_gradient = compute_gradients()
gradient_norm = norm(computed_gradient)

if gradient_norm > threshold:
    clipped_gradient = (threshold / gradient_norm) * computed_gradient
else:
    clipped_gradient = computed_gradient

update_weights(clipped_gradient)
```

**Effect**: 
- Preserves gradient direction
- Caps magnitude at threshold

### Numeric Example

**Computed gradient**: $\nabla = [100, 50, -30]$

Norm: $\|\nabla\| = \sqrt{100^2 + 50^2 + 30^2} = \sqrt{13900} \approx 117.9$

**Threshold**: 1.0

**Scaling factor**: $\frac{1.0}{117.9} \approx 0.0085$

**Clipped**: $\nabla_{\text{clipped}} = [0.85, 0.425, -0.255]$

Direction unchanged, magnitude capped.

### Common Thresholds

- Norm clipping: threshold = 1.0 or 5.0
- Value clipping (rare): clip individual elements to $[-5, 5]$

Most frameworks use gradient clipping by default for RNNs.

## Solution 2: Careful Initialization

Initialize $W_{hh}$ so eigenvalues ≈ 1.

### Orthogonal Initialization

Initialize $W_{hh}$ as orthogonal matrix.

Orthogonal matrices have eigenvalues = 1.

Property: $W^T W = I$, so multiplication preserves norm.

**Consequence**: Gradient doesn't vanish or explode (stays constant magnitude).

### Numeric Effect

**Standard RNN with orthogonal $W_{hh}$**:

Eigenvalues all = 1.0 (approximately, in practice 0.99-1.01).

Product: $(1.0)^{100} \approx 1.0$

Gradient stays constant across 100 time steps!

Compare to 0.95 eigenvalue: $(0.95)^{100} \approx 0.00006$

**Improvement: 16,000× larger gradients.**

## Solution 3: [[LSTM (Long Short-Term Memory)]] and [[GRU (Gated Recurrent Unit)]]

Fundamental architectural change.

### Why LSTMs Work

Cell state updates through addition (not multiplication):

$$c_t = f_t \odot c_{t-1} + i_t \odot \tilde{c}_t$$

Taking derivative:

$$\frac{\partial c_t}{\partial c_{t-1}} = f_t$$

Forget gate $f_t \in (0, 1)$ but not as constrained as weight matrix eigenvalues.

Network learns optimal forget gate values.

**Effect**: Gradient flows through addition, not shrinking exponentially.

### Numeric Comparison

**Standard RNN, 100 steps**:
- Gradient: $(0.95)^{100} \approx 0.00006$ (vanishes)

**LSTM, 100 steps**:
- Forget gates: $f_1 = 0.99, f_2 = 0.98, ..., f_{100} = 0.90$ (learned to preserve)
- Gradient: $0.99 \times 0.98 \times ... \times 0.90 \approx (0.95)^{100}$ WAIT, same math!

**But wait—why does LSTM help?**

Answer: Network learns forget gates adaptively.

For important information paths: forget gates $\approx 0.999$ (gradient $\approx 1$)
For noise: forget gates $\approx 0.1$ (gradient $\approx 0.1$)

Plus multiple gradient paths through input/output gates.

Effective gradient: Much larger than standard RNN.

## Solution 4: Layer Normalization

Normalize hidden state before applying RNN update:

$$h'_{t-1} = \frac{h_{t-1} - \mu}{\sigma + \epsilon}$$

Where $\mu, \sigma$ are mean, std of $h_{t-1}$ elements.

**Effect**: Keeps activations in reasonable range, prevents gradient explosion.

## Comparison of Solutions

| Solution | Cost | Effectiveness | Ease |
|----------|------|----------------|------|
| Gradient Clipping | Minimal | Good for explosion, doesn't fix vanishing | Easy |
| Orthogonal Init | Minimal | Better gradient flow | Easy |
| LSTM/GRU | 4× parameters | Excellent, near-complete fix | Medium |
| Layer Norm | Small overhead | Good stabilization | Easy |
| Multiple + combined | Minimal | Excellent | Medium |

**Best practice**: Use LSTM/GRU (primary) + gradient clipping (safety) + careful initialization (optimization).

## Empirical Results

### Standard RNN on Language Modeling

- Maximum effective sequence length: ~20 tokens
- Perplexity on Penn Treebank: 150-200

### RNN + Gradient Clipping

- Maximum effective sequence length: ~30 tokens
- Perplexity: 100-150

### LSTM

- Maximum effective sequence length: ~100-200 tokens
- Perplexity: 60-80

### LSTM + Layer Norm

- Maximum effective sequence length: ~200+ tokens
- Perplexity: 50-70

**Improvement from standard to LSTM+LayerNorm: 3-4× longer sequences, 2-3× better perplexity.**

## Debugging Vanishing/Exploding Gradients

### Test 1: Gradient Norm Printing

```python
for layer in model.layers:
    grad_norm = torch.norm(layer.weight.grad)
    print(f"Layer {layer.name}: gradient norm = {grad_norm:.4f}")
```

**Vanishing**: Norms decrease by layer (1.0, 0.1, 0.01, ...)
**Exploding**: Norms increase by layer (1.0, 10.0, 100.0, ...)
**Healthy**: Norms stable across layers (0.1-1.0 range)

### Test 2: Sequence Length Scaling

Train on sequences of increasing length:

| Sequence Length | Accuracy |
|-----------------|----------|
| 5 | 95% |
| 10 | 90% |
| 20 | 70% |
| 30 | 40% |
| 50 | 5% |

Sharp drop = vanishing gradients.

### Test 3: Weight Divergence

Monitor weight statistics during training:

```python
weight_mean = layer.weight.mean()
weight_std = layer.weight.std()
print(f"Weight mean: {weight_mean:.4f}, std: {weight_std:.4f}")
```

Exploding gradients → weight_std becomes huge (100+)

## Summary

Vanishing/exploding gradients prevent learning long-range dependencies.

Caused by chain rule multiplication across many time steps.

Vanishing: gradient shrinks exponentially.
Exploding: gradient grows exponentially.

Solutions:
1. Gradient clipping (bandaid)
2. Careful initialization (helps)
3. LSTM/GRU (fundamental fix)
4. Layer normalization (stabilizes)

Use combination for best results.

LSTMs/GRUs now standard for sequence modeling (before transformers).
