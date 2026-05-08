# Calculus for Neural Networks

## Essential Derivatives

Neural networks rely on derivatives (gradients) for learning.

Must understand how derivatives combine across nested functions.

## The Derivative: Formal Definition

Rate of change of function $f$ at point $x$:

$$f'(x) = \frac{df}{dx} = \lim_{h \to 0} \frac{f(x+h) - f(x)}{h}$$

Geometric interpretation: Slope of tangent line to $f(x)$ at point $x$.

### Numeric Approximation

For computation, use finite differences:

$$f'(x) \approx \frac{f(x + \epsilon) - f(x - \epsilon)}{2\epsilon}$$

Where $\epsilon$ is small (e.g., 0.0001).

Example: $f(x) = x^2$

$$f'(2) = \frac{(2 + 0.0001)^2 - (2 - 0.0001)^2}{2 \times 0.0001}$$

$$= \frac{4.0004 - 3.9996}{0.0002} = \frac{0.0008}{0.0002} = 4$$

Exact derivative: $\frac{d}{dx}[x^2] = 2x = 2(2) = 4$ (check)

## Common Derivatives

**Power rule**: $\frac{d}{dx}[x^n] = n x^{n-1}$

Example: $\frac{d}{dx}[x^3] = 3x^2$

**Exponential**: $\frac{d}{dx}[e^x] = e^x$

**Logarithm**: $\frac{d}{dx}[\ln(x)] = \frac{1}{x}$

**Sigmoid**: $\sigma(x) = \frac{1}{1+e^{-x}}$

$$\frac{d\sigma}{dx} = \sigma(x)(1 - \sigma(x))$$

At $x=0$: $\sigma(0) = 0.5$, so $\frac{d\sigma}{dx}|_{x=0} = 0.5 \times 0.5 = 0.25$

**Tanh**: $\tanh(x) = \frac{e^x - e^{-x}}{e^x + e^{-x}}$

$$\frac{d\tanh}{dx} = 1 - \tanh^2(x)$$

At $x=0$: $\tanh(0) = 0$, so $\frac{d\tanh}{dx}|_{x=0} = 1 - 0 = 1$

**ReLU**: $\text{ReLU}(x) = \max(0, x)$

$$\frac{d\text{ReLU}}{dx} = \begin{cases} 1 & \text{if } x > 0 \\ 0 & \text{if } x < 0 \end{cases}$$

## Chain Rule: The Foundation of Backprop

Fundamental rule for composite functions.

If $y = f(g(x))$, then:

$$\frac{dy}{dx} = \frac{dy}{dg} \cdot \frac{dg}{dx}$$

### Numeric Example

$f(u) = u^2, g(x) = 3x + 1$

$y = f(g(x)) = (3x+1)^2$

Method 1 (expand, then differentiate):
$$y = 9x^2 + 6x + 1$$
$$\frac{dy}{dx} = 18x + 6$$

At $x=2$: $\frac{dy}{dx} = 18(2) + 6 = 42$

Method 2 (chain rule):
$$\frac{dy}{du} = 2u = 2(3x+1) = 6x + 2$$
$$\frac{du}{dx} = 3$$

$$\frac{dy}{dx} = (6x+2) \times 3 = 18x + 6$$

At $x=2$: $\frac{dy}{dx} = 42$ (check)

### Deep Chain (Multiple Layers)

$$y = f_3(f_2(f_1(x)))$$

$$\frac{dy}{dx} = \frac{dy}{df_3} \cdot \frac{df_3}{df_2} \cdot \frac{df_2}{df_1} \cdot \frac{df_1}{dx}$$

### Neural Network Application

Network: $y = \sigma(w_2 \sigma(w_1 x + b_1) + b_2)$

Three function compositions:

1. $u_1 = w_1 x + b_1$ (linear)
2. $u_2 = \sigma(u_1)$ (sigmoid)
3. $u_3 = w_2 u_2 + b_2$ (linear)
4. $y = \sigma(u_3)$ (sigmoid)

Gradient w.r.t. $x$:

$$\frac{\partial y}{\partial x} = \frac{\partial y}{\partial u_3} \cdot \frac{\partial u_3}{\partial u_2} \cdot \frac{\partial u_2}{\partial u_1} \cdot \frac{\partial u_1}{\partial x}$$

Computing right-to-left:
$$= \sigma'(u_3) \cdot w_2 \cdot \sigma'(u_1) \cdot w_1$$

## Partial Derivatives

Functions often have multiple inputs.

**Partial derivative** $\frac{\partial f}{\partial x_i}$: derivative w.r.t. one variable, treating others as constants.

Example: $f(x, y) = 3x^2 y + y^3$

$$\frac{\partial f}{\partial x} = 6xy + 0 = 6xy$$

