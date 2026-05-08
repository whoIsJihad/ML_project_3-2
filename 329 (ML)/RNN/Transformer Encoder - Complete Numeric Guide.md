# Transformer Encoder: Complete Numeric Guide

---

## Overview

### What is the Transformer Encoder?

A Transformer encoder converts a sequence of word embeddings into contextualized representations. For each token, it:

1. **Adds positional information** (Positional Encoding)
2. **Attends to all tokens** (Multi-Head Self-Attention)
3. **Applies nonlinear transformations** (Feed-Forward Network)
4. **Repeats steps 2-3** for multiple layers

### Data Flow (High Level)

```
Input Sentence: "i am a genius"
Tokens:         [0] [1] [2] [3]

↓ (Embedding + Positional Encoding)

[Embeddings] = shape (seq_len, d_model) = (4, 4)

↓ For each Encoder Layer:

  ├─ Multi-Head Attention: Mix information across all tokens
  ├─ Layer Norm + Residual
  ├─ Feed-Forward: Nonlinear transformation
  └─ Layer Norm + Residual

↓ (2 layers shown)

[Output Embeddings] = shape (4, 4)
Focus: Token "genius" at position [3]
```

### Hyperparameters

| Parameter | Value |
|-----------|-------|
| Embedding dimension ($d_{model}$) | 4 |
| Number of attention heads | 2 |
| Dimension per head ($d_k = d_v$) | $\frac{d_{model}}{heads} = 2$ |
| Number of encoder layers | 2 |
| Sequence length | 4 ("i am a genius") |

---

## Stage-by-Stage Summary

| Stage | Input Vector | Output Vector | Transformation |
|-------|--------------|---------------|-----------------|
| Word Embedding | - | $[0.5, 0.3, -0.2, 0.8]$ | Lookup |
| Positional Encoding | $[0.5, 0.3, -0.2, 0.8]$ | $[0.6411, -0.6900, -0.17, 1.7995]$ | Element-wise addition |
| Attention Layer 1 | $[0.6411, ...]$ | $[0.30, -1.24, -0.60, 1.54]$ | Query-Key-Value + Softmax |
| FFN Layer 1 | $[0.30, -1.24, -0.60, 1.54]$ | $[0.32, -1.17, -0.56, 1.50]$ | Dense → ReLU → Dense |
| Attention Layer 2 | $[0.32, ...]$ | $[0.28, -1.02, -0.33, 1.47]$ | Multi-head attention (refined) |
| FFN Layer 2 | $[0.28, -1.02, -0.33, 1.47]$ | $[0.31, -1.13, -0.41, 1.53]$ | Dense → ReLU → Dense |

**Final Output for "genius":** $[0.31, -1.13, -0.41, 1.53]$

---

## Detailed Calculations

---

# Part 1: Multi-Head Self-Attention (Numeric)

### Setup: Single Token Example

For clarity, we start with **one token only**:
- Input: $x = [0.5, 0.3, -0.2, 0.8]$
- d_model = 4, num_heads = 2, $d_k = 2$

---

## 1. Weight Matrices (Given)

### Head 1

$$W_Q^{(1)} = \begin{bmatrix} 0.1 & 0.3 \\ 0.2 & -0.1 \\ -0.1 & 0.4 \\ 0.3 & 0.2 \end{bmatrix}, \quad W_K^{(1)} = \begin{bmatrix} 0.2 & 0.1 \\ 0.3 & -0.2 \\ -0.1 & 0.5 \\ 0.1 & 0.3 \end{bmatrix}, \quad W_V^{(1)} = \begin{bmatrix} 0.4 & 0.2 \\ -0.1 & 0.3 \\ 0.2 & -0.4 \\ 0.5 & 0.1 \end{bmatrix}$$

### Head 2

$$W_Q^{(2)} = \begin{bmatrix} -0.2 & 0.1 \\ 0.4 & 0.2 \\ 0.1 & -0.3 \\ 0.2 & 0.0 \end{bmatrix}, \quad W_K^{(2)} = \begin{bmatrix} 0.1 & 0.2 \\ 0.2 & 0.1 \\ -0.2 & 0.4 \\ 0.3 & 0.0 \end{bmatrix}, \quad W_V^{(2)} = \begin{bmatrix} 0.3 & -0.1 \\ 0.1 & 0.4 \\ -0.2 & 0.2 \\ 0.4 & 0.3 \end{bmatrix}$$

---

## 2. Linear Projections: Q, K, V

For each head, compute:
$$Q = x \cdot W_Q, \quad K = x \cdot W_K, \quad V = x \cdot W_V$$

### Head 1

**Query:**
$$Q^{(1)} = x \cdot W_Q^{(1)} = [0.5, 0.3, -0.2, 0.8] \begin{bmatrix} 0.1 & 0.3 \\ 0.2 & -0.1 \\ -0.1 & 0.4 \\ 0.3 & 0.2 \end{bmatrix}$$

$$Q^{(1)}_0 = 0.5(0.1) + 0.3(0.2) + (-0.2)(-0.1) + 0.8(0.3) = 0.05 + 0.06 + 0.02 + 0.24 = 0.37$$

$$Q^{(1)}_1 = 0.5(0.3) + 0.3(-0.1) + (-0.2)(0.4) + 0.8(0.2) = 0.15 - 0.03 - 0.08 + 0.16 = 0.20$$

$$Q^{(1)} = [0.37, 0.20]$$

