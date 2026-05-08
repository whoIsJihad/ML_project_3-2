
---

# ✅ PyTorch Fully Connected Neural Network (DNN) — Complete Exam Template

```python
import torch
import torch.nn as nn
import torch.optim as optim

# -------------------------------
# Hyperparameters
# -------------------------------
INPUT_SIZE = 10      # number of features
HIDDEN1 = 32         # first hidden layer neurons
HIDDEN2 = 16         # second hidden layer neurons
OUTPUT_SIZE = 1      # output dimension
LR = 0.01            # learning rate
EPOCHS = 20          # number of training epochs

# -------------------------------
# Sample Data (replace with your own)
# -------------------------------
x = torch.randn(64, INPUT_SIZE)  # batch of 64 samples
y = torch.randn(64, OUTPUT_SIZE) # target values

# -------------------------------
# Model Definition
# -------------------------------
class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.fc1 = nn.Linear(INPUT_SIZE, HIDDEN1)
        self.fc2 = nn.Linear(HIDDEN1, HIDDEN2)
        self.fc3 = nn.Linear(HIDDEN2, OUTPUT_SIZE)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        x = self.fc3(x)
        return x

model = Net()

# -------------------------------
# Loss and Optimizer
# -------------------------------
criterion = nn.MSELoss()           # for regression
# criterion = nn.CrossEntropyLoss() # for classification
optimizer = optim.SGD(model.parameters(), lr=LR)
# optimizer = optim.Adam(model.parameters(), lr=LR)

# -------------------------------
# Training Loop
# -------------------------------
for epoch in range(EPOCHS):
    optimizer.zero_grad()           # reset gradients

    output = model(x)               # forward pass
    loss = criterion(output, y)    # compute loss

    loss.backward()                 # backward pass
    optimizer.step()                # update weights

    # Print progress
    print(f"Epoch {epoch+1}/{EPOCHS} | Loss: {loss.item():.4f}")
```

---

## ⚡ Quick Notes for Exam

1. **Activation**: `torch.relu(...)` between hidden layers.
2. **Loss**: MSE for regression, CrossEntropy for classification.
3. **Optimizer**: SGD or Adam — same training loop.
4. **Zero gradients**: Always `optimizer.zero_grad()` before backward pass.
5. **Batch**: `x` shape = `(batch_size, INPUT_SIZE)`
6. **Output**: Matches `y` shape `(batch_size, OUTPUT_SIZE)`

---

##   SCENARIO 1: Binary Classification (Predict 0 or 1)

```python
# Problem: Predict if email is spam (0) or not (1)

INPUT_SIZE = 20      # 20 features from email
HIDDEN1 = 64         # wider hidden layer
OUTPUT_SIZE = 1      # binary output

class BinaryNet(nn.Module):
    def __init__(self):
        super(BinaryNet, self).__init__()
        self.fc1 = nn.Linear(INPUT_SIZE, HIDDEN1)
        self.fc2 = nn.Linear(HIDDEN1, OUTPUT_SIZE)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.sigmoid(self.fc2(x))  # ⭐ SIGMOID for binary (outputs 0-1)
        return x

# Data:
x_binary = torch.randn(100, INPUT_SIZE)
y_binary = torch.randint(0, 2, (100, 1)).float()  # labels: 0 or 1

# Loss and Training:
model = BinaryNet()
criterion = nn.BCELoss()  # ⭐ Binary Cross Entropy
optimizer = optim.Adam(model.parameters(), lr=0.001)

for epoch in range(20):
    optimizer.zero_grad()
    output = model(x_binary)
    loss = criterion(output, y_binary)
    loss.backward()
    optimizer.step()
    if (epoch+1) % 5 == 0:
        print(f"Epoch {epoch+1} | Loss: {loss.item():.4f}")
```

---

##   SCENARIO 2: Multiclass Classification (Predict 0, 1, 2, or 3)

