---

# 📷 PyTorch Convolutional Neural Networks (CNN) — Beginner Guide

This guide explains **CNNs** from scratch for beginners. CNNs are designed for **image data** (photos, handwritten digits, etc.). They work differently from DNNs.

---

## 📐 CNN Dimension Flow Diagram

Here's how dimensions change through a typical CNN (example with 100 images of 300×300 RGB photos):

```
Input Images
│
│  Shape: (100, 3, 300, 300)
│  Meaning: 100 images, 3 color channels (RGB), 300×300 pixels each
│
├─ Conv2d(3, 64, kernel_size=3, padding=1)
│  Shape: (100, 64, 300, 300)
│  Meaning: 100 images, 64 feature maps, 300×300 pixels (same size due to padding)
│
├─ MaxPool2d(2, 2)
│  Shape: (100, 64, 150, 150)
│  Meaning: 100 images, 64 feature maps, 150×150 pixels (half size)
│
├─ Conv2d(64, 128, kernel_size=3, padding=1)
│  Shape: (100, 128, 150, 150)
│  Meaning: 100 images, 128 feature maps, 150×150 pixels
│
├─ MaxPool2d(2, 2)
│  Shape: (100, 128, 75, 75)
│  Meaning: 100 images, 128 feature maps, 75×75 pixels (half size)
│
├─ Conv2d(128, 256, kernel_size=3, padding=1)
│  Shape: (100, 256, 75, 75)
│  Meaning: 100 images, 256 feature maps, 75×75 pixels
│
├─ MaxPool2d(2, 2)
│  Shape: (100, 256, 37, 37)
│  Meaning: 100 images, 256 feature maps, 37×37 pixels (half size)
│
├─ Flatten()
│  Shape: (100, 256×37×37) = (100, 341056)
│  Meaning: 100 images, 341056 values (2D → 1D)
│
├─ Linear(341056, 512)
│  Shape: (100, 512)
│  Meaning: 100 images, 512 hidden features
│
└─ Linear(512, 10)
   Shape: (100, 10)
   Meaning: 100 images, 10 class probabilities
```

**Key Points:**
- **Batch size** (100) stays the same throughout
- **Channels** increase: 3 → 64 → 128 → 256 (more patterns detected)
- **Height/Width** decrease: 300 → 150 → 75 → 37 (spatial information compressed)
- **Pooling** halves dimensions (300→150, 150→75, 75→37)
- **Flatten** converts 2D image features to 1D vector for dense layers

---

## 🤔 What is a CNN? (Super Simple)

## 🤔 What is a CNN? (Super Simple)

A CNN is a neural network that recognizes **patterns in images**.

**DNN (what you learned)**: Takes flat list of numbers
- Input: [0.5, 0.3, 0.2, 0.1, ...] (100 numbers)
- Uses all numbers together

**CNN (new)**: Takes actual image
- Input: Image grid (height × width × color channels)
- Looks at small neighborhoods (like zooming in on image)
- Recognizes shapes → features → objects

**Example**:
- **Digit 7**: DNN needs to learn "this pattern of pixels = 7"
- **CNN**: First learns "curved lines", then "this curved line = 7"

---

## 📊 Key Terms for CNN (Explained Simply)

- **Kernel/Filter**: A small square window that slides over the image looking for patterns
  - Size: Usually 3×3 or 5×5 pixels
  - Think: Pattern detector

- **Convolutional Layer**: Applies kernels to image to find patterns
  - Input: Image (28×28 pixels for digit)
  - Output: Feature map showing where patterns are found

- **Max Pooling**: Shrinks the image, keeps only strongest patterns
  - Reduces size: 28×28 → 14×14
  - Keeps important info, throws away detail

- **Flatten**: Converts 2D image into 1D list for final layers
  - Like unrolling paper into a line

- **Channel**: Color dimension
  - Black & white: 1 channel
  - RGB image: 3 channels (red, green, blue)

---

## 🏗️ Basic CNN Architecture (Step by Step)

