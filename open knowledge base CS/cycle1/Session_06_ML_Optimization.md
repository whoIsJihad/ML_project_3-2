# Session 6 – Convex Optimization & Gradient Methods

## Linked Domain
[[ML & Optimization]]

---

## Phase 1 – Clean Theory

### 1. Convexity Definitions

**Convex Set**: $C \subseteq \mathbb{R}^n$ is convex if:
$$\forall x, y \in C, \forall \lambda \in [0,1]: \lambda x + (1-\lambda)y \in C$$

**Convex Function**: $f: \mathbb{R}^n \to \mathbb{R}$ is convex if:
$$f(\lambda x + (1-\lambda)y) \leq \lambda f(x) + (1-\lambda)f(y)$$

**Equivalent Characterizations**:

| Condition | Requirement |
|-----------|-------------|
| First-order | $f(y) \geq f(x) + \nabla f(x)^\top (y - x)$ |
| Second-order | $\nabla^2 f(x) \succeq 0$ (Hessian PSD) |

**Strongly Convex**: $f$ is $\mu$-strongly convex if $f(x) - \frac{\mu}{2}\|x\|^2$ is convex.
- Equivalent: $\nabla^2 f(x) \succeq \mu I$

**$L$-Smooth**: $\|\nabla f(x) - \nabla f(y)\| \leq L \|x - y\|$
- Equivalent: $\nabla^2 f(x) \preceq LI$

---

### 2. Gradient Descent Convergence

| Function Class | Step Size | Convergence Rate | Iterations to $\epsilon$ |
|----------------|-----------|------------------|-------------------------|
| Convex + $L$-smooth | $\alpha = 1/L$ | $O(1/t)$ | $O(1/\epsilon)$ |
| $\mu$-strongly convex + $L$-smooth | $\alpha = 1/L$ | Linear: $O(\rho^t)$ | $O(\kappa \log(1/\epsilon))$ |

**Condition Number**: $\kappa = L/\mu$

**Convergence bound** (strongly convex):
$$f(x_t) - f(x^*) \leq \left(1 - \frac{1}{\kappa}\right)^t \cdot (f(x_0) - f(x^*))$$

---

### 3. Accelerated Methods

| Method | Update Rule | Convergence |
|--------|-------------|-------------|
| **Vanilla GD** | $x_{t+1} = x_t - \alpha \nabla f(x_t)$ | $O(\kappa \log(1/\epsilon))$ |
| **Heavy Ball** | $v_{t+1} = \beta v_t + \nabla f(x_t)$, $x_{t+1} = x_t - \alpha v_{t+1}$ | $O(\sqrt{\kappa} \log(1/\epsilon))$ |
| **Nesterov** | Lookahead gradient | Optimal: $O(\sqrt{\kappa} \log(1/\epsilon))$ |

**Optimal momentum**: $\beta = \frac{\sqrt{\kappa} - 1}{\sqrt{\kappa} + 1}$

---

### 4. Second-Order Methods

| Method | Per-Iteration Cost | Iterations | Use Case |
|--------|-------------------|------------|----------|
| Gradient Descent | $O(n)$ | $O(\kappa \log(1/\epsilon))$ | Large-scale, simple |
| Newton's Method | $O(n^3)$ | $O(\log \log(1/\epsilon))$ | Small $n$, ill-conditioned |
| Quasi-Newton (BFGS) | $O(n^2)$ | $O(\log(1/\epsilon))$ | Medium-scale |

---

### 5. Stochastic Gradient Descent

**SGD**: Use noisy gradient $\nabla f_i$ instead of full gradient $\nabla f = \frac{1}{n}\sum_i \nabla f_i$

| Property | GD | SGD |
|----------|-----|-----|
| Per-iteration cost | $O(n)$ | $O(1)$ |
| Convergence (strongly convex) | $O(\kappa \log(1/\epsilon))$ | $O(1/(\mu \epsilon))$ |
| Variance | None | High (oscillates near optimum) |

**Variance Reduction** (SVRG, SAGA): Compute full gradient periodically, use for variance correction.

---

### 6. Edge Cases

1. **Non-Lipschitz Gradient**: E.g., $f(x) = x^4$. Fixed step size fails. Need line search or adaptive methods.

2. **Saddle Points**: Non-convex functions have saddle points where $\nabla f = 0$. GD stalls. Requires perturbations or second-order information.

3. **High Condition Number**: $\kappa = 10^6$ requires $10^6$ iterations. Preconditioning essential.

4. **SGD Variance**: Constant step size SGD oscillates near optimum. Need decreasing step size $\alpha_t = O(1/t)$ or variance reduction.

5. **Discrete Constraints**: GD produces continuous solutions. Integer programming requires projected GD or rounding.

---

### Common Mistakes

1. **Step size $\alpha = 1$**: Ignores Lipschitz constant. Diverges if $L > 1$.

2. **Assuming global convergence for non-convex**: GD only finds local minima for non-convex functions.

3. **Strong vs. strict convexity confusion**: Strong convexity implies strict, but not converse. Strong convexity has bounded curvature.

4. **Ignoring condition number**: Saying "$O(1/\epsilon)$ iterations" without $\kappa$ dependence. True count: $O(\kappa \log(1/\epsilon))$.

5. **Excessive momentum**: $\beta \to 1$ causes oscillation. Use optimal $\beta = (\sqrt{\kappa} - 1)/(\sqrt{\kappa} + 1)$.

