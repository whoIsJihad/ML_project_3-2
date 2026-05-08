# Evaluation Metrics Guide

## 🎯 Why Evaluation Matters

When comparing ensemble methods and hyperparameters, you need to:
1. **Measure performance** accurately
2. **Compare fairly** across methods
3. **Understand tradeoffs** (speed vs accuracy, bias vs variance)

---

## 📊 Classification Metrics

### 1. Accuracy

**What**: Percentage of correct predictions

```python
from sklearn.metrics import accuracy_score

y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy:.4f}")
```

**When to use**: Balanced datasets

**Warning**: Misleading for imbalanced data!
- Example: 95% of data is class 0 → Predict all 0 → 95% accuracy (but useless!)

---

### 2. Precision, Recall, F1-Score

```python
from sklearn.metrics import precision_score, recall_score, f1_score, classification_report

y_pred = model.predict(X_test)

precision = precision_score(y_test, y_pred, average='binary')  # or 'macro', 'weighted'
recall = recall_score(y_test, y_pred, average='binary')
f1 = f1_score(y_test, y_pred, average='binary')

print(f"Precision: {precision:.4f}")
print(f"Recall: {recall:.4f}")
print(f"F1-Score: {f1:.4f}")

# Complete report
print(classification_report(y_test, y_pred))
```

**Formulas**:
- **Precision** = TP / (TP + FP) - "Of predicted positives, how many are correct?"
- **Recall** = TP / (TP + FN) - "Of actual positives, how many did we find?"
- **F1** = 2 × (Precision × Recall) / (Precision + Recall) - Harmonic mean

**When to use**:
- **Precision**: When false positives are costly (spam detection)
- **Recall**: When false negatives are costly (disease detection)
- **F1**: Balance between precision and recall

---

### 3. ROC AUC (Area Under ROC Curve)

```python
from sklearn.metrics import roc_auc_score, roc_curve
import matplotlib.pyplot as plt

# Get probability predictions
y_pred_proba = model.predict_proba(X_test)[:, 1]  # Probability of positive class

# Calculate AUC
auc = roc_auc_score(y_test, y_pred_proba)
print(f"ROC AUC: {auc:.4f}")

# Plot ROC curve
fpr, tpr, thresholds = roc_curve(y_test, y_pred_proba)

plt.figure(figsize=(8, 6))
plt.plot(fpr, tpr, linewidth=2, label=f'Model (AUC = {auc:.4f})')
plt.plot([0, 1], [0, 1], 'k--', label='Random (AUC = 0.5)')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC Curve')
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()
```

**When to use**: Comparing models on imbalanced data

**Interpretation**:
- AUC = 1.0 → Perfect classifier
- AUC = 0.5 → Random classifier
- AUC > 0.8 → Good classifier

---

### 4. Confusion Matrix

```python
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay

y_pred = model.predict(X_test)
cm = confusion_matrix(y_test, y_pred)

print("Confusion Matrix:")
print(cm)

# Visualize
disp = ConfusionMatrixDisplay(confusion_matrix=cm)
disp.plot(cmap='Blues')
plt.title('Confusion Matrix')
plt.show()
```

**Interpretation**:
```
                Predicted
                0       1
Actual  0      TN      FP
        1      FN      TP
```

---

## 📈 Regression Metrics

### 1. Mean Squared Error (MSE) and RMSE

```python
from sklearn.metrics import mean_squared_error
import numpy as np

y_pred = model.predict(X_test)

mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)

print(f"MSE: {mse:.4f}")
print(f"RMSE: {rmse:.4f}")
```

**RMSE** is in same units as target → easier to interpret

---

### 2. Mean Absolute Error (MAE)

```python
from sklearn.metrics import mean_absolute_error

mae = mean_absolute_error(y_test, y_pred)
print(f"MAE: {mae:.4f}")
```

**Less sensitive to outliers** than MSE

---

### 3. R² Score (Coefficient of Determination)

```python
from sklearn.metrics import r2_score

r2 = r2_score(y_test, y_pred)
print(f"R² Score: {r2:.4f}")
```

**Interpretation**:
- R² = 1.0 → Perfect predictions
- R² = 0.0 → Model is as good as predicting mean
- R² < 0.0 → Model is worse than predicting mean

**Formula**: R² = 1 - (SS_residual / SS_total)

---

## 🔄 Cross-Validation

**Why**: Single train-test split can be misleading (lucky/unlucky split)

### K-Fold Cross-Validation

```python
from sklearn.model_selection import cross_val_score

# 5-fold CV
scores = cross_val_score(model, X_train, y_train, 
                        cv=5, scoring='accuracy')

print(f"CV Scores: {scores}")
print(f"Mean: {scores.mean():.4f}")
print(f"Std: {scores.std():.4f}")
print(f"95% CI: {scores.mean():.4f} +/- {1.96 * scores.std():.4f}")
```

### Multiple Metrics with Cross-Validation

