# 🏗️ Sequential, BatchNorm & Dropout — PyTorch Essentials

**Master these 3 fundamental building blocks of modern neural networks**

---

## 🎯 **Overview**

These three concepts are the **foundation** of modern PyTorch models:

| Concept | Purpose | When to Use |
|---------|---------|-------------|
| **Sequential** | Clean model building | Simple linear architectures |
| **BatchNorm** | Stabilize training | Almost always (except very small networks) |
| **Dropout** | Prevent overfitting | Training phase only |

---

## 1️⃣ **Sequential — Clean Model Building**

### **What is nn.Sequential?**

**Sequential** is PyTorch's way to **stack layers linearly**. Instead of manually defining `forward()`, you just list layers in order.

### **Without Sequential (Manual)**
```python
class ManualModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc1 = nn.Linear(784, 128)
        self.relu1 = nn.ReLU()
        self.fc2 = nn.Linear(128, 64)
        self.relu2 = nn.ReLU()
        self.fc3 = nn.Linear(64, 10)
    
    def forward(self, x):
        x = self.relu1(self.fc1(x))
        x = self.relu2(self.fc2(x))
        x = self.fc3(x)
        return x
```

### **With Sequential (Clean)**
```python
model = nn.Sequential(
    nn.Linear(784, 128),  # Input: 784 → Output: 128
    nn.ReLU(),            # Activation
    nn.Linear(128, 64),   # 128 → 64
    nn.ReLU(),            # Activation
    nn.Linear(64, 10)     # 64 → 10 (output classes)
)
```

**That's it!** Sequential handles the `forward()` pass automatically.

### **Why Sequential?**
- ✅ **Cleaner code**: No manual forward pass
- ✅ **Less boilerplate**: No need for `__init__` layer assignments
- ✅ **Easy debugging**: Layers execute in order
- ✅ **Perfect for**: Simple feedforward networks

### **Advanced Sequential Usage**
```python
# With BatchNorm and Dropout
model = nn.Sequential(
    nn.Linear(784, 128),
    nn.BatchNorm1d(128),    # Normalize activations
    nn.ReLU(),
    nn.Dropout(0.2),        # Drop 20% of neurons
    
    nn.Linear(128, 64),
    nn.BatchNorm1d(64),
    nn.ReLU(),
    nn.Dropout(0.2),
    
    nn.Linear(64, 10)
)
```

---

## 2️⃣ **BatchNorm — Normalize Activations**

### **What is Batch Normalization?**

**BatchNorm** **normalizes layer outputs** to stabilize training. It makes training faster and more reliable.

### **The Problem Without BatchNorm**

Neural networks can be **unstable** during training:
- Layer outputs can become very large/small
- Training becomes slow or unstable
- Different batches can have different statistics

### **How BatchNorm Fixes It**

For each mini-batch, BatchNorm:
1. **Calculates mean & variance** of the batch
2. **Normalizes** outputs: `(x - mean) / sqrt(variance + epsilon)`
3. **Scales & shifts** with learnable parameters

### **BatchNorm Types**

| Type | Use Case | Input Shape |
|------|----------|-------------|
| `BatchNorm1d` | Dense layers | `(batch_size, features)` |
| `BatchNorm2d` | Conv2D layers | `(batch_size, channels, H, W)` |
| `BatchNorm3d` | Conv3D/Video | `(batch_size, channels, D, H, W)` |

### **Dense Network with BatchNorm**
```python
model = nn.Sequential(
    nn.Linear(784, 128),
    nn.BatchNorm1d(128),    # ← Normalize 128 features
    nn.ReLU(),
    
    nn.Linear(128, 64),
    nn.BatchNorm1d(64),     # ← Normalize 64 features
    nn.ReLU(),
    
    nn.Linear(64, 10)
)
```

### **CNN with BatchNorm**
```python
model = nn.Sequential(
    nn.Conv2d(3, 64, 3, padding=1),
    nn.BatchNorm2d(64),     # ← Normalize 64 channels
    nn.ReLU(),
    nn.MaxPool2d(2),
    
    nn.Conv2d(64, 128, 3, padding=1),
    nn.BatchNorm2d(128),    # ← Normalize 128 channels
    nn.ReLU(),
    nn.MaxPool2d(2),
    
    nn.AdaptiveAvgPool2d(1),
    nn.Flatten(),
    nn.Linear(128, 10)
)
```

### **Why BatchNorm Works**
- ✅ **Faster training**: Higher learning rates possible
- ✅ **More stable**: Reduces internal covariate shift
- ✅ **Better generalization**: Acts as regularization
- ✅ **Almost always use it**: Except very small/simple networks

### **Training vs Inference**

**Training**: Uses batch statistics  
**Inference**: Uses running averages computed during training

```python
model.train()  # Uses batch stats (training)
model.eval()   # Uses running averages (inference)
```

---

## 3️⃣ **Dropout — Prevent Overfitting**

### **What is Dropout?**

**Dropout** randomly **"turns off" neurons** during training to prevent overfitting.

### **How Dropout Works**

During training:
- Randomly set some neurons to **zero** (with probability `p`)
- Scale remaining neurons by `1/(1-p)` to maintain output magnitude
- Different random pattern each batch

During inference:
- **All neurons active** (no dropout)
- No scaling needed

### **Dropout in Action**

