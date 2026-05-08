---

# 📊 PyTorch Data Preprocessing Cheatsheet — From Raw Data to Training

This guide covers **data preprocessing** in PyTorch: cleaning data, splitting, and creating DataLoaders. Essential for any ML project!

---

## 🧹 1. BASIC DATA CLEANING WITH PANDAS

Before PyTorch, clean your data with pandas:

```python
import pandas as pd
import numpy as np

# ================================
# LOAD DATA
# ================================

# CSV file
df = pd.read_csv('data.csv')

# Excel file
df = pd.read_excel('data.xlsx')

# ================================
# INSPECT DATA
# ================================

print(df.head())        # First 5 rows
print(df.info())        # Data types, null values
print(df.describe())    # Statistics
print(df.shape)         # (rows, columns)

# ================================
# HANDLE MISSING VALUES
# ================================

# Check for nulls
print(df.isnull().sum())

# Drop rows with any nulls
df_clean = df.dropna()

# Fill nulls with mean (numeric columns)
df['column_name'] = df['column_name'].fillna(df['column_name'].mean())

# Fill nulls with mode (categorical)
df['category_col'] = df['category_col'].fillna(df['category_col'].mode()[0])

# ================================
# FILTER ROWS & COLUMNS
# ================================

# Filter rows by condition
adults = df[df['age'] >= 18]                    # Age >= 18
males = df[df['gender'] == 'male']              # Only males
high_salary = df[df['salary'] > 50000]          # Salary > 50k

# Multiple conditions
young_males = df[(df['age'] < 30) & (df['gender'] == 'male')]

# Filter by list of values
specific_cities = df[df['city'].isin(['NYC', 'LA', 'Chicago'])]

# ================================
# FILTER COLUMNS
# ================================

# Select specific columns
subset = df[['name', 'age', 'salary']]

# Drop columns
df_reduced = df.drop(['unnecessary_col1', 'unnecessary_col2'], axis=1)

# Select columns by type
numeric_cols = df.select_dtypes(include=[np.number]).columns
categorical_cols = df.select_dtypes(include=['object']).columns

# ================================
# REMOVE DUPLICATES
# ================================

# Check for duplicates
print(df.duplicated().sum())

# Remove duplicate rows
df_unique = df.drop_duplicates()

# Remove duplicates based on specific columns
df_unique_id = df.drop_duplicates(subset=['id'])

# ================================
# OUTLIER REMOVAL
# ================================

# Using IQR method (Interquartile Range)
Q1 = df['salary'].quantile(0.25)
Q3 = df['salary'].quantile(0.75)
IQR = Q3 - Q1

lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

df_no_outliers = df[(df['salary'] >= lower_bound) & (df['salary'] <= upper_bound)]

# ================================
# DATA TYPE CONVERSION
# ================================

# Convert to numeric
df['numeric_col'] = pd.to_numeric(df['numeric_col'], errors='coerce')

# Convert to categorical
df['category_col'] = df['category_col'].astype('category')

# Convert to datetime
df['date_col'] = pd.to_datetime(df['date_col'])

# ================================
# ENCODING CATEGORICAL VARIABLES
# ================================

# Label Encoding (for ordinal categories)
from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()
df['size_encoded'] = le.fit_transform(df['size'])  # S=0, M=1, L=2, XL=3

# One-Hot Encoding (for nominal categories)
df_encoded = pd.get_dummies(df, columns=['color', 'brand'])

# ================================
# FEATURE SCALING
# ================================

from sklearn.preprocessing import StandardScaler, MinMaxScaler

# StandardScaler: mean=0, std=1
scaler = StandardScaler()
df[['age_scaled', 'salary_scaled']] = scaler.fit_transform(df[['age', 'salary']])

# MinMaxScaler: 0 to 1 range
minmax = MinMaxScaler()
df[['age_minmax', 'salary_minmax']] = minmax.fit_transform(df[['age', 'salary']])
```

---

## ✂️ 2. TRAIN/TEST SPLIT

