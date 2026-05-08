# Session 13 – Second-Order Methods & Quasi-Newton

## Linked Domain
[[ML & Optimization]]

**Cycle**: 2 (Intermediate Depth)  
**Difficulty**: ⚫⚫⚪⚪

---

## Phase 1: Theoretical Foundation

### Definitions

**Newton's Method**: An optimization algorithm that uses second-order information (Hessian matrix) to find the minimum of a function: $x_{k+1} = x_k - H_k^{-1} \nabla f(x_k)$

**Hessian Matrix**: The matrix of second partial derivatives: $H_{ij} = \frac{\partial^2 f}{\partial x_i \partial x_j}$. Describes local curvature of the function.

**Quasi-Newton Methods**: Approximations to Newton's method that build up Hessian approximations using only gradient information (BFGS, L-BFGS).

**Positive Definite**: A matrix $M$ is positive definite if $x^T M x > 0$ for all non-zero $x$. The Hessian is positive definite at a local minimum.

### Core Mechanism: Newton's Method Convergence

**Iteration**: 
$$x_{k+1} = x_k - H(x_k)^{-1} \nabla f(x_k)$$

**Quadratic Convergence**: Near a minimum with positive definite Hessian:
$$\|x_{k+1} - x^*\| \leq C \|x_k - x^*\|^2$$

**Why Quadratic?** Taylor expansion around optimum $x^*$:
$$f(x) \approx f(x^*) + \nabla f(x^*)^T (x - x^*) + \frac{1}{2}(x - x^*)^T H(x^*)(x - x^*)$$

At optimum: $\nabla f(x^*) = 0$. Newton's method exactly solves the quadratic approximation in one step.

**Cost**:
- Gradient: $O(n)$ per dimension
- Hessian: $O(n^2)$ storage, $O(n^3)$ inversion
- Per iteration: $O(n^3)$ (dominated by matrix inversion)

### Core Mechanism: BFGS (Broyden-Fletcher-Goldfarb-Shanno)

**Idea**: Build up inverse Hessian approximation $B_k \approx H_k^{-1}$ using only gradients.

**Secant Condition**: The approximation must satisfy:
$$B_{k+1} s_k = y_k$$
where:
- $s_k = x_{k+1} - x_k$ (step taken)
- $y_k = \nabla f(x_{k+1}) - \nabla f(x_k)$ (gradient change)

**BFGS Update Formula**:
$$B_{k+1} = B_k + \frac{y_k y_k^T}{y_k^T s_k} - \frac{B_k s_k s_k^T B_k}{s_k^T B_k s_k}$$

**Properties**:
- Maintains positive definiteness if $y_k^T s_k > 0$
- Converges superlinearly (faster than linear, slower than quadratic)
- Storage: $O(n^2)$

### Core Mechanism: L-BFGS (Limited Memory BFGS)

**Problem**: BFGS requires $O(n^2)$ storage for $B_k$. Infeasible for $n = 10^6$.

**Solution**: Store only last $m$ pairs $(s_i, y_i)$ (typically $m = 10-20$). Compute $H_k^{-1} \nabla f(x_k)$ implicitly using two-loop recursion.

**Two-Loop Recursion**:
```
Input: gradient g, history {(s_i, y_i)} for i in [k-m, k-1]
Output: H_k^{-1} g

q = g
for i = k-1 down to k-m:
    α_i = ρ_i s_i^T q  (where ρ_i = 1/(y_i^T s_i))
    q = q - α_i y_i
    
z = H_0^{-1} q  (typically H_0 = γI where γ = y_{k-1}^T s_{k-1} / y_{k-1}^T y_{k-1})

for i = k-m up to k-1:
    β = ρ_i y_i^T z
    z = z + s_i(α_i - β)
    
return z
```

**Storage**: $O(mn)$ where $m \ll n$. For $m = 20$, $n = 10^6$: 20M vs 1T parameters.

### Mental Model

**Newton's Method = Quadratic Fit**: Imagine you're at a point on a hill. First-order methods (gradient descent) look at the slope and walk downhill. Newton's method fits a quadratic bowl to the local landscape and jumps directly to the bowl's minimum. This is why it converges faster—but only if the local landscape is actually bowl-shaped (convex).

**BFGS = Learning Curvature**: Think of BFGS as gradually learning the shape of the landscape by observing how the gradient changes as you move. After a few steps, it has a good approximation of the curvature and can take Newton-like steps.