```python
# Problem: Classify handwritten digits (0-9)
# OR classify iris flower type (0, 1, 2)

NUM_CLASSES = 3      # if iris: 3 classes. if mnist: 10 classes
INPUT_SIZE = 50      # features
HIDDEN1 = 128        # deep and wide for complex data
HIDDEN2 = 64

class MulticlassNet(nn.Module):
    def __init__(self):
        super(MulticlassNet, self).__init__()
        self.fc1 = nn.Linear(INPUT_SIZE, HIDDEN1)
        self.fc2 = nn.Linear(HIDDEN1, HIDDEN2)
        self.fc3 = nn.Linear(HIDDEN2, NUM_CLASSES)  # output = number of classes

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        x = self.fc3(x)  # NO activation here. Loss applies softmax internally
        return x

# Data:
x_multi = torch.randn(100, INPUT_SIZE)
y_multi = torch.randint(0, NUM_CLASSES, (100,))  # labels: 0, 1, 2, ..., NUM_CLASSES-1

# Loss and Training:
model = MulticlassNet()
criterion = nn.CrossEntropyLoss()  # ⭐ Handles softmax + cross entropy
optimizer = optim.Adam(model.parameters(), lr=0.001)

for epoch in range(20):
    optimizer.zero_grad()
    output = model(x_multi)  # shape: (100, 3)
    loss = criterion(output, y_multi)
    loss.backward()
    optimizer.step()
    if (epoch+1) % 5 == 0:
        pred = torch.argmax(output, dim=1)  # pick highest class
        accuracy = (pred == y_multi).float().mean()
        print(f"Epoch {epoch+1} | Loss: {loss.item():.4f} | Acc: {accuracy:.2%}")
```

---

## SCENARIO 3: Regression (Predict Continuous Values)

```python
# Problem: Predict house price based on features
# Output can be any real number (not just 0-1 or class label)

INPUT_SIZE = 15      # features: size, rooms, age, etc.
OUTPUT_SIZE = 1      # one continuous output: price

class RegressionNet(nn.Module):
    def __init__(self):
        super(RegressionNet, self).__init__()
        self.fc1 = nn.Linear(INPUT_SIZE, 64)
        self.fc2 = nn.Linear(64, 32)
        self.fc3 = nn.Linear(32, OUTPUT_SIZE)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        x = self.fc3(x)  # NO activation. Output can be any value
        return x

# Data:
x_reg = torch.randn(100, INPUT_SIZE)
y_reg = torch.randn(100, 1) * 100 + 300000  # prices between 200k-400k

# Loss and Training:
model = RegressionNet()
criterion = nn.MSELoss()  # ⭐ Mean Squared Error for regression
optimizer = optim.Adam(model.parameters(), lr=0.01)

for epoch in range(20):
    optimizer.zero_grad()
    output = model(x_reg)
    loss = criterion(output, y_reg)
    loss.backward()
    optimizer.step()
    if (epoch+1) % 5 == 0:
        print(f"Epoch {epoch+1} | Loss: {loss.item():.0f}")
```

---

## 🧠 DIFFERENT ACTIVATIONS (When to Use)

```python
# ┌─────────────────────────────────────────────┐
# │ Activation Function Cheat Sheet              │
# └─────────────────────────────────────────────┘

# 1. ReLU (Rectified Linear Unit) — MOST COMMON
x = torch.randn(5)
y = torch.relu(x)  # If x < 0 → 0, else x
# Use: Hidden layers (most popular)

# 2. Sigmoid — for binary classification only
y = torch.sigmoid(x)  # Output between 0 and 1
# Use: Last layer for binary classification

# 3. Tanh — smoother than ReLU
y = torch.tanh(x)  # Output between -1 and 1
# Use: Hidden layers (alternative to ReLU)

# 4. Softmax — for multiclass classification
y = torch.softmax(x, dim=1)  # Converts to probabilities, sum=1
# Use: Already built into CrossEntropyLoss, don't apply manually

# 5. Leaky ReLU — improved ReLU
y = torch.nn.functional.leaky_relu(x, negative_slope=0.01)
# Use: Hidden layers (when ReLU doesn't work well)

# 6. ELU (Exponential Linear Unit)
y = torch.nn.functional.elu(x)
# Use: Hidden layers (smooth alternative)

# ┌─────────────────────────────────────────────┐
# │ Quick Decision:                              │
# │ Hidden layers? → ReLU                        │
# │ Binary output? → Sigmoid                     │
# │ Multiclass output? → None (loss handles it)  │
# └─────────────────────────────────────────────┘
```

