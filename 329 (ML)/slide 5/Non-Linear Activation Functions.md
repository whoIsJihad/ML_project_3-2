> [[MOC (NN)]] | Prev: [[The Artificial Neuron]] | Next: [[Multilayer Perceptron Architecture]]

# Non-Linear Activation Functions

In [[The Artificial Neuron]], the activation function $\sigma(\cdot)$ is responsible for introducing non-linearity into the network.

## The Requirement for Non-linearity

Assume a network uses the identity function $\sigma(z) = z$ for all layers. A two-layer network would compute:

$$a^{(1)} = W^{(1)}x + b^{(1)}$$$$a^{(2)} = W^{(2)}a^{(1)} + b^{(2)} = W^{(2)}(W^{(1)}x + b^{(1)}) + b^{(2)}$$$$a^{(2)} = (W^{(2)}W^{(1)})x + (W^{(2)}b^{(1)} + b^{(2)})$$

The composition of linear functions is itself a linear function. Without non-linear activations, a network with infinite hidden layers is mathematically equivalent to a single-layer linear model.

## Common Activation Functions

### 1. Sigmoid

Defined as:

$$\sigma(z) = \frac{1}{1 + e^{-z}}$$

Output range: $(0, 1)$. Primarily used in the output layer for [[Binary and Multi-class Classification]].

### 2. Hyperbolic Tangent (Tanh)

Defined as:

$$\tanh(z) = \frac{e^z - e^{-z}}{e^z + e^{-z}}$$

Output range: $(-1, 1)$. Zero-centered, which often aids in faster convergence during [[Optimization and Empirical Risk Minimization]].

### 3. Rectified Linear Unit (ReLU)

Defined as:

$$\text{ReLU}(z) = \max(0, z)$$

The standard choice for hidden layers due to its sparsity and mitigation of the vanishing gradient problem.

### 4. Leaky ReLU

Defined as:

$$\text{Leaky ReLU}(z) = \max(\alpha z, z)$$

Where $\alpha$ is a small constant (e.g., $0.01$), ensuring a non-zero gradient for negative inputs.