$$\frac{\partial f}{\partial y} = 3x^2 + 3y^2$$

At $(x, y) = (2, 1)$:
$$\frac{\partial f}{\partial x} = 6(2)(1) = 12$$
$$\frac{\partial f}{\partial y} = 3(4) + 3(1) = 15$$

## The Gradient Vector

All partial derivatives collected:

$$\nabla f = \begin{bmatrix} \frac{\partial f}{\partial x_1} \\ \frac{\partial f}{\partial x_2} \\ \vdots \\ \frac{\partial f}{\partial x_n} \end{bmatrix}$$

Points in direction of steepest increase.

**Gradient descent**: Update parameters opposite gradient direction.

$$x_{\text{new}} = x_{\text{old}} - \alpha \nabla f$$

$\alpha$ = learning rate.

### Numeric Example: 2D Gradient Descent

Function: $f(x, y) = x^2 + 4y^2$ (bowl-shaped)

Gradient: $\nabla f = [2x, 8y]$

**Initial point**: $(x, y) = (4, 2)$

$$\nabla f = [8, 16]$$

**Update** (learning rate $\alpha = 0.1$):

$$x_{\text{new}} = 4 - 0.1 \times 8 = 3.2$$
$$y_{\text{new}} = 2 - 0.1 \times 16 = 0.4$$

**Next step**: $(3.2, 0.4)$

$$\nabla f = [6.4, 3.2]$$

$$x_{\text{new}} = 3.2 - 0.1 \times 6.4 = 2.56$$
$$y_{\text{new}} = 0.4 - 0.1 \times 3.2 = 0.08$$

After many steps: approaches $(0, 0)$ (minimum).

## Matrix Derivatives

For vector/matrix functions, derivatives are more complex.

**Jacobian matrix**: All partial derivatives organized in matrix form.

For function $\mathbf{y} = f(\mathbf{x})$ where $\mathbf{x} \in \mathbb{R}^m, \mathbf{y} \in \mathbb{R}^n$:

$$J = \begin{bmatrix} \frac{\partial y_1}{\partial x_1} & \cdots & \frac{\partial y_1}{\partial x_m} \\ \vdots & \ddots & \vdots \\ \frac{\partial y_n}{\partial x_1} & \cdots & \frac{\partial y_n}{\partial x_m} \end{bmatrix}$$

Shape: $(n \times m)$

### Example: Linear Transformation

$\mathbf{y} = W \mathbf{x}$ where $W \in \mathbb{R}^{2 \times 3}, \mathbf{x} \in \mathbb{R}^3, \mathbf{y} \in \mathbb{R}^2$

$$y_1 = w_{11} x_1 + w_{12} x_2 + w_{13} x_3$$
$$y_2 = w_{21} x_1 + w_{22} x_2 + w_{23} x_3$$

Jacobian:
$$J = \begin{bmatrix} w_{11} & w_{12} & w_{13} \\ w_{21} & w_{22} & w_{23} \end{bmatrix} = W$$

Jacobian is just the weight matrix!

## Matrix Chain Rule

For composed matrix functions:

$\mathbf{y} = f(g(\mathbf{x}))$

$$\frac{\partial \mathbf{y}}{\partial \mathbf{x}} = \frac{\partial \mathbf{y}}{\partial g} \cdot \frac{\partial g}{\partial \mathbf{x}}$$

(Matrix multiplication of Jacobians)

### Neural Network Layer

Input: $\mathbf{x} \in \mathbb{R}^n$

$$\mathbf{z} = W \mathbf{x} + \mathbf{b}$$
$$\mathbf{a} = \sigma(\mathbf{z})$$

Jacobian $\frac{\partial \mathbf{a}}{\partial \mathbf{x}}$:

$$\frac{\partial \mathbf{a}}{\partial \mathbf{x}} = \frac{\partial \mathbf{a}}{\partial \mathbf{z}} \cdot \frac{\partial \mathbf{z}}{\partial \mathbf{x}}$$