```python
from sklearn.model_selection import cross_validate

scoring = ['accuracy', 'precision', 'recall', 'f1', 'roc_auc']

cv_results = cross_validate(model, X_train, y_train,
                           cv=5, scoring=scoring,
                           return_train_score=True)

for metric in scoring:
    test_scores = cv_results[f'test_{metric}']
    print(f"{metric}: {test_scores.mean():.4f} (+/- {test_scores.std():.4f})")
```

---

## 📉 Learning Curves

**Purpose**: Diagnose bias/variance (overfitting/underfitting)

```python
from sklearn.model_selection import learning_curve
import numpy as np
import matplotlib.pyplot as plt

# Generate learning curve data
train_sizes, train_scores, val_scores = learning_curve(
    model, X_train, y_train,
    train_sizes=np.linspace(0.1, 1.0, 10),
    cv=5,
    scoring='accuracy',
    n_jobs=-1
)

# Calculate means and std
train_mean = train_scores.mean(axis=1)
train_std = train_scores.std(axis=1)
val_mean = val_scores.mean(axis=1)
val_std = val_scores.std(axis=1)

# Plot
plt.figure(figsize=(10, 6))
plt.plot(train_sizes, train_mean, 'o-', label='Training Score', linewidth=2)
plt.fill_between(train_sizes, train_mean - train_std, train_mean + train_std, alpha=0.3)

plt.plot(train_sizes, val_mean, 'o-', label='Validation Score', linewidth=2)
plt.fill_between(train_sizes, val_mean - val_std, val_mean + val_std, alpha=0.3)

plt.xlabel('Training Set Size')
plt.ylabel('Accuracy')
plt.title('Learning Curve')
plt.legend(loc='best')
plt.grid(True, alpha=0.3)
plt.show()
```

**Interpretation**:

1. **High Bias (Underfitting)**:
   - Both train and validation scores are low
   - Curves are close together
   - → Add more features, increase model complexity

2. **High Variance (Overfitting)**:
   - Large gap between train and validation
   - Training score is high, validation is low
   - → Add more data, regularize, reduce complexity

3. **Good Fit**:
   - Small gap between curves
   - Both converge to high score

---

## 📊 Validation Curves

**Purpose**: See how performance changes with hyperparameter

```python
from sklearn.model_selection import validation_curve

# Example: Testing max_depth for XGBoost
param_range = [1, 2, 3, 5, 7, 10, 15, 20]

train_scores, val_scores = validation_curve(
    xgb.XGBClassifier(random_state=42),
    X_train, y_train,
    param_name='max_depth',
    param_range=param_range,
    cv=5,
    scoring='accuracy',
    n_jobs=-1
)

train_mean = train_scores.mean(axis=1)
train_std = train_scores.std(axis=1)
val_mean = val_scores.mean(axis=1)
val_std = val_scores.std(axis=1)

plt.figure(figsize=(10, 6))
plt.plot(param_range, train_mean, 'o-', label='Training', linewidth=2)
plt.fill_between(param_range, train_mean - train_std, train_mean + train_std, alpha=0.3)

plt.plot(param_range, val_mean, 'o-', label='Validation', linewidth=2)
plt.fill_between(param_range, val_mean - val_std, val_mean + val_std, alpha=0.3)

plt.xlabel('max_depth')
plt.ylabel('Accuracy')
plt.title('Validation Curve: max_depth')
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()

# Find optimal value
optimal_depth = param_range[np.argmax(val_mean)]
print(f"Optimal max_depth: {optimal_depth}")
```

---

## ⏱️ Time and Computational Metrics

```python
import time

# Training time
start = time.time()
model.fit(X_train, y_train)
train_time = time.time() - start

# Prediction time
start = time.time()
y_pred = model.predict(X_test)
pred_time = time.time() - start

print(f"Training time: {train_time:.4f} seconds")
print(f"Prediction time: {pred_time:.4f} seconds")
print(f"Prediction time per sample: {pred_time / len(X_test):.6f} seconds")
```

---

## 📋 Complete Comparison Function