```python
import torch
import torch.nn as nn
import torch.optim as optim

# CNN for MNIST (handwritten digits)

class SimpleCNN(nn.Module):
    def __init__(self):
        super(SimpleCNN, self).__init__()
        
        # Convolutional layers (find patterns)
        self.conv1 = nn.Conv2d(in_channels=1, out_channels=32, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(in_channels=32, out_channels=64, kernel_size=3, padding=1)
        
        # Pooling layer (shrink image)
        self.pool = nn.MaxPool2d(kernel_size=2, stride=2)
        
        # Dense layers (classification)
        self.fc1 = nn.Linear(64 * 7 * 7, 128)
        self.fc2 = nn.Linear(128, 10)

    def forward(self, x):
        # x shape: (batch_size, 1, 28, 28)
        
        # Convolutional block 1
        x = self.conv1(x)          # (batch, 32, 28, 28)
        x = torch.relu(x)
        x = self.pool(x)           # (batch, 32, 14, 14)
        
        # Convolutional block 2
        x = self.conv2(x)          # (batch, 64, 14, 14)
        x = torch.relu(x)
        x = self.pool(x)           # (batch, 64, 7, 7)
        
        # Flatten and classify
        x = x.view(x.size(0), -1)  # (batch, 3136)
        x = torch.relu(self.fc1(x))
        x = self.fc2(x)
        
        return x

# Data
train_images = torch.randn(100, 1, 28, 28)
train_labels = torch.randint(0, 10, (100,))

# Setup and training
model = SimpleCNN()
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

for epoch in range(5):
    optimizer.zero_grad()
    output = model(train_images)
    loss = criterion(output, train_labels)
    loss.backward()
    optimizer.step()
    
    pred = torch.argmax(output, dim=1)
    acc = (pred == train_labels).float().mean()
    print(f"Epoch {epoch+1} | Loss: {loss.item():.4f} | Acc: {acc:.2%}")
```

---

## 🧩 CNN Components Explained

### Conv2d (Convolutional Layer)

```python
nn.Conv2d(in_channels, out_channels, kernel_size, padding=0, stride=1)
```

- **in_channels**: Number of input channels
  - 1 = grayscale (black & white)
  - 3 = RGB (color photo)
  
- **out_channels**: Number of filters (pattern detectors)
  - Higher = more patterns found
  - Common: 32, 64, 128, 256
  
- **kernel_size**: Window size for patterns
  - 3 = 3×3 square (very common)
  - 5 = 5×5 square (less common)
  
- **padding**: Add zeros around image
  - 0 = no padding (shrinks)
  - 1 = padding (stays same size)
  - Use: 1 usually
  
- **stride**: How many pixels to slide
  - 1 = slide 1 pixel (default, standard)
  - 2 = slide 2 pixels (shrinks)

**Example:**
```python
# Find 64 patterns in 32-channel input with 3×3 window
nn.Conv2d(32, 64, kernel_size=3, padding=1)
```

**How channels work (super important!):**

Imagine you have a **32-channel input** (from previous layer):
- Channel 1: Detects edges
- Channel 2: Detects corners
- Channel 3: Detects circles
- ... up to 32 different patterns

Now you apply **64 different filters**:
- Filter 1: Looks for "vertical lines" across all 32 input channels
- Filter 2: Looks for "horizontal lines" across all 32 input channels
- Filter 3: Looks for "diagonal lines" across all 32 input channels
- ... up to 64 different pattern types

Each filter produces **1 output channel**, so:
- 64 filters → 64 output channels
- Each output channel shows where that specific pattern was found

**Think of it as:** Input has 32 "feature maps", we create 64 new "feature maps" by combining information from all 32 inputs in different ways.

### MaxPool2d (Pooling Layer)

```python
nn.MaxPool2d(kernel_size=2, stride=2)
```

- **kernel_size**: Size of shrinking window
  - 2 = 2×2 (shrink by 2, almost always use this)
  
- **stride**: How to move window
  - Same as kernel_size (no overlap)

**What it does**: Takes 2×2 block, keeps biggest value
- 28×28 image → 14×14 (half size)
- 14×14 image → 7×7 (half size)

**Why?** Removes noise, finds important patterns, speeds up training.

---

## 📐 CNN Shapes (Critical!)

**Understand this or CNN won't work:**