```python
from sklearn.model_selection import train_test_split
import torch

# ================================
# BASIC TRAIN/TEST SPLIT
# ================================

# Features (X) and target (y)
X = df.drop('target_column', axis=1)
y = df['target_column']

# 80% train, 20% test
X_train, X_test, y_train, y_test = train_test_split(
    X, y, 
    test_size=0.2,      # 20% for testing
    random_state=42,    # For reproducibility
    stratify=y          # Keep class distribution same
)

print(f"Train shape: {X_train.shape}, Test shape: {X_test.shape}")

# ================================
# TRAIN/VALIDATION/TEST SPLIT
# ================================

# First split: train+val vs test
X_temp, X_test, y_temp, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Second split: train vs validation
X_train, X_val, y_train, y_val = train_test_split(
    X_temp, y_temp, test_size=0.25, random_state=42, stratify=y_temp
)  # 0.25 * 0.8 = 0.2 of original

print(f"Train: {X_train.shape}, Val: {X_val.shape}, Test: {X_test.shape}")

# ================================
# TIME SERIES SPLIT (if data has time order)
# ================================

# For time series, don't shuffle!
X_train, X_test, y_train, y_test = train_test_split(
    X, y, 
    test_size=0.2, 
    shuffle=False,      # Keep time order
    random_state=42
)

# ================================
# CONVERT TO PYTORCH TENSORS
# ================================

# Convert pandas to numpy, then to torch
X_train_tensor = torch.FloatTensor(X_train.values)
y_train_tensor = torch.LongTensor(y_train.values)

X_test_tensor = torch.FloatTensor(X_test.values)
y_test_tensor = torch.LongTensor(y_test.values)

print(f"Train tensor shape: {X_train_tensor.shape}")
```

---

## 🏗️ 3. PYTORCH DATASET CLASS

```python
from torch.utils.data import Dataset, DataLoader
import torch

# ================================
# BASIC DATASET CLASS
# ================================

class CustomDataset(Dataset):
    def __init__(self, features, labels, transform=None):
        """
        Args:
            features: numpy array or tensor of shape (n_samples, n_features)
            labels: numpy array or tensor of shape (n_samples,)
            transform: optional transforms to apply
        """
        self.features = torch.FloatTensor(features) if not isinstance(features, torch.Tensor) else features
        self.labels = torch.LongTensor(labels) if not isinstance(labels, torch.Tensor) else labels
        self.transform = transform
    
    def __len__(self):
        """Return total number of samples"""
        return len(self.features)
    
    def __getitem__(self, idx):
        """Return one sample"""
        feature = self.features[idx]
        label = self.labels[idx]
        
        if self.transform:
            feature = self.transform(feature)
        
        return feature, label

# ================================
# USAGE EXAMPLE
# ================================

# Create datasets
train_dataset = CustomDataset(X_train.values, y_train.values)
test_dataset = CustomDataset(X_test.values, y_test.values)

print(f"Dataset size: {len(train_dataset)}")
print(f"Sample shape: {train_dataset[0][0].shape}")  # Feature shape
print(f"Sample label: {train_dataset[0][1]}")        # Label

# ================================
# DATASET WITH AUGMENTATION (for images)
# ================================

import torchvision.transforms as transforms

class ImageDataset(Dataset):
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

# With data augmentation
train_transform = transforms.Compose([
    transforms.RandomHorizontalFlip(),    # Random flip
    transforms.RandomRotation(10),        # Random rotation
    transforms.ToTensor(),
    transforms.Normalize(mean, std)
])

train_dataset = ImageDataset(train_paths, train_labels, transform=train_transform)
```

---

## 🔄 4. PYTORCH DATALOADER