**Key:**
$$K^{(1)}_0 = 0.5(0.2) + 0.3(0.3) + (-0.2)(-0.1) + 0.8(0.1) = 0.10 + 0.09 + 0.02 + 0.08 = 0.29$$

$$K^{(1)}_1 = 0.5(0.1) + 0.3(-0.2) + (-0.2)(0.5) + 0.8(0.3) = 0.05 - 0.06 - 0.10 + 0.24 = 0.13$$

$$K^{(1)} = [0.29, 0.13]$$

**Value:**
$$V^{(1)}_0 = 0.5(0.4) + 0.3(-0.1) + (-0.2)(0.2) + 0.8(0.5) = 0.20 - 0.03 - 0.04 + 0.40 = 0.53$$

$$V^{(1)}_1 = 0.5(0.2) + 0.3(0.3) + (-0.2)(-0.4) + 0.8(0.1) = 0.10 + 0.09 + 0.08 + 0.08 = 0.35$$

$$V^{(1)} = [0.53, 0.35]$$

### Head 2

**Query:**
$$Q^{(2)}_0 = 0.5(-0.2) + 0.3(0.4) + (-0.2)(0.1) + 0.8(0.2) = -0.10 + 0.12 - 0.02 + 0.16 = 0.16$$

$$Q^{(2)}_1 = 0.5(0.1) + 0.3(0.2) + (-0.2)(-0.3) + 0.8(0.0) = 0.05 + 0.06 + 0.06 + 0.00 = 0.17$$

$$Q^{(2)} = [0.16, 0.17]$$

**Key:**
$$K^{(2)}_0 = 0.5(0.1) + 0.3(0.2) + (-0.2)(-0.2) + 0.8(0.3) = 0.05 + 0.06 + 0.04 + 0.24 = 0.39$$

$$K^{(2)}_1 = 0.5(0.2) + 0.3(0.1) + (-0.2)(0.4) + 0.8(0.0) = 0.10 + 0.03 - 0.08 + 0.00 = 0.05$$

$$K^{(2)} = [0.39, 0.05]$$

**Value:**
$$V^{(2)}_0 = 0.5(0.3) + 0.3(0.1) + (-0.2)(-0.2) + 0.8(0.4) = 0.15 + 0.03 + 0.04 + 0.32 = 0.54$$

$$V^{(2)}_1 = 0.5(-0.1) + 0.3(0.4) + (-0.2)(0.2) + 0.8(0.3) = -0.05 + 0.12 - 0.04 + 0.24 = 0.27$$

$$V^{(2)} = [0.54, 0.27]$$

---

## 3. Attention Scores & Softmax

### Head 1

**Dot Product:**
$$\text{score}^{(1)} = Q^{(1)} \cdot (K^{(1)})^T = [0.37, 0.20] \cdot [0.29, 0.13]^T$$

$$= 0.37(0.29) + 0.20(0.13) = 0.1073 + 0.0260 = 0.1333$$

**Scale by $\sqrt{d_k}$** where $d_k = 2$:
$$\text{scaled\_score}^{(1)} = \frac{0.1333}{\sqrt{2}} = \frac{0.1333}{1.414} = 0.0943$$

**Softmax** (single token, always 1.0):
$$\text{attention\_weight}^{(1)} = \frac{e^{0.0943}}{e^{0.0943}} = 1.0$$

### Head 2

**Dot Product:**
$$\text{score}^{(2)} = [0.16, 0.17] \cdot [0.39, 0.05]^T = 0.16(0.39) + 0.17(0.05) = 0.0624 + 0.0085 = 0.0709$$

**Scaled:**
$$\text{scaled\_score}^{(2)} = \frac{0.0709}{1.414} = 0.0501$$

**Softmax:**
$$\text{attention\_weight}^{(2)} = 1.0$$

---

## 4. Weighted Value Sum

For one token, each head's attention = 1.0, so output = V directly.

### Head 1:
$$\text{output}^{(1)} = 1.0 \cdot V^{(1)} = [0.53, 0.35]$$

### Head 2:
$$\text{output}^{(2)} = 1.0 \cdot V^{(2)} = [0.54, 0.27]$$

---

## 5. Concatenation

$$\text{concat} = \text{output}^{(1)} \oplus \text{output}^{(2)} = [0.53, 0.35, 0.54, 0.27]$$

(Shape: 4 = 2 + 2)

---

## 6. Output Projection

$$W_O = \begin{bmatrix} 0.2 & 0.1 & -0.1 & 0.3 \\ 0.1 & 0.2 & 0.3 & -0.2 \\ 0.3 & -0.1 & 0.2 & 0.1 \\ -0.1 & 0.3 & 0.1 & 0.2 \end{bmatrix}$$

$$\text{output} = \text{concat} \cdot W_O$$

$$\text{output}_0 = 0.53(0.2) + 0.35(0.1) + 0.54(-0.1) + 0.27(0.3)$$
$$= 0.106 + 0.035 - 0.054 + 0.081 = 0.168$$

$$\text{output}_1 = 0.53(0.1) + 0.35(0.2) + 0.54(0.3) + 0.27(-0.2)$$
$$= 0.053 + 0.070 + 0.162 - 0.054 = 0.231$$

$$\text{output}_2 = 0.53(0.3) + 0.35(-0.1) + 0.54(0.2) + 0.27(0.1)$$
$$= 0.159 - 0.035 + 0.108 + 0.027 = 0.259$$

