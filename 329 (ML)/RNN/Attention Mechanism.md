# Attention Mechanism

## Motivation: Why Seq2Seq Fails on Long Sequences

[[Sequence-to-Sequence Models]] compress entire input into single context vector.

For input of length $n$, this vector must encode:
- All tokens
- All grammatical relationships
- All semantic meanings

Example: Translating 50-word English sentence to French.

Encoder processes all 50 words, outputs single 256-dimensional vector.

Decoder must decode entire translation from this vector.

**Problem**: Information loss. Early words compressed away.

Empirical result: BLEU score drops sharply for sentences > 15 words.

Graph:
```
BLEU Score
   35 |     ╱╲
   30 |    ╱  ╲╲
   25 |   ╱    ╲╲
   20 |  ╱      ╲╲___
   15 | ╱             ╲___
        0   10   20   30  40 50
           Input Length (words)
```

No attention: performance degrades quickly.

## Solution: Attention Weights

Instead of single context vector, use **weighted sum of all encoder states**.

At each decoder step, learn which encoder states matter.

### Attention Mechanism Components

**1. Query** (from decoder):
- Current decoder hidden state $s_t$
- "What am I trying to decode now?"

**2. Keys** (from encoder):
- All encoder hidden states $h_1, h_2, ..., h_T$
- "What information is available?"

**3. Compatibility function**:
$$e_{t,i} = \text{score}(s_t, h_i)$$

Measures how relevant encoder state $i$ is for decoder step $t$.

**4. Attention weights** (normalize scores):
$$\alpha_{t,i} = \frac{\exp(e_{t,i})}{\sum_{j=1}^{T} \exp(e_{t,j})} = \text{softmax}(e_{t,:})$$

Sum to 1: $\sum_i \alpha_{t,i} = 1$

**5. Context vector** (weighted sum):
$$c_t = \sum_{i=1}^{T} \alpha_{t,i} h_i$$

**6. Use in decoding**:
$$s_t = \text{RNN}_{\text{decoder}}(s_{t-1}, [y_{t-1}; c_t])$$

Or alternative:
$$s_t = \tanh(W_c [s_{t-1}; c_t])$$

## Scoring Functions: How to Compute Attention

### 1. Dot Product (Multiplicative)

Simplest scoring:
$$e_{t,i} = s_t^T h_i$$

Cost: $O(1)$ per pair.

Assumption: Query and key have same dimension.

### 2. Scaled Dot Product

$$e_{t,i} = \frac{s_t^T h_i}{\sqrt{d_k}}$$

Where $d_k$ is key dimension.

Scaling prevents very large values (which hurt softmax).

**Why scale?** If $d_k = 512$, dot products average around 0 but variance is high.

Softmax on very large/small values saturates (gradients → 0).

Dividing by $\sqrt{d_k} = \sqrt{512} \approx 22.6$ keeps values moderate.

### 3. General (Additive, Bahdanau)

$$e_{t,i} = v^T \tanh(W [s_t; h_i])$$

Where:
- $W$: learned matrix
- $v$: learned vector
- $[\cdot; \cdot]$: concatenation

More expressive. Learns what to compare.

Cost: More parameters than dot product.

Works similarly well in practice.

### 4. Multiplicative (Luong)

$$e_{t,i} = s_t^T W h_i$$

Learned weight matrix $W$ modulates dot product.

Middle ground: more flexible than dot product, cheaper than additive.

## Numeric Example: Attention in Translation

**Encoder output** (after encoding "The cat sat"):
- $h_1 = [0.5, 0.2, -0.1]$ (after "The")
- $h_2 = [0.7, 0.4, 0.2]$ (after "cat")
- $h_3 = [0.3, -0.1, 0.5]$ (after "sat")

**Decoder state** at step 2 (generating "chat" in French):
- $s_2 = [0.4, 0.3, 0.1]$

**Scaled dot product attention** (scale factor $\sqrt{3} \approx 1.73$):

Step 1: Compute scores:
$$e_{2,1} = \frac{[0.4, 0.3, 0.1] \cdot [0.5, 0.2, -0.1]}{\sqrt{3}} = \frac{0.2 + 0.06 - 0.01}{1.73} = \frac{0.25}{1.73} = 0.145$$

$$e_{2,2} = \frac{[0.4, 0.3, 0.1] \cdot [0.7, 0.4, 0.2]}{\sqrt{3}} = \frac{0.28 + 0.12 + 0.02}{1.73} = \frac{0.42}{1.73} = 0.243$$

$$e_{2,3} = \frac{[0.4, 0.3, 0.1] \cdot [0.3, -0.1, 0.5]}{\sqrt{3}} = \frac{0.12 - 0.03 + 0.05}{1.73} = \frac{0.14}{1.73} = 0.081$$

Step 2: Softmax:
$$\exp(0.145) = 1.156, \exp(0.243) = 1.275, \exp(0.081) = 1.084$$
$$\text{Sum} = 3.515$$

$$\alpha_{2,1} = 1.156 / 3.515 = 0.329$$
$$\alpha_{2,2} = 1.275 / 3.515 = 0.363$$
$$\alpha_{2,3} = 1.084 / 3.515 = 0.308$$

Step 3: Context vector:
$$c_2 = 0.329 \times [0.5, 0.2, -0.1] + 0.363 \times [0.7, 0.4, 0.2] + 0.308 \times [0.3, -0.1, 0.5]$$

