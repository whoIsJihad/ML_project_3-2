# Word2vec & Deep Learning Fundamentals: From N-grams to Neural Embeddings

## Topic Index

- The Old Way: N-grams and Bag of Words (and why they fail)
- Enter Vectors: Word Embeddings and Cosine Similarity
- Word2Vec Architectures: CBOW vs. Skip-gram
- The Computational Bottleneck and Negative Sampling
- The Flaws of Word2Vec: Biases, Time-Dependence, and Polysemy
- Why RNNs are Necessary: Beyond Word2Vec

---

## The Old Way: N-grams and Bag of Words

### What are N-grams?

An **N-gram** is a sequence of N consecutive words from a text.

**Examples:**
- Unigrams (N=1): ["the", "cat", "sat", "on", "the", "mat"]
- Bigrams (N=2): ["the cat", "cat sat", "sat on", "on the", "the mat"]
- Trigrams (N=3): ["the cat sat", "cat sat on", "sat on the", "on the mat"]

**How they're used for NLP:**
- Count how often each N-gram appears
- Use these counts as features for machine learning models
- Example: Document classification by detecting common phrase patterns

### What is Bag of Words (BoW)?

**Bag of Words** treats a document as an unordered collection of words, ignoring grammar and word order.

**Simple example:**
```
Document 1: "the cat sat on the mat"
Bag of Words representation:
- the: 2
- cat: 1
- sat: 1
- on: 1
- mat: 1

This becomes a vector: [2, 1, 1, 1, 1, ...]
(one position for each word in the vocabulary)
```

**How it works:**
1. Build a vocabulary of all unique words across your corpus
2. For each document, count occurrences of each word
3. Represent the document as a count vector
4. Feed these vectors to classifiers

### Fatal Flaws of N-grams and Bag of Words

#### 1. **High Dimensionality**
- Vocabulary size = 50,000 words → each document becomes a 50,000-dimensional vector
- Most entries are zeros (sparse representation)
- High dimensionality = computational burden + overfitting risk

#### 2. **Loss of Word Order and Context**
- "The movie is not good" and "The movie is good" produce similar vectors
- Negation is completely lost
- BoW cannot distinguish between contradictory meanings

#### 3. **No Semantic Understanding**
- "king" and "queen" are treated as unrelated words (different dimensions)
- "car" and "automobile" are treated as different words despite synonym relationship
- The model cannot capture meaning through word relationships

#### 4. **Sparse Representations**
- 50,000-dimensional vectors with mostly zeros are inefficient
- Takes massive amounts of memory and computation
- Difficult to train models effectively with such sparse data

#### 5. **No Generalization Across Similar Words**
- If you've never seen "automobile" in training, the model has zero knowledge about it
- Words that appear in similar contexts should be related, but BoW treats them as completely independent

#### 6. **Curse of Dimensionality**
- More dimensions = need exponentially more training data to properly cover the space
- With 50,000 dimensions, you'd need billions of examples to cover meaningful regions

---

## Enter Vectors: Word Embeddings and Cosine Similarity

### What is a Word Embedding?

A **word embedding** is a fixed-length, dense vector of real numbers that represents a word's meaning.

**Key properties:**
- **Dense:** Most numbers are non-zero (not sparse like BoW)
- **Low-dimensional:** Typically 50-300 dimensions (vs. 50,000 for BoW)
- **Learned:** Values are learned from data, not assigned arbitrarily
- **Semantic:** Similar words have similar vectors

**Example:**
```
Old way (BoW):
"king" → [0, 0, 1, 0, 0, 0, ... 0]  (50,000 dimensions, mostly zeros)

New way (Embedding):
"king" → [0.23, -0.15, 0.89, 0.34, ... 0.12]  (300 dimensions, all meaningful)
```

### The Big Five Personality Traits Analogy

Instead of describing a person by their unique ID, describe them by meaningful characteristics.

**Old way (BoW):**
- Person A = [ID: 1]
- Person B = [ID: 2]
- No way to tell if A and B are similar

