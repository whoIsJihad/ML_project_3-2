---

# 🔄 Activation Functions, Loss Functions & Optimizers — PyTorch Examples

This note shows **practical examples** of combining different activation functions, loss functions, and optimizers in PyTorch DNNs. Each example is a complete, runnable template.

---

## 📈 EXAMPLE 1: Regression with ReLU + MSE + SGD

```python
import torch
import torch.nn as nn
import torch.optim as optim

# Model with ReLU activations
class RegressionModel(nn.Module):
    def __init__(self):
        super(RegressionModel, self).__init__()
        self.fc1 = nn.Linear(10, 32)
        self.fc2 = nn.Linear(32, 16)
        self.fc3 = nn.Linear(16, 1)

    def forward(self, x):
        x = torch.relu(self.fc1(x))  # ReLU activation
        x = torch.relu(self.fc2(x))  # ReLU activation
        x = self.fc3(x)              # No activation for regression
        return x

# Data
x = torch.randn(100, 10)
y = torch.randn(100, 1) * 10 + 50  # Target values

# Loss: MSE (Mean Squared Error)
criterion = nn.MSELoss()

# Optimizer: SGD (Stochastic Gradient Descent)
optimizer = optim.SGD(model.parameters(), lr=0.01)

# Training
model = RegressionModel()
for epoch in range(10):
    optimizer.zero_grad()
    output = model(x)
    loss = criterion(output, y)
    loss.backward()
    optimizer.step()
    if epoch % 3 == 0:
        print(f"Epoch {epoch} | Loss: {loss.item():.4f}")
```

---

## 📊 EXAMPLE 2: Binary Classification with Sigmoid + BCELoss + Adam

```python
# Model with Sigmoid for binary output
class BinaryModel(nn.Module):
    def __init__(self):
        super(BinaryModel, self).__init__()
        self.fc1 = nn.Linear(20, 64)
        self.fc2 = nn.Linear(64, 1)

    def forward(self, x):
        x = torch.relu(self.fc1(x))     # ReLU hidden
        x = torch.sigmoid(self.fc2(x))  # Sigmoid for binary (0-1)
        return x

# Data
x = torch.randn(100, 20)
y = torch.randint(0, 2, (100, 1)).float()  # Binary labels (0 or 1)

# Loss: BCELoss (Binary Cross Entropy)
criterion = nn.BCELoss()

# Optimizer: Adam
optimizer = optim.Adam(model.parameters(), lr=0.001)

# Training
model = BinaryModel()
for epoch in range(10):
    optimizer.zero_grad()
    output = model(x)
    loss = criterion(output, y)
    loss.backward()
    optimizer.step()
    if epoch % 3 == 0:
        pred = (output > 0.5).float()
        acc = (pred == y).float().mean()
        print(f"Epoch {epoch} | Loss: {loss.item():.4f} | Acc: {acc:.2%}")
```

---

## 🏷️ EXAMPLE 3: Multiclass Classification with Tanh + CrossEntropy + RMSprop

```python
# Model with Tanh activations
class MulticlassModel(nn.Module):
    def __init__(self):
        super(MulticlassModel, self).__init__()
        self.fc1 = nn.Linear(50, 128)
        self.fc2 = nn.Linear(128, 64)
        self.fc3 = nn.Linear(64, 10)  # 10 classes

    def forward(self, x):
        x = torch.tanh(self.fc1(x))  # Tanh activation
        x = torch.tanh(self.fc2(x))  # Tanh activation
        x = self.fc3(x)              # No activation (CrossEntropy handles softmax)
        return x

# Data
x = torch.randn(100, 50)
y = torch.randint(0, 10, (100,))  # Class labels (0-9)

# Loss: CrossEntropyLoss (includes softmax)
criterion = nn.CrossEntropyLoss()

# Optimizer: RMSprop
optimizer = optim.RMSprop(model.parameters(), lr=0.001)

# Training
model = MulticlassModel()
for epoch in range(10):
    optimizer.zero_grad()
    output = model(x)
    loss = criterion(output, y)
    loss.backward()
    optimizer.step()
    if epoch % 3 == 0:
        pred = torch.argmax(output, dim=1)
        acc = (pred == y).float().mean()
        print(f"Epoch {epoch} | Loss: {loss.item():.4f} | Acc: {acc:.2%}")
```

---

## 🔄 EXAMPLE 4: Regression with Leaky ReLU + L1Loss + Adam

