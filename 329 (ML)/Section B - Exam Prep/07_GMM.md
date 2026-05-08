# 📘 Gaussian Mixture Models (GMM)

## 1. Core Idea (Intuition)

**Problem:** Data comes from multiple groups, but group labels unknown. How to cluster?

**GMM solution:** Data generated from mixture of Gaussians. Each cluster is one Gaussian.

**Key insight:** Soft clustering — each point has probability of belonging to each cluster.

---

## 2. Mathematical Formulation

### Model
$$p(x) = \sum_{k=1}^{K} \pi_k \mathcal{N}(x | \mu_k, \Sigma_k)$$

where:
- $K$: number of clusters (Gaussians)
- $\pi_k$: mixing coefficient (weight), $\sum_k \pi_k = 1$
- $\mathcal{N}(x | \mu_k, \Sigma_k)$: $k$-th Gaussian with mean $\mu_k$, covariance $\Sigma_k$

### Responsibility (Soft Assignment)
Probability that point $x_i$ belongs to cluster $k$:
$$r_{ik} = \frac{\pi_k \mathcal{N}(x_i | \mu_k, \Sigma_k)}{\sum_j \pi_j \mathcal{N}(x_i | \mu_j, \Sigma_j)}$$

**Interpretation:** If cluster $k$ likely generated $x_i$, then $r_{ik} \approx 1$; else $\approx 0$.

---

## 3. EM Algorithm (Expectation-Maximization)

### E-Step (Expectation)
Compute responsibilities $r_{ik}$ using current parameters:
$$r_{ik} = \frac{\pi_k \mathcal{N}(x_i | \mu_k, \Sigma_k)}{\sum_j \pi_j \mathcal{N}(x_i | \mu_j, \Sigma_j)}$$

### M-Step (Maximization)
Update parameters using responsibilities:
$$N_k = \sum_i r_{ik} \quad \text{(effective count for cluster } k \text{)}$$

$$\mu_k = \frac{1}{N_k} \sum_i r_{ik} x_i$$

$$\Sigma_k = \frac{1}{N_k} \sum_i r_{ik} (x_i - \mu_k)(x_i - \mu_k)^T$$

$$\pi_k = \frac{N_k}{n}$$

### Iteration
Repeat E-step and M-step until convergence.

---

## 4. Log-Likelihood (Objective)

$$\mathcal{L} = \sum_i \log p(x_i) = \sum_i \log \left( \sum_k \pi_k \mathcal{N}(x_i | \mu_k, \Sigma_k) \right)$$

**EM increases log-likelihood monotonically** (guaranteed to improve, though may converge to local optimum).

---

## 5. Hard vs. Soft Clustering

| Aspect | K-means | GMM |
|--------|---------|-----|
| **Assignment** | Hard (cluster $k$ or none) | Soft (probability) |
| **Clusters** | Spherical | Ellipsoidal (full covariance) |
| **Uncertainty** | None | Probabilistic |
| **Interpretability** | Simple | Probabilistic interpretation |

---

## 6. Number of Clusters Selection

| Method | How |
|--------|-----|
| **Elbow method** | Plot log-likelihood vs. $K$; pick "elbow" point |
| **BIC / AIC** | Information criteria balancing fit and complexity |
| **Silhouette score** | Measure cluster separation (average distance within vs. between) |

---

## 7. Applications

- **Image segmentation:** Each pixel soft-assigned to color cluster
- **Document clustering:** Articles soft-assigned to topics
- **Anomaly detection:** Assign to mixture; low probability = anomaly
- **Model selection:** Which model fits data?

---

## 8. Failure Cases / Limitations

| Problem | Why |
|---------|-----|
| **Local optima** | EM converges to local optimum (not global) |
| **Covariance singularity** | If cluster has zero variance, matrix singular |
| **Slow convergence** | May take many iterations |

---

## 9. Exam Questions

### Conceptual
1. What does "responsibility" $r_{ik}$ mean? How is it computed?
2. Explain E-step and M-step in GMM training.
3. When would you use GMM over K-means?

### Practical
1. How to choose number of clusters $K$ in GMM?
2. Dataset: mix of two Gaussians with different variances. K-means vs. GMM?

---

## 10. Key Takeaways

- **GMM:** Mixture of $K$ Gaussians; soft clustering
- **Responsibility:** $r_{ik} = P(\text{cluster } k | x_i)$; computed via Bayes rule
- **EM algorithm:** E-step (compute responsibilities), M-step (update parameters)
- **Log-likelihood:** Monotonically increasing; convergence guaranteed (to local optimum)
- **Soft clustering:** Each point assigned probability to each cluster
- **Covariance:** Full $\Sigma_k$ (vs. K-means' spherical clusters)
- **Modern alternative:** Variational Autoencoders (VAE) for more complex distributions

---
