---

# 🔬 Complete DNN Examples — From Raw Data to Production

**Full end-to-end examples** of Deep Neural Networks covering preprocessing, training, testing, and deployment.

---

## 📊 Example 1: Binary Classification (Predict Loan Default)

### **Problem**: Predict if a loan applicant will default (0=No, 1=Yes)

```python
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
import matplotlib.pyplot as plt

# ================================
# 1. DATA LOADING & PREPROCESSING
# ================================

# Load dataset (assuming CSV with loan data)
df = pd.read_csv('loan_data.csv')

# Inspect data
print("Dataset shape:", df.shape)
print("Columns:", df.columns.tolist())
print("Missing values:\n", df.isnull().sum())

# Handle missing values
df = df.dropna()  # Simple approach - drop missing values

# Encode categorical variables
categorical_cols = ['employment_type', 'education_level', 'marital_status']
label_encoders = {}

for col in categorical_cols:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    label_encoders[col] = le

# Separate features and target
X = df.drop(['loan_id', 'default'], axis=1)  # Drop ID and target
y = df['default']

# Train/validation/test split
X_temp, X_test, y_temp, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
X_train, X_val, y_train, y_val = train_test_split(X_temp, y_temp, test_size=0.25, random_state=42, stratify=y_temp)

print(f"Train: {X_train.shape}, Val: {X_val.shape}, Test: {X_test.shape}")

# Scale features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_val_scaled = scaler.transform(X_val)
X_test_scaled = scaler.transform(X_test)

# ================================
# 2. PYTORCH DATASET CLASS
# ================================

class LoanDataset(Dataset):
    def __init__(self, features, labels):
        self.features = torch.FloatTensor(features)
        self.labels = torch.FloatTensor(labels.values).unsqueeze(1)  # Shape: (N, 1)

    def __len__(self):
        return len(self.features)

    def __getitem__(self, idx):
        return self.features[idx], self.labels[idx]

# Create datasets
train_dataset = LoanDataset(X_train_scaled, y_train)
val_dataset = LoanDataset(X_val_scaled, y_val)
test_dataset = LoanDataset(X_test_scaled, y_test)

# Create data loaders
batch_size = 64
train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False)
test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False)

# ================================
# 3. MODEL ARCHITECTURE
# ================================

class LoanDefaultPredictor(nn.Module):
    def __init__(self, input_size):
        super(LoanDefaultPredictor, self).__init__()

        # Deep architecture for complex patterns
        self.layers = nn.Sequential(
            nn.Linear(input_size, 128),
            nn.BatchNorm1d(128),  # Normalize activations
            nn.ReLU(),
            nn.Dropout(0.3),     # Prevent overfitting

            nn.Linear(128, 64),
            nn.BatchNorm1d(64),
            nn.ReLU(),
            nn.Dropout(0.2),

            nn.Linear(64, 32),
            nn.ReLU(),
            nn.Dropout(0.1),

            nn.Linear(32, 1),
            nn.Sigmoid()         # Binary output (0-1)
        )

    def forward(self, x):
        return self.layers(x)

# Initialize model
input_size = X_train.shape[1]
model = LoanDefaultPredictor(input_size)
print(f"Model input size: {input_size}")

# ================================
# 4. LOSS & OPTIMIZER
# ================================

criterion = nn.BCELoss()  # Binary Cross Entropy Loss
optimizer = optim.Adam(model.parameters(), lr=0.001, weight_decay=1e-4)

# Learning rate scheduler
scheduler = optim.lr_scheduler.ReduceLROnPlateau(
    optimizer, mode='min', factor=0.5, patience=5, verbose=True
)

# ================================
# 5. TRAINING LOOP
# ================================

def train_epoch(model, train_loader, criterion, optimizer, device):
    model.train()
    total_loss = 0
    correct = 0
    total = 0

    for features, labels in train_loader:
        features, labels = features.to(device), labels.to(device)

        optimizer.zero_grad()
        outputs = model(features)
        loss = criterion(outputs, labels)

        loss.backward()
        optimizer.step()

        total_loss += loss.item()
        predicted = (outputs > 0.5).float()
        correct += (predicted == labels).sum().item()
        total += labels.size(0)

    avg_loss = total_loss / len(train_loader)
    accuracy = correct / total
    return avg_loss, accuracy

def validate_epoch(model, val_loader, criterion, device):
    model.eval()
    total_loss = 0
    correct = 0
    total = 0

    with torch.no_grad():
        for features, labels in val_loader:
            features, labels = features.to(device), labels.to(device)

            outputs = model(features)
            loss = criterion(outputs, labels)

            total_loss += loss.item()
            predicted = (outputs > 0.5).float()
            correct += (predicted == labels).sum().item()
            total += labels.size(0)

    avg_loss = total_loss / len(val_loader)
    accuracy = correct / total
    return avg_loss, accuracy

# Training setup
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = model.to(device)

epochs = 50
best_val_loss = float('inf')
patience = 10
patience_counter = 0

# Track metrics
train_losses = []
val_losses = []
train_accs = []
val_accs = []

print("Starting training...")
for epoch in range(epochs):
    # Train
    train_loss, train_acc = train_epoch(model, train_loader, criterion, optimizer, device)

    # Validate
    val_loss, val_acc = validate_epoch(model, val_loader, criterion, optimizer, device)

    # Store metrics
    train_losses.append(train_loss)
    val_losses.append(val_loss)
    train_accs.append(train_acc)
    val_accs.append(val_acc)

    # Learning rate scheduling
    scheduler.step(val_loss)

    # Print progress
    if (epoch + 1) % 5 == 0:
        print(f"Epoch {epoch+1}/{epochs}")
        print(".4f")
        print(".4f")

    # Early stopping
    if val_loss < best_val_loss:
        best_val_loss = val_loss
        patience_counter = 0
        torch.save(model.state_dict(), 'best_loan_model.pth')
    else:
        patience_counter += 1
        if patience_counter >= patience:
            print(f"Early stopping at epoch {epoch+1}")
            break

# ================================
# 6. EVALUATION ON TEST SET
# ================================

def evaluate_model(model, test_loader, device):
    model.eval()
    all_preds = []
    all_labels = []
    all_probs = []

    with torch.no_grad():
        for features, labels in test_loader:
            features, labels = features.to(device), labels.to(device)

            outputs = model(features)
            probs = outputs.squeeze().cpu().numpy()
            preds = (outputs > 0.5).float().squeeze().cpu().numpy()
            labels = labels.squeeze().cpu().numpy()

            all_preds.extend(preds)
            all_labels.extend(labels)
            all_probs.extend(probs)

    return np.array(all_preds), np.array(all_labels), np.array(all_probs)

# Load best model
model.load_state_dict(torch.load('best_loan_model.pth'))

# Evaluate
test_preds, test_labels, test_probs = evaluate_model(model, test_loader, device)

# Calculate metrics
accuracy = accuracy_score(test_labels, test_preds)
precision = precision_score(test_labels, test_preds)
recall = recall_score(test_labels, test_preds)
f1 = f1_score(test_labels, test_preds)
auc = roc_auc_score(test_labels, test_probs)

print("\n" + "="*50)
print("TEST RESULTS")
print("="*50)
print(".4f")
print(".4f")
print(".4f")
print(".4f")
print(".4f")

# ================================
# 7. VISUALIZATION & ANALYSIS
# ================================

# Plot training curves
plt.figure(figsize=(12, 4))

plt.subplot(1, 2, 1)
plt.plot(train_losses, label='Train Loss')
plt.plot(val_losses, label='Val Loss')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.legend()
plt.title('Training & Validation Loss')

plt.subplot(1, 2, 2)
plt.plot(train_accs, label='Train Acc')
plt.plot(val_accs, label='Val Acc')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.legend()
plt.title('Training & Validation Accuracy')

plt.tight_layout()
plt.savefig('training_curves.png', dpi=300, bbox_inches='tight')
plt.show()

# ================================
# 8. MODEL INTERPRETATION
# ================================

# Feature importance (simple approach - using weights)
def get_feature_importance(model, feature_names):
    """Get feature importance based on absolute weights of first layer"""
    first_layer_weights = model.layers[0].weight.data.abs().mean(dim=0).cpu().numpy()
    importance_dict = dict(zip(feature_names, first_layer_weights))
    return sorted(importance_dict.items(), key=lambda x: x[1], reverse=True)

feature_names = X_train.columns.tolist()
feature_importance = get_feature_importance(model, feature_names)

print("\nTop 10 Most Important Features:")
for feature, importance in feature_importance[:10]:
    print(".4f")

# ================================
# 9. PREDICTION ON NEW DATA
# ================================

def predict_single_loan(model, scaler, new_data, device):
    """
    Predict loan default probability for new applicant

    Args:
        model: Trained PyTorch model
        scaler: Fitted StandardScaler
        new_data: Dict of feature values
        device: torch device
    """
    model.eval()

    # Convert to DataFrame (assuming same structure)
    df_new = pd.DataFrame([new_data])

    # Encode categorical variables
    for col in categorical_cols:
        if col in df_new.columns:
            df_new[col] = label_encoders[col].transform(df_new[col])

    # Scale features
    features_scaled = scaler.transform(df_new)

    # Convert to tensor
    features_tensor = torch.FloatTensor(features_scaled).to(device)

    # Predict
    with torch.no_grad():
        prob = model(features_tensor).item()

    return prob

# Example prediction
new_applicant = {
    'age': 35,
    'income': 75000,
    'credit_score': 720,
    'employment_type': 'salaried',
    'education_level': 'bachelors',
    'marital_status': 'married',
    'loan_amount': 250000,
    'loan_term': 60
}

default_probability = predict_single_loan(model, scaler, new_applicant, device)
print(".2%")

# ================================
# 10. MODEL DEPLOYMENT PREPARATION
# ================================

def save_model_artifacts(model, scaler, label_encoders, feature_names):
    """Save all necessary artifacts for deployment"""
    torch.save(model.state_dict(), 'loan_model_weights.pth')

    # Save preprocessing artifacts
    artifacts = {
        'scaler': scaler,
        'label_encoders': label_encoders,
        'feature_names': feature_names,
        'input_size': len(feature_names),
        'model_class': 'LoanDefaultPredictor'
    }

    torch.save(artifacts, 'model_artifacts.pth')
    print("Model artifacts saved!")

save_model_artifacts(model, scaler, label_encoders, feature_names)
```

