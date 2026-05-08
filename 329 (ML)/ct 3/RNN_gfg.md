## Recurrent Neural Networks (RNNs)

**Last Updated:** February 7, 2026

## Overview

Recurrent Neural Networks (RNNs) are a class of neural networks specifically designed to process sequential data by retaining information from previous steps. They excel in tasks where context and temporal order are critical.

**Key Characteristics:**
- Designed for sequential and temporal data processing
- Maintains memory of past inputs through hidden states
- Widely used in NLP, time-series forecasting, and speech recognition

## Intuition: How RNNs Remember

Imagine reading a sentence and trying to predict the next word. You don't rely solely on the current word—you remember the context from previous words. RNNs work similarly by "remembering" past information and using it to make better predictions at each step.

**Key Advantage:** This memory of previous steps allows the network to understand context and capture long-range dependencies within sequential data.

---

## Key Components of RNNs

### 1. Recurrent Neurons

The fundamental processing unit in an RNN is a **recurrent neuron** (or recurrent unit). These units maintain a hidden state that carries information about previous inputs in the sequence. By feeding back their output as input to themselves, recurrent neurons can "remember" information from prior steps and capture temporal dependencies.

### 2. RNN Unfolding (Unrolling)

RNN unfolding is the process of expanding the recurrent structure over multiple time steps. Each step in the sequence is represented as a separate layer, which visualizes how information flows across time.

#### Why Unfolding Matters:  


This representation enables Backpropagation Through Time (BPTT), a learning algorithm that propagates errors backward through time steps, allowing the network to learn temporal dependencies effectively.

![[Pasted image 20260225222552.png]]
---

## RNN Architecture

RNNs share similarities with other deep learning architectures in their input/output structure, but differ fundamentally in how information flows. While traditional neural networks have distinct weight matrices for each layer, **RNNs share weights across time steps**, enabling them to maintain memory over sequences.

### Core Components

For each input $X_t$, the network computes a hidden state $h_t$ to retain sequential dependencies. The computations follow these fundamental equations:

#### 1. Hidden State Calculation

$$h_t = \sigma(U \cdot X_t + W \cdot h_{t-1} + B)$$

where:
- $h_t$ = current hidden state
- $U$ = weight matrix for input
- $W$ = weight matrix for recurrence (previous hidden state)
- $B$ = bias vector
- $\sigma$ = activation function (typically $\tanh$ or ReLU)

#### 2. Output Calculation

$$Y_t = O(V \cdot h_t + C)$$

where:
- $Y_t$ = output at time step $t$
- $V$ = output weight matrix
- $C$ = output bias
- $O$ = output activation function (softmax for classification, linear for regression)

#### 3. Overall Function

$$Y_t = f(X_t, h_t, W, U, V, B, C)$$

This equation encapsulates the entire RNN operation, where the state matrix $S$ holds each element $s_i$ representing the network's state at each time step $i$.

---

## How RNNs Work: Forward Pass

At each time step, RNNs process inputs through recurrent units with fixed activation functions. Each unit maintains a hidden state that acts as **memory**, retaining information from previous time steps and allowing the network to learn from sequential context.

### Hidden State Updates

The current hidden state $h_t$ depends on both the previous state $h_{t-1}$ and the current input $x_t$:

#### 1. State Update Function

$$h_t = f(h_{t-1}, x_t)$$

where:
- $h_t$ = current hidden state
- $h_{t-1}$ = previous hidden state
- $x_t$ = input at the current time step

#### 2. Activation with Weights

$$h_t = \tanh(W_{hh} \cdot h_{t-1} + W_{xh} \cdot x_t)$$

where:
- $W_{hh}$ = weight matrix for recurrent connections (previous hidden state)
- $W_{xh}$ = weight matrix for input connections

#### 3. Output Generation

$$y_t = W_{hy} \cdot h_t$$

where:
- $y_t$ = output at time step $t$
- $W_{hy}$ = weight matrix from hidden to output layer

**Training:** These parameters are updated using an advanced variant of backpropagation called **Backpropagation Through Time (BPTT)**, which accounts for the sequential nature of RNNs. 

---

## Backpropagation Through Time (BPTT)

![[Pasted image 20260225222620.png]]
Since RNNs process sequential data, we cannot use standard backpropagation. Instead, we use **Backpropagation Through Time (BPTT)**, which unrolls the network across time steps and propagates gradients backward through them.

### Dependency Chain

The loss function $L(\theta)$ is computed from the final hidden state, and each hidden state depends on its predecessors, forming a chain:

$$h_3 \text{ depends on } h_2, \quad h_2 \text{ depends on } h_1, \quad h_1 \text{ depends on } h_0$$

### Gradient Computation

#### 1. Basic Gradient Formula

$$\frac{\partial L(\theta)}{\partial W} = \frac{\partial L(\theta)}{\partial h_T} \cdot \frac{\partial h_T}{\partial W}$$

#### 2. Dependencies Through Layers

For a sequence with hidden states $h_3$:

$$h_3 = \sigma(W \cdot h_2 + b)$$

The gradient must account for dependencies from previous hidden states, requiring us to trace back through all time steps.

#### 3. Complete Gradient Through Time

$$\frac{\partial h_T}{\partial W} = \frac{\partial h_T}{\partial W} + \frac{\partial h_T}{\partial h_{T-1}} \cdot \frac{\partial h_{T-1}}{\partial W}$$

#### 4. Final Loss Derivative

$$\frac{\partial L(\theta)}{\partial W} = \frac{\partial L(\theta)}{\partial h_T} \cdot \sum_{k=1}^{T} \frac{\partial h_T}{\partial h_k} \cdot \frac{\partial h_k}{\partial W}$$

**Key Terms:**
- **$\theta$ (theta):** Represents **all network parameters** — the complete set of weights and biases: $\theta = \{W, U, V, B, C\}$
- **$W$:** The **recurrent weight matrix** connecting the previous hidden state $h_{t-1}$ to the current hidden state $h_t$. It's one specific component of $\theta$.

**Interpretation:** This equation computes the gradient of the total loss with respect to the recurrent weight matrix $W$. The summation traces how changes to $W$ affect the loss through all previous time steps, capturing the complete chain of dependencies. This is why it's called "Backpropagation **Through Time**" — gradients flow backward across all time steps to determine how $W$ impacts the final loss.

---

## Types of RNNs

RNNs are categorized based on the structure of their inputs and outputs. Here are the four major types:

### 1. One-to-One RNN

**Single input → Single output**

The simplest RNN architecture used for straightforward classification tasks where no sequential data is involved (e.g., binary classification).

![[Pasted image 20260225222630.png]]
### 2. One-to-Many RNN
![[Pasted image 20260225222643.png]]
**Single input → Sequence of outputs**

The network processes a single input to produce multiple outputs over time. Useful when one input triggers a sequence of predictions.

**Example:** Image captioning—a single image generates a sequence of words describing it.

### 3. Many-to-One RNN
![[Pasted image 20260225222650.png]]
**Sequence of inputs → Single output**

The network receives a sequence of inputs and produces a single output. Ideal when you need to aggregate information from an entire sequence.

**Example:** Sentiment analysis—a sequence of words (sentence) produces a single sentiment label (positive/negative/neutral).

### 4. Many-to-Many RNN
![[Pasted image 20260225222657.png]]
**Sequence of inputs → Sequence of outputs**

The network processes a sequence of inputs and generates a sequence of outputs. Common in tasks requiring parallel transformations.
**Example:** Machine translation—a sequence of words in one language translates to a sequence of words in another language.

---

## Variants of RNNs

Several RNN variants have been developed to address specific challenges or optimize for particular tasks:

### 1. Vanilla RNN

The simplest form of RNN, consisting of a single hidden layer with weights shared across time steps.

**Strengths:** Simple to implement and understand

**Limitations:** 
- Struggles with long sequences due to the **vanishing gradient problem**
- Difficulty learning long-term dependencies
- Limited to short-range context

### 2. Bidirectional RNNs

Process the input sequence in both forward and backward directions, capturing context from both past and future.

**Advantages:**
- Accesses both left and right context for each time step
- Improves performance on complete sequences
- Ideal when the entire sequence is available

**Best For:** Named entity recognition, question answering, machine translation

### 3. Long Short-Term Memory Networks (LSTMs)

LSTMs introduce a sophisticated memory mechanism to overcome the vanishing gradient problem through **gated architecture**.

**Key Gates:**
- **Input Gate:** Controls how much new information enters the cell state
- **Forget Gate:** Decides which past information to discard
- **Output Gate:** Regulates what information to output at the current step

**Advantages:**
- Captures long-term dependencies effectively
- Handles sequences of varying lengths
- Stable gradient flow through gates

**Best For:** Language modeling, machine translation, speech recognition

### 4. Gated Recurrent Units (GRUs)

A simplified alternative to LSTMs that combines the input and forget gates into a single update gate.

**Key Differences from LSTM:**
- Two gates instead of three (fewer parameters to train)
- Computationally more efficient
- Often performs comparably to LSTMs

**Best For:** Tasks where computational efficiency and simplicity are valued

---

## RNNs vs Feedforward Neural Networks

| Aspect | **Feedforward Neural Networks (FFNNs)** | **Recurrent Neural Networks (RNNs)** |
|--------|----------------------------------------|-------------------------------------|
| **Data Flow** | Single direction: input → output | Includes feedback loops; information cycles |
| **Memory** | No memory of previous inputs | Maintains hidden state across time steps |
| **Purpose** | Tasks with independent data points | Sequential and time-dependent data |
| **Best For** | Image classification, static tasks | Text, time-series, speech, video |
| **Context** | Each input processed independently | Each step informed by previous steps |
| **Architecture** | Distinct weights per layer | Shared weights across time steps |

---

## Practical Implementation: Character-Based Text Generator

Let's build a character-based text generator using a simple RNN in TensorFlow and Keras. This example demonstrates how RNNs learn patterns from sequences and generate new text.

