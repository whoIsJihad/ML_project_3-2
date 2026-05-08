# The Illustrated Word2vec: Beginner's Guide to Word Embeddings

## Topic List (Table of Contents)

- What are Vectors?
- Understanding Cosine Similarity
- Introduction to Word Embeddings
- Visualizing Word Embeddings
- The King - Man + Woman = Queen Analogy
- Language Modeling Basics
- Word2vec Architectures: CBOW vs Skip-gram
- The Softmax Bottleneck Problem
- Negative Sampling Solution
- The Word2vec Training Process
- Input and Context Embeddings
- The Dot Product and Activation
- Calculating Error and Backpropagation
- Updating Weights

---

## Introduction to Vectors

### What is a Vector?

A **vector** is simply a list of numbers that represents something. Think of it like a personality profile.

**The Big Five Personality Traits Analogy:**
- Imagine describing a person using 5 numbers (0-100):
  - Openness: 85
  - Conscientiousness: 72
  - Extraversion: 60
  - Agreeableness: 78
  - Neuroticism: 45

This list of numbers IS a vector: **[85, 72, 60, 78, 45]**

**Why use vectors for words?**
- We want computers to understand meaning numerically
- Each number in a word's vector captures something about the word's meaning
- Words with similar meanings will have similar vectors

### Cosine Similarity: Measuring How Alike Two Vectors Are

**The Problem:** How do we know if two vectors are "similar"?

**The Solution:** Use **cosine similarity**, which measures the angle between two vectors.

**Simple Explanation:**
- If two vectors point in nearly the same direction → cosine similarity ≈ 1 (very similar)
- If two vectors point in opposite directions → cosine similarity ≈ -1 (very different)
- If two vectors are perpendicular → cosine similarity ≈ 0 (unrelated)

**Example:**
```
Word Vector 1: "king" = [0.2, 0.9, 0.3, ...]
Word Vector 2: "queen" = [0.25, 0.88, 0.32, ...]
Cosine Similarity = 0.97  ← Very similar! (Both are royalty)

Word Vector 3: "apple" = [0.1, 0.2, 0.8, ...]
Cosine Similarity("king", "apple") = 0.15  ← Not similar
```

**Key Insight:** Words used in similar contexts will have vectors pointing in similar directions.

---

## Introduction to Word Embeddings

### What is a Word Embedding?

A **word embedding** is a vector of numbers that represents a word's meaning. Instead of storing a word as text ("king"), we store it as numbers ([0.2, 0.9, 0.3, ...]).

**Why embeddings matter:**
- Computers work with numbers, not words
- Embeddings capture semantic meaning (what the word means)
- Similar words have similar embeddings
- We can do arithmetic with embeddings! (see analogy below)

### Visualizing Word Embeddings: Color-Coded Arrays

Word embeddings are often shown as **colored grids** or **arrays**:

```
Word: "king"
┌─────┬─────┬─────┬─────┐
│0.2  │0.9  │0.3  │-0.1 │  (each cell is one number)
└─────┴─────┴─────┴─────┘
 Red   Blue  Green Yellow

In practice, embeddings have hundreds of numbers (e.g., 300-dimensional)
```

Each color intensity represents the strength of that number:
- **Bright red** = Large positive number
- **Dark blue** = Large negative number
- **Gray** = Number close to zero

### The King - Man + Woman = Queen Analogy

This is the magic of word embeddings!

**The Concept:**
```
king - man + woman = queen
```

**What this means:**
- Take the embedding vector for "king"
- Subtract the embedding vector for "man" (removes "male" meaning)
- Add the embedding vector for "woman" (adds "female" meaning)
- You get something very close to the embedding vector for "queen"!

**Why does this work?**
- "king" captures meaning about [royalty, male, authority, ...]
- "man" captures meaning about [male, human, ...]
- "woman" captures meaning about [female, human, ...]
- When you do the math: [royalty, male, ...] - [male, ...] + [female, ...] = [royalty, female, ...]
- That's exactly what "queen" means!

