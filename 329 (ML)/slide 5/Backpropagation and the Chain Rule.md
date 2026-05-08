> [[MOC (NN)]] | Prev: [[Cross-Entropy Loss Function]] | Next: [[Optimization and Empirical Risk Minimization]]

# Backpropagation and the Chain Rule

Backpropagation is the algorithm used to compute the gradient of the cost function $J$ with respect to every weight $W$ and bias $b$ in the network.

## The Univariate Chain Rule

If $f(x)$ and $x(t)$ are univariate functions, the derivative of the composite function $f(x(t))$ is:

$$\frac{df}{dt} = \frac{df}{dx} \cdot \frac{dx}{dt}$$

## The Multivariate Chain Rule

If $f(x, y)$ is a function of $x(t)$ and $y(t)$, the total derivative is:

$$\frac{df}{dt} = \frac{\partial f}{\partial x} \frac{dx}{dt} + \frac{\partial f}{\partial y} \frac{dy}{dt}$$

## Propagation Logic

The algorithm works backward from the output layer to the input layer:

1. Compute the error signal at the output layer $\delta^{[L]} = \frac{\partial L}{\partial z^{[L]}}$.
2. Propagate the error to the previous layer:

   $$\delta^{[l]} = (W^{[l+1]})^T \delta^{[l+1]} \odot \sigma'(z^{[l]})$$

   Where $\odot$ denotes the element-wise (Hadamard) product.

3. Compute gradients for parameters:

   $$\frac{\partial L}{\partial W^{[l]}} = \delta^{[l]} (a^{[l-1]})^T$$$$\frac{\partial L}{\partial b^{[l]}} = \delta^{[l]}$$

These gradients are then used by [[Optimization and Empirical Risk Minimization]] to update the model.
