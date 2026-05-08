# Linear Regression Parameter Derivation

## 1. Hypothesis Definition

The linear model approximates $y$ as a weighted sum of features $x$.

- **Input:** $x$ (feature vector, includes $x_0 = 1$ for bias).
    
- **Parameters:** $\theta$ (weights).
    
- **Equation:**
    
    $$h_\theta(x) = \sum_{i=0}^d \theta_i x_i = \theta^T x$$

## 2. Cost Function (J)

We measure error using Least Mean Squares (LMS).

- **Objective:** Minimize sum of squared differences.
    
- **Formula:**
    
    $$J(\theta) = \frac{1}{2} \sum_{k=1}^n (h_\theta(x^{(k)}) - y^{(k)})^2$$
    - $n$: Training examples count.
        
    - $\frac{1}{2}$: Simplifies derivative.
        

## 3. Minimization Strategy

Find optimal $\theta^*$ by calculating gradient of $J(\theta)$ and setting to zero.

$$\theta^* = \underset{\theta}{\arg\min} J(\theta)$$

### Partial Derivative Step

For each weight $\theta_j$:

$$\frac{\partial J}{\partial \theta_j} = \sum_{k=1}^n (h_\theta(x^{(k)}) - y^{(k)}) x_j^{(k)} = 0$$

## 4. Solving for Parameters

Setting derivatives to 0 creates a linear equation system.

### Algebraic Expansion

For $n$ samples, expanding summation:

$$\sum_{k=1}^n (\theta_0 x_0^{(k)} + \theta_1 x_1^{(k)} + \dots + \theta_d x_d^{(k)} - y^{(k)}) x_j^{(k)} = 0$$

### Matrix (Vectorized) Form

Uses linear algebra for efficiency.

- **Design Matrix (**$X$**):** Dimensions $n \times (d+1)$.
    
    - Row: One training example $(x^{(i)})^T$.
        
    - Column: One feature across all examples.
        
    - Col 1: All $1$s (bias $x_0$).
        $$X = \begin{bmatrix} (x^{(1)})^T \\ (x^{(2)})^T \\ \vdots \\ (x^{(n)})^T \end{bmatrix} = \begin{bmatrix} 1 & x_1^{(1)} & x_2^{(1)} & \dots & x_d^{(1)} \\ 1 & x_1^{(2)} & x_2^{(2)} & \dots & x_d^{(2)} \\ \vdots & \vdots & \vdots & \ddots & \vdots \\ 1 & x_1^{(n)} & x_2^{(n)} & \dots & x_d^{(n)} \end{bmatrix}$$
- **Target Vector (**$y$**):** Dimensions $n \times 1$.
    
    $$y = \begin{bmatrix} y^{(1)} \\ y^{(2)} \\ \vdots \\ y^{(n)} \end{bmatrix}$$
- **Parameter Vector (**$\theta$**):** Dimensions $(d+1) \times 1$.
    
    $$\theta = \begin{bmatrix} \theta_0 \\ \theta_1 \\ \vdots \\ \theta_d \end{bmatrix}$$

**System of Equations:**

$$(X^T X)\theta = X^T y$$

**Normal Equation (Closed-form Solution):**

$$\theta^* = (X^T X)^{-1} X^T y$$

## 5. Summary

- **Derivatives to 0:** Finds minimum.
    
- **Normal Equation:** Direct $\theta$ calculation (no iteration).
    
- **Computation:** Inverting $X^T X$ is expensive for large $d$.