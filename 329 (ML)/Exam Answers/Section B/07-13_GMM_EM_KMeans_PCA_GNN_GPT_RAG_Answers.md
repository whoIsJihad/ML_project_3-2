# 📝 GMM, EM, K-Means, PCA, GNN, GPT, RAG - Exam Answers

## GMM & EM Algorithm

### Q1: Why is GMM soft clustering while K-Means is hard?

**K-Means:** Each point assigned to exactly one cluster
$$r_{ik} \in \{0, 1\}$$

**GMM:** Each point has probability of belonging to each cluster
$$r_{ik} = P(z=k | x_i) \in [0, 1]$$

**Advantages of soft:**
- Captures uncertainty (point could be on cluster boundary)
- Probabilistic interpretation
- Fits better when clusters overlap

---

### Q2: EM algorithm: E-step and M-step

**E-step (Expectation):** Compute responsibilities (how much each data point belongs to each cluster)
$$r_{ik} = \frac{\pi_k \mathcal{N}(x_i | \mu_k, \Sigma_k)}{\sum_{j} \pi_j \mathcal{N}(x_i | \mu_j, \Sigma_j)}$$

**M-step (Maximization):** Update parameters to maximize expected log-likelihood
$$\mu_k ← \frac{\sum_i r_{ik} x_i}{\sum_i r_{ik}}$$
$$\Sigma_k ← \frac{\sum_i r_{ik} (x_i - \mu_k)(x_i - \mu_k)^T}{\sum_i r_{ik}}$$

**Convergence:** Guaranteed (monotonically increases likelihood).

---

### Q3: Why EM works for latent variables

**Latent variables:** Unobserved (e.g., which cluster each point belongs to).

**Complete likelihood:** If we knew latent assignments
$$L = \sum_{i,k} r_{ik} [\log \pi_k + \log \mathcal{N}(x_i | \mu_k)]$$

Easy to maximize!

**Incomplete likelihood:** We don't know $r_{ik}$
$$L = \sum_i \log \sum_k \pi_k \mathcal{N}(x_i | \mu_k)$$

Hard (intractable).

**EM bridges:** E-step estimates $r_{ik}$ from current parameters. M-step uses estimates to optimize.

---

## K-Means Clustering

### Q1: Why does K-Means++ initialization help?

**Random init:** May pick clusters close together → poor local optimum.

**K-Means++:**
1. Pick first center randomly
2. For remaining $K-1$: Pick point $x$ with probability $\propto \min_k \|x - \mu_k\|^2$

**Effect:** Spreads initial centers → better initialization → better final solution.

**Empirical:** ~10% better accuracy, ~2× faster convergence.

---

### Q2: How to choose K?

**Elbow method:**
- Plot objective $J = \sum_i \|x_i - \mu_{k(i)}\|^2$ vs. $K$
- Find "elbow" (diminishing returns)
- Example: $J$ drops fast K=1-3, then slow after K=3 → choose K=3

**Silhouette score:**
$$s_i = \frac{b_i - a_i}{\max(a_i, b_i)}$$

where $a_i$ = intra-cluster distance, $b_i$ = inter-cluster distance.

Higher is better (tight clusters, far apart).

---

## PCA (Principal Component Analysis)

### Q1: How to choose number of components?

**Explained variance:** Component $k$ explains $\lambda_k / \sum_j \lambda_j$ of total variance.

**Cumulative:** Keep components until cumulative ≥ 95% or 99%.

**Example:**
```
λ₁=50, λ₂=30, λ₃=15, λ₄=5 (total=100)

PC1: 50/100 = 50%  cumulative = 50%
PC2: 30/100 = 30%  cumulative = 80%
PC3: 15/100 = 15%  cumulative = 95%  ← stop here

Keep 3 components for 95% variance
```

---

### Q2: Why PCA sensitive to scale?

**Large-scale features dominate:**
- Feature 1: range [0, 1]
- Feature 2: range [0, 10000]

Variance of feature 2: ~ $10000^2$ → dominates PCA

First PC captures feature 2 (not interesting patterns).

**Solution:** Standardize features before PCA (mean=0, std=1).

---

## GNN (Graph Neural Networks)

### Q1: Message passing explained

$$h_i^{(l+1)} = \text{UPDATE}(h_i^{(l)}, \text{AGGREGATE}(\{h_j^{(l)} : j \in N(i)\}))$$

**Aggregate:** Combine neighbor features (mean, sum, max, attention).

**Update:** Non-linear transformation (neural network).

**Effect:** Each node incorporates neighborhood information.

---

### Q2: Why GNN powerful for graphs?

**Leverage structure:** Ignores edges = loses information.

**Inductive:** Generalizes to unseen nodes (unlike spectral methods).

**Flexible:** Different aggregation strategies for different graph types.

---

## Decoder-Only Architectures (GPT)

### Q1: Causal masking explained

**Standard attention:** Token can see all positions.

**Causal masking:** Token at position $t$ can only see positions $< t$ (not future).

**Why:** Prevents "cheating" during training. Model must predict future based on past only.

**Implementation:** Set attention scores to $-\infty$ for future positions before softmax.

---

### Q2: In-context learning explained

**Few-shot prompt:**
```
Input: apple → Category: fruit
Input: car → Category: vehicle
Input: dog → Category: ?
```

**How it works:**
- Attention over examples
- Weights attend to relevant examples
- Model learns pattern without gradient updates
- Predicts: animal (or pet)

**Magic:** Large models can "learn" from examples in prompt (in-context).

---

## RAG (Retrieval-Augmented Generation)

### Q1: Retriever types

**Sparse (BM25):** Keyword matching
- Fast
- Misses semantic synonyms

**Dense (embeddings):** Semantic similarity
- Slow (compute embeddings)
- Catches synonyms
- Requires vector DB (Pinecone, Weaviate)

**Hybrid:** Combine sparse + dense
- Best of both
- Slightly slower

---

### Q2: Why RAG better than fine-tuning?

**Fine-tuning:**
- Train on new data
- Knowledge encoded in parameters
- No source attribution
- Must retrain for new data

**RAG:**
- Retrieve new data at inference
- Knowledge in external database
- Can cite sources
- Add new documents without retraining

**Trade-off:** RAG faster to update, fine-tuning may be more accurate if high quality training data.

---