---

## 🏷️ Example 2: Multiclass Classification (Predict Customer Churn)

### **Problem**: Predict customer churn level (0=Stay, 1=Churn Soon, 2=Churn Now)

```python
# Similar structure but with CrossEntropyLoss and 3 output classes
class ChurnPredictor(nn.Module):
    def __init__(self, input_size, num_classes=3):
        super(ChurnPredictor, self).__init__()
        self.layers = nn.Sequential(
            nn.Linear(input_size, 256),
            nn.BatchNorm1d(256),
            nn.ReLU(),
            nn.Dropout(0.4),

            nn.Linear(256, 128),
            nn.BatchNorm1d(128),
            nn.ReLU(),
            nn.Dropout(0.3),

            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Dropout(0.2),

            nn.Linear(64, num_classes)  # No activation - CrossEntropyLoss handles it
        )

    def forward(self, x):
        return self.layers(x)

# Usage
model = ChurnPredictor(input_size=X_train.shape[1], num_classes=3)
criterion = nn.CrossEntropyLoss()  # For multiclass
optimizer = optim.Adam(model.parameters(), lr=0.001)

# Training loop similar to binary classification
# But predictions: torch.argmax(outputs, dim=1)
```

---

## 📈 Example 3: Regression (Predict House Prices)

### **Problem**: Predict house sale price (continuous value)