---

## ⚖️ HIGH DEPTH vs HIGH WIDTH

```python
# WIDE but SHALLOW (Few layers, many neurons)
class WideNet(nn.Module):
    def __init__(self):
        super(WideNet, self).__init__()
        self.fc1 = nn.Linear(50, 1024)     # VERY WIDE
        self.fc2 = nn.Linear(1024, 512)    # VERY WIDE
        self.fc3 = nn.Linear(512, 10)      # output
        # Only 3 layers (shallow)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        return self.fc3(x)

# DEEP but NARROW (Many layers, few neurons)
class DeepNet(nn.Module):
    def __init__(self):
        super(DeepNet, self).__init__()
        # 10 layers! (deep)
        self.fc1 = nn.Linear(50, 128)
        self.fc2 = nn.Linear(128, 128)
        self.fc3 = nn.Linear(128, 128)
        self.fc4 = nn.Linear(128, 128)
        self.fc5 = nn.Linear(128, 128)
        self.fc6 = nn.Linear(128, 128)
        self.fc7 = nn.Linear(128, 128)
        self.fc8 = nn.Linear(128, 128)
        self.fc9 = nn.Linear(128, 128)
        self.fc10 = nn.Linear(128, 10)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        x = torch.relu(self.fc3(x))
        x = torch.relu(self.fc4(x))
        x = torch.relu(self.fc5(x))
        x = torch.relu(self.fc6(x))
        x = torch.relu(self.fc7(x))
        x = torch.relu(self.fc8(x))
        x = torch.relu(self.fc9(x))
        return self.fc10(x)

# ┌────────────────────────────────────────────────┐
# │ WIDE (Few, Big Layers)                         │
# │ ✓ Easier to train                              │
# │ ✗ May forget information from early layers     │
# │ Use: Simple problems (linear separable)        │
# └────────────────────────────────────────────────┘

# ┌────────────────────────────────────────────────┐
# │ DEEP (Many, Thin Layers)                       │
# │ ✓ Learns hierarchical features                 │
# │ ✗ Harder to train (vanishing gradients)        │
# │ Use: Complex problems (images, NLP)            │
# └────────────────────────────────────────────────┘

# RULE OF THUMB:
# - Start with 2-3 hidden layers
# - Increase depth for complex data (images, sequences)
# - Increase width if model underfits
```

---

## 📊 SOFTMAX EXPLAINED (For Multiclass)

```python
# What is Softmax? It converts raw scores to probabilities

import torch.nn.functional as F

# Raw scores from neural network (logits)
logits = torch.tensor([[2.0, 1.0, 0.1],  # sample 1
                        [0.5, 2.0, 0.3]]) # sample 2

# Apply softmax
probabilities = F.softmax(logits, dim=1)
print(probabilities)
# Output: tensor([[0.6590, 0.2424, 0.0986],
#                  [0.0900, 0.8066, 0.1034]])

# Each row sums to 1.0 (valid probability distribution)
print(probabilities.sum(dim=1))  # tensor([1.0000, 1.0000])

# Get predicted class (highest probability)
predicted_classes = torch.argmax(probabilities, dim=1)
print(predicted_classes)  # tensor([0, 1])

# ⭐ IMPORTANT: nn.CrossEntropyLoss applies softmax internally!
# Do NOT apply softmax manually before CrossEntropyLoss

# WRONG:
# logits = model(x)
# probs = F.softmax(logits, dim=1)  # ❌ Don't do this
# loss = nn.CrossEntropyLoss()(probs, y)

# RIGHT:
# logits = model(x)
# loss = nn.CrossEntropyLoss()(logits, y)  # ✓ Loss applies softmax internally

# Why? For numerical stability and efficiency - loss functions can do more than just "calculate loss"!
```

