# Multi-Head Self-Attention: Full Numeric Forward Pass

**Setup:**
- Input: 1 token
- Embedding dimension: d_model = 4
- Number of heads: 2
- Dimension per head: d_k = d_model / num_heads = 4 / 2 = 2

---

## 1. Input Token & Embedding

```
x = [0.5, 0.3, -0.2, 0.8]  (shape: 4)
```

---

## 2. Weight Matrices (Given)

**Head 1** (projects 4 → 2):
```
W_Q^1 = [  0.1   0.3 ]     W_K^1 = [  0.2   0.1 ]     W_V^1 = [  0.4   0.2 ]
        [  0.2  -0.1 ]             [  0.3  -0.2 ]             [ -0.1   0.3 ]
        [ -0.1   0.4 ]             [ -0.1   0.5 ]             [  0.2  -0.4 ]
        [  0.3   0.2 ]             [  0.1   0.3 ]             [  0.5   0.1 ]
```

**Head 2** (projects 4 → 2):
```
W_Q^2 = [ -0.2   0.1 ]     W_K^2 = [  0.1   0.2 ]     W_V^2 = [  0.3  -0.1 ]
        [  0.4   0.2 ]             [  0.2   0.1 ]             [  0.1   0.4 ]
        [  0.1  -0.3 ]             [ -0.2   0.4 ]             [ -0.2   0.2 ]
        [  0.2   0.0 ]             [  0.3   0.0 ]             [  0.4   0.3 ]
```

---

## 3. Compute Q, K, V (Linear Projections)

### Head 1:

**Q¹ = x · W_Q^1:**
```
Q¹ = [0.5, 0.3, -0.2, 0.8] · [  0.1   0.3 ]
                              [  0.2  -0.1 ]
                              [ -0.1   0.4 ]
                              [  0.3   0.2 ]

Q¹[0] = 0.5(0.1) + 0.3(0.2) + (-0.2)(-0.1) + 0.8(0.3)
      = 0.05 + 0.06 + 0.02 + 0.24 = 0.37

Q¹[1] = 0.5(0.3) + 0.3(-0.1) + (-0.2)(0.4) + 0.8(0.2)
      = 0.15 - 0.03 - 0.08 + 0.16 = 0.20

Q¹ = [0.37, 0.20]  (shape: 2)
```

**K¹ = x · W_K^1:**
```
K¹[0] = 0.5(0.2) + 0.3(0.3) + (-0.2)(-0.1) + 0.8(0.1)
      = 0.10 + 0.09 + 0.02 + 0.08 = 0.29

K¹[1] = 0.5(0.1) + 0.3(-0.2) + (-0.2)(0.5) + 0.8(0.3)
      = 0.05 - 0.06 - 0.10 + 0.24 = 0.13

K¹ = [0.29, 0.13]  (shape: 2)
```

**V¹ = x · W_V^1:**
```
V¹[0] = 0.5(0.4) + 0.3(-0.1) + (-0.2)(0.2) + 0.8(0.5)
      = 0.20 - 0.03 - 0.04 + 0.40 = 0.53

V¹[1] = 0.5(0.2) + 0.3(0.3) + (-0.2)(-0.4) + 0.8(0.1)
      = 0.10 + 0.09 + 0.08 + 0.08 = 0.35

V¹ = [0.53, 0.35]  (shape: 2)
```

### Head 2:

**Q² = x · W_Q^2:**
```
Q²[0] = 0.5(-0.2) + 0.3(0.4) + (-0.2)(0.1) + 0.8(0.2)
      = -0.10 + 0.12 - 0.02 + 0.16 = 0.16

Q²[1] = 0.5(0.1) + 0.3(0.2) + (-0.2)(-0.3) + 0.8(0.0)
      = 0.05 + 0.06 + 0.06 + 0.00 = 0.17

Q² = [0.16, 0.17]  (shape: 2)
```

**K² = x · W_K^2:**
```
K²[0] = 0.5(0.1) + 0.3(0.2) + (-0.2)(-0.2) + 0.8(0.3)
      = 0.05 + 0.06 + 0.04 + 0.24 = 0.39

K²[1] = 0.5(0.2) + 0.3(0.1) + (-0.2)(0.4) + 0.8(0.0)
      = 0.10 + 0.03 - 0.08 + 0.00 = 0.05

K² = [0.39, 0.05]  (shape: 2)
```