---

### Code Snippet – Condition Number Impact on Convergence

```python
import numpy as np
import matplotlib.pyplot as plt

def quadratic_loss(x, A, b):
    """f(x) = 1/2 x^T A x - b^T x"""
    return 0.5 * x.T @ A @ x - b.T @ x

def gradient(x, A, b):
    """∇f(x) = Ax - b"""
    return A @ x - b

def condition_number(A):
    """κ = λ_max / λ_min"""
    eigvals = np.linalg.eigvalsh(A)
    return eigvals[-1] / eigvals[0]

def gradient_descent(A, b, x0, alpha, num_iters):
    """Run GD and track convergence."""
    x = x0.copy()
    x_opt = np.linalg.solve(A, b)
    f_opt = quadratic_loss(x_opt, A, b)
    errors = []

    for _ in range(num_iters):
        f_t = quadratic_loss(x, A, b)
        errors.append(f_t - f_opt)
        x = x - alpha * gradient(x, A, b)

    return errors

def compare_condition_numbers():
    n = 10
    np.random.seed(42)

    # Well-conditioned: κ ≈ 1
    A1 = np.eye(n)
    b1 = np.random.randn(n)

    # Ill-conditioned: κ ≈ 100
    eigvals = np.linspace(1, 100, n)
    Q = np.linalg.qr(np.random.randn(n, n))[0]
    A2 = Q @ np.diag(eigvals) @ Q.T
    b2 = np.random.randn(n)

    x0 = np.zeros(n)

    errors1 = gradient_descent(A1, b1, x0, 1.0, 100)
    errors2 = gradient_descent(A2, b2, x0, 0.01, 1000)

    plt.figure(figsize=(10, 5))
    plt.semilogy(errors1, label=f'κ = {condition_number(A1):.1f}')
    plt.semilogy(errors2, label=f'κ = {condition_number(A2):.1f}')
    plt.xlabel('Iteration')
    plt.ylabel('f(x) - f(x*)')
    plt.legend()
    plt.title('GD Convergence: Well-conditioned vs Ill-conditioned')
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    compare_condition_numbers()
```

---

## Phase 2 – Conceptual Stress Questions

**Q1**: Prove that if $f$ is $\mu$-strongly convex and $L$-smooth, then GD with $\alpha = 1/L$ achieves linear convergence with rate $\rho = 1 - \mu/L$. Start from:
$$f(x_{t+1}) \leq f(x_t) - \frac{1}{2L}\|\nabla f(x_t)\|^2$$
and use strong convexity: $\|\nabla f(x_t)\|^2 \geq 2\mu(f(x_t) - f(x^*))$.

**Q2**: SGD with mini-batch size $b$ on dataset of size $n$. Iteration cost: $O(b)$. Full GD: $O(n)$. SGD converges in $T_{\text{SGD}} = O(1/(\mu \epsilon))$ iterations, GD in $T_{\text{GD}} = O(\kappa \log(1/\epsilon))$. For what values of $n, \kappa, b$ is SGD faster in total time?

**Q3**: Training neural network (non-convex). GD converges but momentum diverges. How is this possible? Construct concrete example where vanilla GD converges but momentum with $\beta = 0.9, \alpha = 0.01$ diverges. (Hint: high curvature regions.)

---

## Phase 3 – Applied Problem

**Problem Statement**:

Train **logistic regression**:
$$\min_w \frac{1}{n}\sum_{i=1}^n \log(1 + e^{-y_i w^\top x_i}) + \frac{\lambda}{2}\|w\|^2$$

where $(x_i, y_i) \in \mathbb{R}^d \times \{-1, +1\}$ and $\lambda > 0$.

**Part A**: Prove objective is $(\lambda + L)$-smooth where $L = \frac{1}{4n}\sum_i \|x_i\|^2$. Use fact that $\sigma(z) = 1/(1+e^{-z})$ has $|\sigma''(z)| \leq 1/4$.

**Part B**: $n = 10^9$ data points, $d = 10^6$ dimensions. Full GD too expensive ($O(nd)$ per iteration). SGD with mini-batch $b = 100$. Compute:
- Iteration cost ratio: SGD vs GD
- Convergence iteration ratio: SGD vs GD (assume $\kappa = 100$)
- Total time ratio: When is SGD faster?

**Part C**: **Variance-reduced SGD (SVRG)**: Compute full gradient every $m$ iterations (snapshot), then use stochastic gradients with variance correction. Analyze trade-off:
- $m = n$: cost same as GD
- $m = 1$: variance reduction weak

Derive optimal $m$ as function of $n$ and $\kappa$ to minimize total time.

---

## Phase 4 – Feedback & Weakness Log Update

**Awaiting your responses to Phase 2 and Phase 3.**

Critique will focus on:
- Proof rigor and inequalities
- Quantitative analysis (not just big-O)
- Condition number impact understanding
- Time-accuracy trade-off analysis
- Convex optimization application to ML

---

## Cross-Links for Reinforcement
- [[Convex Analysis Fundamentals]]
- [[Newton's Method & Quasi-Newton]]
- [[Stochastic Optimization]]
- [[Variance Reduction (SVRG, SAGA)]]
- [[Adaptive Methods (Adam, RMSprop)]]
- [[Non-Convex Optimization Landscape]]

---

**Status**: Awaiting Phase 2 & 3 responses.
