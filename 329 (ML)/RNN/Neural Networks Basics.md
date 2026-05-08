# Neural Networks Basics

## Definition

An **artificial neural network** is a computational model inspired by biological neurons.

It's a directed acyclic graph of differentiable functions.

Information flows from input nodes through hidden layers to output nodes.

## Neuron (Perceptron): Single Computation Unit

A neuron computes:

$$z = \sum_{i=1}^{n} w_i x_i + b = \mathbf{w}^T \mathbf{x} + b$$

$$a = g(z)$$

Where:
- $x_i$ are inputs (or outputs from previous layer)
- $w_i$ are weights (parameters to learn)
- $b$ is bias (also learned)
- $g$ is activation function
- $a$ is activation (output)

The neuron performs: weighted sum → bias addition → nonlinear activation.

## Activation Functions

Activation functions introduce nonlinearity. Without them, neural network is just linear transformation.

### Sigmoid

$$\sigma(z) = \frac{1}{1 + e^{-z}}$$

Range: (0, 1). Smooth, differentiable everywhere.

Historically popular. Now rarely used in hidden layers (numerical issues).

**Numeric example**: 
- $\sigma(0) = 0.5$
- $\sigma(2) = 0.88$
- $\sigma(-2) = 0.12$

### Tanh (Hyperbolic Tangent)

$$\tanh(z) = \frac{e^z - e^{-z}}{e^z + e^{-z}}$$

Range: (-1, 1). Centered at zero (helps training).

Derivative: $\tanh'(z) = 1 - \tanh^2(z)$

**Numeric example**:
- $\tanh(0) = 0$
- $\tanh(1) = 0.76$
- $\tanh(-1) = -0.76$

### ReLU (Rectified Linear Unit)

$$\text{ReLU}(z) = \max(0, z)$$

Range: [0, ∞). Simple, computationally efficient.

Derivative: $1$ if $z > 0$, else $0$.

**Numeric example**:
- $\text{ReLU}(-5) = 0$
- $\text{ReLU}(0) = 0$
- $\text{ReLU}(3) = 3$

**Advantage**: Avoids saturation (sigmoid/tanh flatten for large |z|, gradients become tiny).

**Disadvantage**: Not differentiable at $z = 0$ (in practice, not a real issue; use subgradient).

Dead ReLU problem: if weights make $z < 0$ consistently, neuron stops learning (gradient = 0).

### Leaky ReLU

$$\text{LeakyReLU}(z) = \begin{cases} z & \text{if } z > 0 \\ \alpha z & \text{if } z \leq 0 \end{cases}$$

Where $\alpha$ is small (e.g., 0.01).

Avoids completely dead neurons. Gradient is always nonzero.

## Feedforward Network Architecture

Layers process data sequentially:

**Input layer**: Raw data (not a computation, just data).

**Hidden layers**: Intermediate computations.

**Output layer**: Final prediction.

### Example: 3-Layer Network

Input: $n_0 = 3$ features
Hidden 1: $n_1 = 4$ neurons
Hidden 2: $n_2 = 2$ neurons
Output: $n_3 = 1$ neuron

**Layer 1 computation**:

$$z^{[1]} = W^{[1]} x + b^{[1]}$$
$$a^{[1]} = g(z^{[1]})$$

Where:
- $x$ is input: shape $(3,)$
- $W^{[1]}$: shape $(4, 3)$ - 4 neurons, each processes 3 inputs
- $b^{[1]}$: shape $(4,)$ - one bias per neuron
- $z^{[1]}$: shape $(4,)$ - pre-activation
- $a^{[1]}$: shape $(4,)$ - activation (hidden layer output)

**Layer 2 computation**:

$$z^{[2]} = W^{[2]} a^{[1]} + b^{[2]}$$
$$a^{[2]} = g(z^{[2]})$$

Where:
- $W^{[2]}$: shape $(2, 4)$
- $a^{[2]}$: shape $(2,)$

**Layer 3 (Output) computation**:

$$z^{[3]} = W^{[3]} a^{[2]} + b^{[3]}$$
$$a^{[3]} = g(z^{[3]})$$