```python
def comprehensive_evaluation(model, X_train, X_test, y_train, y_test,
                            model_name='Model', task='classification'):
    """
    Complete evaluation with all metrics
    """
    import time
    from sklearn.metrics import (accuracy_score, precision_score, recall_score,
                                f1_score, roc_auc_score, classification_report,
                                mean_squared_error, r2_score)
    import numpy as np
    
    results = {'model_name': model_name}
    
    # Training time
    start = time.time()
    model.fit(X_train, y_train)
    results['train_time'] = time.time() - start
    
    # Prediction time
    start = time.time()
    y_pred = model.predict(X_test)
    results['pred_time'] = time.time() - start
    
    if task == 'classification':
        # Classification metrics
        results['accuracy'] = accuracy_score(y_test, y_pred)
        results['precision'] = precision_score(y_test, y_pred, average='weighted')
        results['recall'] = recall_score(y_test, y_pred, average='weighted')
        results['f1'] = f1_score(y_test, y_pred, average='weighted')
        
        # ROC AUC (if binary classification)
        if hasattr(model, 'predict_proba'):
            y_proba = model.predict_proba(X_test)
            if y_proba.shape[1] == 2:
                results['roc_auc'] = roc_auc_score(y_test, y_proba[:, 1])
        
        # Training score (check for overfitting)
        results['train_accuracy'] = model.score(X_train, y_train)
        results['overfit_gap'] = results['train_accuracy'] - results['accuracy']
        
    else:  # regression
        results['mse'] = mean_squared_error(y_test, y_pred)
        results['rmse'] = np.sqrt(results['mse'])
        results['r2'] = r2_score(y_test, y_pred)
        
        # Training score
        y_train_pred = model.predict(X_train)
        results['train_r2'] = r2_score(y_train, y_train_pred)
        results['overfit_gap'] = results['train_r2'] - results['r2']
    
    return results


# Usage example
from xgboost import XGBClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier

models = {
    'XGBoost': XGBClassifier(random_state=42),
    'Random Forest': RandomForestClassifier(random_state=42),
    'Gradient Boosting': GradientBoostingClassifier(random_state=42)
}

all_results = []
for name, model in models.items():
    results = comprehensive_evaluation(model, X_train, X_test, y_train, y_test,
                                      model_name=name, task='classification')
    all_results.append(results)

df_results = pd.DataFrame(all_results)
print(df_results.round(4))
```

---

## 🎨 Visualization Function

```python
def plot_model_comparison(df_results, metric='accuracy'):
    """
    Create comprehensive comparison plots
    """
    import matplotlib.pyplot as plt
    import seaborn as sns
    
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    
    # 1. Main metric comparison
    ax = axes[0, 0]
    df_sorted = df_results.sort_values(metric, ascending=False)
    colors = sns.color_palette('viridis', len(df_sorted))
    ax.barh(df_sorted['model_name'], df_sorted[metric], color=colors)
    ax.set_xlabel(metric.capitalize())
    ax.set_title(f'{metric.capitalize()} Comparison')
    for i, v in enumerate(df_sorted[metric]):
        ax.text(v + 0.005, i, f'{v:.4f}', va='center')
    
    # 2. Training time
    ax = axes[0, 1]
    ax.barh(df_results['model_name'], df_results['train_time'], color='steelblue')
    ax.set_xlabel('Training Time (seconds)')
    ax.set_title('Training Time Comparison')
    
    # 3. Overfitting gap
    ax = axes[1, 0]
    ax.barh(df_results['model_name'], df_results['overfit_gap'], color='coral')
    ax.set_xlabel('Overfitting Gap (Train - Test)')
    ax.set_title('Overfitting Analysis')
    ax.axvline(x=0, color='red', linestyle='--', alpha=0.5)
    
    # 4. Multiple metrics radar (if classification)
    ax = axes[1, 1]
    if 'accuracy' in df_results.columns:
        metrics_to_plot = ['accuracy', 'precision', 'recall', 'f1']
        for idx, row in df_results.iterrows():
            values = [row[m] for m in metrics_to_plot]
            ax.plot(metrics_to_plot, values, marker='o', label=row['model_name'])
        ax.set_ylim(0, 1)
        ax.set_ylabel('Score')
        ax.set_title('Multiple Metrics Comparison')
        ax.legend()
        ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()

# Usage
plot_model_comparison(df_results, metric='accuracy')
```

---

## 💡 Quick Tips for Lab

### 1. Always Report Multiple Metrics

```python
print(f"Accuracy: {accuracy:.4f}")
print(f"Precision: {precision:.4f}")
print(f"Recall: {recall:.4f}")
print(f"F1: {f1:.4f}")
print(f"Training time: {train_time:.2f}s")
```

### 2. Use Cross-Validation for Comparison

```python
# Don't just use single test set
scores = cross_val_score(model, X_train, y_train, cv=5)
print(f"CV Accuracy: {scores.mean():.4f} (+/- {scores.std():.4f})")
```

### 3. Check for Overfitting

```python
train_score = model.score(X_train, y_train)
test_score = model.score(X_test, y_test)
print(f"Train: {train_score:.4f}, Test: {test_score:.4f}")
if train_score - test_score > 0.1:
    print("Warning: Model may be overfitting!")
```

### 4. Create Summary Tables

```python
results = {
    'Model': ['XGBoost', 'RF', 'GB'],
    'Accuracy': [0.95, 0.93, 0.94],
    'F1': [0.94, 0.92, 0.93],
    'Time': [0.5, 1.2, 2.1]
}
df = pd.DataFrame(results)
print(df.sort_values('Accuracy', ascending=False))
```

---

## 🔗 Next Steps

- **Code Templates**: See [05_Code_Templates.md](05_Code_Templates.md)
- **Common Issues**: See [06_Common_Pitfalls.md](06_Common_Pitfalls.md)
