---

## 🎯 THE BIG PICTURE

Think of tensors as **containers of numbers**. The "dimension" tells you how many "ways" you can access the numbers:

- **1D tensor**: `[a, b, c]` - like a list (1 way to access)
- **2D tensor**: `[[a, b], [c, d]]` - like a table (2 ways: row + column)
- **3D tensor**: `[[[a, b]], [[c, d]]]` - like a book of tables (3 ways: book + row + column)

### **🔤 Layer Naming Conventions (The Answer to Your Question!)**

```python
# Common naming patterns in PyTorch:
fc1, fc2, fc3 = nn.Linear(...)  # "fc" = Fully Connected (dense) layers
conv1, conv2, conv3 = nn.Conv2d(...)  # Convolutional layers  
pool1, pool2 = nn.MaxPool2d(...)  # Pooling layers
bn1, bn2 = nn.BatchNorm2d(...)  # Batch normalization
relu1, relu2 = nn.ReLU()  # Activation functions

# "fc" stands for FULLY CONNECTED layers
# These are the dense/feedforward layers that connect ALL neurons
# between layers (unlike conv layers which connect only nearby neurons)
```

**Example:**
```python
self.fc1 = nn.Linear(784, 128)  # Input: 784 features → Output: 128 features
self.fc2 = nn.Linear(128, 64)   # Input: 128 features → Output: 64 features  
self.fc3 = nn.Linear(64, 10)    # Input: 64 features → Output: 10 classes
```

---

## 📊 DATA FLOW IN NEURAL NETWORKS

### **The Golden Rule: Batch First!**
```
Input:  (batch_size, features)
Output: (batch_size, predictions)
```

**Example:** 32 images, each with 784 pixels → `(32, 784)`

---

## 🔢 COMMON TENSOR SHAPES YOU'LL SEE

### **1. Tabular Data (CSV, Excel)**
```python
# Raw data: 1000 samples, 5 features each
data = torch.randn(1000, 5)  # Shape: (1000, 5)
# Meaning: 1000 rows, 5 columns
```

### **2. Images**
```python
# Single image: 28×28 grayscale
image = torch.randn(28, 28)  # Shape: (28, 28)

# Batch of images: 32 images, 28×28 each
batch_images = torch.randn(32, 28, 28)  # Shape: (32, 28, 28)

# RGB images: 32 images, 3 channels, 28×28 each
rgb_batch = torch.randn(32, 3, 28, 28)  # Shape: (32, 3, 28, 28)
```

### **3. Text/Sequences**
```python
# Batch of sentences: 16 sentences, max 50 words each
sentences = torch.randint(0, 10000, (16, 50))  # Shape: (16, 50)
# Each number is a word ID
```

---

## 🏗️ LAYER-BY-LAYER DIMENSION CHANGES

### **Linear Layer (Fully Connected)**
```python
import torch.nn as nn

# Input: (batch_size, input_features)
# Output: (batch_size, output_features)

layer = nn.Linear(in_features=10, out_features=5)

# Example
x = torch.randn(32, 10)  # 32 samples, 10 features each
output = layer(x)        # Shape: (32, 5)
```

**Visual:**
```
Input:  [sample1: [f1,f2,...,f10],
         sample2: [f1,f2,...,f10],
         ...
         sample32: [f1,f2,...,f10]]

Layer:  Weights: (10, 5) matrix
        Bias: (5,) vector

Output: [sample1: [o1,o2,o3,o4,o5],
         sample2: [o1,o2,o3,o4,o5],
         ...
         sample32: [o1,o2,o3,o4,o5]]
```

### **Convolution Layer (CNN)**
```python
# Input:  (batch, channels, height, width)
# Output: (batch, out_channels, out_height, out_width)

conv = nn.Conv2d(in_channels=3, out_channels=64, kernel_size=3, padding=1)

# Example: RGB images
x = torch.randn(16, 3, 32, 32)   # 16 RGB images, 32×32 each
output = conv(x)                  # Shape: (16, 64, 32, 32)
```

**Visual:**
```
Input:  Batch of 16 images
        Each image: 3 channels (RGB) × 32×32 pixels

Conv:   64 filters, each 3×3×3 (channels×height×width)
        Output: 64 feature maps × 32×32 each

Output: 16 images × 64 channels × 32×32 pixels
```