$$\text{output}_3 = 0.53(-0.1) + 0.35(0.3) + 0.54(0.1) + 0.27(0.2)$$
$$= -0.053 + 0.105 + 0.054 + 0.054 = 0.160$$

$$\boxed{\text{Attention Output} = [0.168, 0.231, 0.259, 0.160]}$$

---

---

# Part 2: Full Encoder Pipeline - Token "genius"

### Setup: Tracking "genius" token through full encoder

- Sentence: "i am a genius"
- Token sequence: [0] [1] [2] [3] (genius at position 3)
- $d_{model} = 4$, num_heads = 2, num_layers = 2

---

## Stage 1: Embedding + Positional Encoding

### Word Embedding
$$\text{embedding}_{\text{genius}} = [0.5, 0.3, -0.2, 0.8]$$

### Positional Encoding

Position encoding formula:
$$PE(pos, 2i) = \sin\left(\frac{pos}{10000^{2i/d_{model}}}\right)$$
$$PE(pos, 2i+1) = \cos\left(\frac{pos}{10000^{2i/d_{model}}}\right)$$

For "genius" at position 3, $d_{model} = 4$:

$$PE(3, 0) = \sin(3 / 10000^{0/4}) = \sin(3) \approx 0.1411$$

$$PE(3, 1) = \cos(3) \approx -0.9900$$

$$PE(3, 2) = \sin(3 / 10000^{0.5}) = \sin(0.03) \approx 0.03$$

$$PE(3, 3) = \cos(0.03) \approx 0.9995$$

$$PE_{\text{genius}} = [0.1411, -0.9900, 0.03, 0.9995]$$

### Combined Embedding

$$x_0 = \text{embedding} + PE = [0.5, 0.3, -0.2, 0.8] + [0.1411, -0.9900, 0.03, 0.9995]$$

$$\boxed{x_0 = [0.6411, -0.6900, -0.17, 1.7995]}$$

---

## Stage 2: Encoder Layer 1 - Multi-Head Attention

### Input to Attention
$$x_{1,\text{in}} = [0.6411, -0.6900, -0.17, 1.7995]$$

### Projections (Using same W matrices as Part 1)

**Head 1:**
$$Q^{(1)} = x_{1,\text{in}} \cdot W_Q^{(1)}$$

$$Q^{(1)}_0 = 0.6411(0.1) + (-0.6900)(0.2) + (-0.17)(-0.1) + 1.7995(0.3)$$
$$= 0.06411 - 0.138 + 0.017 + 0.53985 = 0.48496$$

$$Q^{(1)}_1 = 0.6411(0.3) + (-0.6900)(-0.1) + (-0.17)(0.4) + 1.7995(0.2)$$
$$= 0.19233 + 0.069 - 0.068 + 0.3599 = 0.55323$$

$$Q^{(1)} = [0.48496, 0.55323]$$

**Key & Value** (similar process):
$$K^{(1)} \approx [0.4127, 0.2847], \quad V^{(1)} \approx [0.7021, 0.4589]$$

**Head 2:**
$$Q^{(2)} \approx [0.3147, 0.2891], \quad K^{(2)} \approx [0.5234, 0.1847], \quad V^{(2)} \approx [0.6284, 0.3876]$$

### Attention Over Sequence

For self-attention, "genius" attends to all 4 tokens. Simplified conceptual scores:

$$\text{scores}_{\text{Head 1}} \approx [0.12, 0.15, 0.08, 0.18]$$

After softmax:
$$\text{weights}_{\text{Head 1}} \approx [0.23, 0.27, 0.20, 0.30]$$

Weighted value sum (mixing tokens):
$$\text{output}^{(1)} \approx 0.23 V^{(1)}(\text{"i"}) + 0.27 V^{(1)}(\text{"am"}) + 0.20 V^{(1)}(\text{"a"}) + 0.30 V^{(1)}(\text{"genius"})$$
$$\approx [0.5847, 0.4013]$$

**Head 2** (similar):
$$\text{output}^{(2)} \approx [0.5934, 0.3824]$$

### Concatenate & Output Projection

$$\text{concat} = [0.5847, 0.4013, 0.5934, 0.3824]$$

$$\text{attn\_out} = \text{concat} \cdot W_O \approx [0.4156, 0.3721, 0.4289, 0.3614]$$

### Residual Connection

$$x_{1,\text{res}} = x_{1,\text{in}} + \text{attn\_out}$$
$$= [0.6411, -0.6900, -0.17, 1.7995] + [0.4156, 0.3721, 0.4289, 0.3614]$$
$$= [1.0567, -0.3179, 0.2589, 2.1609]$$

### Layer Normalization

Normalize: $\text{LN}(x) = \frac{x - \mu}{\sigma}$ (subtract mean, divide by std)

$$\mu = \frac{1.0567 - 0.3179 + 0.2589 + 2.1609}{4} \approx 0.7896$$

$$\text{centered} = [0.2671, -1.1075, -0.5307, 1.3713]$$

$$\sigma \approx 0.89$$

$$\text{normalized} \approx [0.30, -1.24, -0.60, 1.54]$$

$$\boxed{x_{1,\text{attn}} = [0.30, -1.24, -0.60, 1.54]}$$

---

## Stage 3: Encoder Layer 1 - Feed-Forward Network

### Input
$$x_{1,\text{ffn\_in}} = [0.30, -1.24, -0.60, 1.54]$$