```python
from torch.utils.data import DataLoader

# ================================
# BASIC DATALOADER
# ================================

# Create DataLoader
train_loader = DataLoader(
    dataset=train_dataset,     # Your dataset
    batch_size=32,             # Number of samples per batch
    shuffle=True,              # Shuffle data each epoch
    num_workers=2,             # Parallel data loading (0 for Windows)
    drop_last=False            # Drop last incomplete batch
)

test_loader = DataLoader(
    dataset=test_dataset,
    batch_size=32,
    shuffle=False,             # Don't shuffle test data
    num_workers=2
)

# ================================
# ITERATE THROUGH DATALOADER
# ================================

# Training loop
for epoch in range(10):
    for batch_idx, (features, labels) in enumerate(train_loader):
        # features shape: (batch_size, n_features)
        # labels shape: (batch_size,)
        
        # Your training code here
        outputs = model(features)
        loss = criterion(outputs, labels)
        # ... backprop ...
        
        if batch_idx % 100 == 0:
            print(f"Epoch {epoch}, Batch {batch_idx}, Loss: {loss.item():.4f}")

# ================================
# DATALOADER WITH SAMPLERS
# ================================

from torch.utils.data import WeightedRandomSampler

# For imbalanced datasets
class_counts = np.bincount(y_train)
class_weights = 1.0 / class_counts
sample_weights = class_weights[y_train]

sampler = WeightedRandomSampler(
    weights=sample_weights,
    num_samples=len(sample_weights),
    replacement=True
)

balanced_loader = DataLoader(
    train_dataset, 
    batch_size=32, 
    sampler=sampler  # Use sampler instead of shuffle
)

# ================================
# MULTIPLE DATALOADERS
# ================================

# Different batch sizes for different phases
train_loader = DataLoader(train_dataset, batch_size=64, shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=32, shuffle=False)
test_loader = DataLoader(test_dataset, batch_size=1, shuffle=False)  # Batch size 1 for testing

# ================================
# CUSTOM COLLATE FUNCTION
# ================================

def custom_collate(batch):
    """Custom function to combine samples into batch"""
    features = [item[0] for item in batch]
    labels = [item[1] for item in batch]
    
    # Custom processing here
    features = torch.stack(features)
    labels = torch.tensor(labels)
    
    return features, labels

custom_loader = DataLoader(
    dataset, 
    batch_size=32, 
    collate_fn=custom_collate
)
```

---

## 📋 COMPLETE PIPELINE EXAMPLE

```python
import pandas as pd
import numpy as np
import torch
from torch.utils.data import Dataset, DataLoader
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# ================================
# COMPLETE WORKFLOW
# ================================

# 1. Load and clean data
df = pd.read_csv('data.csv')
df = df.dropna()  # Remove nulls
df = df.drop_duplicates()  # Remove duplicates

# 2. Feature engineering
X = df.drop('target', axis=1)
y = df['target']

# 3. Encode categorical variables
X_encoded = pd.get_dummies(X, columns=['categorical_col'])

# 4. Scale features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_encoded)

# 5. Train/test split
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, random_state=42, stratify=y
)

# 6. Create PyTorch Dataset
class TabularDataset(Dataset):
    def __init__(self, features, labels):
        self.features = torch.FloatTensor(features)
        self.labels = torch.LongTensor(labels.values)
    
    def __len__(self):
        return len(self.features)
    
    def __getitem__(self, idx):
        return self.features[idx], self.labels[idx]

train_dataset = TabularDataset(X_train, y_train)
test_dataset = TabularDataset(X_test, y_test)

# 7. Create DataLoaders
train_loader = DataLoader(train_dataset, batch_size=64, shuffle=True)
test_loader = DataLoader(test_dataset, batch_size=64, shuffle=False)

# 8. Ready for training!
print(f"Train batches: {len(train_loader)}")
print(f"Test batches: {len(test_loader)}")
print(f"Batch shape: {next(iter(train_loader))[0].shape}")
```

---

## 💡 PREPROCESSING CHECKLIST

- [ ] **Load data**: CSV, Excel, or other format
- [ ] **Inspect data**: head(), info(), describe()
- [ ] **Handle missing values**: dropna() or fillna()
- [ ] **Remove duplicates**: drop_duplicates()
- [ ] **Filter data**: Select relevant rows/columns
- [ ] **Encode categories**: Label encoding or one-hot
- [ ] **Scale features**: StandardScaler or MinMaxScaler
- [ ] **Split data**: train_test_split()
- [ ] **Create Dataset**: Custom Dataset class
- [ ] **Create DataLoader**: With appropriate batch_size
- [ ] **Verify shapes**: Check tensor dimensions

**Common Issues:**
- **Memory errors**: Reduce batch_size
- **Shape mismatches**: Check tensor dimensions
- **Slow loading**: Use num_workers > 0
- **Imbalanced data**: Use WeightedRandomSampler

---

This covers everything from raw CSV to PyTorch DataLoader ready for training!

---</content>
<parameter name="filePath">/mnt/Data/3-2/330 (ML lab)/Online 2/cheatsheets/data_preprocessing_tutorial.md