Where:
- $W^{[3]}$: shape $(1, 2)$
- $a^{[3]}$: shape $(1,)$ - final prediction

Total parameters:
- Layer 1: $4 \times 3 + 4 = 16$ parameters
- Layer 2: $2 \times 4 + 2 = 10$ parameters
- Layer 3: $1 \times 2 + 1 = 3$ parameters
- **Total: 29 parameters**

### Numerical Simulation

**Input**: $x = [1.0, 2.0, 0.5]$

**Layer 1**:

Random initialization:
$$W^{[1]} = \begin{bmatrix} 0.5 & -0.2 & 0.1 \\ 0.3 & 0.4 & -0.1 \\ -0.1 & 0.2 & 0.3 \\ 0.2 & -0.3 & 0.4 \end{bmatrix}, \quad b^{[1]} = [0.1, -0.1, 0.2, -0.2]$$

Compute $z^{[1]} = W^{[1]} x + b^{[1]}$:

$$z^{[1]}_1 = 0.5(1) - 0.2(2) + 0.1(0.5) + 0.1 = 0.5 - 0.4 + 0.05 + 0.1 = 0.25$$
$$z^{[1]}_2 = 0.3(1) + 0.4(2) - 0.1(0.5) - 0.1 = 0.3 + 0.8 - 0.05 - 0.1 = 0.95$$
$$z^{[1]}_3 = -0.1(1) + 0.2(2) + 0.3(0.5) + 0.2 = -0.1 + 0.4 + 0.15 + 0.2 = 0.65$$
$$z^{[1]}_4 = 0.2(1) - 0.3(2) + 0.4(0.5) - 0.2 = 0.2 - 0.6 + 0.2 - 0.2 = -0.4$$

$$z^{[1]} = [0.25, 0.95, 0.65, -0.4]$$

Apply ReLU: $a^{[1]} = [0.25, 0.95, 0.65, 0]$ (last value killed by ReLU)

**Layer 2** (using tanh):

$$W^{[2]} = \begin{bmatrix} 0.4 & -0.2 & 0.1 & 0.3 \\ -0.1 & 0.5 & -0.3 & 0.2 \end{bmatrix}, \quad b^{[2]} = [0.05, -0.05]$$

$$z^{[2]}_1 = 0.4(0.25) - 0.2(0.95) + 0.1(0.65) + 0.3(0) + 0.05 = 0.1 - 0.19 + 0.065 + 0.05 = 0.025$$
$$z^{[2]}_2 = -0.1(0.25) + 0.5(0.95) - 0.3(0.65) + 0.2(0) - 0.05 = -0.025 + 0.475 - 0.195 - 0.05 = 0.205$$

$$z^{[2]} = [0.025, 0.205]$$

Apply tanh: $a^{[2]} = [\tanh(0.025), \tanh(0.205)] \approx [0.025, 0.202]$

**Layer 3** (Output, linear for regression):

$$W^{[3]} = [0.6, -0.4], \quad b^{[3]} = 0.1$$

$$a^{[3]} = 0.6(0.025) - 0.4(0.202) + 0.1 = 0.015 - 0.081 + 0.1 = 0.034$$

**Prediction**: $0.034$ (depends on task; if classification, apply sigmoid for probability)

## Loss Function

Measures prediction error.

### Mean Squared Error (Regression)

$$\mathcal{L} = \frac{1}{m} \sum_{i=1}^{m} (y_i - \hat{y}_i)^2$$

Where:
- $m$ is number of training examples
- $y_i$ is true label
- $\hat{y}_i$ is prediction

### Cross-Entropy (Classification)

For binary classification:

$$\mathcal{L} = -\frac{1}{m} \sum_{i=1}^{m} [y_i \log(\hat{y}_i) + (1-y_i) \log(1-\hat{y}_i)]$$

For multi-class:

$$\mathcal{L} = -\frac{1}{m} \sum_{i=1}^{m} \sum_{c=1}^{C} y_{i,c} \log(\hat{y}_{i,c})$$

Where $y_{i,c} = 1$ if example $i$ is class $c$, else 0.

## Backpropagation: Training Neural Networks

Backpropagation computes gradients of loss w.r.t. all parameters.