**New way (Embedding):**
- Person A = [Openness: 0.85, Conscientiousness: 0.72, Extraversion: 0.60, Agreeableness: 0.78, Neuroticism: 0.45]
- Person B = [Openness: 0.87, Conscientiousness: 0.70, Extraversion: 0.58, Agreeableness: 0.80, Neuroticism: 0.43]

Now you can immediately see: **A and B are very similar people** (most dimensions match closely).

**Applying to words:**
```
"king" embedding might capture:
- Royalty dimension: 0.92
- Male dimension: 0.88
- Authority dimension: 0.85
- Human dimension: 0.95

"queen" embedding would be similar:
- Royalty dimension: 0.91
- Male dimension: -0.87  ← Different here
- Authority dimension: 0.84
- Human dimension: 0.96

Result: "king" and "queen" vectors are very similar (differ mainly in gender).
```

### Cosine Similarity: Measuring Vector Distance

**Definition:** Cosine similarity measures the angle between two vectors. It answers: "How similar are these two direction vectors?"

**Formula:**
$$\text{cosine similarity}(A, B) = \frac{A \cdot B}{||A|| \times ||B||}$$

**Where:**
- A · B = dot product (sum of element-wise multiplication)
- ||A|| = magnitude of vector A
- ||B|| = magnitude of vector B

**Result Range:**
- cosine similarity = **1.0** → vectors point in the same direction (identical meaning)
- cosine similarity = **0.0** → vectors are perpendicular (unrelated)
- cosine similarity = **-1.0** → vectors point in opposite directions (opposite meaning)

**Practical Example:**
```
Vector "king" =   [0.2, 0.9, 0.3, 0.1]
Vector "queen" =  [0.25, 0.88, 0.32, 0.15]

Dot product = (0.2)(0.25) + (0.9)(0.88) + (0.3)(0.32) + (0.1)(0.15)
            = 0.05 + 0.792 + 0.096 + 0.015 = 0.953

Magnitudes ≈ 1.0 each (normalized)

Cosine similarity ≈ 0.953  (Very similar! 95% aligned)

Vector "king" =    [0.2, 0.9, 0.3, 0.1]
Vector "car" =     [0.01, 0.05, 0.8, 0.2]

Dot product = 0.002 + 0.045 + 0.24 + 0.02 = 0.307

Cosine similarity ≈ 0.31  (Quite different! Only 31% aligned)
```

### Why Cosine Similarity (Not Euclidean Distance)?

**Cosine similarity** measures angle, not absolute distance. This is crucial:
- Two vectors pointing in the same direction are similar, even if magnitudes differ
- Robust to scaling (if you double a vector, cosine similarity stays the same)
- Intuitive for meaning: words with same semantic direction = same meaning

**Euclidean distance** measures straight-line distance, which is less appropriate for semantic similarity.

---

## Word2Vec Architectures: CBOW vs. Skip-gram

### Continuous Bag of Words (CBOW)

**Task:** Predict the target word from its surrounding context words.

**Input:** Multiple context words  
**Output:** Single target word  
**Analogy:** Fill-in-the-blank

**Mechanism:**
```
Sentence: "The quick brown fox jumps over the lazy dog"

Training example (window size = 2):
Context input:  ["brown", "fox", "jumps", "over"]  ← Surrounding words
Target output:  "lazy"  ← Word to predict

Another example:
Context input:  ["quick", "brown", "fox", "jumps"]
Target output:  "over"
```

**How embeddings are learned:**
1. Look up embedding vectors for each context word
2. Average them together (or sum them)
3. Pass through a single hidden layer
4. Output layer predicts probability of each possible target word
5. Compare prediction to actual word
6. Backpropagate error to update context embeddings

**Strengths:**
- Faster to train
- Works with smaller datasets
- Good for frequent words

**Weaknesses:**
- Treats order as irrelevant (["brown", "fox"] averaged same as ["fox", "brown"])
- Less effective for rare words

### Skip-gram

**Task:** Predict the context words from a single target word.

**Input:** Single target word  
**Output:** Multiple context words  
**Analogy:** "What words appear near this word?"

**Mechanism:**
```
Sentence: "The quick brown fox jumps over the lazy dog"

Training example:
Target input:    "lazy"  ← Word to predict from
Context targets: ["brown", "fox", "jumps", "over"]  ← Words to predict

Another example:
Target input:    "jumps"
Context targets: ["brown", "fox", "over", "the"]
```

