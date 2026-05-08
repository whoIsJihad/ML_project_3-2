# Transformers: A Beginner's Guide

## The Simple Problem

Imagine you're reading a sentence:

> "The **cat** sat on the mat"

When you read the word "cat", your brain instantly connects it to concepts like:
- What "the" refers to
- Where it sits ("mat" at the end)
- What happens to it ("sat")

You don't read word-by-word linearly and lose information. You see the whole picture.

But older AI models ([[RNN (Recurrent Neural Network)]] - Recurrent Neural Networks) worked like this:
- Read word 1 ("The") → remember something
- Read word 2 ("cat") → update memory with word 1 info
- Read word 3 ("sat") → update memory with words 1-2 info
- ...and so on

**Problem**: By the time you reach word 6 ("mat"), the memory from word 1 ("the") has gotten fuzzy. Important connections get lost over time.

**Transformers solve this** by letting every word see every other word at the same time. No sequential reading. No fuzzy memories.

## The Core Idea: Attention

Instead of passing information sequentially, transformers use **attention**.

Think of it like this:

> When reading "cat", look at ALL words in the sentence and decide which ones matter most for understanding it.

```
Sentence: The cat sat on the mat
Word: "cat"

How much should I care about each word?
- "The"      → 15% (it's describing me)
- "cat"      → 70% (that's me!)
- "sat"      → 10% (what I did)
- "on"       → 0% (not relevant)
- "the"      → 0% (not relevant)
- "mat"      → 5% (where I sat)
```

That's attention. Each word asks: "Which other words are important for me?"

## Why This Matters

### Speed: Process Everything in Parallel

**Old way (RNN)**:
- Step 1: Read "The"
- Step 2: Read "cat"
- Step 3: Read "sat"
- ...

One step at a time. No shortcuts.

**Transformer way**:
- Read ALL words at once
- Each word looks at ALL other words simultaneously
- Done in one shot (not quite, but conceptually)

**Real numbers**:
- RNN on a 1000-word text: 1000 sequential steps
- Transformer on same text: ~10 parallel steps
- Speed-up: **100× faster**

Your GPU (graphics processor) loves parallel work. Transformers take full advantage.

### Understanding: No Information Loss

**RNN problem**:
```
"The quick brown fox jumps over the lazy dog"
                                        ↓
Word 1: "The"     ← hard to remember by the end
```

By word 8-9, the model has partially "forgotten" word 1. Like a game of telephone.

**Transformer solution**:
```
"The quick brown fox jumps over the lazy dog"

"dog" directly looks at "The" (and all others)
No information decay over distance
```

All words are equally "fresh" to each other.

---

# Building the Transformer: Step by Step

## Step 1: What Is a Token?

First, split text into chunks (tokens). Usually words or word-pieces.

```
"Hello world" → ["Hello", "world"]
"I'm happy"  → ["I", "'m", "happy"]  (word-pieces)
```

Each token gets a number (embedding):

```
"Hello" → [0.2, 0.5, -0.1, 0.8, ...]  (512 numbers)
"world" → [0.1, -0.3, 0.4, 0.2, ...]
```

This vector is the token's numerical representation. It captures meaning.

## Step 2: Positional Information

Here's a problem: Transformers don't inherently know the order of words.

To them:
```
"cat sat" and "sat cat" look identical
```

Solution: Add **position information** to each token.

```
Token 1 (position 0): [0.2, 0.5, ...] + [1.0, 0.0, 0.1, ...]  (position encoding)
Token 2 (position 1): [0.1, -0.3, ...] + [0.8, 0.6, 0.0, ...] (position encoding)
```

Now each token knows: "I'm at position 1, position 2", etc.

The position encoding is calculated using math (sine/cosine waves), but the key idea is: **tokens know their order**.

## Step 3: The Attention Mechanism

This is the magic. Here's how one token pays attention to all others.

### The Process (Simplified)

For token "cat", we ask three questions about each word:

1. **Query** (Q): "What am I looking for?" 
   - "cat" asks: "What descriptions and actions apply to me?"