### Step 1: Import Libraries

```python
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import SimpleRNN, Dense
```

### Step 2: Define Input Text and Create Character Encoding

```python
text = "This is GeeksforGeeks a software training institute"
chars = sorted(list(set(text)))
char_to_index = {char: i for i, char in enumerate(chars)}
index_to_char = {i: char for i, char in enumerate(chars)}
```

We create mappings to convert characters to indices and back, enabling the model to process text.

### Step 3: Create Sequences and Labels

```python
seq_length = 3
sequences = []
labels = []

for i in range(len(text) - seq_length):
    seq = text[i:i + seq_length]
    label = text[i + seq_length]
    sequences.append([char_to_index[char] for char in seq])
    labels.append(char_to_index[label])

X = np.array(sequences)
y = np.array(labels)
```

We create training pairs: fixed-length sequences (input) and the following character (target label).

### Step 4: One-Hot Encoding

```python
X_one_hot = tf.one_hot(X, len(chars))
y_one_hot = tf.one_hot(y, len(chars))
```

Convert sequences and labels to one-hot encoding for neural network training.

### Step 5: Build the RNN Model

```python
model = Sequential()
model.add(SimpleRNN(50, input_shape=(seq_length, len(chars)), activation='relu'))
model.add(Dense(len(chars), activation='softmax'))
```

**Architecture:**
- **SimpleRNN layer:** 50 hidden units with ReLU activation
- **Dense layer:** Output size equals number of unique characters with softmax (for probability distribution)

### Step 6: Compile and Train

```python
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
model.fit(X_one_hot, y_one_hot, epochs=100)
```

Train the model to predict the next character given a sequence.

### Step 7: Generate New Text

```python
start_seq = "This is G"
generated_text = start_seq

for i in range(50):
    x = np.array([[char_to_index[char] for char in generated_text[-seq_length:]]])
    x_one_hot = tf.one_hot(x, len(chars))
    prediction = model.predict(x_one_hot)
    next_index = np.argmax(prediction)
    next_char = index_to_char[next_index]
    generated_text += next_char

print("Generated Text:")
print(generated_text)
```

**Process:** 
1. Start with a seed sequence
2. Predict the next character using the last $\text{seq\_length}$ characters
3. Append the predicted character to the generated text
4. Repeat until desired length is reached

---

## Advantages and Strengths

- **Sequential Memory:** RNNs retain information from previous inputs, making them ideal for time-series predictions where past data significantly influences future outcomes.

- **Enhanced Pixel Neighborhoods:** RNNs can be combined with convolutional layers to capture extended spatial and temporal neighborhoods, improving performance in image and video processing tasks.

- **Flexible Architecture:** Support for different configurations (one-to-one, many-to-one, one-to-many, many-to-many) enables diverse applications.

---

## Limitations and Challenges

While RNNs excel at handling sequential data, they face significant training challenges:

### 1. Vanishing Gradient Problem

During backpropagation through time, gradients exponentially diminish as they propagate backward through time steps:

$$\frac{\partial L}{\partial W} \rightarrow 0 \text{ as } T \rightarrow \infty$$

**Consequences:**
- Minimal weight updates in early time steps
- Network fails to learn long-term dependencies
- Critical for tasks like language translation where distant context matters

### 2. Exploding Gradient Problem

Conversely, gradients can grow exponentially, causing unstable training:

$$\frac{\partial L}{\partial W} \rightarrow \infty$$

**Consequences:**
- Excessively large weight updates
- Training destabilization and NaN values
- Network fails to converge

**Mitigation:** Gradient clipping limits gradient values to a maximum threshold.

### 3. Computational Complexity

- BPTT requires unrolling the entire sequence, consuming significant memory
- Training is slower compared to feedforward networks
- Difficult to parallelize across time steps

---

## Real-World Applications

RNNs are deployed across numerous domains where sequential or temporal data is fundamental:

| **Domain** | **Application** | **Task** |
|-----------|-----------------|---------|
| **Time-Series** | Stock market prediction | Forecasting future prices |
| **Time-Series** | Weather forecasting | Predicting atmospheric conditions |
| **NLP** | Language modeling | Predicting next word/character |
| **NLP** | Sentiment analysis | Classifying text emotion |
| **NLP** | Machine translation | Translating between languages |
| **Speech** | Speech-to-text | Converting audio to text |
| **Speech** | Voice recognition | Identifying speakers |
| **Video** | Action recognition | Classifying actions in video |
| **Video** | Gesture recognition | Identifying hand/body gestures |
| **Video** | Video captioning | Generating descriptions for videos |

---

## Summary

Recurrent Neural Networks represent a fundamental breakthrough in processing sequential data. Their ability to maintain memory through hidden states and share weights across time steps enables them to capture temporal dependencies that traditional feedforward networks cannot. While they face challenges like vanishing/exploding gradients, advanced variants like LSTMs and GRUs have largely overcome these limitations, making RNNs indispensable in modern deep learning applications.