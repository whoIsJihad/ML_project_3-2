> [[MOC (NN)]] | Prev: [[Stochastic Gradient Descent Variants]] | Next: [[Universal Approximation Theorem]]

# Advanced Optimization Algorithms

Standard SGD often oscillates in ravines or gets stuck in saddle points. Advanced optimizers address these issues using momentum and adaptive learning rates.

## Momentum

Introduces a velocity term $v$ to smooth out updates:

$$v_t = \gamma v_{t-1} + \eta \nabla_\theta J(\theta)$$$$\theta = \theta - v_t$$

This allows the optimization to "build speed" in consistent directions and dampen oscillations.

## Nesterov Accelerated Gradient (NAG)

A "look-ahead" version of momentum. It computes the gradient at the predicted future position of the parameters, allowing for more responsive corrections.

## Adaptive Learning Rates

Instead of a global $\epsilon$, these algorithms adjust the learning rate for each parameter individually based on the history of gradients.

1. **AdaGrad**: Scales learning rate by the inverse of the square root of the sum of all past squared gradients.
2. **RMSProp**: Uses an exponentially weighted moving average of squared gradients to prevent the learning rate from vanishing too quickly.
3. **Adam (Adaptive Moment Estimation)**: Combines momentum (first moment) and RMSProp (second moment). It is the current industry standard for training deep networks.