```python
model = nn.Sequential(
    nn.Linear(784, 128),
    nn.ReLU(),
    nn.Dropout(0.2),        # ← Drop 20% of neurons randomly
    
    nn.Linear(128, 64),
    nn.ReLU(),
    nn.Dropout(0.2),        # ← Drop another 20%
    
    nn.Linear(64, 10)
)
```

### **Dropout Types**

| Type | Use Case | Where to Apply |
|------|----------|----------------|
| `Dropout` | Dense layers | After Linear + Activation |
| `Dropout2d` | Conv2D features | After Conv2D + Activation |
| `Dropout3d` | Conv3D features | After Conv3D + Activation |

### **CNN with Dropout**
```python
model = nn.Sequential(
    nn.Conv2d(3, 64, 3, padding=1),
    nn.BatchNorm2d(64),
    nn.ReLU(),
    nn.Dropout2d(0.1),      # ← Drop entire channels
    nn.MaxPool2d(2),
    
    nn.Conv2d(64, 128, 3, padding=1),
    nn.BatchNorm2d(128),
    nn.ReLU(),
    nn.Dropout2d(0.1),
    nn.MaxPool2d(2),
    
    nn.AdaptiveAvgPool2d(1),
    nn.Flatten(),
    nn.Dropout(0.5),        # ← Dense dropout before output
    nn.Linear(128, 10)
)
```

### **Dropout Best Practices**

| Dropout Rate | Use Case |
|--------------|----------|
| `0.1 - 0.3` | Light regularization |
| `0.3 - 0.5` | Standard regularization |
| `0.5 - 0.7` | Heavy regularization (large networks) |

### **Training vs Inference Mode**

```python
# Training: Dropout active
model.train()
output = model(x)  # Some neurons randomly dropped

# Inference: Dropout inactive
model.eval()
with torch.no_grad():
    output = model(x)  # All neurons active
```

---

## 🏗️ **Complete Modern Architecture**

Here's a **production-ready** model using all three concepts:

```python
class ModernDNN(nn.Module):
    def __init__(self, input_size=784, hidden_sizes=[512, 256, 128], num_classes=10, dropout_rate=0.3):
        super().__init__()
        
        # Build layers list
        layers = []
        
        # Input layer
        layers.extend([
            nn.Linear(input_size, hidden_sizes[0]),
            nn.BatchNorm1d(hidden_sizes[0]),
            nn.ReLU(),
            nn.Dropout(dropout_rate)
        ])
        
        # Hidden layers
        for i in range(len(hidden_sizes)-1):
            layers.extend([
                nn.Linear(hidden_sizes[i], hidden_sizes[i+1]),
                nn.BatchNorm1d(hidden_sizes[i+1]),
                nn.ReLU(),
                nn.Dropout(dropout_rate)
            ])
        
        # Output layer (no dropout before output)
        layers.append(nn.Linear(hidden_sizes[-1], num_classes))
        
        # Create sequential model
        self.model = nn.Sequential(*layers)
    
    def forward(self, x):
        return self.model(x)

# Usage
model = ModernDNN(input_size=784, hidden_sizes=[512, 256, 128], num_classes=10)

# Training mode
model.train()
# ... training code ...

# Inference mode
model.eval()
with torch.no_grad():
    predictions = model(test_data)
```

---

## 📋 **Quick Reference**

### **Sequential**
```python
# Simple stack
model = nn.Sequential(
    nn.Linear(in, hidden),
    nn.ReLU(),
    nn.Linear(hidden, out)
)

# With regularization
model = nn.Sequential(
    nn.Linear(in, hidden),
    nn.BatchNorm1d(hidden),
    nn.ReLU(),
    nn.Dropout(0.2),
    nn.Linear(hidden, out)
)
```

### **BatchNorm**
```python
# Dense: BatchNorm1d
nn.BatchNorm1d(num_features)

# Conv2D: BatchNorm2d  
nn.BatchNorm2d(num_channels)

# Always after Linear/Conv, before activation
```

### **Dropout**
```python
# Dense layers
nn.Dropout(p=0.2)        # Drop 20%

# Conv layers
nn.Dropout2d(p=0.1)      # Drop channels

# Only during training!
model.train() / model.eval()
```

---

## ⚡ **Performance Impact**

| Technique | Training Speed | Memory | Accuracy | Stability |
|-----------|---------------|--------|----------|-----------|
| **Sequential** | Faster (no custom forward) | Same | Same | Same |
| **BatchNorm** | Slightly slower | More | Much better | Much better |
| **Dropout** | Same | Same | Better (less overfitting) | Same |

---

## 💡 **Pro Tips**

1. **Sequential**: Perfect for simple architectures, use custom `nn.Module` for complex ones
2. **BatchNorm**: Almost always use it, especially for deep networks
3. **Dropout**: Start with 0.2-0.3, increase if overfitting, don't use before output layer
4. **Training mode**: Always call `model.train()` before training, `model.eval()` for inference
5. **CNN Dropout**: Use `Dropout2d` for conv features, regular `Dropout` for dense layers

---

**Sequential for clean code, BatchNorm for stability, Dropout for generalization!** 🎯</content>
<parameter name="filePath">/mnt/Data/3-2/330 (ML lab)/Online 2/cheatsheets/sequential_batchnorm_dropout.md