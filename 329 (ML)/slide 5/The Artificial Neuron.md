> [[MOC (NN)]] | Next: [[Non-Linear Activation Functions]]

# The Artificial Neuron

The artificial neuron is the fundamental atomic unit of a [[Deep Learning]] system. It is a mathematical function that maps an input vector to a scalar output.

## Formal Definition

Given an input vector $x \in \mathbb{R}^n$, a neuron is defined by its parameters: a weight vector $w \in \mathbb{R}^n$ and a scalar bias $b \in \mathbb{R}$. The output $a$ is computed in two stages:

1. **Linear Aggregation (Pre-activation)**:

   $$z = w^T x + b = \sum_{j=1}^n w_j x_j + b$$

2. **Non-linear Transformation (Activation)**:

   $$a = \sigma(z)$$

   Where $\sigma(\cdot)$ is a [[Non-Linear Activation Functions]].

## Interpretation of Parameters

- **Weights (**$w$**)**: Represent the relative importance or "strength" of each input feature.
- **Bias (**$b$**)**: A thresholding parameter that allows the activation function to shift along the horizontal axis, providing the model with flexibility even when inputs are zero.

## Complexity through Stacking

While a single neuron can model basic non-linear relations, stacking them in layers allows the network to learn progressively more complex abstractions. This lead to the [[Multilayer Perceptron Architecture]].
