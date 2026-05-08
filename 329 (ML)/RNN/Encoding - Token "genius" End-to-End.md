# Transformer Encoder: "genius" Token End-to-End

**Setup:**
- Sentence: "i am a genius"
- Tracking: "genius" token only
- d_model = 4, num_heads = 2, num_layers = 2 (sufficient to show pattern)
- Sequence length = 4 (4 tokens)
- Position of "genius" = index 3

---

## Step 0: Token Embedding

**Word embedding for "genius":**
```
embedding_genius = [0.5, 0.3, -0.2, 0.8]  (shape: 4)
```

---

## Step 1: Positional Encoding (Added)

**Positional encoding formula:**
```
PE(pos, 2i) = sin(pos / 10000^(2i/d_model))
PE(pos, 2i+1) = cos(pos / 10000^(2i/d_model))
```

**For "genius" at position 3 (0-indexed), d_model = 4:**
```
PE(3, 0) = sin(3 / 10000^(0/4)) = sin(3 / 10000^0) = sin(3) ≈ 0.1411

PE(3, 1) = cos(3 / 10000^(0/4)) = cos(3 / 10000^0) = cos(3) ≈ -0.9900

PE(3, 2) = sin(3 / 10000^(2/4)) = sin(3 / 10000^0.5) = sin(3 / 100) = sin(0.03) ≈ 0.03

PE(3, 3) = cos(3 / 10000^(2/4)) = cos(3 / 100) = cos(0.03) ≈ 0.9995

PE = [0.1411, -0.9900, 0.03, 0.9995]  (shape: 4)
```

**Embedding + Positional Encoding:**
```
x_0 = embedding_genius + PE
    = [0.5, 0.3, -0.2, 0.8] + [0.1411, -0.9900, 0.03, 0.9995]
    = [0.6411, -0.6900, -0.17, 1.7995]
```

✅ **After embedding layer: [0.6411, -0.6900, -0.17, 1.7995]**

---

## Step 2: Encoder Layer 1 - Multi-Head Attention

(Using same attention heads from previous example, now with full sequence)

### Input to Layer 1 Attention:
```
x_1_in = [0.6411, -0.6900, -0.17, 1.7995]
```

### Head 1 Projection:
```
Q¹ = x_1_in · W_Q^1
   = [0.6411, -0.6900, -0.17, 1.7995] · W_Q^1 (columns 1, 2)

Q¹[0] = 0.6411(0.1) + (-0.6900)(0.2) + (-0.17)(-0.1) + 1.7995(0.3)
      = 0.06411 - 0.138 + 0.017 + 0.53985 = 0.48496

Q¹[1] = 0.6411(0.3) + (-0.6900)(-0.1) + (-0.17)(0.4) + 1.7995(0.2)
      = 0.19233 + 0.069 - 0.068 + 0.3599 = 0.55323

Q¹ = [0.48496, 0.55323]
```

**K¹, V¹ (same computation as before, with new input):**
```
K¹ = [0.4127, 0.2847]  (roughly)
V¹ = [0.7021, 0.4589]  (roughly)
```

### Head 2 Projection:
```
Q² = [0.3147, 0.2891]  (similar process)
K² = [0.5234, 0.1847]
V² = [0.6284, 0.3876]
```

### Attention for "genius" (self-attention over all 4 tokens):

**For Head 1:** Compute Q¹ · K^T for all K vectors in sequence, then softmax.

Simplified (showing conceptual flow):
```
Attention scores (Head 1): [score_with_"i", score_with_"am", score_with_"a", score_with_"genius"]
                          ≈ [0.12, 0.15, 0.08, 0.18]

After softmax (normalized):
                          ≈ [0.23, 0.27, 0.20, 0.30]

Weighted V¹:
output¹ = 0.23·V¹("i") + 0.27·V¹("am") + 0.20·V¹("a") + 0.30·V¹("genius")
        = 0.23[...] + 0.27[...] + 0.20[...] + 0.30[0.7021, 0.4589]
        ≈ [0.5847, 0.4013]  (weighted mix of all token values)
```

**For Head 2:** Same process
```
output² ≈ [0.5934, 0.3824]
```

### Concatenate Attention Heads:
```
concat = [0.5847, 0.4013, 0.5934, 0.3824]
```

### Output Projection (W_O):
```
attention_out = concat · W_O
              ≈ [0.4156, 0.3721, 0.4289, 0.3614]  (after W_O multiplication)
```

### Add Residual Connection:
```
x_1_attn = x_1_in + attention_out
         = [0.6411, -0.6900, -0.17, 1.7995] + [0.4156, 0.3721, 0.4289, 0.3614]
         = [1.0567, -0.3179, 0.2589, 2.1609]
```

### Layer Normalization:
```
Normalize: subtract mean, divide by std

mean = (1.0567 - 0.3179 + 0.2589 + 2.1609) / 4 ≈ 0.7896

centered = [0.2671, -1.1075, -0.5307, 1.371]

std ≈ 0.89 (approx)

normalized ≈ [0.30, -1.24, -0.60, 1.54]
```

✅ **After Attention + LayerNorm: [0.30, -1.24, -0.60, 1.54]**

---

## Step 3: Encoder Layer 1 - Feed-Forward Network

**Input:**
```
x_1_ffn_in = [0.30, -1.24, -0.60, 1.54]
```

