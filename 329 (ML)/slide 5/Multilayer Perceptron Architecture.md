> [[MOC (NN)]] | Prev: [[Non-Linear Activation Functions]] | Next: [[Neural Network Vectorization]]

# Multilayer Perceptron Architecture

A Multilayer Perceptron (MLP), or a Fully-connected Neural Network, is a structured arrangement of [[The Artificial Neuron]] units organized into layers.

## Layer Classification

1. **Input Layer**: Receives the raw feature vector $x$. It contains $n$ units, where $n$ is the number of features.
2. **Hidden Layers**: Intermediate layers that perform feature extraction. A network is "Deep" if it contains multiple hidden layers.
3. **Output Layer**: Produces the final prediction $y$. The number of units $m$ depends on the task (see [[Binary and Multi-class Classification]]).

## Fully-connected Property

In a standard MLP, the output of every neuron in layer $l$ serves as an input to every neuron in layer $l+1$. This dense connectivity ensures that the network can learn dependencies between any combination of input features.

## Formal Notation

For a layer $l$:

- $W^{[l]}$ is the weight matrix where $W^{[l]}_{ij}$ is the weight between the $j$-th neuron of layer $l-1$ and the $i$-th neuron of layer $l$.
- $b^{[l]}$ is the bias vector for layer $l$.
- $a^{[l]}$ is the activation vector of layer $l$.

The forward propagation step is formalized in [[Neural Network Vectorization]].