2. **Key** (K): "What information do I have?"
   - Each word answers: "I have this information"
   - "sat" → "I'm an action"
   - "the" → "I'm a descriptor"

3. **Value** (V): "What should I remember?"
   - Each word provides actual content to be remembered

### Simplified Example

**Sentence**: "The cat sat"

**Token "cat" paying attention:**

```
Query (Q): "cat is asking - what describes/affects me?"

Looking at each word:

"The" (key): "I'm a descriptor" → Match score: 0.3 (moderate match)
"cat" (key): "I'm a noun"      → Match score: 0.9 (high match, it's me!)
"sat" (key): "I'm an action"   → Match score: 0.4 (some match, I did it)

Normalize these to sum to 100%:
"The": 25%
"cat": 60%  ← focus most on self
"sat": 15%

Mix all the values with these weights:
Output = 0.25×(The's value) + 0.60×(cat's value) + 0.15×(sat's value)
```

Result: "cat" now has a richer representation that includes context from the whole sentence.

## Step 4: Multi-Head Attention

One attention isn't enough. Different words matter for different reasons.

Think of it as asking the question in multiple ways:

```
Head 1: "What adjectives describe me?"     → looks at "The"
Head 2: "What actions do I perform?"       → looks at "sat"
Head 3: "What locations do I relate to?"   → looks at "mat"
```

Eight "attention heads" running in parallel. Each learns different patterns.

Then combine all their insights:

```
Insight 1 (adjectives):  "described, singular"
Insight 2 (actions):     "sat, stationary"
Insight 3 (locations):   "on mat"

Combine: Rich representation of "cat" with multiple perspectives
```

## Step 5: Feed-Forward Network

After attention, each token passes through a simple neural network.

```
Token representation (e.g., "cat's context")
        ↓
  Neural Network
  (2-3 hidden layers)
        ↓
  Enhanced representation
```

Think of it as: "Now that I know my context, let me refine my meaning."

Not much to explain here—it's standard neural network stuff.

## Step 6: Put It Together (One Transformer Block)

```
Input: "The cat sat"
  ↓
Add positional info
  ↓
Multi-head attention (8 heads)
  ↓
Feed-forward network
  ↓
Output: Enhanced representations
```

This is **one block**. Stack 12+ of these, and you have BERT or GPT.

---

# Complete Example: Walking Through "The Cat"

Let's trace one word through a transformer.

```
Input sentence: "The cat sat"

STEP 1: Tokenize
[The] → [0.2, 0.1, -0.3, ...]    (embedding)
[cat] → [0.5, -0.2, 0.1, ...]
[sat] → [0.1, 0.6, -0.1, ...]

STEP 2: Add positions
[The] + pos_0 = [0.2, 0.1, -0.3, ...] + [1.0, 0.0, 0.0, ...]
[cat] + pos_1 = [0.5, -0.2, 0.1, ...] + [0.8, 0.6, 0.0, ...]
[sat] + pos_2 = [0.1, 0.6, -0.1, ...] + [0.0, 1.0, 0.0, ...]

STEP 3: Multi-head attention (for "cat")

Head 1: "cat" looks at all three words
  - Attend 20% to "The", 60% to "cat", 20% to "sat"
  - Output: blend of all three

Head 2: "cat" looks at all three words
  - Attend 10% to "The", 70% to "cat", 20% to "sat"
  - Output: different perspective

...8 heads total

STEP 4: Concatenate head outputs
cat_enhanced = [head1_output, head2_output, ..., head8_output]

STEP 5: Feed-forward network
cat_final = FFN(cat_enhanced)

OUTPUT: "cat" now understands context from "The" and "sat"
```

---

# Why Transformers Win

## 1. **Speed**
- Process all words at once (parallelization)
- GPU-friendly
- ~100× faster than RNNs on long texts

## 2. **Understanding Long Sentences**
- RNNs: Forget word 1 by the time they read word 100
- Transformers: Word 100 directly sees word 1 (no forgetting)
- Works for documents, not just sentences

## 3. **Interpretability**
You can look at attention weights and see what mattered:

```
Predicting next word after "The cat sat on the ___"

Word "cat" focuses 80% on token [___] (what should fill the blank?)
This makes sense! We're looking for what the cat is on.
→ Output: "mat"
```

## 4. **Transfer Learning**
- Pre-train on huge internet text
- Fine-tune on specific tasks
- Works because transformers learn general language understanding

---

# Common Questions

## Q: Doesn't attention need to see the whole sentence to work?

**A**: Yes, but that's actually faster in practice.
- RNN: Sees one word at a time (forced sequential)
- Transformer: Sees whole sentence at once (parallel)

Paradoxically, the transformer is much faster because parallelization overwhelms the overhead.

## Q: What if the sentence is too long?

**A**: Attention has a memory problem:
- Sentence with 1000 words → attention matrix is 1000×1000 (1 million values)
- Sentence with 10,000 words → 100 million values (memory explosion)

Solution: Only attend to nearby words, or use newer techniques (not covered here).

## Q: Why sinusoid for position encoding?

**A**: Sine waves have nice properties:
- Repeating pattern helps model learn relative distances
- Works for any sequence length
- All positions treated similarly

Mathematical, but the intuition: it's a consistent way to represent "position 1, position 2, position 3..." that the model can learn from.

---

# Simple Numeric Example

Let's see attention in action with tiny numbers.

**Input sentence**: "cat sat" (2 tokens, embedding dimension 2)

**Embeddings** (made up numbers):
```
"cat" → [1.0, 0.5]
"sat" → [0.3, 0.8]
```

**Weight matrices** (learned during training):
```
W^Q = [[0.2, 0.1], [0.3, 0.4]]  (query)
W^K = [[0.5, 0.2], [0.1, 0.6]]  (key)  
W^V = [[0.4, 0.3], [0.2, 0.7]]  (value)
```

**Compute Q, K, V**:
```
Q = embeddings × W^Q
K = embeddings × W^K
V = embeddings × W^V
```

For "cat" (first token):
- Query: [1.0, 0.5] × W^Q = [0.25, 0.3]
- Key: [1.0, 0.5] × W^K = [0.4, 0.35]
- Value: [1.0, 0.5] × W^V = [0.35, 0.4]

For "sat" (second token):
- Query: [0.3, 0.8] × W^Q = [0.31, 0.38]
- Key: [0.3, 0.8] × W^K = [0.19, 0.54]
- Value: [0.3, 0.8] × W^V = [0.26, 0.62]

**Attention scores** (for "cat" attending to both):
- Score with "cat": [0.25, 0.3] · [0.4, 0.35] = 0.175
- Score with "sat": [0.25, 0.3] · [0.19, 0.54] = 0.139

**After softmax** (divide by sqrt(2) ≈ 1.41, then normalize):
- Weight to "cat": 0.52
- Weight to "sat": 0.48

**Output for "cat"**:
```
0.52 × [0.35, 0.4] + 0.48 × [0.26, 0.62] = [0.304, 0.508]
```

"cat" now has a blended representation that includes context from "sat".

---

# The Big Picture

Transformers are the foundation of modern AI:
- **BERT**: Understanding text (bidirectional)
- **GPT**: Generating text (one-direction, predicting next word)
- **T5**: Translation and summarization
- **Vision Transformers (ViT)**: Understanding images
- **CLIP**: Understanding text + images together

All use the same core mechanism: **Self-attention on all positions in parallel**.

That's it. That's the transformer.

## Core Innovation: Self-Attention Instead of Recurrence

Transformers replace RNN recurrence with [[Attention Mechanism]].

No hidden state passed between time steps.

Each output position attends to all input positions simultaneously.

**Architecture**:
- Input: Sequence $x_1, x_2, ..., x_T$
- Layer 1: Multi-head self-attention (attends to all positions)
- Layer 2: Feed-forward network (position-wise)
- Repeat (stack many layers)
- Output: Transformed sequence $y_1, y_2, ..., y_T$

## Parallelization

All positions computed simultaneously (parallel for GPU).