```python
# Start: 28×28 image, 1 channel (grayscale)
shape_0 = (batch_size, 1, 28, 28)

# After Conv2d(1, 32, padding=1) + ReLU
shape_1 = (batch_size, 32, 28, 28)  # Same size

# After MaxPool2d(2, 2)
shape_2 = (batch_size, 32, 14, 14)  # Half size

# After Conv2d(32, 64, padding=1) + ReLU
shape_3 = (batch_size, 64, 14, 14)  # Same size

# After MaxPool2d(2, 2)
shape_4 = (batch_size, 64, 7, 7)    # Half size

# After Flatten()
shape_5 = (batch_size, 3136)        # 64 × 7 × 7 = 3136

# After Linear(3136, 128)
shape_6 = (batch_size, 128)

# After Linear(128, 10)
shape_7 = (batch_size, 10)          # Output: 10 classes
```

---

## 🎯 Different CNN Architectures

### Small CNN (MNIST - 28×28)

```python
class SmallCNN(nn.Module):
    def __init__(self):
        super(SmallCNN, self).__init__()
        self.conv1 = nn.Conv2d(1, 32, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, padding=1)
        self.pool = nn.MaxPool2d(2, 2)
        self.fc1 = nn.Linear(64 * 7 * 7, 128)
        self.fc2 = nn.Linear(128, 10)

    def forward(self, x):
        x = self.pool(torch.relu(self.conv1(x)))
        x = self.pool(torch.relu(self.conv2(x)))
        x = x.view(x.size(0), -1)
        x = torch.relu(self.fc1(x))
        return self.fc2(x)
```

**What the fuck happened here? Forward pass explained line by line:**

```python
def forward(self, x):
    # x starts as: (batch_size, 1, 28, 28) - batch of 28×28 grayscale images
    
    # Line 1: x = self.pool(torch.relu(self.conv1(x)))
    # conv1: (batch, 1, 28, 28) → (batch, 32, 28, 28) - find 32 patterns
    # relu: Apply activation to make outputs positive
    # pool: (batch, 32, 28, 28) → (batch, 32, 14, 14) - shrink by half
    # Result: x = (batch, 32, 14, 14)
    
    # Line 2: x = self.pool(torch.relu(self.conv2(x)))
    # conv2: (batch, 32, 14, 14) → (batch, 64, 14, 14) - find 64 more complex patterns
    # relu: Activation again
    # pool: (batch, 64, 14, 14) → (batch, 64, 7, 7) - shrink by half again
    # Result: x = (batch, 64, 7, 7)
    
    # Line 3: x = x.view(x.size(0), -1)
    # PROBLEM: Dense layers need 1D vectors, but we have 2D images!
    # SOLUTION: Flatten the 2D image into 1D vector
    # x.view(batch_size, -1) means: keep batch_size, flatten everything else
    # (batch, 64, 7, 7) → (batch, 64×7×7) = (batch, 3136)
    # Result: x = (batch, 3136) - now it's a 1D vector!
    
    # Line 4: x = torch.relu(self.fc1(x))
    # fc1: (batch, 3136) → (batch, 128) - learn combinations of features
    # relu: Activation for non-linearity
    # Result: x = (batch, 128)
    
    # Line 5: return self.fc2(x)
    # fc2: (batch, 128) → (batch, 10) - final classification (10 classes)
    # NO activation here - CrossEntropyLoss handles it
    # Result: x = (batch, 10) - class scores
```

**Why x.view(x.size(0), -1)?**
- **Problem**: Convolutional layers output 2D/3D tensors (images), but dense layers need 1D vectors
- **Solution**: `view()` reshapes without copying data
- **x.size(0)**: Keep the batch size (first dimension)
- **-1**: PyTorch automatically calculates this (flattens all remaining dimensions)
- **Example**: (100, 64, 7, 7).view(100, -1) → (100, 3136)

**Think of it as:** Unrolling a 2D image into a long 1D line for the final classifier.
```

**Use when:** Images are 28×28 (like MNIST digits)

### Medium CNN (CIFAR10 - 32×32 or 64×64)

```python
class MediumCNN(nn.Module):
    def __init__(self):
        super(MediumCNN, self).__init__()
        self.conv1 = nn.Conv2d(3, 32, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, padding=1)
        self.conv3 = nn.Conv2d(64, 128, kernel_size=3, padding=1)
        self.pool = nn.MaxPool2d(2, 2)
        self.fc1 = nn.Linear(128 * 4 * 4, 256)
        self.fc2 = nn.Linear(256, 10)

    def forward(self, x):
        x = self.pool(torch.relu(self.conv1(x)))  # 32 → 16
        x = self.pool(torch.relu(self.conv2(x)))  # 16 → 8
        x = self.pool(torch.relu(self.conv3(x)))  # 8 → 4
        x = x.view(x.size(0), -1)
        x = torch.relu(self.fc1(x))
        return self.fc2(x)
