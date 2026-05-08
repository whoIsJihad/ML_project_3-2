> [[MOC (NN)]] | Prev: [[Binary and Multi-class Classification]] | Next: [[Cross-Entropy Loss Function]]

# One-Hot Encoding

One-hot encoding is a representation method for categorical variables where each category is mapped to a unique binary vector. This is essential in [[Binary and Multi-class Classification]] to avoid implying an ordinal relationship between labels.

## The Problem with Integer Encoding

Assume a target variable $y \in \{\text{Cat, Dog, Chicken}\}$.. If we represent these as $y \in \{1, 2, 3\}$:

1. The model might assume that $\text{Cat} < \text{Dog} < \text{Chicken}$.
2. The [[Cross-Entropy Loss Function]] would compute a larger error for predicting "Cat" when the truth is "Chicken" ($|3-1|=2$) than when the truth is "Dog" ($|2-1|=1$).

In classification, all incorrect classes should be treated as equally "wrong" unless specified otherwise.

## Mathematical Definition

Let $K$ be the number of unique classes. A category $k \in \{1, \dots, K\}$ is represented by a vector $\mathbf{y} \in \{0, 1\}^K$ such that:

$$
y_i = \begin{cases} 1 & \text{if } i = k \\ 0 & \text{if } i \neq k \end{cases}
$$

### Example

For $K=3$ (Cat, Dog, Chicken):

- **Cat**: $[1, 0, 0]^T$
- **Dog**: $[0, 1, 0]^T$
- **Chicken**: $[0, 0, 1]^T$

## Relation to the Output Layer

In a [[Multilayer Perceptron Architecture]] designed for multi-class tasks:

1. The output layer must have $K$ neurons.
2. The ground truth for each training example is provided as a one-hot vector.
3. The network's prediction $\mathbf{\hat{y}}$ is a vector of probabilities (via Softmax).
4. The loss is computed by comparing the one-hot vector $\mathbf{y}$ with the probability vector $\mathbf{\hat{y}}$ using [[Cross-Entropy Loss Function]].

## Sparsity Note

One-hot encoding creates sparse vectors (mostly zeros). While inefficient for memory if you have millions of classes (like in NLP), it is the standard for basic computer vision and structured data classification.
