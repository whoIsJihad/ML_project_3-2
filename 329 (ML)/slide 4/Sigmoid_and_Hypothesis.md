# The Sigmoid Function and Hypothesis

To turn a linear prediction into a probability, [[Logistic_Regression_Core|Logistic Regression]] uses the **Sigmoid Function** (also called the Logistic Function).

## The Hypothesis

The hypothesis is defined as:

$$h_{\theta}(x) = g(\theta^T x) = \frac{1}{1 + e^{-\theta^T x}}$$

## The Sigmoid Function $g(z)$

$$g(z) = \frac{1}{1 + e^{-z}}$$

### Properties

- **Range**: $(0, 1)$.
    
- **Threshold**:
    
    - If $z \ge 0$, then $g(z) \ge 0.5 \implies$ Predict Class 1.
        
    - If $z < 0$, then $g(z) < 0.5 \implies$ Predict Class 0.
        
- **The Derivative (Critical for Learning)**: The derivative of the sigmoid is elegantly defined by itself:
    
    $$g'(z) = g(z)(1 - g(z))$$

## Why not use a straight line?

A straight line doesn't respect the boundaries of probability. The Sigmoid provides a smooth, differentiable "S-curve" that allows us to use calculus for optimization.