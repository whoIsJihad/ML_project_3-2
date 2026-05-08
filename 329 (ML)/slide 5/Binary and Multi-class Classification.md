> [[MOC (NN)]] | Prev: [[Neural Network Vectorization]] | Next: [[One-Hot Encoding]]

# Binary and Multi-class Classification

Classification tasks in [[Deep Learning]] involve mapping the network's output layer to a discrete set of classes.

## Binary Classification

Used when the target $y \in \{0, 1\}$.

- **Output Layer**: A single neuron with a Sigmoid activation.
- **Interpretation**: The output $\hat{y}$ represents the probability $P(y=1|x)$.

## Multi-class Classification

Used when $y \in \{1, 2, \dots, K\}$ where $K > 2$.

### One-Hot Encoding

Targets are represented as vectors $y \in \{0, 1\}^K$. For class $k$, the $k$-th element is 1 and all others are 0. This treats the problem as $K$ distinct binary classification tasks.

### The Softmax Function

To ensure the output represents a valid probability distribution ($\sum \hat{y}_k = 1$), we use the Softmax activation on the output layer:

$$\text{Softmax}(z_i) = \frac{e^{z_i}}{\sum_{j=1}^K e^{z_j}}$$

The output $\hat{y}_i$ is the predicted probability that the input belongs to class $i$.

The discrepancy between $\hat{y}$ and the ground truth $y$ is measured using the [[Cross-Entropy Loss Function]].