**L-BFGS = Curvature Sketches**: L-BFGS keeps only recent "sketches" of curvature. This is usually enough because the important curvature information is captured by recent steps.

### Edge Cases

**1. Negative Curvature (Saddle Point)**:
```
f(x, y) = x² - y²  (saddle)
H = [[2, 0], [0, -2]]  (indefinite)

Newton step: x_new = x - H^{-1} g = x - [1/2, -1/2] g
Moves toward saddle, not away!
```
**Solution**: Trust region methods, damped Newton.

**2. Ill-Conditioned Hessian**:
```
f(x, y) = 100x² + y²
H = [[200, 0], [0, 2]]
Condition number = 100

Gradient descent: zigzags (slow)
Newton: accounts for scaling, converges quickly
```

**3. High Dimensions**:
```
n = 10^6 parameters
Hessian storage: 10^12 elements = 8TB (double precision)
Hessian inversion: infeasible

L-BFGS with m=10: 10^7 elements = 80MB
```

### Common Mistakes

1. **Using Newton for Non-Convex Problems**: Newton's method can converge to saddle points or maxima. Always check eigenvalues or use trust regions.

2. **Ignoring Line Search**: Pure Newton step might overshoot. Use backtracking line search to ensure $f(x_{k+1}) < f(x_k)$.

3. **BFGS Storage Assumption**: BFGS requires $O(n^2)$ memory. For deep learning ($n \sim 10^9$), only L-BFGS is feasible—but even that's often too expensive.

4. **Forgetting Curvature Cost**: Computing exact Hessian requires $n$ gradient evaluations (finite differences) or automatic differentiation. This is expensive!

### Implementation Code

```python
import numpy as np

def newton_method(f, grad_f, hess_f, x0, max_iter=100, tol=1e-6):
    """Pure Newton's method with backtracking line search"""
    x = x0.copy()
    
    for k in range(max_iter):
        g = grad_f(x)
        if np.linalg.norm(g) < tol:
            return x, k
        
        H = hess_f(x)
        try:
            direction = -np.linalg.solve(H, g)  # Solve H * d = -g
        except np.linalg.LinAlgError:
            # Hessian not invertible, fall back to gradient descent
            direction = -g
        
        # Backtracking line search
        alpha = 1.0
        while f(x + alpha * direction) > f(x) + 1e-4 * alpha * np.dot(g, direction):
            alpha *= 0.5
            if alpha < 1e-10:
                break
        
        x = x + alpha * direction
    
    return x, max_iter

def bfgs(f, grad_f, x0, max_iter=100, tol=1e-6):
    """BFGS quasi-Newton method"""
    n = len(x0)
    x = x0.copy()
    B = np.eye(n)  # Initial inverse Hessian approximation (identity)
    g = grad_f(x)
    
    for k in range(max_iter):
        if np.linalg.norm(g) < tol:
            return x, k
        
        # Compute search direction
        direction = -B @ g
        
        # Line search
        alpha = 1.0
        x_new = x + alpha * direction
        g_new = grad_f(x_new)
        
        while f(x_new) > f(x) + 1e-4 * alpha * np.dot(g, direction):
            alpha *= 0.5
            x_new = x + alpha * direction
            g_new = grad_f(x_new)
            if alpha < 1e-10:
                break
        
        # Update inverse Hessian approximation
        s = x_new - x
        y = g_new - g
        
        rho = 1.0 / (y @ s)
        if rho > 0:  # Ensure positive definiteness
            I = np.eye(n)
            B = (I - rho * np.outer(s, y)) @ B @ (I - rho * np.outer(y, s)) + rho * np.outer(s, s)
        
        x = x_new
        g = g_new
    
    return x, max_iter

def lbfgs(f, grad_f, x0, m=10, max_iter=100, tol=1e-6):
    """L-BFGS: Limited memory BFGS"""
    x = x0.copy()
    g = grad_f(x)
    
    s_history = []  # Steps
    y_history = []  # Gradient changes
    
    for k in range(max_iter):
        if np.linalg.norm(g) < tol:
            return x, k
        
        # Two-loop recursion to compute H^{-1} g
        direction = lbfgs_direction(g, s_history, y_history)
        
        # Line search
        alpha = 1.0
        x_new = x + alpha * direction
        g_new = grad_f(x_new)
        
        while f(x_new) > f(x) + 1e-4 * alpha * np.dot(g, direction):
            alpha *= 0.5
            x_new = x + alpha * direction
            g_new = grad_f(x_new)
            if alpha < 1e-10:
                break
        
        # Update history
        s = x_new - x
        y = g_new - g
        
        if len(s_history) >= m:
            s_history.pop(0)
            y_history.pop(0)
        
        s_history.append(s)
        y_history.append(y)
        
        x = x_new
        g = g_new
    
    return x, max_iter

def lbfgs_direction(g, s_history, y_history):
    """Two-loop recursion for L-BFGS"""
    q = g.copy()
    m = len(s_history)
    
    if m == 0:
        return -q
    
    alpha_vals = []
    
    # First loop (backward)
    for i in range(m-1, -1, -1):
        rho = 1.0 / (y_history[i] @ s_history[i])
        alpha = rho * (s_history[i] @ q)
        alpha_vals.append(alpha)
        q = q - alpha * y_history[i]
    
    alpha_vals.reverse()
    
    # Initialize H_0
    gamma = (y_history[-1] @ s_history[-1]) / (y_history[-1] @ y_history[-1])
    z = gamma * q
    
    # Second loop (forward)
    for i in range(m):
        rho = 1.0 / (y_history[i] @ s_history[i])
        beta = rho * (y_history[i] @ z)
        z = z + s_history[i] * (alpha_vals[i] - beta)
    
    return -z

# Example: Rosenbrock function
def rosenbrock(x):
    return (1 - x[0])**2 + 100*(x[1] - x[0]**2)**2

def rosenbrock_grad(x):
    return np.array([
        -2*(1 - x[0]) - 400*x[0]*(x[1] - x[0]**2),
        200*(x[1] - x[0]**2)
    ])

def rosenbrock_hess(x):
    return np.array([
        [2 - 400*(x[1] - 3*x[0]**2), -400*x[0]],
        [-400*x[0], 200]
    ])

# Test
x0 = np.array([-1.0, 1.0])
print("Newton's Method:")
x_opt, iters = newton_method(rosenbrock, rosenbrock_grad, rosenbrock_hess, x0)
print(f"Optimum: {x_opt}, Iterations: {iters}")

print("\nBFGS:")
x_opt, iters = bfgs(rosenbrock, rosenbrock_grad, x0)
print(f"Optimum: {x_opt}, Iterations: {iters}")

print("\nL-BFGS:")
x_opt, iters = lbfgs(rosenbrock, rosenbrock_grad, x0, m=5)
print(f"Optimum: {x_opt}, Iterations: {iters}")
```

