# EM Algorithm in Gaussian Mixture Models (GMM)

A deep dive into how the Expectation-Maximization algorithm learns Gaussian clusters from data.

---

## The Core Idea

A **Gaussian Mixture Model** is a probabilistic model that says:

> "My data is a mixture of $K$ Gaussian distributions. I don't know which sample came from which Gaussian, but I can learn them."

**Generative Model:**

To generate a sample $\mathbf{x}$:
$$z \sim \text{Categorical}(\boldsymbol{\pi}) \quad \Rightarrow \quad \mathbf{x} | z=k \sim \mathcal{N}(\boldsymbol{\mu}_k, \boldsymbol{\Sigma}_k)$$

Where:
- $z \in \{1, 2, \ldots, K\}$ is the **hidden** cluster assignment
- $\boldsymbol{\pi} = [\pi_1, \pi_2, \ldots, \pi_K]$ are mixing weights with $\sum_{k=1}^K \pi_k = 1$
- $\boldsymbol{\mu}_k$ is the mean of cluster $k$ (shape: $d \times 1$)
- $\boldsymbol{\Sigma}_k$ is the covariance of cluster $k$ (shape: $d \times d$)

We observe $\mathbf{x}$ but not $z$.

---

## The Learning Problem

**Given:** Data $\mathbf{X} = \{\mathbf{x}_1, \mathbf{x}_2, \ldots, \mathbf{x}_n\}$

**Find:** Parameters $\boldsymbol{\theta} = (\boldsymbol{\mu}_1, \ldots, \boldsymbol{\mu}_K, \boldsymbol{\Sigma}_1, \ldots, \boldsymbol{\Sigma}_K, \boldsymbol{\pi})$

**Goal:** Maximize likelihood:

$$\boldsymbol{\theta}^* = \arg\max_{\boldsymbol{\theta}} \log P(\mathbf{X}|\boldsymbol{\theta}) = \arg\max_{\boldsymbol{\theta}} \sum_{i=1}^n \log\left(\sum_{k=1}^K \pi_k \mathcal{N}(\mathbf{x}_i | \boldsymbol{\mu}_k, \boldsymbol{\Sigma}_k)\right)$$

The sum inside the log makes direct optimization hard (non-convex).

---

## The EM Solution

### E-Step: Compute Responsibilities

Given current $\boldsymbol{\theta}$, compute the **responsibility** (posterior probability):

$$r_{ik} = P(z_i = k | \mathbf{x}_i, \boldsymbol{\theta}) = \frac{\pi_k \mathcal{N}(\mathbf{x}_i | \boldsymbol{\mu}_k, \boldsymbol{\Sigma}_k)}{\sum_{j=1}^K \pi_j \mathcal{N}(\mathbf{x}_i | \boldsymbol{\mu}_j, \boldsymbol{\Sigma}_j)}$$

Properties:
- $\sum_{k=1}^K r_{ik} = 1$ for each $i$ (probabilities sum to $1$)
- $0 \leq r_{ik} \leq 1$ (valid probabilities)
- $r_{ik}$ large $\Rightarrow$ $\mathbf{x}_i$ likely from cluster $k$

---

### M-Step: Update Parameters

Compute effective count for each cluster:
$$N_k = \sum_{i=1}^n r_{ik}$$

Then update:

**Mean:**
$$\boldsymbol{\mu}_k^{\text{new}} = \frac{1}{N_k} \sum_{i=1}^n r_{ik} \mathbf{x}_i$$

**Covariance:**
$$\boldsymbol{\Sigma}_k^{\text{new}} = \frac{1}{N_k} \sum_{i=1}^n r_{ik} (\mathbf{x}_i - \boldsymbol{\mu}_k)(\mathbf{x}_i - \boldsymbol{\mu}_k)^T$$

**Mixing weight:**
$$\pi_k^{\text{new}} = \frac{N_k}{n}$$

---

## Full Algorithm

```
Initialize: μ₁, ..., μₖ, Σ₁, ..., Σₖ, π₁, ..., πₖ
ll_prev = -∞

repeat:
    # E-STEP
    for i = 1 to n:
        for k = 1 to K:
            r_ik = (π_k × 𝒩(x_i | μ_k, Σ_k)) / Σⱼ(πⱼ × 𝒩(x_i | μⱼ, Σⱼ))
    
    # M-STEP
    for k = 1 to K:
        Nₖ = Σᵢ rᵢₖ
        μₖ = (1/Nₖ) Σᵢ (rᵢₖ × xᵢ)
        Σₖ = (1/Nₖ) Σᵢ (rᵢₖ × (xᵢ - μₖ)(xᵢ - μₖ)ᵀ)
        πₖ = Nₖ/n
    
    # CHECK CONVERGENCE
    ll_curr = Σᵢ log(Σₖ πₖ × 𝒩(xᵢ | μₖ, Σₖ))
    if |ll_curr - ll_prev| < ε:
        break
    ll_prev = ll_curr

return μ, Σ, π
```

