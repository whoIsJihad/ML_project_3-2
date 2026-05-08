---

# 🔄 Complete CNN Pipeline Examples — From Data to Results

This note shows **complete, runnable examples** of CNN pipelines. Each example includes data loading, model, training, and evaluation. Copy and modify for your projects!

---

## 📊 Example 1: MNIST Digit Classification (28×28 Grayscale)

```python
import torch
import torch.nn as nn
import torch.optim as optim
import torchvision
import torchvision.transforms as transforms
from torch.utils.data import DataLoader

# ================================
# 1. DATA LOADING & PREPROCESSING
# ================================

# Define transformations (convert to tensor, normalize)
transform = transforms.Compose([
    transforms.ToTensor(),  # Convert PIL image to tensor (0-1 range)
    transforms.Normalize((0.1307,), (0.3081,))  # MNIST mean/std normalization
])

# Load MNIST dataset
train_dataset = torchvision.datasets.MNIST(
    root='./data', 
    train=True, 
    download=True, 
    transform=transform
)

test_dataset = torchvision.datasets.MNIST(
    root='./data', 
    train=False, 
    download=True, 
    transform=transform
)

# Create data loaders
train_loader = DataLoader(train_dataset, batch_size=64, shuffle=True)
test_loader = DataLoader(test_dataset, batch_size=64, shuffle=False)

# ================================
# 2. MODEL DEFINITION
# ================================

class MNIST_CNN(nn.Module):
    def __init__(self):
        super(MNIST_CNN, self).__init__()
        self.conv1 = nn.Conv2d(1, 32, kernel_size=3, padding=1)    # 28×28 → 28×28
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, padding=1)   # 28×28 → 28×28
        self.pool = nn.MaxPool2d(2, 2)                             # → 14×14 → 7×7
        self.fc1 = nn.Linear(64 * 7 * 7, 128)
        self.fc2 = nn.Linear(128, 10)

    def forward(self, x):
        x = self.pool(torch.relu(self.conv1(x)))  # 28→14
        x = self.pool(torch.relu(self.conv2(x)))  # 14→7
        x = x.view(x.size(0), -1)                 # Flatten
        x = torch.relu(self.fc1(x))
        return self.fc2(x)

model = MNIST_CNN()

# ================================
# 3. LOSS & OPTIMIZER
# ================================

criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# ================================
# 4. TRAINING LOOP
# ================================

def train_model(model, train_loader, criterion, optimizer, epochs=5):
    model.train()  # Set to training mode
    
    for epoch in range(epochs):
        total_loss = 0
        correct = 0
        total = 0
        
        for images, labels in train_loader:
            optimizer.zero_grad()
            
            outputs = model(images)
            loss = criterion(outputs, labels)
            
            loss.backward()
            optimizer.step()
            
            # Track accuracy
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()
            total_loss += loss.item()
        
        avg_loss = total_loss / len(train_loader)
        accuracy = 100 * correct / total
        print(f"Epoch {epoch+1}/{epochs} | Loss: {avg_loss:.4f} | Acc: {accuracy:.2f}%")

# Train the model
train_model(model, train_loader, criterion, optimizer, epochs=5)

# ================================
# 5. EVALUATION ON TEST DATA
# ================================

def evaluate_model(model, test_loader):
    model.eval()  # Set to evaluation mode
    correct = 0
    total = 0
    
    with torch.no_grad():  # No gradients needed for evaluation
        for images, labels in test_loader:
            outputs = model(images)
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()
    
    accuracy = 100 * correct / total
    print(f"Test Accuracy: {accuracy:.2f}%")
    return accuracy

# Evaluate
test_accuracy = evaluate_model(model, test_loader)

# ================================
# 6. INFERENCE ON SINGLE IMAGE
# ================================

def predict_single_image(model, image):
    model.eval()
    with torch.no_grad():
        output = model(image.unsqueeze(0))  # Add batch dimension
        _, predicted = torch.max(output, 1)
        return predicted.item()

# Example: Predict on first test image
test_image, test_label = test_dataset[0]
prediction = predict_single_image(model, test_image)
print(f"Predicted: {prediction}, Actual: {test_label}")
```

---

## 🐱 Example 2: CIFAR10 Image Classification (32×32 RGB)

