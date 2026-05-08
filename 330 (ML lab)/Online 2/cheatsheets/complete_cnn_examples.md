---

# 🖼️ Complete CNN Examples — From Images to Predictions

**Full end-to-end examples** of Convolutional Neural Networks covering preprocessing, training, testing, and deployment.

---

## 🐱 Example 1: CIFAR-10 Image Classification (32×32 RGB Images)

### **Problem**: Classify images into 10 categories (airplane, automobile, bird, cat, deer, dog, frog, horse, ship, truck)

```python
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader, random_split
import torchvision
import torchvision.transforms as transforms
from torchvision.datasets import CIFAR10
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import classification_report, confusion_matrix
import seaborn as sns
import time

# ================================
# 1. DATA LOADING & AUGMENTATION
# ================================

# Advanced data augmentation for better generalization
train_transform = transforms.Compose([
    transforms.RandomHorizontalFlip(),        # Random flip
    transforms.RandomCrop(32, padding=4),     # Random crop with padding
    transforms.RandomRotation(15),            # Random rotation
    transforms.ColorJitter(brightness=0.1, contrast=0.1, saturation=0.1, hue=0.1),  # Color variations
    transforms.ToTensor(),
    transforms.Normalize((0.4914, 0.4822, 0.4465), (0.2470, 0.2435, 0.2616)),  # CIFAR-10 stats
    transforms.RandomErasing(p=0.1)           # Random erasing for robustness
])

test_transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.4914, 0.4822, 0.4465), (0.2470, 0.2435, 0.2616))
])

# Load CIFAR-10 dataset
full_train_dataset = CIFAR10(root='./data', train=True, download=True, transform=train_transform)
test_dataset = CIFAR10(root='./data', train=False, download=True, transform=test_transform)

# Split training into train/validation
train_size = int(0.9 * len(full_train_dataset))
val_size = len(full_train_dataset) - train_size
train_dataset, val_dataset = random_split(full_train_dataset, [train_size, val_size])

# Override validation transform (no augmentation for validation)
val_dataset.dataset.transform = test_transform

# Create data loaders
batch_size = 128
train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True, num_workers=4, pin_memory=True)
val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False, num_workers=4, pin_memory=True)
test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False, num_workers=4, pin_memory=True)

# Class names
classes = ['airplane', 'automobile', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck']

print(f"Train: {len(train_dataset)}, Val: {len(val_dataset)}, Test: {len(test_dataset)}")
print(f"Classes: {classes}")

# ================================
# 2. VISUALIZE DATA
# ================================

def imshow(img):
    """Unnormalize and display image"""
    img = img / 2 + 0.5  # Unnormalize
    npimg = img.numpy()
    plt.imshow(np.transpose(npimg, (1, 2, 0)))
    plt.show()

# Show some training images
dataiter = iter(train_loader)
images, labels = next(dataiter)

# Display batch of images
plt.figure(figsize=(12, 8))
for i in range(16):
    plt.subplot(4, 4, i+1)
    imshow(images[i])
    plt.title(classes[labels[i]])
    plt.axis('off')
plt.tight_layout()
plt.savefig('cifar10_samples.png', dpi=300, bbox_inches='tight')
plt.show()

# ================================
# 3. MODERN CNN ARCHITECTURE
# ================================

class ModernCNN(nn.Module):
    def __init__(self, num_classes=10):
        super(ModernCNN, self).__init__()

        # Feature extraction layers
        self.features = nn.Sequential(
            # Block 1
            nn.Conv2d(3, 64, kernel_size=3, padding=1, bias=False),
            nn.BatchNorm2d(64),
            nn.ReLU(inplace=True),
            nn.Conv2d(64, 64, kernel_size=3, padding=1, bias=False),
            nn.BatchNorm2d(64),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2, 2),  # 32x32 -> 16x16
            nn.Dropout2d(0.1),

            # Block 2
            nn.Conv2d(64, 128, kernel_size=3, padding=1, bias=False),
            nn.BatchNorm2d(128),
            nn.ReLU(inplace=True),
            nn.Conv2d(128, 128, kernel_size=3, padding=1, bias=False),
            nn.BatchNorm2d(128),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2, 2),  # 16x16 -> 8x8
            nn.Dropout2d(0.1),

            # Block 3
            nn.Conv2d(128, 256, kernel_size=3, padding=1, bias=False),
            nn.BatchNorm2d(256),
            nn.ReLU(inplace=True),
            nn.Conv2d(256, 256, kernel_size=3, padding=1, bias=False),
            nn.BatchNorm2d(256),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2, 2),  # 8x8 -> 4x4
            nn.Dropout2d(0.1),
        )

        # Classification layers
        self.classifier = nn.Sequential(
            nn.AdaptiveAvgPool2d((1, 1)),  # Global average pooling
            nn.Flatten(),
            nn.Linear(256, 512),
            nn.BatchNorm1d(512),
            nn.ReLU(inplace=True),
            nn.Dropout(0.5),
            nn.Linear(512, num_classes)
        )

        # Initialize weights
        self._initialize_weights()

    def _initialize_weights(self):
        """Initialize model weights using Kaiming initialization"""
        for m in self.modules():
            if isinstance(m, nn.Conv2d):
                nn.init.kaiming_normal_(m.weight, mode='fan_out', nonlinearity='relu')
            elif isinstance(m, nn.BatchNorm2d):
                nn.init.constant_(m.weight, 1)
                nn.init.constant_(m.bias, 0)
            elif isinstance(m, nn.Linear):
                nn.init.normal_(m.weight, 0, 0.01)
                nn.init.constant_(m.bias, 0)

    def forward(self, x):
        x = self.features(x)
        x = self.classifier(x)
        return x

# Initialize model
model = ModernCNN(num_classes=10)

# Count parameters
total_params = sum(p.numel() for p in model.parameters())
trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
print(f"Total parameters: {total_params:,}")
print(f"Trainable parameters: {trainable_params:,}")

# ================================
# 4. LOSS, OPTIMIZER & SCHEDULER
# ================================

criterion = nn.CrossEntropyLoss()

# AdamW optimizer (better than Adam for regularization)
optimizer = optim.AdamW(model.parameters(), lr=0.001, weight_decay=1e-4, betas=(0.9, 0.999))

# Cosine annealing with warm restarts
scheduler = optim.lr_scheduler.CosineAnnealingWarmRestarts(
    optimizer, T_0=10, T_mult=2, eta_min=1e-6
)

# ================================
# 5. TRAINING LOOP WITH ADVANCED FEATURES
# ================================

def train_epoch(model, train_loader, criterion, optimizer, scheduler, device, epoch):
    model.train()
    running_loss = 0.0
    correct = 0
    total = 0

    for batch_idx, (inputs, targets) in enumerate(train_loader):
        inputs, targets = inputs.to(device), targets.to(device)

        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs, targets)

        loss.backward()

        # Gradient clipping to prevent exploding gradients
        torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)

        optimizer.step()

        running_loss += loss.item()
        _, predicted = outputs.max(1)
        total += targets.size(0)
        correct += predicted.eq(targets).sum().item()

        # Print progress
        if batch_idx % 50 == 0:
            print(f"Epoch {epoch+1}, Batch {batch_idx}/{len(train_loader)}, Loss: {loss.item():.3f}")

    # Update learning rate
    scheduler.step()

    epoch_loss = running_loss / len(train_loader)
    epoch_acc = 100. * correct / total
    return epoch_loss, epoch_acc

def validate_epoch(model, val_loader, criterion, device):
    model.eval()
    running_loss = 0.0
    correct = 0
    total = 0

    with torch.no_grad():
        for inputs, targets in val_loader:
            inputs, targets = inputs.to(device), targets.to(device)

            outputs = model(inputs)
            loss = criterion(outputs, targets)

            running_loss += loss.item()
            _, predicted = outputs.max(1)
            total += targets.size(0)
            correct += predicted.eq(targets).sum().item()

    epoch_loss = running_loss / len(val_loader)
    epoch_acc = 100. * correct / total
    return epoch_loss, epoch_acc

# Training setup
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = model.to(device)

if torch.cuda.device_count() > 1:
    print(f"Using {torch.cuda.device_count()} GPUs")
    model = nn.DataParallel(model)

epochs = 50
best_acc = 0.0
patience = 15
patience_counter = 0

# Track metrics
train_losses = []
val_losses = []
train_accs = []
val_accs = []
learning_rates = []

print("Starting training...")
start_time = time.time()

for epoch in range(epochs):
    # Train
    train_loss, train_acc = train_epoch(model, train_loader, criterion, optimizer, scheduler, device, epoch)

    # Validate
    val_loss, val_acc = validate_epoch(model, val_loader, criterion, device)

    # Store metrics
    train_losses.append(train_loss)
    val_losses.append(val_loss)
    train_accs.append(train_acc)
    val_accs.append(val_acc)
    learning_rates.append(optimizer.param_groups[0]['lr'])

    # Print progress
    print(f"Epoch {epoch+1}/{epochs}:")
    print(".4f")
    print(".4f")
    print(".6f")

    # Save best model
    if val_acc > best_acc:
        best_acc = val_acc
        patience_counter = 0
        torch.save({
            'epoch': epoch,
            'model_state_dict': model.state_dict(),
            'optimizer_state_dict': optimizer.state_dict(),
            'scheduler_state_dict': scheduler.state_dict(),
            'val_acc': val_acc,
            'val_loss': val_loss
        }, 'best_cifar10_model.pth')
        print("Saved best model!")
    else:
        patience_counter += 1

    # Early stopping
    if patience_counter >= patience:
        print(f"Early stopping at epoch {epoch+1}")
        break

training_time = time.time() - start_time
print(".2f")

# ================================
# 6. COMPREHENSIVE EVALUATION
# ================================

# Load best model
checkpoint = torch.load('best_cifar10_model.pth')
model.load_state_dict(checkpoint['model_state_dict'])
model = model.to(device)

def evaluate_comprehensive(model, test_loader, device, classes):
    model.eval()
    all_preds = []
    all_targets = []
    all_probs = []

    with torch.no_grad():
        for inputs, targets in test_loader:
            inputs, targets = inputs.to(device), targets.to(device)

            outputs = model(inputs)
            probs = torch.softmax(outputs, dim=1)
            _, preds = torch.max(outputs, 1)

            all_preds.extend(preds.cpu().numpy())
            all_targets.extend(targets.cpu().numpy())
            all_probs.extend(probs.cpu().numpy())

    all_preds = np.array(all_preds)
    all_targets = np.array(all_targets)
    all_probs = np.array(all_probs)

    # Calculate metrics
    accuracy = np.mean(all_preds == all_targets)

    # Per-class accuracy
    class_correct = np.zeros(10)
    class_total = np.zeros(10)
    for i in range(len(all_targets)):
        class_total[all_targets[i]] += 1
        if all_preds[i] == all_targets[i]:
            class_correct[all_targets[i]] += 1

    class_acc = class_correct / class_total

    return accuracy, class_acc, all_preds, all_targets, all_probs

# Evaluate
test_acc, class_acc, test_preds, test_targets, test_probs = evaluate_comprehensive(model, test_loader, device, classes)

print("\n" + "="*60)
print("FINAL TEST RESULTS")
print("="*60)
print(".4f")

print("\nPer-Class Accuracy:")
for i, acc in enumerate(class_acc):
    print("10s")

# Classification report
print("\nDetailed Classification Report:")
print(classification_report(test_targets, test_preds, target_names=classes))

# ================================
# 7. VISUALIZATION & ANALYSIS
# ================================

# Plot training curves
plt.figure(figsize=(16, 8))

plt.subplot(2, 3, 1)
plt.plot(train_losses, label='Train Loss')
plt.plot(val_losses, label='Val Loss')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.legend()
plt.title('Training & Validation Loss')

plt.subplot(2, 3, 2)
plt.plot(train_accs, label='Train Acc')
plt.plot(val_accs, label='Val Acc')
plt.xlabel('Epoch')
plt.ylabel('Accuracy (%)')
plt.legend()
plt.title('Training & Validation Accuracy')

plt.subplot(2, 3, 3)
plt.plot(learning_rates)
plt.xlabel('Epoch')
plt.ylabel('Learning Rate')
plt.title('Learning Rate Schedule')
plt.yscale('log')

# Confusion matrix
plt.subplot(2, 3, 4)
cm = confusion_matrix(test_targets, test_preds)
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=classes, yticklabels=classes)
plt.xlabel('Predicted')
plt.ylabel('True')
plt.title('Confusion Matrix')

# Per-class accuracy bar plot
plt.subplot(2, 3, 5)
plt.bar(classes, class_acc * 100)
plt.xlabel('Class')
plt.ylabel('Accuracy (%)')
plt.title('Per-Class Accuracy')
plt.xticks(rotation=45, ha='right')

# Sample predictions
plt.subplot(2, 3, 6)
dataiter = iter(test_loader)
images, labels = next(dataiter)
images, labels = images[:8], labels[:8]  # Show 8 images

outputs = model(images.to(device))
_, preds = torch.max(outputs, 1)
preds = preds.cpu().numpy()

for i in range(8):
    plt.subplot(2, 3, 6)
    plt.imshow(np.transpose(images[i].numpy() / 2 + 0.5, (1, 2, 0)))
    plt.title(f'True: {classes[labels[i]]}\nPred: {classes[preds[i]]}')
    plt.axis('off')

plt.tight_layout()
plt.savefig('cifar10_analysis.png', dpi=300, bbox_inches='tight')
plt.show()

# ================================
# 8. MODEL INTERPRETATION (Grad-CAM)
# ================================

def grad_cam(model, image, target_class, device):
    """Generate Grad-CAM visualization"""
    model.eval()

    # Hook to get gradients
    gradients = []
    def save_gradient(grad):
        gradients.append(grad)

    # Get the last conv layer
    final_conv = None
    for module in model.modules():
        if isinstance(module, nn.Conv2d):
            final_conv = module

    if final_conv is None:
        return None

    # Register hook
    handle = final_conv.register_backward_hook(lambda m, i, o: save_gradient(o[0]))

    # Forward pass
    image = image.unsqueeze(0).to(device)
    output = model(image)

    # Get target class score
    target_score = output[0, target_class]

    # Backward pass
    model.zero_grad()
    target_score.backward()

    # Get gradients and feature maps
    gradients = gradients[0].cpu().data.numpy()[0]
    feature_maps = final_conv.output.cpu().data.numpy()[0]

    # Global average pooling of gradients
    weights = np.mean(gradients, axis=(1, 2))

    # Weighted sum of feature maps
    cam = np.zeros(feature_maps.shape[1:], dtype=np.float32)
    for i, w in enumerate(weights):
        cam += w * feature_maps[i]

    # ReLU and normalize
    cam = np.maximum(cam, 0)
    cam = cam - np.min(cam)
    cam = cam / np.max(cam)

    handle.remove()
    return cam

# Visualize Grad-CAM for a few examples
plt.figure(figsize=(12, 8))
dataiter = iter(test_loader)
images, labels = next(dataiter)

for i in range(6):
    image, label = images[i], labels[i]

    # Get Grad-CAM
    cam = grad_cam(model, image, label.item(), device)

    if cam is not None:
        plt.subplot(2, 6, i+1)
        plt.imshow(np.transpose(image.numpy() / 2 + 0.5, (1, 2, 0)))
        plt.title(f'Original\n{classes[label]}')
        plt.axis('off')

        plt.subplot(2, 6, i+7)
        plt.imshow(cam, cmap='jet', alpha=0.5)
        plt.imshow(np.transpose(image.numpy() / 2 + 0.5, (1, 2, 0)), alpha=0.5)
        plt.title(f'Grad-CAM\n{classes[label]}')
        plt.axis('off')

plt.tight_layout()
plt.savefig('gradcam_visualization.png', dpi=300, bbox_inches='tight')
plt.show()

# ================================
# 9. SINGLE IMAGE PREDICTION
# ================================

def predict_single_image(model, image_path, transform, device, classes):
    """Predict class for a single image"""
    from PIL import Image

    model.eval()

    # Load and preprocess image
    image = Image.open(image_path).convert('RGB')
    image_tensor = transform(image).unsqueeze(0).to(device)

    # Predict
    with torch.no_grad():
        outputs = model(image_tensor)
        probs = torch.softmax(outputs, dim=1)[0]
        pred_class = torch.argmax(outputs, dim=1).item()
        confidence = probs[pred_class].item()

    return classes[pred_class], confidence, probs.cpu().numpy()

# Example usage (assuming you have an image)
# pred_class, confidence, all_probs = predict_single_image(
#     model, 'path/to/image.jpg', test_transform, device, classes
# )
# print(f"Predicted: {pred_class} (Confidence: {confidence:.2%})")

# ================================
# 10. MODEL EXPORT & DEPLOYMENT
# ================================

def save_model_for_deployment(model, transform, classes):
    """Save model and preprocessing for deployment"""
    # Save model weights
    torch.save(model.state_dict(), 'cifar10_model_weights.pth')

    # Save model architecture and metadata
    model_info = {
        'model_class': 'ModernCNN',
        'num_classes': len(classes),
        'classes': classes,
        'input_size': (3, 32, 32),
        'transform_mean': [0.4914, 0.4822, 0.4465],
        'transform_std': [0.2470, 0.2435, 0.2616]
    }

    torch.save(model_info, 'cifar10_model_info.pth')
    print("Model saved for deployment!")

save_model_for_deployment(model, test_transform, classes)

# ================================
# 11. PERFORMANCE COMPARISON
# ================================

def compare_models():
    """Compare different model architectures"""
    models_to_test = {
        'Simple CNN': nn.Sequential(
            nn.Conv2d(3, 32, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
            nn.Conv2d(32, 64, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
            nn.Flatten(), nn.Linear(64*8*8, 128), nn.ReLU(), nn.Linear(128, 10)
        ),
        'Our Modern CNN': model
    }

    results = {}

    for name, test_model in models_to_test.items():
        test_model = test_model.to(device)
        test_model.eval()

        correct = 0
        total = 0
        start_time = time.time()

        with torch.no_grad():
            for inputs, targets in test_loader:
                inputs, targets = inputs.to(device), targets.to(device)
                outputs = test_model(inputs)
                _, preds = torch.max(outputs, 1)
                correct += preds.eq(targets).sum().item()
                total += targets.size(0)

        accuracy = 100. * correct / total
        inference_time = time.time() - start_time

        results[name] = {
            'accuracy': accuracy,
            'inference_time': inference_time,
            'params': sum(p.numel() for p in test_model.parameters())
        }

    # Print comparison
    print("\n" + "="*60)
    print("MODEL COMPARISON")
    print("="*60)
    for name, metrics in results.items():
        print(f"{name}:")
        print(".2f")
        print(".2f")
        print(f"  Parameters: {metrics['params']:,}")

compare_models()
```

