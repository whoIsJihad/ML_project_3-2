### Topic: Computing the Gradient (Derivatives)

#### The Mathematical Goal

To use Gradient Descent, we need to solve for $\frac{\partial J}{\partial w}$ (slope relative to weight) and $\frac{\partial J}{\partial b}$ (slope relative to bias).

The Calculus (Chain Rule)

Recall our Loss Function (MSE) for a single example:

$$J = (y - \hat{y})^2$$

$$J = (y - (wx + b))^2$$

To find the derivative with respect to $w$, we apply the Chain Rule:

$$\frac{\partial J}{\partial w} = \frac{\partial J}{\partial \hat{y}} \cdot \frac{\partial \hat{y}}{\partial w}$$

**Step-by-Step Derivation**

1. **Outer Derivative:** Derivative of the square function.
    
    - $\frac{\partial}{\partial \hat{y}}(y - \hat{y})^2 = 2(y - \hat{y}) \cdot (-1)$
        
    - Result: $-2(y - \hat{y})$
        
2. **Inner Derivative:** Derivative of the line equation $\hat{y} = wx + b$ with respect to $w$.
    
    - $\frac{\partial}{\partial w}(wx + b) = x$
        
3. **Combine them:**
    
    - $\frac{\partial J}{\partial w} = -2(y - \hat{y}) \cdot x$
        

The Final Gradient Formulas (Averaged over N)

When we average this over the entire dataset ($N$), we get the gradients we use in code:

- Gradient for Weight ($dw$):
    
    $$\frac{\partial J}{\partial w} = -\frac{2}{N} \sum_{i=1}^{N} x_i (y_i - \hat{y}_i)$$
    
- Gradient for Bias ($db$):
    
    (Since the inner derivative of $b$ is just 1)
    
    $$\frac{\partial J}{\partial b} = -\frac{2}{N} \sum_{i=1}^{N} (y_i - \hat{y}_i)$$
    

####  **Interpretation**

- **The Error term $(y - \hat{y})$:** The larger the error, the larger the gradient (step size). If the prediction is perfect, gradient is 0 (stop moving).
    
- **The Input term $(x)$:** For weights, the gradient is scaled by the input. If input $x$ is huge, a tiny change in weight causes a huge change in output, so the gradient must reflect that sensitivity.
    