---

## 🔗 ACTIVATION FUNCTION DECISION TREE

```
┌─ What is your problem?
│
├─ CLASSIFICATION (predict label/class)
│  │
│  ├─ Binary (0 or 1)?
│  │  ├─ Last Layer: Sigmoid
│  │  ├─ Loss: BCELoss
│  │  └─ Hidden: ReLU
│  │
│  └─ Multiclass (0, 1, 2, ...)?
│     ├─ Last Layer: None (CrossEntropyLoss handles it)
│     ├─ Loss: CrossEntropyLoss
│     └─ Hidden: ReLU
│
└─ REGRESSION (predict continuous number)
   ├─ Last Layer: None (no activation)
   ├─ Loss: MSELoss
   └─ Hidden: ReLU
```

---

## 📋 LOSS FUNCTION QUICK REFERENCE

```python
# 1. Binary Classification
criterion = nn.BCELoss()  # Binary Cross Entropy
# Use with: Sigmoid activation on last layer

# 2. Multiclass Classification
criterion = nn.CrossEntropyLoss()  # Cross Entropy
# Use with: NO activation on last layer (loss applies softmax)

# 3. Regression
criterion = nn.MSELoss()  # Mean Squared Error
# Use with: NO activation on last layer

# 4. Regression (Robust to outliers)
criterion = nn.L1Loss()  # Mean Absolute Error
# Use with: NO activation on last layer

# Least common (not needed for 330):
# criterion = nn.NLLLoss()  # Negative Log Likelihood
# criterion = nn.KLDivLoss()  # Kullback-Leibler Divergence
```

---

## 🎮 OPTIMIZER QUICK REFERENCE

```python
# Both work the same in training loop. Pick one:

# 1. SGD (Stochastic Gradient Descent)
optimizer = optim.SGD(model.parameters(), lr=0.01)
# Simple, reliable, slower sometimes

# 2. Adam (Adaptive Moment Estimation) — usually better
optimizer = optim.Adam(model.parameters(), lr=0.001)
# Adaptive, usually converges faster, default choice

# 3. RMSprop
optimizer = optim.RMSprop(model.parameters(), lr=0.001)
# Less common, middle ground

# Learning rates: 
# - SGD: usually 0.01 or 0.1
# - Adam: usually 0.001 or 0.0001 (smaller!)
```

---

## 💡 COMMON MISTAKES (Don't Do These)

```python
# ❌ WRONG: Forgetting optimizer.zero_grad()
for epoch in range(EPOCHS):
    output = model(x)
    loss = criterion(output, y)
    loss.backward()
    optimizer.step()  # Gradients accumulate! Very wrong!

# ✓ RIGHT:
for epoch in range(EPOCHS):
    optimizer.zero_grad()  # Clear old gradients
    output = model(x)
    loss = criterion(output, y)
    loss.backward()
    optimizer.step()

# ❌ WRONG: Applying softmax before CrossEntropyLoss
output = model(x)
probs = F.softmax(output, dim=1)
loss = nn.CrossEntropyLoss()(probs, y)  # Double softmax!

# ✓ RIGHT:
output = model(x)
loss = nn.CrossEntropyLoss()(output, y)  # Loss does softmax

# ❌ WRONG: Sigmoid activation on multiclass output
self.fc_out = nn.Linear(64, 10)
x = torch.sigmoid(self.fc_out(x))  # Wrong for multiclass

# ✓ RIGHT:
self.fc_out = nn.Linear(64, 10)
x = self.fc_out(x)  # No activation, let loss handle it

# ❌ WRONG: MSELoss for classification
criterion = nn.MSELoss()  # For continuous values!

# ✓ RIGHT:
criterion = nn.CrossEntropyLoss()  # For classification
```

---

This is **everything you need** for Online-2 **FNN code-completion**.
You just need to:

* Copy the scenario that matches your problem
* Adjust layer sizes and data shape
* Change activation/loss if needed
* Run the training loop

---