### **Pooling Layer**
```python
# Input:  (batch, channels, height, width)
# Output: (batch, channels, height/2, width/2)  [for 2×2 pool]

pool = nn.MaxPool2d(kernel_size=2, stride=2)

x = torch.randn(16, 64, 32, 32)  # From conv layer
output = pool(x)                  # Shape: (16, 64, 16, 16)
```

### **Flatten Layer**
```python
# Input:  (batch, channels, height, width)
# Output: (batch, channels * height * width)

flatten = nn.Flatten()

x = torch.randn(16, 64, 16, 16)  # From pooling
output = flatten(x)              # Shape: (16, 64*16*16) = (16, 16384)
```

---

## 🔍 COMMON DIMENSION MISTAKES & FIXES

### **Mistake 1: Wrong Input Shape to Linear Layer**
```python
# ❌ WRONG
layer = nn.Linear(10, 5)
x = torch.randn(10)  # 1D tensor, missing batch dimension
output = layer(x)    # ERROR!

# ✅ CORRECT
layer = nn.Linear(10, 5)
x = torch.randn(32, 10)  # Add batch dimension
output = layer(x)         # Shape: (32, 5)
```

### **Mistake 2: Forgetting Batch Dimension**
```python
# ❌ WRONG (single sample)
x = torch.randn(784)      # 1 image flattened
output = model(x)         # May work, but inefficient

# ✅ CORRECT (with batch)
x = torch.randn(32, 784)  # 32 images
output = model(x)         # Proper batching
```

### **Mistake 3: Wrong Channel Order in CNNs**
```python
# ❌ WRONG (channels last)
x = torch.randn(32, 224, 224, 3)  # TensorFlow style
conv = nn.Conv2d(3, 64, 3)
output = conv(x)  # ERROR! PyTorch expects channels second

# ✅ CORRECT (channels first)
x = torch.randn(32, 3, 224, 224)  # PyTorch style
conv = nn.Conv2d(3, 64, 3)
output = conv(x)  # Shape: (32, 64, 222, 222)
```

### **Mistake 4: Shape Mismatch in Loss Functions**
```python
# Classification: need (batch, classes)
outputs = torch.randn(32, 10)  # 32 samples, 10 classes
targets = torch.randint(0, 10, (32,))  # 32 target labels (0-9)

loss = nn.CrossEntropyLoss()
loss_value = loss(outputs, targets)  # ✅ Correct

# ❌ WRONG targets shape
targets_wrong = torch.randint(0, 10, (32, 10))  # One-hot encoded
loss_value = loss(outputs, targets_wrong)  # ERROR!
```

---

## 🛠️ DEBUGGING DIMENSION ISSUES

### **Essential Debug Tools**
```python
# Check tensor shape
print(x.shape)      # torch.Size([32, 784])
print(x.size())     # Same as above
print(x.size(0))    # First dimension: 32
print(x.size(1))    # Second dimension: 784

# Check tensor dimensions
print(x.dim())      # Number of dimensions: 2
print(len(x.shape)) # Same as above

# Reshape tensor
x = torch.randn(32, 784)
x_reshaped = x.view(32, 28, 28)    # Reshape to image
x_flattened = x.view(32, -1)       # Flatten last dimensions

# Add/remove dimensions
x = torch.randn(32, 784)
x_unsqueezed = x.unsqueeze(1)       # Add dim: (32, 1, 784)
x_squeezed = x_unsqueezed.squeeze(1) # Remove dim: (32, 784)
```

### **Common Reshaping Patterns**
```python
# Pattern 1: Add batch dimension
single_image = torch.randn(784)           # (784,)
batched = single_image.unsqueeze(0)       # (1, 784)

# Pattern 2: Remove batch dimension
batch_output = torch.randn(1, 10)         # (1, 10)
single_output = batch_output.squeeze(0)   # (10,)

# Pattern 3: Flatten for Linear layer
conv_output = torch.randn(32, 64, 7, 7)  # (32, 64, 7, 7)
flattened = conv_output.view(32, -1)      # (32, 64*7*7) = (32, 3136)

# Pattern 4: Add channel dimension
grayscale = torch.randn(32, 28, 28)      # (32, 28, 28)
rgb_like = grayscale.unsqueeze(1)         # (32, 1, 28, 28)
```

---

## 📈 COMPLETE NETWORK EXAMPLE WITH SHAPES