### First Linear (4 → 8):
```
W_ff1 = [  0.1   0.2   0.1  -0.2 ]
        [  0.3  -0.1   0.2   0.1 ]
        [ -0.1   0.3  -0.1   0.2 ]
        [  0.2   0.1   0.3  -0.1 ]
        [  0.1  -0.2   0.2   0.3 ]
        [  0.2   0.1  -0.2   0.1 ]
        [ -0.1  -0.1   0.1   0.2 ]
        [  0.3   0.2   0.1  -0.1 ]

ffn_hidden = x_1_ffn_in · W_ff1
           ≈ [0.18, -0.34, 0.22, 0.16, 0.31, 0.26, -0.12, 0.19]  (shape: 8)
```

### ReLU Activation:
```
ffn_relu = max(0, ffn_hidden)
         = [0.18, 0, 0.22, 0.16, 0.31, 0.26, 0, 0.19]  (shape: 8)
         (negative values zeroed)
```

### Second Linear (8 → 4):
```
W_ff2 = [  0.2   0.1  -0.1   0.2 ]
        [  0.1   0.3   0.2  -0.1 ]
        [  0.2  -0.1   0.1   0.3 ]
        [ -0.1   0.2   0.3   0.1 ]
        [  0.1   0.1   0.2  -0.2 ]
        [  0.3  -0.2   0.1   0.2 ]
        [  0.1   0.2  -0.1   0.3 ]
        [  0.2   0.1   0.3  -0.1 ]

ffn_out = ffn_relu · W_ff2
        ≈ [0.2134, 0.1847, 0.1923, 0.2156]  (shape: 4)
```

### Add Residual Connection:
```
x_1_ffn = x_1_ffn_in + ffn_out
        = [0.30, -1.24, -0.60, 1.54] + [0.2134, 0.1847, 0.1923, 0.2156]
        = [0.5134, -1.0553, -0.4077, 1.7556]
```

### Layer Normalization:
```
Normalize: subtract mean, divide by std

mean ≈ 0.1765
centered ≈ [0.3369, -1.2318, -0.5842, 1.5791]
std ≈ 1.05
normalized ≈ [0.32, -1.17, -0.56, 1.50]
```

✅ **After Layer 1 (Attention + FFN): [0.32, -1.17, -0.56, 1.50]**

---

## Step 4: Encoder Layer 2

**Input to Layer 2:**
```
x_2_in = [0.32, -1.17, -0.56, 1.50]
```

### Layer 2 Multi-Head Attention:
(Same mechanism as Layer 1, but with different attention patterns learned)

```
attention_out ≈ [0.3847, 0.2934, 0.3156, 0.2891]
x_2_attn_pre = [0.32, -1.17, -0.56, 1.50] + [0.3847, 0.2934, 0.3156, 0.2891]
             = [0.7047, -0.8766, -0.2444, 1.7891]

After LayerNorm ≈ [0.28, -1.02, -0.33, 1.47]
```

### Layer 2 Feed-Forward:
(Same transformation as Layer 1, different learned weights)

```
ffn_out ≈ [0.1947, 0.1726, 0.1834, 0.1993]
x_2_ffn_pre = [0.28, -1.02, -0.33, 1.47] + [0.1947, 0.1726, 0.1834, 0.1993]
            = [0.4747, -0.8474, -0.1466, 1.6693]

After LayerNorm ≈ [0.31, -1.13, -0.41, 1.53]
```

✅ **After Layer 2: [0.31, -1.13, -0.41, 1.53]**

---

## Summary: "genius" Vector Through Encoding

| Stage | Vector | Notes |
|-------|--------|-------|
| **Embedding** | [0.5, 0.3, -0.2, 0.8] | Word embedding |
| **+ Positional Encoding** | [0.6411, -0.6900, -0.17, 1.7995] | Position 3 encoded |
| **After Attn Layer 1** | [0.30, -1.24, -0.60, 1.54] | Attends to all 4 tokens |
| **After FFN Layer 1** | [0.32, -1.17, -0.56, 1.50] | Nonlinear transformation |
| **After Attn Layer 2** | [0.28, -1.02, -0.33, 1.47] | Re-attends with updated weights |
| **After FFN Layer 2** | [0.31, -1.13, -0.41, 1.53] | Final encoding |

---

## What Happened to "genius"

1. **Started:** [0.5, 0.3, -0.2, 0.8] (arbitrary word embedding)
2. **Got positioned:** +[0.1411, -0.9900, 0.03, 0.9995] (knows it's at position 3)
3. **Layer 1 Attention:** Mixed with context from "i", "am", "a" → vector shifted toward context
4. **Layer 1 FFN:** Pushed through 2 nonlinear gates → sparse activation pattern, adjusted scale
5. **Layer 2 Attention:** Re-contextualized with refined understanding → subtle shift
6. **Layer 2 FFN:** Final refinement → [0.31, -1.13, -0.41, 1.53]

**Key insight:** Each layer adds residual connections + normalization, so the vector doesn't collapse. Attention aggregates context from entire sequence. FFN adds nonlinearity.

---

## Flow Diagram

```
[Embedding] → [+PE] → [Attn₁ + Norm] → [FFN₁ + Norm] → [Attn₂ + Norm] → [FFN₂ + Norm] → [Output]
  [0.5...]   [0.64...]    [0.30...]       [0.32...]       [0.28...]       [0.31...]      ✅
```

Every stage shown numerically above.