**How embeddings are learned:**
1. Look up embedding vector for the target word
2. Pass through hidden layer
3. For each context word, compute probability of being a neighbor
4. Compare each prediction to actual context words
5. Backpropagate error to update target embeddings

**Strengths:**
- Produces higher-quality embeddings overall
- Better for rare and infrequent words
- Captures directional context better

**Weaknesses:**
- Slower to train (more prediction tasks)
- Requires larger datasets

### Direct Comparison

| Property | CBOW | Skip-gram |
|----------|------|-----------|
| **Input** | Context words | Single word |
| **Output** | Single word | Context words |
| **Direction** | Context → Target | Target → Context |
| **Training Speed** | Fast | Slow |
| **Dataset Size** | Works with small | Needs large |
| **Rare Words** | Struggles | Handles well |
| **Word Quality** | Good | Excellent |
| **Practical Use** | Baseline | Production |

---

## The Computational Bottleneck and Negative Sampling

### The Softmax Problem

**Standard approach (naive):**

To predict the target word, use softmax over the entire vocabulary:

$$P(\text{target word}) = \frac{e^{h \cdot v_{\text{target}}}}{\sum_{w \in V} e^{h \cdot v_w}}$$

Where:
- h = hidden layer output
- v_w = embedding vector for word w
- V = entire vocabulary (50,000 - 1,000,000 words)

**The issue:** Computing the denominator requires summing over **every single word in the vocabulary**.

**Computational cost per training example:**
```
Vocabulary size = 50,000 words
Hidden layer dimension = 300

For each training example:
- Compute dot product with target: 300 operations
- Compute dot product with ALL 50,000 words: 50,000 × 300 = 15,000,000 operations

Training on 1 billion examples:
- 1,000,000,000 × 15,000,000 = 15 × 10^15 operations

This is **computationally infeasible** on modern hardware.
```

**Why you can't skip the denominator:**
- Softmax requires normalizing over all classes (words)
- You can't approximate or sample it easily
- You must compute it exactly

### The Solution: Negative Sampling

**Key insight:** Change the problem from multi-class classification to binary classification.

**Old problem:**
> "What is the probability of this specific target word?"

**New problem:**
> "Are these two words neighbors, yes or no?"

**How it works:**

Instead of predicting 50,000 probabilities, predict just one: P(context_word is neighbor of target_word)

```
For target word "lazy":

Positive example:
- Pair: ("lazy", "fox")
- Label: 1 (yes, they appear together)
- Prediction: sigmoid(h · v_lazy) → 0.8
- Loss: Binary cross-entropy

Negative examples (randomly sampled):
- Pair: ("lazy", "car")
- Label: 0 (no, they don't appear together)
- Prediction: sigmoid(h · v_car) → 0.3
- Loss: Binary cross-entropy

- Pair: ("lazy", "pizza")
- Label: 0
- Prediction: sigmoid(h · v_pizza) → 0.2
- Loss: Binary cross-entropy
```

**The sigmoid function:**

$$\text{sigmoid}(x) = \frac{1}{1 + e^{-x}}$$

- Input: Any real number
- Output: Probability between 0 and 1
- Simple to compute and differentiate

**Binary cross-entropy loss:**

$$\text{Loss} = -[y \log(\hat{y}) + (1-y) \log(1-\hat{y})]$$

Where:
- y = true label (0 or 1)
- ŷ = predicted probability

**Computational comparison:**
```
Standard softmax approach:
- Per example: 50,000 × 300 = 15,000,000 operations

Negative sampling approach:
- Per example: ~10-15 word pairs × 300 = 3,000-4,500 operations

Speed improvement: 3,000 to 5,000x faster!
```

### Why Negative Sampling Works

**Core principle:** The model learns from contrasting positive and negative examples.

- Positive example teaches: "These words should have similar vectors"
- Negative example teaches: "These words should have different vectors"

By repeating this thousands of times, the model learns to embed words based on their co-occurrence patterns in the corpus.

The negative samples don't need to be sampled exhaustively. A random sample of ~10-15 negatives per positive example is sufficient for convergence.

---