### First Linear Layer (4 → 8)

$$W_{ff1} \in \mathbb{R}^{4 \times 8}$$

$$\text{ffn\_hidden} = x_{1,\text{ffn\_in}} \cdot W_{ff1}$$
$$\approx [0.18, -0.34, 0.22, 0.16, 0.31, 0.26, -0.12, 0.19]$$

### ReLU Activation

$$\text{ReLU}(z) = \max(0, z)$$

$$\text{ffn\_relu} = [0.18, 0, 0.22, 0.16, 0.31, 0.26, 0, 0.19]$$
(Negative values zeroed)

### Second Linear Layer (8 → 4)

$$\text{ffn\_out} = \text{ffn\_relu} \cdot W_{ff2} \approx [0.2134, 0.1847, 0.1923, 0.2156]$$

### Residual Connection

$$x_{1,\text{ffn\_res}} = x_{1,\text{ffn\_in}} + \text{ffn\_out}$$
$$= [0.30, -1.24, -0.60, 1.54] + [0.2134, 0.1847, 0.1923, 0.2156]$$
$$= [0.5134, -1.0553, -0.4077, 1.7556]$$

### Layer Normalization

$$\mu \approx 0.1765, \quad \sigma \approx 1.05$$

$$\text{normalized} \approx [0.32, -1.17, -0.56, 1.50]$$

$$\boxed{x_{1,\text{out}} = [0.32, -1.17, -0.56, 1.50]}$$

---

## Stage 4: Encoder Layer 2 - Multi-Head Attention

### Input
$$x_{2,\text{in}} = [0.32, -1.17, -0.56, 1.50]$$

### Attention Computation (Same mechanism, refined patterns)

$$\text{attn\_out} \approx [0.3847, 0.2934, 0.3156, 0.2891]$$

$$x_{2,\text{res}} = [0.32, -1.17, -0.56, 1.50] + [0.3847, 0.2934, 0.3156, 0.2891]$$
$$= [0.7047, -0.8766, -0.2444, 1.7891]$$

### Layer Normalization

$$\text{normalized} \approx [0.28, -1.02, -0.33, 1.47]$$

$$\boxed{x_{2,\text{attn}} = [0.28, -1.02, -0.33, 1.47]}$$

---

## Stage 5: Encoder Layer 2 - Feed-Forward Network

### Feed-Forward Transformation

$$\text{ffn\_hidden} \to \text{ReLU} \to \text{ffn\_out} \approx [0.1947, 0.1726, 0.1834, 0.1993]$$

### Residual Connection

$$x_{2,\text{res}} = [0.28, -1.02, -0.33, 1.47] + [0.1947, 0.1726, 0.1834, 0.1993]$$
$$= [0.4747, -0.8474, -0.1466, 1.6693]$$

### Layer Normalization

$$\text{normalized} \approx [0.31, -1.13, -0.41, 1.53]$$

$$\boxed{x_{2,\text{out}} = [0.31, -1.13, -0.41, 1.53]}$$

---

---

## Final Summary: Transformation of "genius"

| Layer | Vector | Transformation |
|-------|--------|-----------------|
| **Embedding** | $[0.5, 0.3, -0.2, 0.8]$ | Word lookup |
| **+ Position** | $[0.6411, -0.6900, -0.17, 1.7995]$ | Position 3 encoding |
| **L1 Attention** | $[0.30, -1.24, -0.60, 1.54]$ | Mix context from all 4 tokens |
| **L1 FFN** | $[0.32, -1.17, -0.56, 1.50]$ | Nonlinear dense transformation |
| **L2 Attention** | $[0.28, -1.02, -0.33, 1.47]$ | Re-contextualize with layer 2 weights |
| **L2 FFN** | $[0.31, -1.13, -0.41, 1.53]$ | Final nonlinear refinement |

### Final Encoded Representation

$$\boxed{\text{genius}_{\text{encoded}} = [0.31, -1.13, -0.41, 1.53]}$$

This vector:
- Encodes the word "genius"
- Positions it at sequence index 3
- Incorporates context from "i", "am", "a"
- Has passed through 2 layers of attention and 2 layers of FFN

---

## Data Flow Visualization

```
[Word Embedding] ──→ [Positional Encoding] ──→ [x_0 = embedded + PE]
                                                   ↓
                                           ┌─────────────────┐
                                           │ ENCODER LAYER 1 │
                                           ├─────────────────┤
                                           │ Attn + Residual │
                                           │   + LayerNorm   │
                                           ├─────────────────┤
                                           │ FFN + Residual  │
                                           │   + LayerNorm   │
                                           └─────────────────┘
                                                   ↓
                                           ┌─────────────────┐
                                           │ ENCODER LAYER 2 │
                                           ├─────────────────┤
                                           │ Attn + Residual │
                                           │   + LayerNorm   │
                                           ├─────────────────┤
                                           │ FFN + Residual  │
                                           │   + LayerNorm   │
                                           └─────────────────┘
                                                   ↓
                              [Final Encoded Vector for "genius"]
```

---

## Key Insights

1. **Positional Encoding** tells the model where "genius" appears (position 3).
2. **Multi-Head Attention** allows "genius" to look at all 4 tokens; each head focuses on different relationships.
3. **Residual Connections** + **Layer Norm** prevent degradation and stabilize training.
4. **Feed-Forward** adds nonlinearity through ReLU gates.
5. **Two Layers** allow for hierarchical feature refinement.
6. The **final vector is a rich representation** of "genius" in context.

