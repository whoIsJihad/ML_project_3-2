# 📘 Expectation-Maximization (EM) Algorithm

## 1. Core Idea (Intuition)

**General framework for learning with missing/latent variables.**

**Key idea:** Alternate between:
1. **E-step:** Infer hidden variables given current parameters
2. **M-step:** Optimize parameters given inferred hidden variables

**Applications:** GMM clustering, HMMs, matrix factorization, etc.

---

## 2. Mathematical Setup

### Problem
Observed data: $X = \{x_1, \ldots, x_n\}$

Latent variables: $Z = \{z_1, \ldots, z_n\}$ (unknown)

Likelihood: $p(X | \theta) = \sum_Z p(X, Z | \theta)$ (marginalize out $Z$)

**Goal:** Maximize $\log p(X | \theta)$.

---

## 3. Complete vs. Incomplete Likelihood

### Incomplete Likelihood (observed only)
$$\ell(\theta) = \log p(X | \theta) = \sum_i \log \left( \sum_{z_i} p(x_i, z_i | \theta) \right)$$

Difficult (sum inside log).

### Complete Likelihood (if $Z$ were known)
$$\ell_c(\theta) = \log p(X, Z | \theta) = \sum_i \log p(x_i, z_i | \theta)$$

Easy to optimize.

---

## 4. E-Step (Expectation)

**Idea:** Can't know $Z$, but compute expected complete likelihood given $X$ and current $\theta$.

$$Q(\theta, \theta^t) = \mathbb{E}_{Z|X, \theta^t}[\log p(X, Z | \theta)]$$

$$= \sum_i \mathbb{E}_{z_i | x_i, \theta^t}[\log p(x_i, z_i | \theta)]$$

**Computation:** Use Bayes rule to get posterior $p(z_i | x_i, \theta^t)$, then compute expectation.

---

## 5. M-Step (Maximization)

Maximize $Q$ w.r.t. $\theta$:
$$\theta^{t+1} = \arg\max_\theta Q(\theta, \theta^t)$$

**Interpretation:** Treating expected latent data as if it were observed.

---

## 6. EM Algorithm (General)

```
Initialize θ^0

For t = 0, 1, 2, ...:
  
  === E-Step ===
  Compute Q(θ, θ^t) = E_{Z|X,θ^t}[log p(X,Z|θ)]
  
  === M-Step ===
  θ^{t+1} = argmax_θ Q(θ, θ^t)
  
  If converged, return θ^t
```

---

## 7. Key Properties

### Monotonic Improvement
$$p(X | \theta^{t+1}) \geq p(X | \theta^t)$$

**Proof sketch:** $Q(\theta, \theta^t)$ lower-bounds $\log p(X|\theta)$. Maximizing $Q$ increases lower bound, which increases $\log p(X|\theta)$.

### Convergence
Guaranteed convergence to **local optimum** (not global).

### Efficiency
- **E-step:** Often closed-form (e.g., Bayes rule for GMM)
- **M-step:** Often simpler than direct maximization (e.g., weighted least squares)

---

## 8. Relationship to Variational Inference

**EM is special case of variational inference** (choosing specific variational family).

**Key idea:** Both alternate between:
- Inferring latent structure (E-step / inference)
- Optimizing parameters (M-step)

---

## 9. Common Applications

| Application | Latent Variables | E-step |
|-------------|------------------|--------|
| **GMM clustering** | Cluster assignments | Compute responsibilities |
| **HMM** | Hidden states sequence | Forward-backward algorithm |
| **Matrix factorization** | Low-rank factors | Gradient descent on factors |
| **Topic modeling (LDA)** | Topic assignments | Infer topic distribution |

---

## 10. Failure Cases

| Problem | Why |
|---------|-----|
| **Local optima** | Non-convex; may converge to local optimum |
| **Slow convergence** | May take many iterations |
| **Model selection** | How many latent variables? |

---

## 11. Exam Questions

### Conceptual
1. Explain the difference between complete and incomplete likelihood.
2. Why is E-step called "expectation"?
3. Why does EM monotonically increase log-likelihood?

### Practical
1. Apply EM to GMM: write E-step and M-step explicitly.
2. Compare EM to K-means. When use each?

---

## 12. Key Takeaways

- **EM:** General algorithm for learning with latent variables
- **E-step:** Compute expected complete likelihood $Q(\theta, \theta^t)$
- **M-step:** Maximize $Q$ w.r.t. $\theta$
- **Monotonic improvement:** Log-likelihood guaranteed to increase
- **Convergence:** Local optimum (not global)
- **Applications:** GMM, HMM, LDA, topic modeling, matrix factorization
- **Efficiency:** E and M steps often simpler than direct likelihood optimization

---
