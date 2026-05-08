# 📊 Dataset vs DataLoader — PyTorch Data Pipeline

**Understanding the difference between Dataset and DataLoader** — the foundation of PyTorch data handling.

---

## 🎯 **The Core Difference**

| **Dataset** | **DataLoader** |
|-------------|----------------|
| **What it is**: Container for your raw data | **What it is**: Iterator that feeds data to your model |
| **What it does**: Stores data & defines how to access samples | **What it does**: Batches data & handles parallel loading |
| **Returns**: Single sample `(data, label)` | **Returns**: Batch of samples `(batch_data, batch_labels)` |

---

## 📦 **Dataset: Your Data Container**

### **What is a Dataset?**
A Dataset tells PyTorch **how to access your data**. It defines:
- How many samples you have (`__len__`)
- How to get a specific sample (`__getitem__`)

### **Built-in Datasets**
```python
from torchvision import datasets

# CIFAR-10 dataset
dataset = datasets.CIFAR10(root='./data', train=True, download=True)

print(f"Total samples: {len(dataset)}")  # → 50000
sample_image, sample_label = dataset[0]  # Get first sample
```

### **Custom Dataset**
```python
from torch.utils.data import Dataset

class MyDataset(Dataset):
    def __init__(self, data_paths, labels):
        self.data_paths = data_paths
        self.labels = labels
    
    def __len__(self):
        return len(self.data_paths)
    
    def __getitem__(self, idx):
        # Load data for sample at index 'idx'
        image = load_image(self.data_paths[idx])
        label = self.labels[idx]
        return image, label  # ← Dataset defines what gets returned
```

---

## 🔄 **DataLoader: Your Data Iterator**

### **What is a DataLoader?**
A DataLoader takes your Dataset and **batches it for training**:
- Groups samples into batches
- Shuffles data (optional)
- Loads data in parallel (optional)
- Moves data to GPU (when you call `.to(device)`)

### **Creating a DataLoader**
```python
from torch.utils.data import DataLoader

# Wrap your dataset in a DataLoader
train_loader = DataLoader(
    dataset=dataset,           # Your Dataset object
    batch_size=32,             # How many samples per batch
    shuffle=True,              # Randomize order each epoch
    num_workers=4,             # Parallel data loading
    pin_memory=True            # Faster GPU transfer
)
```

### **Using the DataLoader**
```python
for images, labels in train_loader:
    # images: (batch_size, channels, height, width) → (32, 3, 32, 32)
    # labels: (batch_size,) → (32,)
    
    # Move to GPU
    images, labels = images.to(device), labels.to(device)
    
    # Forward pass...
    outputs = model(images)
```

---

## 🚀 **Why Both Are Needed**

### **Without DataLoader (Manual Batching)**
```python
# Inefficient and error-prone
batch_size = 32
for i in range(0, len(dataset), batch_size):
    batch_data = []
    batch_labels = []
    for j in range(i, min(i + batch_size, len(dataset))):
        data, label = dataset[j]
        batch_data.append(data)
        batch_labels.append(label)
    
    # Stack into tensors...
    batch_data = torch.stack(batch_data)
    batch_labels = torch.tensor(batch_labels)
```

### **With DataLoader (Automatic Batching)**
```python
# Clean and efficient
for images, labels in train_loader:
    # DataLoader handles everything!
    pass
```

---

## 📋 **Key Parameters**

### **DataLoader Parameters**
```python
DataLoader(
    dataset,              # Your Dataset
    batch_size=32,        # Samples per batch
    shuffle=True,         # Randomize order
    num_workers=4,        # Parallel workers
    pin_memory=True,      # GPU optimization
    drop_last=False,      # Drop incomplete batches
    sampler=None,         # Custom sampling strategy
    collate_fn=None       # Custom batch collation
)
```

### **When to Use What**
- **`shuffle=True`**: Training (prevents overfitting)
- **`shuffle=False`**: Validation/Testing (consistent results)
- **`num_workers > 0`**: Large datasets (parallel loading)
- **`pin_memory=True`**: GPU training (faster transfer)

---

## 🎨 **Visual Flow**

```
Raw Data → Dataset → DataLoader → Model
                    ↑           ↑
              __getitem__   Batches data
              __len__       Handles iteration
```

**Dataset**: "Here's how to access sample #5"  
**DataLoader**: "Here's batch #3 with 32 samples"

---

## 💡 **Common Patterns**

### **Train/Val/Test Split**
```python
from torch.utils.data import random_split

# Split dataset
train_size = int(0.8 * len(dataset))
val_size = len(dataset) - train_size
train_dataset, val_dataset = random_split(dataset, [train_size, val_size])

# Create loaders
train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=32, shuffle=False)
```

### **Custom Collate Function**
```python
def my_collate(batch):
    # Custom batch processing (e.g., for variable-length sequences)
    data = [item[0] for item in batch]
    labels = [item[1] for item in batch]
    return torch.stack(data), torch.tensor(labels)

loader = DataLoader(dataset, collate_fn=my_collate, ...)
```

---

## ⚡ **Performance Tips**

1. **Use `num_workers > 0`** for large datasets
2. **Set `pin_memory=True`** for GPU training  
3. **Choose `batch_size`** that fits in GPU memory
4. **Use `shuffle=True`** only for training
5. **Consider `drop_last=True`** if batch size must be consistent

---

**Dataset stores your data, DataLoader feeds it to your model!** 🎯</content>
<parameter name="filePath">/mnt/Data/3-2/330 (ML lab)/Online 2/cheatsheets/dataset_vs_dataloader.md