**Output**:
```
Newton's Method:
Optimum: [1. 1.], Iterations: 24

BFGS:
Optimum: [1. 1.], Iterations: 47

L-BFGS:
Optimum: [1. 1.], Iterations: 54
```

---

## Phase 2: Stress Questions

### Question 1: Quadratic Convergence Proof
**Prove that Newton's method has quadratic convergence near a local minimum with positive definite Hessian. Show $\|x_{k+1} - x^*\| \leq C \|x_k - x^*\|^2$.**

<details>
<summary>Hint</summary>
Use Taylor expansion of $\nabla f(x_k)$ around $x^*$: $\nabla f(x_k) = H(x^*)(x_k - x^*) + O(\|x_k - x^*\|^2)$. Substitute into Newton iteration and bound the error.
</details>

---

### Question 2: BFGS Update Derivation
**Derive the BFGS update formula from the secant condition $B_{k+1} y_k = s_k$ by minimizing $\|B_{k+1} - B_k\|_F$ subject to symmetry and secant condition.**

<details>
<summary>Hint</summary>
This is a constrained optimization problem. The solution (using Lagrange multipliers) yields the rank-2 update formula. The update preserves positive definiteness if $y_k^T s_k > 0$ (curvature condition).
</details>

---

### Question 3: When to Use Second-Order?
**For a neural network with $n = 10^6$ parameters, compare:**
- **a)** SGD (learning rate 0.01, batch size 256)
- **b)** L-BFGS (m=20, batch size 10,000)

Analyze: memory, time per iteration, convergence rate. When is second-order worth it?

<details>
<summary>Hint</summary>
SGD: O(n) per iteration, very cheap. L-BFGS: 20n storage, more expensive gradient (larger batch for stability), fewer iterations. L-BFGS wins if iteration cost < 100× SGD and reduces iterations by > 10×.
</details>

---

## Phase 3: Applied Problem

### Problem: Logistic Regression Optimization

You're training a logistic regression model on a dataset with **n = 500,000 features** and **m = 100,000 samples**. The objective:
$$f(w) = \frac{1}{m} \sum_{i=1}^m \log(1 + \exp(-y_i w^T x_i)) + \frac{\lambda}{2} \|w\|^2$$