$$= [0.165, 0.066, -0.033] + [0.254, 0.145, 0.073] + [0.092, -0.031, 0.154]$$

$$= [0.511, 0.180, 0.194]$$

**Interpretation**: Attention weights relatively balanced (0.33, 0.36, 0.31).

All encoder states contribute, with slight emphasis on "cat" (0.363).

## Attention Visualization

After training, attention matrices become interpretable.

For English-French translation:

```
                 English input
              The  cat   sat   on   mat
             -----   -----   -----   -----   -----
French  Le  | 0.1 | 0.1 | 0.0 | 0.0 | 0.8 |
output  C   | 0.05| 0.85| 0.05| 0.0 | 0.05|
        h   | 0.1 | 0.8 | 0.05| 0.0 | 0.05|
        a   | 0.05| 0.3 | 0.6 | 0.0 | 0.05|
        t   | 0.0 | 0.1 | 0.05| 0.75| 0.1 |
        e   | 0.1 | 0.1 | 0.2 | 0.4 | 0.2 |
        s   | 0.2 | 0.1 | 0.3 | 0.2 | 0.2 |
```

Reading: "Le" attends mostly to "mat", "chat" attends to "cat" and "sat".

Humans can see if model learned sensible alignments.

Common patterns:
- Monotonic alignment (French order ≈ English order)
- Reordering (German verb moves after noun)
- Copying (numbers, names attend to exact match)

## Multi-Head Attention

Process attention multiple times in parallel.

Each head learns different attention patterns:

$$\text{head}_k = \text{Attention}(W_k^Q s_t, W_k^K h, W_k^V h)$$

Where $W_k^Q, W_k^K$ project queries and keys for head $k$.

Output: Concatenate all heads:
$$\text{MultiHead} = \text{Concat}(\text{head}_1, ..., \text{head}_h) \cdot W^O$$

### Why Multiple Heads?

Different parts of sequence need different attention patterns:

- Head 1: Long-range dependencies (subject-verb agreement)
- Head 2: Local dependencies (adjective-noun agreement)
- Head 3: Rare special cases (punctuation, numbers)

Example with 8 heads (total output dimension 512, so each head 64D):

```
Input: "The quick brown fox jumps"

Head 1 (Subject):   fox ← jumps (object of main verb)
Head 2 (Adjectives): brown → fox, quick → fox
Head 3 (Articles):   The → fox
Head 4 (Verbs):     jumps → (predicate)
Head 5-8 (Mixed):   Various patterns
```

Empirically: Multi-head attention improves performance 2-5% over single head.

## Self-Attention

Attend to positions **within the same sequence**.

Query, key, value all come from same sequence:

$$e_{i,j} = \frac{x_i^T W_Q^T W_K x_j}{\sqrt{d_k}}$$

$$\alpha_{i,j} = \text{softmax}_j(e_{i,j})$$

$$y_i = \sum_j \alpha_{i,j} (W_V x_j)$$

Useful for:
- Understanding relationships within sequence
- Building context without RNN (parallel computation)
- Capturing long-range dependencies directly

### Self-Attention Example: Question Answering

Context: "John gave Mary a book"

Query at position 3 (Mary): "What is Mary's relationship?"

Attention scores (unnormalized):
- Position 1 (John): 0.2
- Position 2 (gave): 0.1
- Position 3 (Mary): 0.9 (attends to self)
- Position 4 (a): 0.0
- Position 5 (book): 0.3

After softmax: $[0.10, 0.06, 0.55, 0.03, 0.16]$

Mary's output combines:
- 55% self
- 10% John (recipient, related to Mary)
- 16% book (object given to Mary)
- Small amounts to other words

Result: Updated Mary representation knows it's connected to John and book.

## Computational Complexity

Standard attention: $O(T^2 d)$ where $T$ = sequence length, $d$ = dimension.

For long sequences, this is expensive:
- $T = 1000$: $10^6$ comparisons
- $T = 10000$: $10^8$ comparisons

### Sparse Attention Variants

**Strided attention**: Only attend to positions $j = i, i-k, i-2k, ...$ (stride $k$).

Reduces to $O(T \cdot T/k) = O(T^2 / k)$.

**Local attention**: Attend to window around position (e.g., $\pm 128$ positions).

Reduces to $O(T \cdot W)$ where $W$ is window size.

**Learnable sparsity**: Attention learns which positions to skip.

More complex, but adaptable.

## Comparison: Seq2Seq with/without Attention

### Seq2Seq (No Attention)

- Context vector: single $h_T$
- Pro: Simple, fewer parameters
- Con: Information bottleneck, fails on long sequences

BLEU on long sequences: 20-25

### Seq2Seq + Attention

- Context vector: $c_t = \sum_i \alpha_{t,i} h_i$ (changes each step)
- Pro: Flexible information flow
- Con: More computation, complex

BLEU on long sequences: 28-32

**Improvement: +7 BLEU points (significant).**

## Attention in Transformers

[[Transformers]] use attention as primary building block.

Multi-head self-attention + feed-forward layer (repeated many times).

No RNNs at all.

Advantages:
- Parallelizable (no sequential dependencies)
- Better for modern GPUs/TPUs
- Scales to very large models (billions of parameters)

Modern state-of-the-art: Transformer-based models (BERT, GPT, T5).

## Summary

Attention solves seq2seq information bottleneck.

Decoder learns what encoder information to use at each step.

Attention weights interpretable: shows which input words matter.

Multi-head attention: different heads learn different patterns.

Foundation for modern Transformers.