Uses chain rule to propagate errors backward through network.

### Chain Rule Review

If $y = f(g(x))$, then:

$$\frac{dy}{dx} = \frac{dy}{dg} \cdot \frac{dg}{dx}$$

### Backprop Through Single Neuron

For neuron: $a = \sigma(z)$, $z = w^T x + b$

Loss depends on $a$: $\frac{\partial \mathcal{L}}{\partial a}$ (computed from next layer).

Gradient w.r.t. weight:

$$\frac{\partial \mathcal{L}}{\partial w} = \frac{\partial \mathcal{L}}{\partial a} \cdot \frac{\partial a}{\partial z} \cdot \frac{\partial z}{\partial w}$$

$$= \frac{\partial \mathcal{L}}{\partial a} \cdot \sigma'(z) \cdot x$$

Gradient w.r.t. bias:

$$\frac{\partial \mathcal{L}}{\partial b} = \frac{\partial \mathcal{L}}{\partial a} \cdot \sigma'(z)$$

Gradient to pass to previous layer:

$$\frac{\partial \mathcal{L}}{\partial x} = \frac{\partial \mathcal{L}}{\partial a} \cdot \sigma'(z) \cdot w$$

### Full Network Backprop

1. Forward pass: compute all activations through network
2. Compute output loss: $\frac{\partial \mathcal{L}}{\partial a^{[L]}}$
3. For each layer (in reverse):
   - Compute pre-activation gradient: $\frac{\partial \mathcal{L}}{\partial z} = \frac{\partial \mathcal{L}}{\partial a} \cdot g'(z)$
   - Compute weight gradient: $\frac{\partial \mathcal{L}}{\partial W} = \frac{\partial \mathcal{L}}{\partial z} \cdot a^{[prev]}$
   - Compute gradient to previous layer: $\frac{\partial \mathcal{L}}{\partial a^{[prev]}} = W^T \frac{\partial \mathcal{L}}{\partial z}$

### Numeric Example: Update a Single Weight

**Setup**: 2-layer network, MSE loss, one training example.

- Input: $x = 1$, Label: $y = 0.5$
- After forward pass: $\hat{y} = 0.3$
- Current weight in layer 1: $w = 0.4$

**Loss**: $\mathcal{L} = (0.5 - 0.3)^2 = 0.04$

**Backward pass**:

1. Loss gradient w.r.t output: $\frac{\partial \mathcal{L}}{\partial \hat{y}} = 2(0.3 - 0.5) = -0.4$

2. Assume second layer just scales: $\hat{y} = 0.5 \cdot a^{[1]}$

   $\frac{\partial \hat{y}}{\partial a^{[1]}} = 0.5$

3. Gradient to first layer activation: $\frac{\partial \mathcal{L}}{\partial a^{[1]}} = -0.4 \times 0.5 = -0.2$

4. First layer uses ReLU, and $z^{[1]} = 0.8$ (was positive)

   $\frac{\partial a^{[1]}}{\partial z^{[1]}} = 1$ (ReLU derivative)

5. Pre-activation gradient: $\frac{\partial \mathcal{L}}{\partial z^{[1]}} = -0.2 \times 1 = -0.2$

6. Weight gradient: $\frac{\partial \mathcal{L}}{\partial w} = -0.2 \times x = -0.2 \times 1 = -0.2$

**Parameter update** (learning rate $\alpha = 0.01$):

$$w_{\text{new}} = w_{\text{old}} - \alpha \frac{\partial \mathcal{L}}{\partial w} = 0.4 - 0.01 \times (-0.2) = 0.4 + 0.002 = 0.402$$

Weight increased slightly because gradient was negative (loss decreases if weight increases).

## Optimization: Stochastic Gradient Descent

Simple learning rule:

$$\theta \leftarrow \theta - \alpha \frac{\partial \mathcal{L}}{\partial \theta}$$

Where $\theta$ represents all parameters, $\alpha$ is learning rate.

**Stochastic**: Update on single example (or small batch), not full dataset.