**Other Examples:**
```
Paris - France + Germany ≈ Berlin
good - better + best ≈ better (showing gradation)
dog - dogs + cats ≈ cat (showing relationships)
```

**Key Insight:** Embeddings don't just capture meaning—they capture *relationships* between meanings!

---

## Language Modeling Basics

### The Core Idea: Predicting the Next Word

Language models work by learning to predict what word comes next.

**Simple Example:**
```
Training sentence: "The quick brown fox jumps over the lazy dog"

We show the model:
Context (input):    "The quick brown"
Next word (target):  "fox"

Then:
Context:     "quick brown fox"
Target:      "jumps"

Then:
Context:     "brown fox jumps"
Target:      "over"
```

### The Sliding Window Technique

We use a **sliding window** (fixed-size context) to create training examples:

```
Original sentence: "The quick brown fox jumps over the lazy dog"

Window size = 3 (look at 3 words to predict the 4th)

─────────────────
The    quick   brown  | FOX        ← Predict "fox" from 3 previous words
─────────────────

       quick   brown  fox  | JUMPS  ← Predict "jumps" from 3 previous words
─────────────────────

       brown   fox    jumps| OVER   ← Predict "over"
─────────────────────

       fox     jumps  over | THE    ← Predict "the"
```

Each (context, target) pair becomes a training example.

### Why This Works