```python
import torch.nn.functional as F

# Model with Leaky ReLU
class LeakyRegressionModel(nn.Module):
    def __init__(self):
        super(LeakyRegressionModel, self).__init__()
        self.fc1 = nn.Linear(15, 64)
        self.fc2 = nn.Linear(64, 32)
        self.fc3 = nn.Linear(32, 1)

    def forward(self, x):
        x = F.leaky_relu(self.fc1(x), 0.01)  # Leaky ReLU
        x = F.leaky_relu(self.fc2(x), 0.01)  # Leaky ReLU
        x = self.fc3(x)
        return x

# Data
x = torch.randn(100, 15)
y = torch.randn(100, 1) * 5 + 100

# Loss: L1Loss (Mean Absolute Error - robust to outliers)
criterion = nn.L1Loss()

# Optimizer: Adam
optimizer = optim.Adam(model.parameters(), lr=0.001)

# Training
model = LeakyRegressionModel()
for epoch in range(10):
    optimizer.zero_grad()
    output = model(x)
    loss = criterion(output, y)
    loss.backward()
    optimizer.step()
    if epoch % 3 == 0:
        print(f"Epoch {epoch} | Loss: {loss.item():.4f}")
```

---

## 🎯 EXAMPLE 5: Binary Classification with ELU + BCELoss + SGD

```python
# Model with ELU activations
class ELUBinaryModel(nn.Module):
    def __init__(self):
        super(ELUBinaryModel, self).__init__()
        self.fc1 = nn.Linear(25, 128)
        self.fc2 = nn.Linear(128, 64)
        self.fc3 = nn.Linear(64, 1)

    def forward(self, x):
        x = F.elu(self.fc1(x))        # ELU activation
        x = F.elu(self.fc2(x))        # ELU activation
        x = torch.sigmoid(self.fc3(x)) # Sigmoid for binary
        return x

# Data
x = torch.randn(100, 25)
y = torch.randint(0, 2, (100, 1)).float()

# Loss: BCELoss
criterion = nn.BCELoss()

# Optimizer: SGD with momentum
optimizer = optim.SGD(model.parameters(), lr=0.01, momentum=0.9)

# Training
model = ELUBinaryModel()
for epoch in range(10):
    optimizer.zero_grad()
    output = model(x)
    loss = criterion(output, y)
    loss.backward()
    optimizer.step()
    if epoch % 3 == 0:
        pred = (output > 0.5).float()
        acc = (pred == y).float().mean()
        print(f"Epoch {epoch} | Loss: {loss.item():.4f} | Acc: {acc:.2%}")
```

---

## 📋 COMBINATION CHEAT SHEET

| Problem Type | Activation (Hidden) | Activation (Output) | Loss Function | Optimizer |
|--------------|---------------------|---------------------|---------------|-----------|
| Regression | ReLU, Tanh, Leaky ReLU | None | MSELoss, L1Loss | SGD, Adam |
| Binary Classification | ReLU, Tanh, ELU | Sigmoid | BCELoss | Adam, SGD |
| Multiclass Classification | ReLU, Tanh, Leaky ReLU | None | CrossEntropyLoss | Adam, RMSprop |

---

## ⚙️ OPTIMIZER HYPERPARAMETERS

```python
# SGD variants
optim.SGD(model.parameters(), lr=0.01)                    # Basic
optim.SGD(model.parameters(), lr=0.01, momentum=0.9)     # With momentum
optim.SGD(model.parameters(), lr=0.01, weight_decay=1e-4) # With L2 regularization

# Adam variants
optim.Adam(model.parameters(), lr=0.001)                 # Default
optim.Adam(model.parameters(), lr=0.001, weight_decay=1e-4) # With L2

# RMSprop
optim.RMSprop(model.parameters(), lr=0.001, alpha=0.9)  # Default alpha=0.99 usually
```

---

## 💡 WHEN TO USE WHAT

- **ReLU**: Default choice, fast, prevents vanishing gradients
- **Tanh**: When you need outputs between -1 and 1, smoother than ReLU
- **Leaky ReLU**: When ReLU causes "dying neurons" (all zeros)
- **ELU**: Smooth alternative to ReLU, can be better for some problems
- **Sigmoid**: Only for binary classification output
- **Softmax**: Built into CrossEntropyLoss, don't use manually

- **MSELoss**: Standard regression
- **L1Loss**: Regression when you want robustness to outliers
- **BCELoss**: Binary classification with sigmoid
- **CrossEntropyLoss**: Multiclass classification (includes softmax)

- **SGD**: Simple, reliable, good for convex problems
- **Adam**: Usually best, adaptive learning rates
- **RMSprop**: Good for RNNs, less common for FNNs

---

Copy any example above and modify the layer sizes, data shapes, and hyperparameters for your specific problem!

---</content>
<parameter name="filePath">/mnt/Data/3-2/330 (ML lab)/Online 2/cheatsheets/activation_loss_optimizer_examples.md