**V² = x · W_V^2:**
```
V²[0] = 0.5(0.3) + 0.3(0.1) + (-0.2)(-0.2) + 0.8(0.4)
      = 0.15 + 0.03 + 0.04 + 0.32 = 0.54

V²[1] = 0.5(-0.1) + 0.3(0.4) + (-0.2)(0.2) + 0.8(0.3)
      = -0.05 + 0.12 - 0.04 + 0.24 = 0.27

V² = [0.54, 0.27]  (shape: 2)
```

---

## 4. Compute Attention Scores & Softmax

For **self-attention with one token**, the sequence is just [x], so:
- Q queries the single token
- K, V are from the single token
- Attention is over itself (self-attention)

### Head 1:

**Attention score (dot product):**
```
score¹ = Q¹ · K¹ᵀ
       = [0.37, 0.20] · [0.29, 0.13]ᵀ
       = 0.37(0.29) + 0.20(0.13)
       = 0.1073 + 0.0260 = 0.1333
```

**Scale by √d_k (d_k = 2):**
```
scaled_score¹ = 0.1333 / √2 = 0.1333 / 1.414 = 0.0943
```

**Softmax (single value, always normalizes to 1.0):**
```
For one token, attention weight = exp(0.0943) / exp(0.0943) = 1.0

attention_weight¹ = 1.0
```

### Head 2:

**Attention score:**
```
score² = [0.16, 0.17] · [0.39, 0.05]ᵀ
       = 0.16(0.39) + 0.17(0.05)
       = 0.0624 + 0.0085 = 0.0709
```

**Scaled:**
```
scaled_score² = 0.0709 / √2 = 0.0709 / 1.414 = 0.0501
```

**Softmax (single value):**
```
attention_weight² = 1.0
```

---

## 5. Compute Weighted Value Sum

Since attention weight = 1.0 for each head (attending to itself with full weight):

### Head 1:
```
output¹ = attention_weight¹ · V¹
        = 1.0 · [0.53, 0.35]
        = [0.53, 0.35]  (shape: 2)
```

### Head 2:
```
output² = attention_weight² · V²
        = 1.0 · [0.54, 0.27]
        = [0.54, 0.27]  (shape: 2)
```

---

## 6. Concatenate Head Outputs

```
concat = [output¹ || output²]
       = [0.53, 0.35, 0.54, 0.27]  (shape: 4 = 2 + 2)
```

---

## 7. Final Output Projection

**W_O (projects 4 → 4):**
```
W_O = [  0.2   0.1  -0.1   0.3 ]
      [  0.1   0.2   0.3  -0.2 ]
      [  0.3  -0.1   0.2   0.1 ]
      [ -0.1   0.3   0.1   0.2 ]
```

**Final output:**
```
output = concat · W_O
       = [0.53, 0.35, 0.54, 0.27] · W_O

output[0] = 0.53(0.2) + 0.35(0.1) + 0.54(-0.1) + 0.27(0.3)
          = 0.106 + 0.035 - 0.054 + 0.081 = 0.168

output[1] = 0.53(0.1) + 0.35(0.2) + 0.54(0.3) + 0.27(-0.2)
          = 0.053 + 0.070 + 0.162 - 0.054 = 0.231

output[2] = 0.53(0.3) + 0.35(-0.1) + 0.54(0.2) + 0.27(0.1)
          = 0.159 - 0.035 + 0.108 + 0.027 = 0.259

output[3] = 0.53(-0.1) + 0.35(0.3) + 0.54(0.1) + 0.27(0.2)
          = -0.053 + 0.105 + 0.054 + 0.054 = 0.160

final_output = [0.168, 0.231, 0.259, 0.160]  (shape: 4)
```

---

## Summary: One Token Through Attention

```
Input:  x = [0.5, 0.3, -0.2, 0.8]
Output: [0.168, 0.231, 0.259, 0.160]
```

**Flow:**
1. **Q, K, V projection:** Input split into 2 heads, each projects 4 → 2.
2. **Attention scores:** Each head computes QK^T, scales, softmax.
3. **Weighted values:** Multiply attention weights by V.
4. **Head outputs:** [0.53, 0.35] and [0.54, 0.27].
5. **Concatenate:** [0.53, 0.35, 0.54, 0.27].
6. **Final projection:** W_O multiplies concatenated output → [0.168, 0.231, 0.259, 0.160].

---

## Key Points

- **Scaling by √d_k** prevents attention weights from becoming too small (numerical stability).
- **Softmax = 1.0 for one token** because attention is normalized over just itself.
- **Each head processes independently** with its own Q, K, V projections, then outputs concatenate.
- **W_O combines information** from all heads after concatenation.