---

## 🐶 Example 2: Custom Dog Breed Classification

### **Problem**: Classify dog images into 120 different breeds

```python
# Similar structure but with:
# - Custom dataset class for loading dog images
# - 120 output classes
# - Data augmentation optimized for dogs
# - Transfer learning from ImageNet-pretrained models

class DogBreedDataset(Dataset):
    def __init__(self, image_paths, labels, transform=None):
        self.image_paths = image_paths
        self.labels = labels
        self.transform = transform

    def __len__(self):
        return len(self.image_paths)

    def __getitem__(self, idx):
        from PIL import Image
        image = Image.open(self.image_paths[idx]).convert('RGB')
        label = self.labels[idx]

        if self.transform:
            image = self.transform(image)

        return image, label

# Usage example
train_transform = transforms.Compose([
    transforms.Resize(256),
    transforms.RandomCrop(224),
    transforms.RandomHorizontalFlip(),
    transforms.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.2, hue=0.1),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

# Load Stanford Dogs dataset or your custom dog images
# train_dataset = DogBreedDataset(train_paths, train_labels, transform=train_transform)
```

---

## 🏥 Example 3: Medical Image Classification (Pneumonia Detection)

### **Problem**: Classify chest X-rays as normal or pneumonia

```python
# Critical for medical applications:
# - Handle class imbalance
# - Use weighted loss
# - Focus on recall (don't miss pneumonia cases)
# - Extensive data augmentation
# - Model interpretability

class MedicalCNN(nn.Module):
    def __init__(self, num_classes=2):
        super(MedicalCNN, self).__init__()
        # Architecture optimized for medical imaging
        # Focus on detecting subtle patterns
        # Use deeper networks with attention mechanisms
```