```python
import torch
import torch.nn as nn

class SimpleCNN(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(3, 32, 3, padding=1)    # 3→32 channels
        self.pool = nn.MaxPool2d(2, 2)                 # /2 size
        self.conv2 = nn.Conv2d(32, 64, 3, padding=1)   # 32→64 channels
        self.flatten = nn.Flatten()
        self.fc1 = nn.Linear(64 * 8 * 8, 128)          # 64*8*8 = 4096 → 128
        self.fc2 = nn.Linear(128, 10)                  # 128 → 10 classes
    
    def forward(self, x):
        print(f"Input: {x.shape}")                    # (32, 3, 32, 32)
        
        x = self.conv1(x)
        print(f"After conv1: {x.shape}")              # (32, 32, 32, 32)
        
        x = self.pool(x)
        print(f"After pool1: {x.shape}")              # (32, 32, 16, 16)
        
        x = self.conv2(x)
        print(f"After conv2: {x.shape}")              # (32, 64, 16, 16)
        
        x = self.pool(x)
        print(f"After pool2: {x.shape}")              # (32, 64, 8, 8)
        
        x = self.flatten(x)
        print(f"After flatten: {x.shape}")            # (32, 4096)
        
        x = torch.relu(self.fc1(x))
        print(f"After fc1: {x.shape}")                # (32, 128)
        
        x = self.fc2(x)
        print(f"Output: {x.shape}")                   # (32, 10)
        
        return x

# Test the network
model = SimpleCNN()
x = torch.randn(32, 3, 32, 32)  # 32 RGB images, 32×32 each
output = model(x)
```

---

## 🎨 VISUAL MIND MAP

```
DATA FLOW:
Raw Data → Dataset → DataLoader → Model → Loss → Optimizer

TENSOR SHAPES:
• Images: (batch, channels, height, width)
• Text: (batch, sequence_length, embedding_dim)  
• Tabular: (batch, features)
• Labels: (batch,) for classification, (batch, features) for regression

LAYER TRANSFORMATIONS:
• Conv2d: (b,c,h,w) → (b,c_out,h_out,w_out)
• Pool2d: (b,c,h,w) → (b,c,h/2,w/2)
• Flatten: (b,c,h,w) → (b, c*h*w)
• Linear: (b, in_f) → (b, out_f)
```

---

## 🚨 QUICK FIXES FOR COMMON ERRORS

### **"RuntimeError: size mismatch"**
```python
# Problem: Wrong input size to Linear
layer = nn.Linear(100, 10)
x = torch.randn(32, 50)  # 50 features, but layer expects 100
# Fix: Change layer to nn.Linear(50, 10)

# Problem: Wrong target shape for loss
loss = nn.CrossEntropyLoss()
outputs = torch.randn(32, 10)    # (batch, classes)
targets = torch.randn(32, 10)    # Wrong! Should be (batch,)
# Fix: targets = torch.randint(0, 10, (32,))
```

### **"RuntimeError: input size mismatch"**
```python
# Problem: Conv input channels don't match
conv = nn.Conv2d(1, 64, 3)       # Expects 1 channel
x = torch.randn(32, 3, 28, 28)   # Has 3 channels
# Fix: Change conv to nn.Conv2d(3, 64, 3)
```

### **"RuntimeError: mat1 and mat2 shapes cannot be multiplied"**
```python
# Problem: Linear layer input size wrong
fc = nn.Linear(100, 10)
x = torch.randn(32, 50)  # 50 features, but expects 100
# Fix: Change to nn.Linear(50, 10) or flatten properly
```

---

## 💡 PRO TIPS

1. **Always check shapes**: `print(x.shape)` after every operation
2. **Batch first**: PyTorch convention is `(batch_size, ...)`
3. **Channels first**: Images are `(batch, channels, height, width)`
4. **Flatten before Linear**: CNN → Flatten → Linear
5. **Use `.view()` or `.reshape()`**: To change tensor shapes
6. **Debug with small batches**: Easier to see shape changes
7. **Keep a shape tracker**: Write down shapes as you build networks

**Remember:** Dimensions are just ways to organize your data. Once you get the patterns, it becomes second nature! 🎯

---

Now go build your networks with confidence! The shapes will make sense soon. 🚀</content>
<parameter name="filePath">/mnt/Data/3-2/330 (ML lab)/Online 2/cheatsheets/pytorch_dimensions_for_noobs.md