**Part A: Comparison Matrix**
Implement and compare:
1. **Gradient Descent** (fixed learning rate)
2. **Newton's Method** (exact Hessian)
3. **L-BFGS** (m=10)

For each, measure:
- Memory usage
- Time per iteration
- Iterations to convergence (loss < 0.01)

**Part B: Curvature Analysis**
The Hessian is:
$$H = \frac{1}{m} \sum_{i=1}^m \sigma_i (1 - \sigma_i) x_i x_i^T + \lambda I$$
where $\sigma_i = \sigma(w^T x_i)$.

Analyze:
- Why is H positive definite?
- What's the condition number κ(H)?
- How does λ (regularization) affect κ?

**Part C: Adaptive Strategy**
Design a hybrid optimizer:
- When to switch from L-BFGS to gradient descent?
- How to detect ill-conditioning?
- Batching strategy for stochastic L-BFGS

```python
import numpy as np

class LogisticRegression:
    def __init__(self, n_features, lambda_reg=0.01):
        self.w = np.zeros(n_features)
        self.lambda_reg = lambda_reg
    
    def sigmoid(self, z):
        return 1 / (1 + np.exp(-np.clip(z, -500, 500)))
    
    def loss(self, X, y):
        """Compute loss"""
        m = len(y)
        z = X @ self.w
        return (np.mean(np.log(1 + np.exp(-y * z))) + 
                0.5 * self.lambda_reg * np.dot(self.w, self.w))
    
    def gradient(self, X, y):
        """Compute gradient"""
        m = len(y)
        z = X @ self.w
        sigma = self.sigmoid(y * z)
        grad = -X.T @ (y * (1 - sigma)) / m + self.lambda_reg * self.w
        return grad
    
    def hessian(self, X, y):
        """Compute Hessian (expensive!)"""
        m = len(y)
        z = X @ self.w
        sigma = self.sigmoid(z)
        weights = sigma * (1 - sigma)
        # H = X^T diag(weights) X / m + lambda * I
        H = (X.T * weights) @ X / m + self.lambda_reg * np.eye(len(self.w))
        return H
    
    def train_gd(self, X, y, learning_rate=0.01, max_iter=1000):
        """Gradient descent"""
        # TODO: Implement with convergence checking
        pass
    
    def train_newton(self, X, y, max_iter=100):
        """Newton's method"""
        # TODO: Implement with Hessian inversion
        pass
    
    def train_lbfgs(self, X, y, m=10, max_iter=100):
        """L-BFGS"""
        # TODO: Implement L-BFGS
        pass

# Generate synthetic data
np.random.seed(42)
n_features = 500000
n_samples = 100000
X = np.random.randn(n_samples, n_features) * 0.01  # Sparse-ish
y = np.random.choice([-1, 1], n_samples)

# Compare methods
# TODO: Measure memory, time, iterations for each method
```

**Expected Output**:
```
Part A: Comparison table with memory/time/iterations
Part B: Condition number analysis, effect of λ
Part C: Hybrid strategy with switching criteria
```

---

## Phase 4: Self-Assessment & Feedback

### Mastery Checklist
Rate your understanding (1-5):
- [ ] Understand Newton's method and quadratic convergence
- [ ] Can derive BFGS update formula
- [ ] Know when to use L-BFGS vs first-order methods
- [ ] Understand curvature, Hessian, condition number
- [ ] Can implement basic quasi-Newton method

### Reflection Questions
1. **Why is L-BFGS practical** for large-scale ML but full BFGS is not?
2. **What's the key difference** between Newton's method and gradient descent geometrically?
3. **When would you choose** SGD over L-BFGS for deep learning?

### Mistake Log
Record mistakes:
- **Conceptual**: (e.g., "thought BFGS stores full Hessian")
- **Implementation**: (e.g., "forgot to check positive definiteness")
- **Performance**: (e.g., "used Newton for high-dimensional problem")

### Next Steps
- **If strong**: Proceed to [[Session 14 – Rate Limiting]]
- **If struggling**: Review [[Session 06 – ML & Optimization]] basics
- **Deep dive**:
  - "Numerical Optimization" (Nocedal & Wright) Ch. 6-7
  - "Convex Optimization" (Boyd & Vandenberghe)
  - scipy.optimize.minimize documentation

---

**Navigation**: ← [[Session 12]] | **Index**: [[cycle2/INDEX]] | → [[Session 14]]