---

## Convergence Guarantee

**Theorem:** Each EM iteration increases (or maintains) log-likelihood:

$$\log P(\mathbf{X}|\boldsymbol{\theta}^{(t+1)}) \geq \log P(\mathbf{X}|\boldsymbol{\theta}^{(t)})$$

**Proof sketch:** 
- E-step: Compute lower-bound on likelihood using Jensen's inequality
- M-step: Maximize this lower-bound
- Together: Both steps increase likelihood

**Important:** EM finds a **local maximum**, not global. Try multiple random initializations.

---

## Why Soft Assignments Matter

**Hard clustering (K-Means):**
- Point on cluster boundary → forced into one cluster
- That cluster's parameters pulled strongly by ambiguous point
- Information loss

**Soft clustering (EM):**
- Point on cluster boundary → split responsibility ($r_{ik} \approx 0.5$)
- Both nearby clusters influenced proportionally
- Preserves uncertainty information

**Example math:**

For point $\mathbf{x} = [0, 0]$ between clusters at $[1, 0]$ and $[-1, 0]$:

K-Means: Assigned to cluster $1$ only
$$\boldsymbol{\mu}_1^{\text{new}} \leftarrow \text{includes } [0, 0]$$
$$\boldsymbol{\mu}_2^{\text{new}} \leftarrow \text{doesn't include } [0, 0]$$

EM: Responsibility $r_{i1} = 0.5, r_{i2} = 0.5$
$$\boldsymbol{\mu}_1^{\text{new}} \leftarrow 0.5 \times [0, 0]$$
$$\boldsymbol{\mu}_2^{\text{new}} \leftarrow 0.5 \times [0, 0]$$

More realistic!

---

## Common Pitfalls & Solutions

### 1. Singular Covariance

**Problem:** $\det(\boldsymbol{\Sigma}_k) = 0$ (not invertible)

**Fix:**
```python
# Add regularization
Σ_k += λ * I  # λ = 1e-6 typical
```

### 2. Empty Clusters

**Problem:** $N_k \approx 0$ for some cluster

**Fix:** Re-initialize that cluster to a random data point

### 3. Poor Local Optimum

**Problem:** EM converged to suboptimal likelihood

**Fix:** Try multiple random initializations, keep best $LL$

### 4Slow Convergence

**Problem:** Takes 1000+ iterations

**Fix:** Use k-means++ initialization, loosen tolerance

---

## Key Differences: EM vs K-Means

| Aspect | K-Means | EM/GMM |
|--------|---------|--------|
| **Output** | Hard labels $z_i \in \{1,\ldots,K\}$ | Soft prob $r_{ik} \in [0,1]$ |
| **E-step** | $z_i = \arg\min_k \\|\mathbf{x}_i - \boldsymbol{\mu}_k\\|^2$ | $r_{ik} = \frac{\pi_k \mathcal{N}(\mathbf{x}_i\vert\boldsymbol{\mu}_k,\boldsymbol{\Sigma}_k)}{\sum_j \pi_j \mathcal{N}(\mathbf{x}_i\vert\boldsymbol{\mu}_j,\boldsymbol{\Sigma}_j)}$ |
| **M-step** | $\boldsymbol{\mu}_k = \frac{1}{N_k}\sum_{i:z_i=k} \mathbf{x}_i$ | $\boldsymbol{\mu}_k = \frac{1}{N_k}\sum_i r_{ik} \mathbf{x}_i$ |
| **Cluster model** | Single point $\boldsymbol{\mu}_k$ | Full distribution $\mathcal{N}(\boldsymbol{\mu}_k, \boldsymbol{\Sigma}_k)$ |
| **Speed** | Faster ($O(nKd)$ per iter) | Slower ($O(nKd^2)$ per iter) |
| **Uncertainty** | None | Full posterior $r_{ik}$ |

---

## Complexity & Computational Considerations

**Per-iteration cost:**
$$O(n \times K \times d^2)$$

Breakdown:
- E-step: Compute $K$ Gaussian likelihoods per point = $O(nKd^2)$ (due to $\boldsymbol{\Sigma}_k^{-1}$ and determinant)
- M-step: Update means ($O(nKd)$) and covariances ($O(nKd^2)$)

**Typical iterations to convergence:** $10$ – $100$

**Total runtime:** $10^{-2}$ to $1$ second for $n=10^4, K=10, d=100$

---

## Key Takeaways

1. **Hidden variables:** Cluster assignments $z$ are latent; we optimize over them implicitly

2. **Soft probs:** $r_{ik}$ encodes uncertainty about assignments; more realistic than hard labels

3. **Weighted updates:** All parameters updated using weighted contributions: $\sum_i r_{ik} \cdot (\cdot)$

4. **Monotonic improvement:** $LL$ guaranteed to increase each iteration (convergence)

5. **Local optima:** EM finds local max; use multiple random initializations

6. **Practical use:** Need probabilistic outputs, can afford $O(nKd^2)$ cost, want uncertainty quantification
