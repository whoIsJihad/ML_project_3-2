# 📘 PCA (Principal Component Analysis)

## 1. Core Idea (Intuition)

**Goal:** Reduce dimensionality while preserving maximum variance.

**Intuition:** High-variance directions contain signal; low-variance directions are noise.

**PCA finds:** Directions (principal components) that maximize variance.

---

## 2. Mathematical Formulation

### Input
Data matrix $X \in \mathbb{R}^{n \times d}$ (n samples, d features).

Assume centered: $\mathbb{E}[X] = 0$ (subtract mean).

### Covariance Matrix
$$\Sigma = \frac{1}{n} X^T X$$

Diagonal elements: variance of each feature.

Off-diagonal: covariance between features.

### Principal Components
Eigenvectors of $\Sigma$ are principal components (directions).

Eigenvalues are variance along each direction.

$$\Sigma v_k = \lambda_k v_k$$

where $\lambda_1 \geq \lambda_2 \geq \cdots \geq \lambda_d$ (sorted).

---

## 3. Projection

### First Principal Component
Direction of maximum variance:
$$v_1 = \arg\max_v \text{Var}(Xv) = \arg\max_v v^T \Sigma v$$

**Projection:** 
$$z_i = X_i v_1 \quad \text{(1D representation of each sample)}$$

### First $k$ Components
$$Z = XV_k \quad \text{where } V_k = [v_1, v_2, \ldots, v_k]$$

Result: $n \times k$ matrix (dimensionality reduced from $d$ to $k$).

---

## 4. Explained Variance

### Variance Explained by Component $k$
$$\text{Var}_k = \lambda_k \quad \text{(eigenvalue)}$$

### Cumulative Explained Variance
$$\text{Cumulative}_k = \frac{\sum_{i=1}^{k} \lambda_i}{\sum_{i=1}^{d} \lambda_i}$$

**Interpretation:** Fraction of total variance captured by first $k$ components.

**Rule of thumb:** Choose $k$ so cumulative variance $\approx 95\%$ or $99\%$.

---

## 5. Algorithm

```
Input: X (n × d matrix)

1. Center data: X ← X - mean(X)

2. Compute covariance: Σ = (1/n) X^T X

3. Eigendecomposition: Σ = U Λ U^T
   (U columns are eigenvectors; Λ diagonal is eigenvalues)

4. Sort by eigenvalues: λ_1 ≥ λ_2 ≥ ... ≥ λ_d

5. Select top k components: V_k = [u_1, ..., u_k]

6. Project: Z = X V_k (n × k)

Output: Z (low-dimensional representation)
```

---

## 6. Reconstruction Error

If reconstruct from $k$ components:
$$\hat{X} = Z V_k^T = X V_k V_k^T$$

**Reconstruction error:**
$$\text{Error} = \| X - \hat{X} \|^2 = \sum_{j=k+1}^{d} \lambda_j$$

**Interpretation:** Variance lost by discarding last $d-k$ components.

---

## 7. Computational Considerations

### Full PCA
Eigendecomposition of $d \times d$ covariance matrix: $O(d^3)$.

**Problem:** If $d$ large (thousands of features), slow.

### SVD (Singular Value Decomposition)
Alternative: Decompose data directly:
$$X = U \Sigma V^T$$

Columns of $U$ scaled by $\Sigma$ give principal components.

**Advantage:** Can compute top-$k$ components without full decomposition.

---

## 8. When It Works Well

- **High-dimensional data:** $d \gg k$ (e.g., 1000 features → 10 components)
- **Linear relationships:** PCA finds linear subspace
- **Variance indicates signal:** True when noise is uniform
- **Real-world:** Image compression, feature extraction, visualization (2D/3D)

---

## 9. Failure Cases / Limitations

| Problem | Why |
|---------|-----|
| **Non-linear data** | PCA linear; misses curved structure |
| **Small variance = noise assumption** | Sometimes low-variance contains signal |
| **Sensitive to scale** | Features with large variance dominate |

---

## 10. Variants

| Variant | Purpose |
|---------|---------|
| **Kernel PCA** | Non-linear PCA using kernel trick |
| **Sparse PCA** | Components are sparse (few non-zero elements); interpretable |
| **Incremental PCA** | Process data in batches (streaming) |
| **Probabilistic PCA** | Probabilistic interpretation (latent variable model) |

---

## 11. PCA vs. Other Dimensionality Reduction

| Method | Linear/Nonlinear | Unsupervised | Interpretable |
|--------|-----------------|-------------|--------------|
| **PCA** | Linear | Yes | Yes (eigenvectors) |
| **Kernel PCA** | Nonlinear | Yes | No |
| **t-SNE** | Nonlinear | Yes | No (visualization only) |
| **Autoencoders** | Nonlinear | Yes | No (black-box) |
| **LDA** | Linear | No (supervised) | Yes |

---

## 12. Exam Questions

### Conceptual
1. What is a principal component? How is it related to eigenvectors?
2. Explain explained variance. How to choose number of components?
3. Why is PCA sensitive to scale?

### Practical
1. 100 features, explained variance curve: 70% with 10 PC, 90% with 20 PC. Choose $k$?
2. Reconstruct from $k$ components. How does reconstruction error depend on $k$?

### Trick Cases
1. All features have same variance. What happens to PCA?
2. Data highly non-linear (e.g., Swiss roll). PCA fails. Why?

---

## 13. Key Takeaways

- **PCA:** Find directions of maximum variance via eigendecomposition
- **Principal components:** Eigenvectors of covariance matrix $\Sigma$
- **Variance explained:** Eigenvalues; sum to total variance
- **Projection:** $Z = XV_k$ (project to top-$k$ components)
- **Reconstruction:** $\hat{X} = ZV_k^T$; error = discarded variance
- **Scale matters:** Standardize features before PCA
- **Linear only:** Non-linear alternatives needed for curved data
- **Complexity:** Eigen-decomposition $O(d^3)$; SVD more efficient

---