## The Flaws of Word2Vec: Biases, Time-Dependence, and Polysemy

### 1. Societal Biases

**The Problem:**
Word2Vec embeddings capture societal biases present in the training text.

**Examples:**
```
Classic bias: gender stereotypes
- "doctor" embedding is closer to "male" than "female"
- "nurse" embedding is closer to "female" than "male"
- "physicist" ~ "male", "homemaker" ~ "female"

This isn't explicitly programmed. It emerges because the training corpus 
reflects these biases in how often certain professions appear with certain genders.

Word arithmetic reveals the bias:
"man" - "woman" ≈ "programmer" - X
Solving for X gives a word closer to "homemaker" than "programmer"
```

**Why this happens:**
- Training data is scraped from the real world (books, news, websites)
- The real world has historical and systemic biases
- Word2Vec faithfully learns statistical patterns from data
- Those patterns include human prejudices

**Consequences:**
- Bias propagates to downstream applications (NLP systems, recommendation systems)
- Perpetuates discrimination in automated decision-making
- May violate fairness and ethics principles

**No perfect solution yet:**
- Can post-process embeddings to reduce known biases (hard to find all)
- Can carefully curate training data (expensive)
- Can use debiasing algorithms (imperfect)
- But bias in embeddings remains a fundamental problem

### 2. Time-Dependence

**The Problem:**
A single Word2Vec model captures meaning frozen at one moment in time. Language evolves.

**Examples:**
```
The word "gay" meant "happy" in 1950s texts.
Training on 1950s texts: "gay" ~ "joyful", "cheerful"

The word "gay" means "homosexual" in 2020s texts.
Training on 2020s texts: "gay" ~ "LGBTQ+", "rainbow"

A single embedding cannot represent both meanings simultaneously.
```

**More dramatic example: "tweet"**
```
Pre-2006: "tweet" = the sound a bird makes
Post-2006: "tweet" = a message on Twitter

Training data from 2000: "tweet" ~ "bird", "chirp"
Training data from 2015: "tweet" ~ "twitter", "social media"
```

**Why this matters:**
- Word meanings shift over time (linguistic drift)
- A frozen embedding cannot track semantic change
- Models trained on old data become outdated
- No easy way to continuously update embeddings without retraining

**The deeper issue:**
- Language is dynamic, but word embeddings are static
- No temporal dimension in the model
- Cannot handle the evolution of meaning

### 3. Polysemy: Multiple Meanings (Homonymy)

**The Problem:**
Words with multiple distinct meanings get a single embedding. The model cannot distinguish between meanings.

**Classic example: "bank"**
```
Meaning 1 (financial): "I deposited money at the bank"
Meaning 2 (river): "We sat on the bank of the river"

Single Word2Vec embedding for "bank":
- Ends up somewhere between financial and geographical meaning
- Not true to either meaning
- Neighbors: ["money", "river", "account", "stream"] (mix of both meanings)

If you use this embedding for a task, which meaning are you getting?
Answer: You get a confused mixture of both.
```

**Another example: "stem"**
```
Meaning 1 (plant): "The rose stem is green"
Meaning 2 (cause): "This problem stems from poor planning"
Meaning 3 (pipe): "The stem of the wine glass broke"

One embedding cannot capture three different meanings well.
```

**Why this is a fundamental limitation:**
- Words have senses, not single meanings
- Context determines the actual meaning
- Word2Vec ignores context during embedding lookup
- A 300-dimensional vector cannot reliably encode multiple unrelated meanings

**Consequences:**
- Embeddings are somewhat meaningful on average, but inaccurate for specific contexts
- Polysemy causes ambiguity in downstream applications
- Information retrieval and similarity tasks fail in edge cases

**Later solutions:**
- **Contextualized embeddings** (ELMo, BERT) generate different vectors for the same word depending on context
- **Sense embeddings** train separate vectors for different word senses
- But Word2Vec doesn't handle this at all

---

## Why RNNs are Necessary: Beyond Word2Vec

### What Word2Vec Cannot Do

Word2Vec produces **static, context-independent embeddings**:
- The vector for "bank" is the same whether discussing money or rivers
- The vector for "running" is the same whether "running" is a verb or adjective
- Word order is completely lost once words are converted to independent embeddings