**Forward pass**:
- Standard RNN: $T$ sequential steps, 1 GPU active per step
- Transformer: 1 parallel step, all $T$ positions computed together

**Speedup**: $O(T)$ for RNN → $O(1)$ for Transformer (constant w.r.t. sequence length).

Wall-clock time: RNN = $T \times t_{\text{per-step}}$, Transformer ≈ constant.

**Numeric example**:
- Sequence length: 1024 tokens
- RNN: 1024 sequential steps × 1ms per step = 1024 ms
- Transformer: ~10 parallel steps × 5ms per step = 50 ms

**Speedup: 20×**

## Architecture: The Transformer Block

### Self-Attention Layer

Input: Sequence $X \in \mathbb{R}^{T \times d}$ (T positions, each d-dimensional).

Create query, key, value projections:

$$Q = X W^Q$$
$$K = X W^K$$
$$V = X W^V$$

Where $W^Q, W^K, W^V \in \mathbb{R}^{d \times d}$ are learned weight matrices.

**Attention computation** (scaled dot-product):

$$\text{Attention}(Q, K, V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right) V$$

Breaking down:

$$\text{Scores} = \frac{QK^T}{\sqrt{d_k}} \in \mathbb{R}^{T \times T}$$

Entry $(i,j)$ = how much position $i$ attends to position $j$.

$$\text{Weights} = \text{softmax}(\text{Scores}) \in \mathbb{R}^{T \times T}$$

Each row sums to 1 (weights for position $i$).

$$\text{Output} = \text{Weights} \times V \in \mathbb{R}^{T \times d}$$

Weighted sum of values.

### Numeric Example: Self-Attention

**Input**: 3-token sequence, embedding dimension 2.

$$X = \begin{bmatrix} 0.5 & 0.1 \\ 0.3 & 0.8 \\ 0.2 & 0.6 \end{bmatrix}$$

(position 1, 2, 3)

**Weight matrices** (random init):

$$W^Q = \begin{bmatrix} 0.1 & 0.2 \\ 0.3 & 0.1 \end{bmatrix}, \quad W^K = \begin{bmatrix} 0.2 & 0.1 \\ 0.1 & 0.3 \end{bmatrix}, \quad W^V = \begin{bmatrix} 0.3 & 0.1 \\ 0.1 & 0.2 \end{bmatrix}$$

**Compute projections**:

$$Q = X W^Q = \begin{bmatrix} 0.5 & 0.1 \\ 0.3 & 0.8 \\ 0.2 & 0.6 \end{bmatrix} \begin{bmatrix} 0.1 & 0.2 \\ 0.3 & 0.1 \end{bmatrix} = \begin{bmatrix} 0.08 & 0.11 \\ 0.27 & 0.14 \\ 0.20 & 0.10 \end{bmatrix}$$

Similarly for $K$ and $V$.

**Attention scores** (first row of Q):

Query 1: $q_1 = [0.08, 0.11]$

$$\text{score}_{1,1} = [0.08, 0.11] \cdot k_1 = \text{(dot with key 1)}$$
$$\text{score}_{1,2} = [0.08, 0.11] \cdot k_2 = \text{(dot with key 2)}$$
$$\text{score}_{1,3} = [0.08, 0.11] \cdot k_3 = \text{(dot with key 3)}$$

(Actual values depend on $K$, but assume scores = $[0.5, 0.3, 0.1]$ after scaling)

**Softmax**:
$$\text{weights}_1 = \text{softmax}([0.5, 0.3, 0.1]) = [0.44, 0.34, 0.22]$$

Position 1 attends to:
- 44% position 1 (self)
- 34% position 2
- 22% position 3

**Output for position 1**:

$$y_1 = 0.44 \cdot v_1 + 0.34 \cdot v_2 + 0.22 \cdot v_3$$

Blended value.

### Multi-Head Attention

Repeat self-attention multiple times (heads), concatenate:

$$\text{head}_i = \text{Attention}(Q W_i^Q, K W_i^K, V W_i^V)$$

$$\text{MultiHead} = \text{Concat}(\text{head}_1, ..., \text{head}_h) W^O$$

