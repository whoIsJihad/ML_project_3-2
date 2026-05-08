> [[MOC (NN)]] | Prev: [[Backpropagation and the Chain Rule]] | Next: [[Stochastic Gradient Descent Variants]]

# Optimization and Empirical Risk Minimization

The goal of learning is to find parameters $\theta = \{W, b\}$ that minimize the expected loss over the data-generating distribution $p_{data}$:

$$\theta^* = \arg \min_\theta \mathbb{E}_{x,y \sim p_{data}} [L(h(x; \theta), y)]$$

## Empirical Risk Minimization (ERM)

Since $p_{data}$ is unknown, we minimize the **Empirical Risk** (average loss on training data):

$$\hat{J}(\theta) = \frac{1}{N} \sum_{i=1}^N L(h(x^{(i)}; \theta), y^{(i)})$$

## Optimization Challenges

1. **Local Minima**: Points where the gradient is zero but are not the global minimum.
2. **Saddle Points**: Points where the gradient is zero, but it is a minimum in some dimensions and a maximum in others. Deep networks often encounter saddle points in high-dimensional space.
3. **Vanishing Gradients**: In deep networks, gradients can become extremely small during backpropagation, halting learning.

## Gradient Descent

The fundamental update rule is:

$$\theta \leftarrow \theta - \epsilon \nabla_\theta J(\theta)$$

Where $\epsilon$ is the learning rate. Variations on this approach are detailed in [[Stochastic Gradient Descent Variants]].