```python
class HousePricePredictor(nn.Module):
    def __init__(self, input_size):
        super(HousePricePredictor, self).__init__()
        self.layers = nn.Sequential(
            nn.Linear(input_size, 256),
            nn.BatchNorm1d(256),
            nn.ReLU(),
            nn.Dropout(0.3),

            nn.Linear(256, 128),
            nn.BatchNorm1d(128),
            nn.ReLU(),
            nn.Dropout(0.2),

            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Dropout(0.1),

            nn.Linear(64, 1)  # No activation for regression
        )

    def forward(self, x):
        return self.layers(x)

# Usage
model = HousePricePredictor(input_size=X_train.shape[1])
criterion = nn.MSELoss()  # Mean Squared Error for regression
optimizer = optim.Adam(model.parameters(), lr=0.01)  # Higher LR for regression

# Training loop similar, but evaluate with RMSE, MAE, R² metrics
```

---

## 📋 DNN Pipeline Checklist

- [ ] **Data Loading**: CSV/Excel → pandas DataFrame
- [ ] **Data Cleaning**: Handle nulls, duplicates, outliers
- [ ] **Feature Engineering**: Encode categoricals, scale features
- [ ] **Train/Val/Test Split**: Stratified for classification
- [ ] **PyTorch Dataset**: Custom class for data loading
- [ ] **DataLoader**: Batch processing with shuffling
- [ ] **Model Architecture**: Appropriate layers for problem type
- [ ] **Loss Function**: BCELoss (binary), CrossEntropyLoss (multiclass), MSELoss (regression)
- [ ] **Optimizer**: Adam with weight decay
- [ ] **Training Loop**: With validation and early stopping
- [ ] **Evaluation**: Accuracy, precision, recall, F1, AUC
- [ ] **Visualization**: Training curves, feature importance
- [ ] **Model Saving**: Weights + preprocessing artifacts
- [ ] **Inference**: Single prediction function

---

## 💡 Pro Tips for DNN Projects

1. **Start Simple**: Begin with basic architecture, add complexity if needed
2. **Batch Normalization**: Almost always helps convergence
3. **Dropout**: Essential for preventing overfitting (0.2-0.5)
4. **Early Stopping**: Monitor validation loss, stop when it increases
5. **Learning Rate Scheduling**: Reduce LR when validation plateaus
6. **Feature Scaling**: Critical for neural networks
7. **Class Imbalance**: Use weighted loss or oversampling if needed
8. **Model Interpretability**: Analyze feature importance for business insights

---

This covers **complete DNN pipelines** for real-world problems! Adapt the examples to your specific datasets and requirements.</content>
<parameter name="filePath">/mnt/Data/3-2/330 (ML lab)/Online 2/cheatsheets/complete_dnn_examples.md