Each head learns different attention patterns.

Example: 8 heads, each 64D (total 512D):
- Head 1: Attends to adjacent tokens
- Head 2: Attends to far tokens
- Head 3-8: Mixed patterns

After concatenation: 512D output, passed through output projection $W^O$.

### Feed-Forward Network

Position-wise (applied independently to each token):

$$\text{FFN}(x) = \max(0, x W_1 + b_1) W_2 + b_2$$

Two linear layers with ReLU activation (hidden layer typically 2-4× input dimension).

**In transformer block**:

Hidden dimension = 512, FFN hidden = 2048.

This is NOT attention; just a neural network per token.

### Layer Normalization and Residual Connections

**Residual connection** (skip connection):

$$x' = x + \text{Attention}(x)$$

(Don't replace, add to original)

**Layer norm**:

$$\text{LayerNorm}(x) = \gamma \cdot \frac{x - \mu}{\sigma + \epsilon} + \beta$$

Normalize each token independently, then scale/shift (learned $\gamma, \beta$).

**Full block**:

```
x ──┐
    ├──→ LayerNorm ──→ MultiHeadAttention ──┐
    │                                        ├──→ +  ──→ y
    └────────────────────────────────────────┘
    
y ──┐
    ├──→ LayerNorm ──→ FFN ────┐
    │                          ├──→ +  ──→ output
    └──────────────────────────┘
```

## Positional Encoding

Transformers have no notion of position (unlike RNNs).

"The cat sat" and "sat cat The" are identical without position information.

**Solution**: Add positional embeddings.

**Sinusoidal positional encoding**:

$$PE_{(t, 2i)} = \sin\left(\frac{t}{10000^{2i/d}}\right)$$

$$PE_{(t, 2i+1)} = \cos\left(\frac{t}{10000^{2i/d}}\right)$$

Where $t$ = position (0, 1, 2, ...), $i$ = dimension index.

### Why sinusoids?

Properties:
- All positions have same encoding dimension
- Encodes absolute and relative positions
- Periodic pattern allows model to learn relative distance

### Numeric Example

Position $t=0$ (first token), dimension $d=4$:

$$PE_{(0,0)} = \sin(0/1) = 0$$
$$PE_{(0,1)} = \cos(0/1) = 1$$
$$PE_{(0,2)} = \sin(0/100) = 0$$
$$PE_{(0,3)} = \cos(0/100) = 1$$

Encoding: $[0, 1, 0, 1]$

Position $t=1$ (second token):

$$PE_{(1,0)} = \sin(1/1) = 0.84$$
$$PE_{(1,1)} = \cos(1/1) = 0.54$$
$$PE_{(1,2)} = \sin(1/100) = 0.01$$
$$PE_{(1,3)} = \cos(1/100) = 1.00$$

Encoding: $[0.84, 0.54, 0.01, 1.00]$

Different from position 0. Model can distinguish positions.

## Masked Self-Attention (For Generation)

During decoding (generating next token), cannot attend to future tokens (don't exist yet).

**Masking**: Set attention scores for future positions to $-\infty$ before softmax.

$$\text{Scores}_{masked} = \text{Scores} + M$$

Where $M_{i,j} = 0$ if $j \leq i$ (can attend), else $-\infty$ (mask out).

After softmax: masked positions have weight 0.

**Effect**: Each position only attends to itself and previous positions.

### Numeric Example

Without mask, attention scores at position 2:
$$\text{Scores} = [0.5, 0.3, 0.7, 0.2] \quad (\text{positions } 1, 2, 3, 4)$$

After softmax:
$$\text{Weights} = [0.25, 0.22, 0.36, 0.17]$$

Position 2 attends 36% to position 3 (future).

**With mask**:
$$M = [0, 0, -\infty, -\infty]$$
$$\text{Scores}_{masked} = [0.5, 0.3, -\infty, -\infty]$$

After softmax:
$$\text{Weights} = [0.62, 0.38, 0, 0]$$

Position 2 cannot attend to future positions.

## Advantages of Transformers

### 1. Parallelization

No sequential dependencies. All positions processed simultaneously.

Training speed: 10-50× faster than RNNs.

### 2. Long-Range Dependencies

Self-attention connects all positions directly.

Gradient flow: Direct path between distant positions.

No vanishing gradients over time.

Effective for sequences up to 2000+ tokens (without truncation).

### 3. Interpretability

Attention weights show which positions matter for each prediction.

```
Input:    "The cat sat on the mat"
Position: 1   2  3  4 5   6

Attention at position 6 (mat):
- Position 1 (The):  0.05
- Position 2 (cat):  0.10
- Position 3 (sat):  0.05
- Position 4 (on):   0.10
- Position 5 (the):  0.20
- Position 6 (mat):  0.50 (self)
```

"mat" mostly attends to itself and "the". This makes sense.

### 4. Transfer Learning

Pre-train on large unlabeled text, fine-tune on downstream tasks.

Transformers capture general language understanding.

Leads to state-of-the-art on many NLP tasks (BERT, GPT, T5, etc.).

## Disadvantages of Transformers

### 1. Memory: Quadratic in Sequence Length

Attention matrix: $T \times T$ (all pairs of positions).

For sequence length 1000: $10^6$ attention weights.
For sequence length 10000: $10^8$ attention weights (memory issues).

RNN memory: Linear in $T$ (only hidden state).

### 2. Slower on Short Sequences

Transformer overhead (multi-head attention, positional encoding) not worth it for short sequences.

RNN: Simple, fast for $T < 20$.

### 3. Position Encoding is Fixed

Learned positional encoding (alternative) doesn't extrapolate beyond training length.

If trained on sequences up to 1000, cannot process 2000-token sequence without retraining.

(Workarounds exist: interpolation, relative positional encoding, ALiBi)

## Transformer Variants

### Encoder-Only (BERT)

Bidirectional attention. Can see full sequence on both sides.

Used for: Classification, tagging, extraction.

### Decoder-Only (GPT)

Masked attention. Can only see previous tokens.

Used for: Language generation, text completion.

### Encoder-Decoder (T5, Transformer)

Encoder: Bidirectional self-attention on input.
Decoder: Masked attention on output, cross-attention to encoder.

Used for: Translation, summarization, question-answering.

## Numeric Complexity

| Component | Complexity | Notes |
|-----------|-----------|-------|
| Multi-head attention | $O(T^2 d)$ | $T$ = seq length, $d$ = hidden dim |
| Feed-forward | $O(T d^2)$ | Per token, fully connected |
| Positional encoding | $O(T d)$ | Computed once |
| Full block | $O(T^2 d + T d^2)$ | Typically $T^2 d$ dominates |
| $L$ stacked blocks | $O(L(T^2 d + T d^2))$ | Full transformer |

For $T=1000, d=512, L=12$ (typical BERT):
$$12 \times (1000^2 \times 512 + 1000 \times 512^2) = 12 \times (5.1 \times 10^8 + 2.6 \times 10^8) \approx 10^{10} \text{ operations}$$

RNN for same setup: $12 \times 1000 \times 512 \times 512 \approx 3 \times 10^9$ operations.

But RNN is sequential (can't parallelize), Transformer is parallel (all tokens at once).

Wall-clock time: Transformer faster despite higher FLOPs.

## State-of-the-Art Models

All modern language models are Transformer-based:

- **BERT**: Pre-trained bidirectional transformer, 110M-340M parameters
- **GPT-2/3/4**: Decoder-only generative transformer, up to 175B parameters
- **T5**: Encoder-decoder for various NLP tasks, 60M-11B parameters
- **Vision Transformer (ViT)**: Applies transformers to images
- **Multimodal**: CLIP (text+image), GPT-4V (text+image+video)

All use same Transformer building blocks described above.

## Summary

Transformers replace RNN recurrence with self-attention.

All positions processed in parallel (fast).

Long-range dependencies handled directly (no vanishing gradients).

Attention weights interpretable.

Memory quadratic in sequence length (limitation).

Foundation of modern deep learning (BERT, GPT, T5, etc.).