**Advantages**:
- Faster (don't need entire dataset for one update)
- Can handle large datasets
- Noisy updates help escape local minima

**Disadvantages**:
- Converges slower than batch gradient descent
- Noisy (may oscillate)
- Requires learning rate tuning

### Modern Optimizers

#### Adam (Adaptive Moment Estimation)

Maintains momentum and adaptive learning rates:

$$m_t = \beta_1 m_{t-1} + (1 - \beta_1) \nabla \theta$$
$$v_t = \beta_2 v_{t-1} + (1 - \beta_2) (\nabla \theta)^2$$

$$\theta \leftarrow \theta - \frac{\alpha}{\sqrt{v_t} + \epsilon} m_t$$

Default: $\beta_1 = 0.9, \beta_2 = 0.999, \epsilon = 10^{-8}$

**Why it works**: Automatically adjusts learning rate per parameter. Steep gradients → smaller effective step. Flat areas → larger step.

#### RMSprop

Simpler variant (uses $v_t$ only):

$$\theta \leftarrow \theta - \frac{\alpha}{\sqrt{v_t}} \nabla \theta$$

## Key Hyperparameters

**Learning rate** $\alpha$: Controls step size. Too large → diverge. Too small → slow.

- Typical range: 0.001 to 0.1
- Start with 0.01, adjust based on training curves

**Batch size**: Number of examples per gradient update.

- Small batch (8-32): Noisy updates, escapes minima
- Large batch (256+): Stable updates, faster per-epoch
- Typical: 32 or 64

**Number of layers**: Network depth.

- Deeper → more capacity, but harder to train
- Typical: 2-4 layers for simple tasks, 10-100+ for complex tasks

**Neurons per layer**: Network width.

- More neurons → more capacity
- Typical: 50-500 per layer

**Activation function**: ReLU most common now (fast, avoids saturation).

## Training Dynamics: Overfitting vs Underfitting

**Underfitting**: Model too simple, poor training performance.

- Solution: add layers, more neurons, train longer

**Overfitting**: Model memorizes training data, poor test performance.

- Solution: regularization, more training data, dropout

### Regularization: L2 (Weight Decay)

Add penalty for large weights to loss:

$$\mathcal{L}_{\text{reg}} = \mathcal{L} + \lambda \sum_{i,j} w_{ij}^2$$

Where $\lambda$ is regularization strength (typical: 0.0001 to 0.01).

Encourages smaller weights, simpler model, better generalization.

### Dropout

Randomly drop neurons during training (set output to 0).

Each neuron has probability $p$ of being dropped (typical: 0.5).

During inference, use all neurons but scale outputs by $(1-p)$.

Prevents co-adaptation (neurons learning to work only with specific other neurons).

## Example: Classification Problem

**Task**: Classify images as cat (1) or dog (0).

**Network**:
- Input: 784 pixels (28×28 image, flattened)
- Hidden 1: 128 neurons, ReLU
- Hidden 2: 64 neurons, ReLU
- Output: 1 neuron, sigmoid (probability)

**Training**:
- Loss: Binary cross-entropy
- Optimizer: Adam
- Batch size: 32
- Learning rate: 0.001
- Epochs: 50

**Pseudocode**:
```
for epoch in 1 to 50:
    for batch in training_data:
        predictions = forward(batch)
        loss = binary_cross_entropy(predictions, labels)
        gradients = backprop(loss)
        update_weights(gradients, learning_rate=0.001)
    validation_loss = evaluate(validation_data)
    print(f"Epoch {epoch}: loss={loss:.4f}, val_loss={validation_loss:.4f}")
```

After 50 epochs, model achieves ~95% accuracy on test set.

## Related Concepts

- [[Backpropagation]] - How networks learn
- [[RNN (Recurrent Neural Network)]] - Networks for sequences
- [[Convolutional Neural Networks]] - Networks for images
- [[Attention Mechanism]] - Networks for selective focus
- [[Calculus for Neural Networks]] - Mathematical foundation

## Summary

Neural networks are layers of differentiable functions.

Each layer applies linear transformation + nonlinear activation.

Backpropagation trains them by computing gradients.

Modern networks use ReLU, Adam optimizer, and dropout.

Key tradeoff: network capacity vs. generalization.
