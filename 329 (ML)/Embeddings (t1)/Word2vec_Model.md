# Word2vec: The Model

## Core Idea

Word2vec learns word embeddings by predicting word co-occurrence. Two words are "neighbors" if they appear close together in text.

**Key insight:** Instead of softmax over 100,000 words (expensive), use binary classification: are these two words neighbors? (cheap)

---

## Notation Guide (Read This First)

Here's what each symbol means:

| Symbol | Meaning | Example |
|--------|---------|---------|
| V | Vocabulary size | 100,000 |
| d | Embedding dimension | 300 |
| W | Input embeddings matrix (V x d) | Each row = one word's vector |
| C | Context embeddings matrix (V x d) | Each row = one word's context vector |
| v_w | Embedding vector of word w | [0.23, -0.15, 0.82, ...] |
| v_c | Context embedding of word c | [0.19, -0.12, 0.78, ...] |
| v_w · v_c | Dot product (element-wise multiply & sum) | 0.0437 + 0.0018 + ... |
| σ(x) | Sigmoid: 1/(1+e^(-x)) | Converts number to 0-1 |
| y | True label | 1 if neighbors, 0 if not |
| ŷ | Model's prediction | Probability 0-1 |
| δ | Error | ŷ - y |
| η | Learning rate | 0.01 to 0.05 |

---

## The Model

### Architecture: Two Embedding Matrices

**Input embeddings:** W in R^(V x d)
- Each row i is the embedding vector for word i as focus word
- Shape: [100,000 words × 300 dimensions]
- Example: word "king" = [0.23, -0.15, 0.82, ..., 0.11]

**Context embeddings:** C in R^(V x d)
- Each row j is the embedding vector for word j in context
- Same shape: [100,000 words × 300 dimensions]
- Learned separately from W

**Why two matrices?** Center words and context words play different roles in training. They learn different vector representations.

---

## Input & Output

### Input
**Positive pair:** Two words that appear together
- Example: ("quick", "brown") from "quick brown fox"

**Negative pair:** Two words that don't appear together
- Example: ("quick", "pizza") — never in corpus together

### Output
**Learned embeddings W** — word vectors capturing meaning from co-occurrence

**Result after training:** Similar words cluster together
- cosine_similarity(king, queen) = 0.92
- cosine_similarity(king, pizza) = 0.15

---

## Training: The Update Rule

**For each word pair (w, c) with label y (0 or 1):**

### Step 1: Predict similarity
```
z = v_w · v_c
ŷ = σ(z) = 1/(1+e^(-z))
```

