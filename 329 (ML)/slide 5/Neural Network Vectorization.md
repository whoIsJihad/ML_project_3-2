> [[MOC (NN)]] | Prev: [[Multilayer Perceptron Architecture]] | Next: [[Binary and Multi-class Classification]]

# Neural Network Vectorization

To compute the activations of a [[Multilayer Perceptron Architecture]] efficiently, we utilize matrix operations. This avoids explicit looping over individual neurons and leverages optimized BLAS (Basic Linear Algebra Subprograms) libraries.

## Dimensionality and Layer Independence

There is **no requirement** for adjacent layers to have the same number of nodes. Each layer $l$ can have an arbitrary number of neurons $n_l$, independent of the previous layer's count $n_{l-1}$.

## The Weight Matrix $W^{[l]}$

For a layer $l$, the weight matrix $W^{[l]}$ encapsulates all connections from layer $l-1$.

- **Rows**: The number of rows equals $n_l$ (the number of neurons in the current layer).
- **Columns**: The number of columns equals $n_{l-1}$ (the number of neurons in the previous layer).
- **Shape**: $W^{[l]} \in \mathbb{R}^{n_l \times n_{l-1}}$.

Each row $i$ in $W^{[l]}$ corresponds to the weights for the $i$-th neuron in the current layer.

## Forward Propagation Equations

For a specific layer $l$, the computation is:

1. **Linear Transformation**:

   $$Z^{[l]} = W^{[l]} a^{[l-1]} + b^{[l]}$$

   Where:
   - $a^{[l-1]}$ is the activation vector from the previous layer $(n_{l-1} \times 1)$.
   - $b^{[l]}$ is the bias vector for the current layer $(n_l \times 1)$.
   - $Z^{[l]}$ is the resulting pre-activation vector $(n_l \times 1)$.

2. **Non-linear Activation**:

   $$a^{[l]} = \sigma^{[l]}(Z^{[l]})$$

   The activation function $\sigma$ is applied element-wise.

## Batch Vectorization (The "Big" Matrix)

When processing a mini-batch of size $m$ (see [[Stochastic Gradient Descent Variants]]), the input becomes a matrix $A^{[l-1]}$ of shape $(n_{l-1} \times m)$.

$$Z^{[l]} = W^{[l]} A^{[l-1]} + b^{[l]}$$

The bias vector $b^{[l]}$ is "broadcasted" across all $m$ columns. The resulting $Z^{[l]}$ is an $(n_l \times m)$ matrix, where each column represents the hidden representation of one example in the batch.
