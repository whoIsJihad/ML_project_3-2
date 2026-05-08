> [[MOC (NN)]] | Prev: [[Optimization and Empirical Risk Minimization]] | Next: [[Advanced Optimization Algorithms]]

# Stochastic Gradient Descent Variants

In practice, computing the true gradient over the entire dataset (Batch Gradient Descent) is computationally prohibitive.

## 1. Stochastic Gradient Descent (SGD)

Computes the gradient using a single randomly chosen training example.

- **Pros**: Fast, can escape local minima due to high variance in updates.
- **Cons**: Extremely noisy, convergence is difficult.

## 2. Mini-batch SGD

Computes the gradient over a small subset (mini-batch) of size $k$:

$$\nabla_\theta J \approx \frac{1}{k} \nabla_\theta \sum_{i \in \text{Batch}} L(\hat{y}^{(i)}, y^{(i)})$$

### Unbiasedness and Variance

The mini-batch gradient is an **unbiased estimate** of the true gradient:

$$\mathbb{E}[\text{g}_{mini-batch}] = \nabla_\theta J_{true}$$

However, the variance of the estimate is inversely proportional to the batch size $m$:

$$\text{Var}(\text{g}_{mini-batch}) \propto \frac{1}{m}$$

Small $m$ introduces noise which can act as a regularizer, while larger $m$ provides more stable updates and benefits from hardware parallelism (vectorization).

Refinements like momentum and adaptive rates are discussed in [[Advanced Optimization Algorithms]].