By learning to predict the next word, the model learns:
- Which words typically go together
- The relationship between words
- The meaning of words (from how they're used)

This is called **distributional semantics**: *"A word is known by the company it keeps"*

---

## Word2vec Architectures: CBOW vs Skip-gram

Word2vec uses two different approaches. Let's compare them:

### Continuous Bag of Words (CBOW)

**Direction:** Context → Target

**How it works:**
- Input: The context words (surrounding words)
- Output: Predict the middle word
- Think of it like fill-in-the-blank

```
Training Example:
Input:   ["The", "quick", "brown", "fox", "jumps", "over", "the"]
         └────────── context ──────────┘        └─ target ─┘

CBOW predicts: "lazy" from ["fox", "jumps", "over", "the"]
(What word comes after these 4 words?)
```

**When to use CBOW:**
- Faster to train
- Works well with small datasets
- Better for frequent words

### Skip-gram

**Direction:** Target → Context

**How it works:**
- Input: The middle word
- Output: Predict the surrounding words
- Think of it like "what words appear near this word?"

```
Training Example:
Input:   "lazy"
Output:  ["fox", "jumps", "over", "the"]

Skip-gram predicts: ["fox", "jumps", "over", "the"] from "lazy"
(What words appear around "lazy"?)
```

**When to use Skip-gram:**
- Slower but produces better embeddings
- Works better with large datasets
- Better for rare words
- Usually preferred in practice

### Side-by-Side Comparison

| Aspect | CBOW | Skip-gram |
|--------|------|-----------|
| Input | Context words | Single word |
| Output | Single word | Context words |
| Speed | Faster | Slower |
| Dataset Size | Small | Large |
| Word Quality | Good for common | Good for rare |
| Use Case | Quick baseline | Production use |

---

 
**Example:**
```
Input: "The quick brown"

Output should be:
- P("fox") = 0.85     ← Correct word, high probability
- P("dog") = 0.05     ← Related but not right
- P("car") = 0.02     ← Unrelated
- P("elephant") = 0.01
- ... (50,000 more probabilities)
```

Every probability must be between 0 and 1, and they must sum to 1.0.

### Why One Neuron Per Word?

In neural networks, each output neuron produces one number (an unnormalized score or "logit").

**Standard approach:**
```
Hidden layer: 100 neurons
       ↓ (fully connected layer)
Output layer: 1 neuron per word in vocabulary
       ↓
If vocabulary = 50,000 words → 50,000 output neurons
```

**Why?** Because we need to score every possible word:
- Neuron 1 scores "the"
- Neuron 2 scores "a"
- Neuron 3 scores "dog"
- ...
- Neuron 50,000 scores "xylophone"

Each neuron produces a raw score (could be -10, 0, 5, 1000, anything).

**The problem:** 50,000 neurons means the weight matrix from hidden→output is massive:
```
Weights matrix size: 100 (hidden) × 50,000 (output) = 5,000,000 parameters

Just storing this matrix takes memory.
Computing the full forward pass takes time.
```

### The Softmax Function: Converting Scores to Probabilities

Raw neuron scores aren't probabilities—they don't sum to 1. We use **softmax** to fix this.

**Softmax formula:**

$$\text{Softmax}_i = \frac{e^{x_i}}{\sum_{j=1}^{V} e^{x_j}}$$

**What this does:**
- Numerator: $e^{x_i}$ — Exponentiates each raw score (makes large scores larger, small scores tiny)
- Denominator: $\sum_{j=1}^{V} e^{x_j}$ — Sum of exponentials over **ALL V words**
- Result: A probability between 0 and 1 that sums to 1

**Concrete example:**
```
Raw scores from hidden layer:
- P_raw("fox") = 5.2
- P_raw("dog") = 3.1
- P_raw("cat") = 2.8
- P_raw("car") = -1.5

Step 1: Exponentiate all scores
- e^5.2 = 181.3
- e^3.1 = 22.2
- e^2.8 = 16.4
- e^(-1.5) = 0.22
- ...50,000 more exponentials...

Step 2: Sum ALL exponentials
- Denominator = 181.3 + 22.2 + 16.4 + 0.22 + ... (50,000 terms)
- Let's say denominator = 52,000 (example)

Step 3: Normalize each score
- P("fox") = 181.3 / 52,000 = 0.349
- P("dog") = 22.2 / 52,000 = 0.043
- P("cat") = 16.4 / 52,000 = 0.032
- P("car") = 0.22 / 52,000 = 0.000004
```

Now the probabilities sum to 1.0 and represent a valid distribution!

### The Bottleneck: Why Softmax Requires the Full Vocabulary

**The mathematical requirement:**

Softmax is defined as:
$$P(w_i|context) = \frac{e^{s_i}}{\sum_{j=1}^{V} e^{s_j}}$$

where $s_i$ is the score for word $i$, and $V$ is vocabulary size (~100,000 words).

**The problem:** Computing this probability requires the denominator $\sum_{j=1}^{V} e^{s_j}$—you must sum over ALL V words, every single example.

**Why you cannot avoid this:**
- The denominator is part of the mathematical definition of softmax
- Cross-entropy loss is: $L = -\log P(w_{target}|context) = -s_{target} + \log(\sum_{j=1}^{V} e^{s_j})$
- You cannot compute the loss without computing the full sum
- Gradient descent requires computing gradients, which depend on the loss
- There is no way to train without this denominator

**Computational cost per example:**
- Forward pass: $V$ exponentials + $V$ additions = O(V)
- Backward pass: Gradient computation also requires O(V) operations
- Training: 1 billion word examples × 100,000 vocabulary = $10^{14}$ operations
- On a GPU (10^12 ops/sec): 100,000 seconds ≈ 27 hours just for one epoch
- Reality: Most datasets need 5-10 epochs = weeks of training per GPU



---

## Negative Sampling Solution

### The Core Change: Reformulate the Objective

**Instead of:**
Maximize: $P(w|context) = \frac{e^{v_w \cdot v_c}}{\sum_{j=1}^{V} e^{v_j \cdot v_c}}$ (requires summing over V words)

**Word2vec does:**
Maximize: $P(D=1|w, c) = \sigma(v_w \cdot v_c)$ (binary classification)

where:
- $v_w$ = embedding of focus word
- $v_c$ = embedding of context word  
- $\sigma(x) = \frac{1}{1+e^{-x}}$ = sigmoid function
- $P(D=1|w,c)$ = probability that $w$ and $c$ are neighbors

### The Loss Function

**For one positive pair and k negative samples:**

$$L = -\log\sigma(v_w \cdot v_c) - \sum_{i=1}^{k} \log\sigma(-v_{w_i} \cdot v_c)$$

**Breaking this down:**
- First term: Push $v_w$ and $v_c$ vectors close together (maximize their dot product)
- Second term: Push $v_{w_i}$ and $v_c$ vectors apart (minimize their dot products)
- $k$ = number of negative samples (typically 5-20)
- Total: 1 + k computations instead of V = 100,000

### Why This Works

**The intuition:**
- Positive pair: maximize $v_w \cdot v_c$ (similarity)
- Negative pairs: minimize $v_{w_i} \cdot v_c$ (dissimilarity)
- Result: Similar words' vectors align; dissimilar words' vectors separate

**The trick:** Random negative sampling approximates the full softmax objective. As $k \to \infty$, negative sampling converges to softmax, but with $k=5-20$ it learns well and stays O(k) instead of O(V).

### Negative Sampling in Practice

**Training example:**
```
Sentence: "the quick brown fox jumps over the lazy dog"
Context window for "brown": ["quick", "fox"]

Positive pairs:
  (brown, quick) → 1
  (brown, fox) → 1

For "brown", sample 5 random negative words:
  (brown, pizza) → 0
  (brown, car) → 0
  (brown, dinosaur) → 0
  (brown, mathematics) → 0
  (brown, elephant) → 0
```

**Per example computation:**
- Positive pairs: compute sigmoid(dot_product) for each
- Negative pairs: compute sigmoid(dot_product) for each
- Total: O(k) operations where k ≈ 10-20, not O(V) where V ≈ 100,000
- Speedup: 5,000-10,000x compared to full softmax

---

## The Word2vec Training Algorithm

### Data Structure: Two Embedding Matrices

Word2vec maintains two embedding matrices:

**$W \in \mathbb{R}^{V \times d}$**: Input embeddings (word as focus)
- Row $i$ = embedding of word $i$ when it's the center word
- Shape: [vocabulary_size × embedding_dimension]
- Example: [100,000 × 300]

**$C \in \mathbb{R}^{V \times d}$**: Context embeddings (word in context)
- Row $j$ = embedding of word $j$ when it's nearby
- Shape: [vocabulary_size × embedding_dimension]
- Example: [100,000 × 300]

**Total parameters: $2 \times V \times d = 60$ million for 300-dim embeddings**

### Training Algorithm (Skip-gram with Negative Sampling)

**Input:** Text corpus  
**Output:** Learned embeddings $W$

```
For each epoch:
  For each word w in corpus:
    For each word c in context_window(w):
      # 1 positive example
      compute_and_update(w, c, label=1)
      
      # k negative examples (sample k random words)
      For i = 1 to k:
        w_neg = random_word_from_vocabulary()
        compute_and_update(w, w_neg, label=0)
```

### Core Update Equation

**For each (word, context) pair with label $y \in \{0, 1\}$:**

1. **Forward pass:**
   $$z = v_w \cdot v_c = \sum_{d=1}^{D} W[w,d] \times C[c,d]$$
   $$\hat{y} = \sigma(z) = \frac{1}{1+e^{-z}}$$

2. **Compute error:**
   $$\delta = \hat{y} - y$$

3. **Update embeddings** (gradient descent with learning rate $\eta$):
   $$W[w, :] \leftarrow W[w, :] - \eta \cdot \delta \cdot C[c, :]$$
   $$C[c, :] \leftarrow C[c, :] - \eta \cdot \delta \cdot W[w, :]$$

**What this does:**
- If $\delta > 0$ (prediction too high): subtract the updates (push vectors apart)
- If $\delta < 0$ (prediction too low): add the updates (pull vectors together)
- Magnitude of update is proportional to error size

### Concrete Example

**Setup:**
- Embedding dimension: $d=3$ (normally 300, using 3 for clarity)
- Learning rate: $\eta=0.025$
- Focus word "king" embedding: $v_w = [0.1, 0.5, 0.2]$
- Context word "queen" embedding: $v_c = [0.15, 0.48, 0.18]$

**Step 1: Forward pass (positive pair, label=1)**
$$z = 0.1 \times 0.15 + 0.5 \times 0.48 + 0.2 \times 0.18$$
$$z = 0.015 + 0.24 + 0.036 = 0.291$$
$$\hat{y} = \sigma(0.291) = \frac{1}{1+e^{-0.291}} = 0.572$$

**Step 2: Error**
$$\delta = 0.572 - 1 = -0.428$$

**Step 3: Update (negative delta means pull vectors together)**
$$W["king", :] \leftarrow [0.1, 0.5, 0.2] - 0.025 \times (-0.428) \times [0.15, 0.48, 0.18]$$
$$W["king", :] \leftarrow [0.1, 0.5, 0.2] + [0.0016, 0.0051, 0.0019]$$
$$W["king", :] \leftarrow [0.1016, 0.5051, 0.2019]$$

**Result:** "king" embedding moved slightly toward "queen"

**Step 4: Negative example (random negative, label=0)**
- Same process but with different context word (e.g., "pizza")
- If prediction was high (vectors too similar), push them apart

### Multiple Epochs

**Epoch 1:** Process entire corpus once, updating all embeddings  
**Epoch 2:** Process corpus again, refining embeddings further  
**Epochs 3-5:** Continue improving (diminishing returns)

**Final result after multiple epochs:**
- Similar words' embeddings converge to similar directions
- Dissimilar words' embeddings diverge
- Analogical relationships emerge automatically

---

## Why Word2vec Works

### The Mechanism

After repeated updates across billions of word pairs:

1. Words that appear together in training data have their embeddings pulled closer (negative $\delta$)
2. Words that don't appear together have their embeddings pushed apart (positive $\delta$)
3. This creates vector clusters: words with similar contexts converge to nearby directions
4. Linear relationships emerge: $v_{king} - v_{man} \approx v_{queen} - v_{woman}$ because both pairs encode the same semantic transformation

### Why Analogies Work

**King-Man+Woman=Queen emerges mechanically because:**
- "king" and "queen" co-occur in similar contexts → updates pull their vectors together
- "king" and "man" often appear together ("king's man", etc.) → their difference captures "maleness"
- "queen" and "woman" often appear together ("queen of women", etc.) → their difference captures "femaleness"
- Vector arithmetic: $v_{king} - v_{male} + v_{female} \approx v_{queen}$ is a consequence of these co-occurrence patterns

**This is deterministic, not magic.** No analogies are hard-coded. Geometry emerges automatically because the training objective (binary classification on word pairs) forces vectors to preserve co-occurrence information in their relative positions.

---

## Summary

**The core idea:** Binary classification on word pairs (are they neighbors?) produces embeddings where:
- Similar words cluster together (pulled by positive examples)
- Dissimilar words separate (pushed by negative examples)
- Vector arithmetic works: $v_a - v_b + v_c$ recovers analogous relationships

**Key equations:**
- Loss per pair: $L = -y\log\sigma(v_w \cdot v_c) - (1-y)\log(1-\sigma(v_w \cdot v_c))$
- Update: $W[w] \leftarrow W[w] - \eta(\sigma(v_w \cdot v_c) - y) \cdot C[c]$
- Speedup: $O(k)$ for k negative samples vs $O(V)$ for full softmax

**Why it works:** Millions of update steps via gradient descent on a well-motivated objective. Word geometry emerges from co-occurrence statistics, not explicit programming.