---

## 📋 CNN Pipeline Checklist

- [ ] **Data Loading**: torchvision datasets or custom Dataset class
- [ ] **Data Augmentation**: Random flips, crops, color jittering
- [ ] **Preprocessing**: Resize, normalize with dataset statistics
- [ ] **Model Architecture**: Conv blocks → Pooling → Flatten → Dense
- [ ] **Regularization**: BatchNorm, Dropout, weight decay
- [ ] **Loss Function**: CrossEntropyLoss for classification
- [ ] **Optimizer**: AdamW with weight decay
- [ ] **Learning Rate**: Cosine annealing scheduler
- [ ] **Training**: With validation, early stopping, gradient clipping
- [ ] **Evaluation**: Accuracy, per-class metrics, confusion matrix
- [ ] **Visualization**: Training curves, Grad-CAM, sample predictions
- [ ] **Model Saving**: Weights + preprocessing artifacts
- [ ] **Deployment**: Single image prediction function

---

## 💡 Pro Tips for CNN Projects

1. **Data Augmentation**: Essential for good generalization
2. **Batch Normalization**: Always use after Conv layers
3. **Skip Connections**: ResNet-style for deeper networks
4. **Progressive Resizing**: Train on small images first, then larger
5. **Transfer Learning**: Use pretrained models when possible
6. **Grad-CAM**: For model interpretability
7. **Mixed Precision**: Use torch.cuda.amp for faster training
8. **Multi-GPU**: Use DataParallel for multiple GPUs
9. **Model Ensembling**: Average predictions from multiple models
10. **Test Time Augmentation**: Average predictions over augmented versions

---

This covers **complete CNN pipelines** for real-world image classification! Adapt the examples to your specific image datasets and requirements.</content>
<parameter name="filePath">/mnt/Data/3-2/330 (ML lab)/Online 2/cheatsheets/complete_cnn_examples.md