$$= \text{diag}(\sigma'(\mathbf{z})) \cdot W$$

**Derivation (step-by-step):**

1. Write pre-activation components: $z_k = \sum_{j} w_{kj} x_j + b_k$. Therefore

$$\frac{\partial z_k}{\partial x_j} = w_{kj} \quad (\text{so } \frac{\partial \mathbf{z}}{\partial \mathbf{x}} = W).$$

2. Activation components: $a_i = \sigma(z_i)$, so

$$\frac{\partial a_i}{\partial z_k} = \sigma'(z_i)\,\delta_{ik}$$

(where $\delta_{ik}$ is the Kronecker delta, $1$ if $i=k$, else $0$). Hence

$$\frac{\partial \mathbf{a}}{\partial \mathbf{z}} = \text{diag}(\sigma'(\mathbf{z})).$$

3. Apply chain rule element-wise:

$$
(\frac{\partial \mathbf{a}}{\partial \mathbf{x}})_{i,j} = \sum_k \frac{\partial a_i}{\partial z_k} \frac{\partial z_k}{\partial x_j}
= \sum_k \sigma'(z_i) \delta_{ik} w_{kj}
= \sigma'(z_i) w_{ij}.
$$

Thus the matrix form follows:

$$
\frac{\partial \mathbf{a}}{\partial \mathbf{x}} = \text{diag}(\sigma'(\mathbf{z})) \, W
$$

with shapes: $\text{diag}(\sigma'(\mathbf{z}))\in\mathbb{R}^{m\times m}$, $W\in\mathbb{R}^{m\times n}$, product $\in\mathbb{R}^{m\times n}$.

**Numeric example:**

- Let $W = \begin{bmatrix}0.2 & -0.5 & 1.0\\ 0.7 & 0.1 & -0.3\end{bmatrix}$, and $\sigma'(z) = [0.1217,\ 0.1683]$.
- Then

$$\text{diag}(\sigma'(z)) = \begin{bmatrix}0.1217 & 0\\ 0 & 0.1683\end{bmatrix},$$

and

$$\text{diag}(\sigma'(z))\,W \approx \begin{bmatrix}0.0243 & -0.0608 & 0.1217\\ 0.1178 & 0.0168 & -0.0505\end{bmatrix}.$$

**Repro (NumPy):**

```python
import numpy as np
sigma_prime = np.array([0.1217, 0.1683])   # shape (2,)
W = np.array([[0.2, -0.5, 1.0],
              [0.7,  0.1, -0.3]])          # shape (2,3)

J = sigma_prime[:, None] * W  # broadcasts -> shape (2,3)
print(J)
```

(Equivalently use `np.diag(sigma_prime).dot(W)`.)

## Hessian: Second Derivatives

Hessian matrix contains all second partial derivatives.

$$H = \begin{bmatrix} \frac{\partial^2 f}{\partial x_1^2} & \frac{\partial^2 f}{\partial x_1 \partial x_2} & \cdots \\ \frac{\partial^2 f}{\partial x_2 \partial x_1} & \frac{\partial^2 f}{\partial x_2^2} & \cdots \\ \vdots & \vdots & \ddots \end{bmatrix}$$

Characterizes local curvature.

**Use in optimization**: Newton's method (second-order).

$$\mathbf{x}_{\text{new}} = \mathbf{x}_{\text{old}} - H^{-1} \nabla f$$

More expensive (computing Hessian inverse) but faster convergence.

Rarely used in deep learning (Hessian too large for millions of parameters).

## Practical: Numerical Gradient Checking

Verify gradient computation is correct.

Compare analytical gradient (from chain rule) with numerical gradient (finite differences).

**Algorithm**:

```
for each parameter w:
    grad_numerical = (f(w + epsilon) - f(w - epsilon)) / (2epsilon)
    grad_analytical = computed_gradient[w]
    
    if |grad_numerical - grad_analytical| > threshold:
        print("ERROR: Gradient mismatch")
```

$\epsilon = 10^{-5}$ typical.

Relative error should be < $10^{-7}$ for float32.

### Numeric Example

Function: $f(w) = (w^2 + 1)$

Analytical gradient: $\frac{df}{dw} = 2w$

At $w=3$: analytical = 6

Numerical ($ \epsilon = 10^{-5}$):
$$\text{numerical} = \frac{f(3 + 10^{-5}) - f(3 - 10^{-5})}{2 \times 10^{-5}}$$

$$= \frac{(3.00001)^2 + 1 - ((2.99999)^2 + 1)}{2 \times 10^{-5}}$$

$$= \frac{9.00060001 - 8.99940001}{0.00002} = \frac{0.0012}{0.00002} = 60$$

Wait, that's not 6! Let me recalculate:

Actually: $f(w) = w^2 + 1$, $f'(w) = 2w$

$f(3.00001) = 3.00001^2 + 1 = 9.00006 + 1 = 10.00006$
$f(2.99999) = 2.99999^2 + 1 = 8.99994 + 1 = 9.99994$

$$\text{numerical} = \frac{10.00006 - 9.99994}{0.00002} = \frac{0.00012}{0.00002} = 6$$

(check) Great! Analytical and numerical agree.

## Summary

Derivatives measure rate of change.

Chain rule composes derivatives across layers.

Gradient vector points toward increasing loss.

Gradient descent updates parameters opposite gradient.

Matrix calculus extends to multi-dimensional functions.

Numerical gradient checking validates implementations.

Essential foundation for understanding [[Neural Networks Basics]] and [[Backpropagation]].