Meaning:
- z = dot product (multiply matching positions, sum all)
- ŷ = sigmoid output (probability 0-1 that they're neighbors)

### Step 2: Compute error
```
δ = ŷ - y
```

Meaning:
- Positive pair (y=1): If ŷ=0.3, then δ=-0.7 (too low, need to increase)
- Negative pair (y=0): If ŷ=0.8, then δ=0.8 (too high, need to decrease)

### Step 3: Update embeddings
```
W[w] ← W[w] - η·δ·C[c]
C[c] ← C[c] - η·δ·W[w]
```

Meaning:
- Multiply error by learning rate by the other word's vector
- If δ < 0 (pull together): subtract becomes add, vectors move toward each other
- If δ > 0 (push apart): subtract moves them away

### Concrete example:
```
Positive pair: ("king", "queen"), y=1
Initial:
  v_king = [0.1, 0.5, 0.2]
  v_queen = [0.15, 0.48, 0.18]

Step 1: Predict
  z = 0.1*0.15 + 0.5*0.48 + 0.2*0.18 = 0.291
  ŷ = σ(0.291) = 0.572 (57.2% confident neighbors)

Step 2: Error
  δ = 0.572 - 1 = -0.428 (too low!)

Step 3: Update (η = 0.025)
  W[king] = [0.1, 0.5, 0.2] - 0.025*(-0.428)*[0.15, 0.48, 0.18]
          = [0.1, 0.5, 0.2] + [0.0016, 0.0051, 0.0019]
          = [0.1016, 0.5051, 0.2019]
          
Result: "king" moved slightly toward "queen"
```

**Repeat billions of times** across corpus, multiple epochs

---

## CBOW vs Skip-gram

| Aspect | CBOW | Skip-gram |
|--------|------|-----------|
| Task | Predict word from context | Predict context from word |
| Input | Context words (surrounding) | Single word (center) |
| Output | Single target word | Multiple context words |
| Training pairs | (context, target) | (word, context_i) for each context word |
| Speed | Faster | Slower |
| Quality | Good for common words | Better overall; good for rare words |
| Use case | Quick baseline | Production; larger datasets |

### CBOW (Continuous Bag of Words)

**Architecture:**
```
Context: ["the", "quick", "brown", "fox", "jumps"]
Input: average their embeddings together
Hidden layer: 300 dimensions
Output: predict "over"
```

**Training:**
- Slide window across text
- Input: 4 context words → average their embeddings
- Output: predict the target word in middle
- Example: ["the", "quick", "brown", "fox"] → predict "jumps"

**When to use:** Small datasets, quick training, focus on frequent words

### Skip-gram

**Architecture:**
```
Input: "brown"
Hidden layer: 300 dimensions
Output: ["quick", "fox"] (each word separately)
```

**Training:**
- For each word in corpus
- For each word in its context window, create separate training example
- Example: word "brown" with window ["quick", "fox"]
  - Train ("brown" → "quick")
  - Train ("brown" → "fox")

**When to use:** Large datasets, better quality, rare words, production systems

---

## The Trick: Negative Sampling

**Traditional approach (expensive):** Predict probabilities for all 100,000 words using softmax

**Word2vec approach (cheap):** Simple yes/no: are these two words neighbors?

**Loss function:**
```
L = -y*log(σ(v_w·v_c)) - (1-y)*log(1-σ(v_w·v_c))
```

**For each positive pair, add k random negative pairs** (k=5-20)
- Positive: (word, nearby_word) → label 1
- Negatives: (word, random_word) → label 0 (k times)

**Why faster:**
- Traditional: compute score for 100,000 words per example
- Word2vec: compute score for 1 positive + k negatives (k ≈ 20)
- Speedup: 100,000 / 20 = **5,000x faster**

---

## Training Algorithm

```
For each epoch:
  For each word w in corpus:
    For each context word c in window(w):
      # Positive pair
      Forward: z = v_w · v_c, ŷ = σ(z)
      Backward: δ = ŷ - 1
      Update: W[w] -= η·δ·C[c], C[c] -= η·δ·W[w]
      
      # k negative samples
      For i = 1 to k:
        w_neg = random_word()
        Forward: z = v_w · v_neg, ŷ = σ(z)
        Backward: δ = ŷ - 0
        Update: W[w] -= η·δ·C[w_neg], C[w_neg] -= η·δ·W[w]
```

After multiple epochs: Similar words' vectors converge; analogies emerge.

---

## Why Analogies Work

**Example:** v_king - v_man + v_woman ≈ v_queen

**How it emerges mathematically:**

The update rule δ = ŷ - y pulls similar words together and pushes dissimilar words apart.

After billions of updates:
- ("king", "queen") appear in similar contexts → vectors v_king and v_queen converge toward each other
- ("king", "man") often appear together → difference v_king - v_man captures what distinguishes "king" from "man"
- ("queen", "woman") often appear together → difference v_queen - v_woman captures what distinguishes "queen" from "woman"
- These differences encode the same transformation (sovereignty), so:

```
v_king - v_man ≈ v_queen - v_woman
```

Rearrange:
```
v_king - v_man + v_woman ≈ v_queen
```

**This is automatic—no explicit programming.** The training objective naturally encodes semantic relationships in vector geometry.

---

## Summary

| Question | Answer |
|----------|--------|
| **What?** | Learn word embeddings via co-occurrence prediction |
| **Input** | Word pairs: positive (nearby) and negative (random) |
| **Training** | Binary classification with sigmoid loss; gradient descent |
| **Output** | Matrix W: embeddings where similar words cluster |
| **CBOW** | Context → target; faster; good for common words |
| **Skip-gram** | Target → context; slower; better quality; good for rare words |
| **Why cheap** | Negative sampling: O(k) instead of O(V) per pair |
| **Why it works** | Update rule pulls similar words together, pushes dissimilar apart |