```python
import torch
import torch.nn as nn
import torch.optim as optim
import torchvision
import torchvision.transforms as transforms
from torch.utils.data import DataLoader

# ================================
# 1. DATA LOADING & PREPROCESSING
# ================================

transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.4914, 0.4822, 0.4465), (0.2470, 0.2435, 0.2616))  # CIFAR10 stats
])

train_dataset = torchvision.datasets.CIFAR10(
    root='./data', train=True, download=True, transform=transform
)
test_dataset = torchvision.datasets.CIFAR10(
    root='./data', train=False, download=True, transform=transform
)

train_loader = DataLoader(train_dataset, batch_size=128, shuffle=True)
test_loader = DataLoader(test_dataset, batch_size=128, shuffle=False)

# ================================
# 2. MODEL DEFINITION (Deeper for RGB)
# ================================

class CIFAR10_CNN(nn.Module):
    def __init__(self):
        super(CIFAR10_CNN, self).__init__()
        self.conv1 = nn.Conv2d(3, 64, kernel_size=3, padding=1)     # 32×32 → 32×32
        self.conv2 = nn.Conv2d(64, 128, kernel_size=3, padding=1)   # 32×32 → 32×32
        self.conv3 = nn.Conv2d(128, 256, kernel_size=3, padding=1)  # 16×16 → 16×16
        self.pool = nn.MaxPool2d(2, 2)                              # → 16×16 → 8×8 → 4×4
        self.fc1 = nn.Linear(256 * 4 * 4, 512)
        self.fc2 = nn.Linear(512, 10)

    def forward(self, x):
        x = torch.relu(self.conv1(x))
        x = self.pool(torch.relu(self.conv2(x)))  # 32→16
        x = self.pool(torch.relu(self.conv3(x)))  # 16→8, then 8→4
        x = x.view(x.size(0), -1)
        x = torch.relu(self.fc1(x))
        return self.fc2(x)

model = CIFAR10_CNN()

# ================================
# 3. LOSS & OPTIMIZER
# ================================

criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# ================================
# 4. TRAINING WITH VALIDATION
# ================================

def train_with_validation(model, train_loader, test_loader, criterion, optimizer, epochs=10):
    best_accuracy = 0
    
    for epoch in range(epochs):
        # Training phase
        model.train()
        train_loss = 0
        train_correct = 0
        train_total = 0
        
        for images, labels in train_loader:
            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            
            train_loss += loss.item()
            _, predicted = torch.max(outputs.data, 1)
            train_total += labels.size(0)
            train_correct += (predicted == labels).sum().item()
        
        # Validation phase
        model.eval()
        val_correct = 0
        val_total = 0
        
        with torch.no_grad():
            for images, labels in test_loader:
                outputs = model(images)
                _, predicted = torch.max(outputs.data, 1)
                val_total += labels.size(0)
                val_correct += (predicted == labels).sum().item()
        
        train_acc = 100 * train_correct / train_total
        val_acc = 100 * val_correct / val_total
        avg_train_loss = train_loss / len(train_loader)
        
        print(f"Epoch {epoch+1}/{epochs}")
        print(f"  Train Loss: {avg_train_loss:.4f}, Train Acc: {train_acc:.2f}%")
        print(f"  Val Acc: {val_acc:.2f}%")
        
        # Save best model
        if val_acc > best_accuracy:
            best_accuracy = val_acc
            torch.save(model.state_dict(), 'best_model.pth')

# Train
train_with_validation(model, train_loader, test_loader, criterion, optimizer, epochs=10)

# ================================
# 5. LOAD BEST MODEL & FINAL EVALUATION
# ================================

model.load_state_dict(torch.load('best_model.pth'))
final_accuracy = evaluate_model(model, test_loader)
print(f"Best Model Test Accuracy: {final_accuracy:.2f}%")
```

---

## 🐶 Example 3: Custom Dataset (Binary Classification)

