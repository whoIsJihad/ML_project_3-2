> [[MOC (NN)]] | Prev: [[Advanced Optimization Algorithms]]

# Universal Approximation Theorem

The Universal Approximation Theorem provides the theoretical justification for the power of the [[Multilayer Perceptron Architecture]].

## Theorem Statement

A feedforward network with a single hidden layer containing a finite number of neurons can approximate any continuous function $f: \mathbb{R}^n \to \mathbb{R}^m$ to any desired degree of accuracy, provided that:

1. The activation function $\sigma$ is non-polynomial almost everywhere.
2. The network has sufficient width (number of neurons in the hidden layer).

## Practical Implications

While the theorem guarantees that a shallow network _can_ represent any function, it does not guarantee that the function is _learnable_ via gradient descent, nor that the required number of neurons is practical. In practice, increasing the **depth** of a network (adding more hidden layers) is often more efficient than increasing its width for learning hierarchical representations.

### Reference

Leshno et al. (1993) proved that multilayer feedforward networks with non-polynomial activation functions are universal approximators.