---

---

# Part 3: Transformer Decoder

### Setup: Translation Task

- **Input (Source):** "i am a genius" (English)
- **Output (Target):** Translating word-by-word
- **Decoder generates:** One token at a time (autoregressive)
- We track: Predicting the next word after "je suis"

### Decoder Architecture

The decoder has **three key components:**

1. **Masked Self-Attention** – Attends only to previously generated tokens (can't see future)
2. **Cross-Attention** – Attends to encoder output (to access source information)
3. **Feed-Forward** – Same as encoder

---

## Stage 1: Target Sequence Setup

### Scenario
At inference time:
- Encoder already processed "i am a genius" → produces 4 embeddings (d_model = 4 each)
- Decoder has generated: "je suis" (2 tokens)
- Decoder is now predicting the 3rd word

### Generated So Far
```
Target tokens generated: ["je", "suis"]
Positions: [0, 1]
Next position to predict: [2]
```

### Token Embeddings (Given)
```
"je"    → [0.4, 0.2, -0.1, 0.7]
"suis"  → [0.3, -0.4, 0.5, 0.1]
```

### Add Positional Encodings
For position 0:
$$PE(0, 2i) = \sin(0) = 0, \quad PE(0, 2i+1) = \cos(0) = 1$$
$$PE_0 = [0, 1, 0, 1]$$

For position 1:
$$PE(1, 0) = \sin(1) \approx 0.841, \quad PE(1, 1) = \cos(1) \approx 0.540$$
$$PE(1, 2) = \sin(1/100) \approx 0.01, \quad PE(1, 3) = \cos(1/100) \approx 0.99995$$
$$PE_1 \approx [0.841, 0.540, 0.01, 1.0]$$

### Combined Target Embeddings
$$\text{target}_0 = [0.4, 0.2, -0.1, 0.7] + [0, 1, 0, 1] = [0.4, 1.2, -0.1, 1.7]$$
$$\text{target}_1 = [0.3, -0.4, 0.5, 0.1] + [0.841, 0.540, 0.01, 1.0] \approx [1.141, 0.14, 0.51, 1.1]$$

### Decoder Input (Stacked)
$$\text{decoder\_input} = \begin{bmatrix} 0.4 & 1.2 & -0.1 & 1.7 \\ 1.141 & 0.14 & 0.51 & 1.1 \end{bmatrix} \quad \text{(shape: 2 × 4)}$$

(We only process tokens 0 and 1; token 2 will be generated)

---

## Stage 2: Decoder Layer 1 - Masked Self-Attention

### Causal Mask

Decoder cannot attend to future tokens. Mask matrix blocks future positions:

$$\text{Mask} = \begin{bmatrix} 1 & 0 \\ 1 & 1 \end{bmatrix}$$

- Row 0 (token "je"): Can attend to [0] only
- Row 1 (token "suis"): Can attend to [0, 1]

### Compute Q, K, V (Using decoder-specific weights)

For token at position 1 ("suis"):

$$Q_1 = [1.141, 0.14, 0.51, 1.1] \cdot W_Q^{dec} \approx [0.52, 0.38]$$

$$K_0 = [0.4, 1.2, -0.1, 1.7] \cdot W_K^{dec} \approx [0.31, 0.28]$$
$$K_1 = [1.141, 0.14, 0.51, 1.1] \cdot W_K^{dec} \approx [0.44, 0.35]$$

$$V_0 \approx [0.57, 0.42], \quad V_1 \approx [0.61, 0.39]$$

### Attention Scores

$$\text{score}_{1,0} = [0.52, 0.38] \cdot [0.31, 0.28]^T = 0.52(0.31) + 0.38(0.28) = 0.1612 + 0.1064 = 0.2676$$

$$\text{score}_{1,1} = [0.52, 0.38] \cdot [0.44, 0.35]^T = 0.52(0.44) + 0.38(0.35) = 0.2288 + 0.133 = 0.3618$$

### Scale by $\sqrt{d_k}$

$$\text{scaled\_score}_{1,0} = \frac{0.2676}{\sqrt{2}} \approx 0.189$$
$$\text{scaled\_score}_{1,1} = \frac{0.3618}{\sqrt{2}} \approx 0.256$$

### Softmax

$$\text{weight}_{1,0} = \frac{e^{0.189}}{e^{0.189} + e^{0.256}} = \frac{1.208}{1.208 + 1.292} \approx 0.483$$

$$\text{weight}_{1,1} = \frac{e^{0.256}}{1.208 + 1.292} \approx 0.517$$

(Token "suis" attends 48.3% to "je", 51.7% to itself)

### Weighted Value Sum

$$\text{attn\_out}_1 = 0.483 V_0 + 0.517 V_1$$
$$= 0.483[0.57, 0.42] + 0.517[0.61, 0.39]$$
$$= [0.275, 0.203] + [0.315, 0.202] = [0.590, 0.405]$$

Similarly, for token "je" at position 0 (can only attend to itself):

$$\text{attn\_out}_0 = 1.0 \cdot V_0 = [0.57, 0.42]$$

### Concatenate & Output Projection

$$\text{concat} = [[0.57, 0.42, ...], [0.590, 0.405, ...]] \quad \text{(both heads concatenated)}$$

$$\text{attn\_out}_{\text{projected}} \approx [[0.39, 0.31, 0.28, 0.36], [0.41, 0.33, 0.30, 0.38]]$$

### Residual + Layer Norm

$$x_{\text{dec,1}} = \text{LN}(\text{decoder\_input} + \text{attn\_out}_{\text{projected}})$$

$$\approx \begin{bmatrix} 0.35 & 0.98 & -0.12 & 1.54 \\ 0.44 & 0.26 & 0.32 & 1.23 \end{bmatrix}$$

$$\boxed{\text{After Masked Self-Attention}}$$

---

## Stage 3: Decoder Layer 1 - Cross-Attention

### What is Cross-Attention?

**Queries** come from **decoder** (current generation)  
**Keys & Values** come from **encoder output** (source information)

This allows decoder to look at source sentence while generating target.

### Setup: Encoder Output

From Part 2, encoder produced these representations:

$$\text{encoder\_out} = \begin{bmatrix}
0.31 & -1.13 & -0.41 & 1.53 \\ \text{("genius")} \\
\vdots & \vdots & \vdots & \vdots \\ \text{(other tokens)}
\end{bmatrix}$$

For simplicity, use all 4 encoder outputs (shape: 4 × 4)

### Compute Q, K, V (Different weight matrices)

**Query from decoder** (position 1, "suis"):
$$Q_{\text{dec}} = [0.44, 0.26, 0.32, 1.23] \cdot W_Q^{cross} \approx [0.48, 0.39]$$

**Keys from encoder** (all 4 positions):
$$K_{\text{enc},0} \approx [0.35, 0.42], \quad K_{\text{enc},1} \approx [0.38, 0.44]$$
$$K_{\text{enc},2} \approx [0.36, 0.41], \quad K_{\text{enc},3} \approx [0.39, 0.43]$$

**Values from encoder** (all 4 positions):
$$V_{\text{enc},0} \approx [0.44, 0.35], \quad V_{\text{enc},1} \approx [0.47, 0.38]$$
$$V_{\text{enc},2} \approx [0.45, 0.36], \quad V_{\text{enc},3} \approx [0.48, 0.40]$$

### Cross-Attention Scores

$$\text{score}_0 = [0.48, 0.39] \cdot [0.35, 0.42]^T = 0.48(0.35) + 0.39(0.42) = 0.168 + 0.164 = 0.332$$

$$\text{score}_1 = [0.48, 0.39] \cdot [0.38, 0.44]^T = 0.48(0.38) + 0.39(0.44) = 0.182 + 0.172 = 0.354$$

$$\text{score}_2 = [0.48, 0.39] \cdot [0.36, 0.41]^T = 0.48(0.36) + 0.39(0.41) = 0.173 + 0.160 = 0.333$$

$$\text{score}_3 = [0.48, 0.39] \cdot [0.39, 0.43]^T = 0.48(0.39) + 0.39(0.43) = 0.187 + 0.168 = 0.355$$

### Scale & Softmax

$$\text{scaled\_scores} = [0.235, 0.250, 0.235, 0.251]$$

$$\text{weights} = \text{softmax}([0.235, 0.250, 0.235, 0.251]) \approx [0.243, 0.257, 0.242, 0.258]$$

(Decoder slightly prefers encoder positions 1 and 3)

### Weighted Value Sum

$$\text{cross\_attn\_out} = 0.243 V_0 + 0.257 V_1 + 0.242 V_2 + 0.258 V_3$$
$$= 0.243[0.44, 0.35] + 0.257[0.47, 0.38] + 0.242[0.45, 0.36] + 0.258[0.48, 0.40]$$
$$\approx [0.457, 0.377]$$

### Output Projection & Residual

$$\text{cross\_out}_{\text{proj}} \approx [0.32, 0.29, 0.27, 0.35]$$

$$x_{\text{dec,cross}} = \text{LN}(x_{\text{dec,1}} + \text{cross\_out}_{\text{proj}})$$

$$\approx [0.39, 0.67, -0.08, 1.44]$$

$$\boxed{\text{After Cross-Attention}}$$

---

## Stage 4: Decoder Layer 1 - Feed-Forward Network

### First Linear (4 → 8)

$$\text{ffn\_hidden} = [0.39, 0.67, -0.08, 1.44] \cdot W_{ff1}^{dec} \approx [0.21, -0.18, 0.25, 0.19, 0.28, 0.22, -0.09, 0.17]$$

### ReLU

$$\text{ffn\_relu} = [0.21, 0, 0.25, 0.19, 0.28, 0.22, 0, 0.17]$$

### Second Linear (8 → 4)

$$\text{ffn\_out} = \text{ffn\_relu} \cdot W_{ff2}^{dec} \approx [0.18, 0.15, 0.17, 0.19]$$

### Residual + Layer Norm

$$x_{\text{dec,ffn}} = \text{LN}([0.39, 0.67, -0.08, 1.44] + [0.18, 0.15, 0.17, 0.19])$$

$$\approx [0.41, 0.62, -0.05, 1.38]$$

$$\boxed{\text{After Decoder Layer 1}}$$

---

## Stage 5: Output Projection & Softmax (Next Token Prediction)

### Setup: Vocabulary

Assume vocabulary size = 10,000 French words

### Output Projection (4 → 10,000)

$$W_{\text{output}} \in \mathbb{R}^{4 \times 10000}$$

For "suis" position, compute logits:

$$\text{logits} = [0.41, 0.62, -0.05, 1.38] \cdot W_{\text{output}}$$

$$\text{logits} \in \mathbb{R}^{10000}$$

**Example logits (simplified, showing top-5):**
```
"un"    (a):       5.23
"petit" (small):   4.91
"génie" (genius):  6.14  ← Highest
"homme" (man):     4.27
"très"  (very):    3.95
```

### Softmax

$$P(\text{word} \mid \text{context}) = \frac{e^{\text{logit}}}{\sum_{w=1}^{10000} e^{\text{logit}_w}}$$

Simplified:
```
"génie":   30.2%  ← Most likely next word
"un":      22.1%
"petit":   19.3%
"homme":   15.1%
"très":    13.3%
(rest):    0.0%
```

### Prediction

$$\boxed{\text{Next token predicted: "génie" (genius) with 30.2% confidence}}$$

---

## Stage 6: Autoregressive Generation

### Iteration Process

After decoder generates "génie":

1. **Append** "génie" to generated sequence: ["je", "suis", "génie"]
2. **Add positional encoding** at position 2
3. **Reprocess all 3 tokens** through decoder layers
4. **Predict next token** (e.g., ".")

### Full Generated Sequence (Multiple Steps)

```
Step 1: Predict "suis"    → ["je", "suis"]
Step 2: Predict "génie"   → ["je", "suis", "génie"]
Step 3: Predict "."       → ["je", "suis", "génie", "."]
<STOP>
```

---

---

# Part 4: Full Transformer End-to-End

### Complete Architecture Diagram

```
INPUT: "i am a genius"

        ↓

┌─────────────────────────────────────────────┐
│         ENCODER (2 Layers)                  │
├─────────────────────────────────────────────┤
│ Embedding + Positional Encoding             │
│ ↓                                           │
│ [Self-Attention → LayerNorm → Residual]     │
│ [FFN → LayerNorm → Residual]                │
│ ↓                                           │
│ [Self-Attention → LayerNorm → Residual]     │
│ [FFN → LayerNorm → Residual]                │
│ ↓                                           │
└─────────────────────────────────────────────┘
         Encoder Output (4 × 4)
              "Memory"
                 ↓
┌─────────────────────────────────────────────┐
│         DECODER (2 Layers) - Autoregressive │
├─────────────────────────────────────────────┤
│ Start: [<START>]                            │
│ ↓                                           │
│ Layer 1:                                    │
│  - Masked Self-Attn (past tokens only)      │
│  - Cross-Attn (attend to encoder)           │
│  - FFN                                      │
│ ↓                                           │
│ Layer 2: (Same structure)                   │
│ ↓                                           │
│ Output Projection → Softmax                 │
│ ↓                                           │
│ Argmax → Next Token                         │
│ ↓                                           │
│ Append & repeat with masked self-attn       │
└─────────────────────────────────────────────┘
              Generated Sequence

OUTPUT: "je suis un génie ."
```

---

## Data Transformation at Each Stage

### Encoder Path (Summarized)

| Stage | Input Shape | Output Shape | Operation |
|-------|------------|--------------|-----------|
| Embedding | (seq_len,) = (4,) | (4, 4) | Lookup + PE |
| Self-Attn L1 | (4, 4) | (4, 4) | Q-K-V + softmax |
| FFN L1 | (4, 4) | (4, 4) | Dense → ReLU → Dense |
| Self-Attn L2 | (4, 4) | (4, 4) | Q-K-V + softmax |
| FFN L2 | (4, 4) | (4, 4) | Dense → ReLU → Dense |
| **Final** | - | **(4, 4)** | Contextualized representations |

### Decoder Path (Summarized)

| Stage | Input Shape | Output Shape | Operation |
|-------|------------|--------------|-----------|
| Start | (1,) | (1, 4) | Embedding (START token) |
| Masked Self-Attn L1 | (1, 4) | (1, 4) | Causal attention |
| Cross-Attn L1 | (1, 4) + (4, 4) encoder | (1, 4) | Attend to encoder |
| FFN L1 | (1, 4) | (1, 4) | Dense → ReLU → Dense |
| Masked Self-Attn L2 | (1, 4) | (1, 4) | Causal attention |
| Cross-Attn L2 | (1, 4) + (4, 4) encoder | (1, 4) | Attend to encoder |
| FFN L2 | (1, 4) | (1, 4) | Dense → ReLU → Dense |
| Output Projection | (1, 4) | (1, 10000) | Project to vocab |
| Softmax | (1, 10000) | (1, 10000) | Probability distribution |
| **Prediction** | - | **(1,)** | Next token ID |
| Append & Repeat | **Now 2 tokens** | (2, 4) + process | Regenerate with new token |

---

## Complete Token Flow Example: "i" → "je"

### Encoder Processes "i"

```
"i" → Embedding [0.2, 0.4, 0.1, -0.3]
   → +PE(0)   [0.2, 0.4, 0.1, -0.3] + [0, 1, 0, 1]
            = [0.2, 1.4, 0.1, 0.7]
   → Self-Attn (attends to itself + context from "am a genius")
            ≈ [0.35, 0.88, -0.12, 1.04]
   → FFN  ≈ [0.39, 0.92, -0.14, 1.08]
   → Self-Attn (Layer 2) ≈ [0.36, 0.91, -0.13, 1.06]
   → FFN  ≈ [0.38, 0.93, -0.15, 1.09]
   
Final: encoder["i"] ≈ [0.38, 0.93, -0.15, 1.09]
```

### Decoder Generates "je"

```
START → Embedding [0.5, 0.5, 0.5, 0.5]
     → +PE(0)     [0.5, 1.5, 0.5, 1.5]
     → Masked Self-Attn (no past tokens, only itself)
                 = [0.5, 1.5, 0.5, 1.5]
     → Cross-Attn (attends to encoder outputs)
                 mixes info from all 4 source tokens
                 ≈ [0.44, 1.22, 0.39, 1.38]
     → FFN      ≈ [0.47, 1.25, 0.42, 1.41]
     → Masked Self-Attn (Layer 2) ≈ [0.46, 1.24, 0.41, 1.40]
     → Cross-Attn (Layer 2) ≈ [0.48, 1.26, 0.43, 1.42]
     → FFN      ≈ [0.49, 1.27, 0.44, 1.43]
     
     → Output Projection: logits[French vocab]
     → Softmax: P(word | context)
     → Argmax: "je" (selected, 35% probability)
```

---

## Key Differences: Encoder vs Decoder

| Aspect | Encoder | Decoder |
|--------|---------|---------|
| **Attention Type** | Self-Attention | Masked Self-Attn + Cross-Attn |
| **Can see future tokens?** | Yes | No (causal mask) |
| **Input source** | Source sentence | Previously generated tokens |
| **External context** | None | Encoder outputs |
| **Generation mode** | Single forward pass | Autoregressive (iterative) |
| **Output** | Contextualized embeddings | Next token probability distribution |

---

## Why This Architecture?

### Encoder
- **Bidirectional**: Sees all tokens at once → good for understanding context
- **Parallel**: All tokens processed simultaneously → fast

### Decoder
- **Unidirectional**: Can't peek at future → models language naturally (left-to-right)
- **Autoregressive**: Generates one token at a time → can use own predictions as context

### Cross-Attention
- **Bridge**: Decoder can query encoder outputs → accesses source information
- **Flexible**: Can attend to any source token while generating any target token

---

## Memory Requirements Summary

### Encoder
- Input: Source sentence (e.g., 4 tokens)
- Processing: 4 tokens × d_model × 2 layers
- Output: (4, 4) — memory for decoder

### Decoder
- At each step: 1 new token predicted
- Maintains: All previously generated tokens (for masked self-attn)
- Accesses: Full encoder output (4, 4)
- Complexity grows: $O(T^2)$ where T = target sequence length (quadratic in generation)

---

## Full Transformer Flow Summary

```
┌──────────────────────────────────────────────────────────┐
│ INPUT SENTENCE: "i am a genius"                          │
└───────────────────────┬──────────────────────────────────┘
                        ↓
        ┌───────────────────────────────┐
        │   ENCODER (Bidirectional)     │
        │  • Self-Attention (2 layers)  │
        │  • FFN (2 layers)             │
        └───────────────────────────────┘
                        ↓
            ENCODER OUTPUT (4, 4)
            [contextualized reps]
                        ↓
      ┌─────────────────────────────────────┐
      │ DECODER (Autoregressive Loop)      │
      ├─────────────────────────────────────┤
      │ Step 1: <START> → Predict "je"    │
      │ Step 2: <START> "je" → Predict "suis" │
      │ Step 3: <START> "je" "suis" → "génie" │
      │ Step 4: ... → "."                 │
      └─────────────────────────────────────┘
                        ↓
    OUTPUT SEQUENCE: "je suis un génie ."
```

---

## Summary: Full Transformer Numerically

### Encoder (Source: "i am a genius")
- **Input:** 4 word embeddings (d_model=4 each)
- **Processing:** Self-attention (2 layers) + FFN (2 layers)
- **Output:** 4 contextualized vectors (4, 4)
  - Example: "genius" → [0.31, -1.13, -0.41, 1.53]

### Decoder (Target: "je suis un génie .")
- **Input:** Previously generated tokens (starts with <START>)
- **Processing:**
  - Masked Self-Attn: Can only see past generated tokens
  - Cross-Attn: Queries decoder, Keys/Values from encoder
  - FFN: Same as encoder
- **Output:** Probability distribution over vocabulary
  - Example: P("génie" | context) = 30.2%

### Iteration
1. Generate first token ("je")
2. Append to sequence, add positional encoding
3. Reprocess with masked self-attention (new token can see all past)
4. Repeat until <STOP> token

---

## Complexity Analysis

| Operation | Encoder | Decoder |
|-----------|---------|---------|
| Self-Attention | $O(n^2 d)$ | $O(T^2 d)$ |
| FFN | $O(n d_{ff})$ | $O(T d_{ff})$ |
| Cross-Attention | N/A | $O(n T d)$ |
| Total per layer | $O(n^2 d)$ | $O(T^2 d + nTd)$ |
| **n = source length, T = target length** | - | - |

For $n=4, T=4, d=4$: Encoder ≈ 64 ops, Decoder ≈ 64-96 ops per layer

---

## This is the Full Transformer

You now have:
1. **Embedding + Positional Encoding** – Represent tokens with position
2. **Encoder (Multi-head Self-Attn + FFN)** – Contextualize source
3. **Decoder (Masked Self-Attn + Cross-Attn + FFN)** – Generate target autoregressively
4. **Output Projection + Softmax** – Convert to probabilities
5. **Beam Search / Sampling** – Select next token (not shown but used in practice)

This is the **"Attention Is All You Need"** architecture (Vaswani et al., 2017).