```python
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
import os
from PIL import Image
import torchvision.transforms as transforms

# ================================
# 1. CUSTOM DATASET CLASS
# ================================

class CustomImageDataset(Dataset):
    def __init__(self, image_paths, labels, transform=None):
        self.image_paths = image_paths
        self.labels = labels
        self.transform = transform
    
    def __len__(self):
        return len(self.image_paths)
    
    def __getitem__(self, idx):
        image = Image.open(self.image_paths[idx]).convert('RGB')
        label = self.labels[idx]
        
        if self.transform:
            image = self.transform(image)
        
        return image, label

# ================================
# 2. DATA PREPARATION (Assume you have images in folders)
# ================================

# Example: Cats vs Dogs classification
transform = transforms.Compose([
    transforms.Resize((128, 128)),  # Resize to 128×128
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])  # ImageNet stats
])

# Assume you have lists of file paths and labels
train_paths = ['path/to/cat1.jpg', 'path/to/dog1.jpg', ...]  # Your image paths
train_labels = [0, 1, ...]  # 0=cat, 1=dog

train_dataset = CustomImageDataset(train_paths, train_labels, transform=transform)
train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)

# ================================
# 3. MODEL FOR LARGER IMAGES
# ================================

class CustomCNN(nn.Module):
    def __init__(self):
        super(CustomCNN, self).__init__()
        self.conv1 = nn.Conv2d(3, 64, kernel_size=3, padding=1)     # 128×128 → 128×128
        self.conv2 = nn.Conv2d(64, 128, kernel_size=3, padding=1)   # 64×64 → 64×64
        self.conv3 = nn.Conv2d(128, 256, kernel_size=3, padding=1)  # 32×32 → 32×32
        self.conv4 = nn.Conv2d(256, 512, kernel_size=3, padding=1)  # 16×16 → 16×16
        self.pool = nn.MaxPool2d(2, 2)                              # → 64×64 → 32×32 → 16×16 → 8×8
        self.fc1 = nn.Linear(512 * 8 * 8, 1024)
        self.fc2 = nn.Linear(1024, 2)  # Binary: cat or dog

    def forward(self, x):
        x = self.pool(torch.relu(self.conv1(x)))   # 128→64
        x = self.pool(torch.relu(self.conv2(x)))   # 64→32
        x = self.pool(torch.relu(self.conv3(x)))   # 32→16
        x = self.pool(torch.relu(self.conv4(x)))   # 16→8
        x = x.view(x.size(0), -1)
        x = torch.relu(self.fc1(x))
        return self.fc2(x)

model = CustomCNN()

# ================================
# 4. TRAINING
# ================================

criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.0001)  # Smaller LR for custom data

# Train for more epochs on custom data
train_model(model, train_loader, criterion, optimizer, epochs=20)

# ================================
# 5. SAVE & LOAD MODEL
# ================================

# Save entire model
torch.save(model, 'custom_cnn_model.pth')

# Load model
loaded_model = torch.load('custom_cnn_model.pth')
loaded_model.eval()

# ================================
# 6. PREDICT ON NEW IMAGE
# ================================

def predict_new_image(model, image_path):
    model.eval()
    image = Image.open(image_path).convert('RGB')
    image = transform(image).unsqueeze(0)  # Add batch dimension
    
    with torch.no_grad():
        output = model(image)
        _, predicted = torch.max(output, 1)
        
    classes = ['Cat', 'Dog']
    return classes[predicted.item()]

# Usage
result = predict_new_image(loaded_model, 'new_image.jpg')
print(f"Prediction: {result}")
```

---

## 📋 Pipeline Summary

Every CNN pipeline follows this structure:

1. **Data Loading**: Use torchvision datasets or create custom Dataset class
2. **Preprocessing**: Resize, normalize, augment images
3. **Model**: Define Conv layers → Pooling → Flatten → Dense layers
4. **Training**: Loop through batches, compute loss, backprop, update weights
5. **Evaluation**: Test on unseen data, calculate accuracy
6. **Inference**: Load model, predict on new images

**Key Differences by Dataset:**
- **MNIST**: Simple, 1 channel, small images (28×28)
- **CIFAR10**: RGB, medium complexity (32×32)
- **Custom**: RGB, large images (128×128+), may need more layers

**Tips:**
- Start with smaller batch sizes if you get memory errors
- Use validation to prevent overfitting
- Save/load models for deployment
- Experiment with learning rates and architectures

---

Copy any example above and adapt it to your specific dataset and problem!

---</content>
<parameter name="filePath">/mnt/Data/3-2/330 (ML lab)/Online 2/cheatsheets/CNN_pipeline_examples.md