```

**Use when:** Images are 32×32 or 64×64 (like CIFAR10)

### Large CNN (ImageNet - 128×128+)

```python
class LargeCNN(nn.Module):
    def __init__(self):
        super(LargeCNN, self).__init__()
        self.conv1 = nn.Conv2d(3, 64, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(64, 128, kernel_size=3, padding=1)
        self.conv3 = nn.Conv2d(128, 256, kernel_size=3, padding=1)
        self.conv4 = nn.Conv2d(256, 512, kernel_size=3, padding=1)
        self.pool = nn.MaxPool2d(2, 2)
        self.fc1 = nn.Linear(512 * 8 * 8, 512)
        self.fc2 = nn.Linear(512, 10)

    def forward(self, x):
        x = self.pool(torch.relu(self.conv1(x)))   # 128 → 64
        x = self.pool(torch.relu(self.conv2(x)))   # 64 → 32
        x = self.pool(torch.relu(self.conv3(x)))   # 32 → 16
        x = self.pool(torch.relu(self.conv4(x)))   # 16 → 8
        x = x.view(x.size(0), -1)
        x = torch.relu(self.fc1(x))
        return self.fc2(x)
```

**Use when:** Images are 128×128 or bigger (real photos)

---

## 🎮 Parameters to Tune

### Number of Filters
```python
# Fewer (32, 64): Fast, low memory, weak features
nn.Conv2d(32, 64, kernel_size=3)

# More (256, 512): Slow, high memory, strong features
nn.Conv2d(256, 512, kernel_size=3)
```

**Increase filters if:** Model underfits (bad accuracy)
**Decrease filters if:** Training is slow or out of memory

### Kernel Size
```python
# Small (3×3): Find fine details, fast
nn.Conv2d(32, 64, kernel_size=3)

# Large (5×5): Find big patterns, slower
nn.Conv2d(32, 64, kernel_size=5)
```

**Use 3×3 in 99% of cases.**

### Number of Conv Layers
```python
# Few layers (2-3): Simple patterns, fast
# Many layers (4-5+): Complex patterns, slow

# Simple: 28×28 image
SmallCNN  # 2 conv layers

# Complex: 128×128 image
LargeCNN  # 4 conv layers
```

**Rule**: More layers = more complex features = slower training

---

## 📋 CNN vs DNN

| Feature | DNN | CNN |
|---------|-----|-----|
| **Input** | Flat numbers | Images (2D) |
| **Speed** | Slow for images | Fast for images |
| **Memory** | High for images | Lower for images |
| **Best for** | Tables/sequences | Images |
| **Complexity** | Easy | Medium |

**When to use CNN:** Image data
**When to use DNN:** Anything else (numbers, tables, text embeddings)

---

## 🚨 Common Mistakes

1. **Using DNN on images**: Works but slow and bad results → Use CNN
2. **Wrong input shape**: Should be (batch, channels, height, width)
3. **Forgetting flatten**: Can't connect Conv to Dense without flatten
4. **Too many filters**: 512+ usually wastes time
5. **Wrong padding**: Image shrinks too fast

---

## 💡 Quick Decision Guide

```
Do you have images?
│
├─ Yes
│  ├─ Size 28×28? → SmallCNN
│  ├─ Size 32-64×32-64? → MediumCNN
│  └─ Size 128×128+? → LargeCNN
│
└─ No → Use DNN
```

---

## 🔧 Training (Same as DNN!)

```python
model = SmallCNN()  # Or MediumCNN, LargeCNN
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

for epoch in range(20):
    optimizer.zero_grad()
    output = model(train_images)
    loss = criterion(output, train_labels)
    loss.backward()
    optimizer.step()
```

**Note**: Training loop is identical to DNN. Only the model architecture changes!

---

This is **everything** for CNN basics. Pick architecture for your image size and train!

---