**Fundamental limitations:**
1. **No context sensitivity:** Same word = same embedding, always
2. **No sequence modeling:** Cannot capture long-range dependencies between words
3. **No temporal dynamics:** Cannot model how meaning changes within a sentence
4. **Fixed vocabulary:** Cannot generalize to unseen words
5. **No grammatical understanding:** Cannot track subject, object, verb relationships across sentences

### The Sequential Problem

Many NLP tasks require understanding **sequences and order**.

**Examples:**
```
Task: Sentiment Analysis
"This movie is not good"
vs.
"This movie is good"

With static embeddings, both become:
[good_embed] [movie_embed] [not_embed] (plus others)

The model must learn that presence of "not" changes meaning.
Word2Vec provides no explicit mechanism for this.

---

Task: Machine Translation
"The bank executive went to the river bank"

To correctly translate each "bank", we need:
- Context from neighboring words
- Understanding of what role "bank" plays in the sentence
- Knowledge of what words will come later

Word2Vec embeddings are context-blind.
```

### Why RNNs (Recurrent Neural Networks)

**Key innovation:** RNNs process text **sequentially**, maintaining a hidden state that carries context forward.

```
Word-by-word processing:
Word 1 "the"      →  RNN  →  hidden_state_1
Word 2 "bank"     →  RNN  →  hidden_state_2  (knows about "the")
Word 3 "manager"  →  RNN  →  hidden_state_3  (knows about "the bank")

At each step, the hidden state accumulates context.
This solves both context-sensitivity AND sequence understanding.
```

**RNNs provide:**
1. **Context sensitivity:** Output depends on all previous words
2. **Sequence modeling:** Can track long-range relationships
3. **Variable length:** Can handle sequences of any length
4. **Learned representation:** Can learn what context matters
5. **Gradient flow:** Can backpropagate through sequences

**Example: RNN predicts next word**
```
Input sequence: "The quick brown"
RNN hidden state builds up meaning progressively
↓
At position 3, the hidden state "understands" we're describing movement/speed
↓
When predicting the 4th word, RNN can output "fox" (fitting the pattern)
vs. random word from a bag-of-words model
```

### The Bridge: From Static to Dynamic

**Word2Vec→ Static representations of words**

**RNN:** Builds dynamic, context-dependent representations of sentences

**The evolution:**
- Word2Vec: "What does each word mean?" (isolated)
- RNN: "What does each word mean given everything before it?" (sequential)
- LSTM/GRU: "What does each word mean given what came before and what comes after?" (bidirectional)
- Transformers: "What does each word mean relative to ALL other words?" (parallel)

**Why the progression was necessary:**
- Harder NLP tasks (translation, question answering, coreference resolution) require context
- Static word embeddings leave context modeling to the neural network
- RNNs build context directly into the architecture
- This makes learning easier and performance better

---

## Summary: The Evolution of Word Representations

### The Problem Statement
How do we represent words so that:
- Similar words are close together
- Computers can process them efficiently
- We capture semantic meaning

### The Solutions

**Bag of Words (Old):**
- ✗ Sparse, high-dimensional
- ✗ No semantic understanding
- ✗ Loss of context
- ✓ Simple

**Word2Vec (Breakthrough):**
- ✓ Dense, low-dimensional
- ✓ Captures some semantics
- ✓ Efficient training
- ✗ Still context-blind
- ✗ Biased, time-dependent, cannot handle polysemy

**RNNs (Next Step):**
- ✓ Context-sensitive
- ✓ Sequential understanding
- ✓ Handles variable length
- ✗ Slower to train
- ✗ More complex

**Future (Transformers/BERT):**
- ✓ Contextualized embeddings (different vector for each occurrence)
- ✓ Parallel processing (faster than RNNs)
- ✓ Captures long-range dependencies
- ✓ Pre-trainable and fine-tunable

### Key Takeaway

Word2Vec solved the immediate problem (meaningful, efficient word representations) but revealed deeper problems (context-sensitivity, bias, polysemy). This motivated the development of RNNs and later, Transformers—models that build sequential/relational understanding into their architecture rather than relying on static embeddings.

