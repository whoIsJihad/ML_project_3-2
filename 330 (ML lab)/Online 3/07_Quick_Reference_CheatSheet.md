# Quick Reference - Cheat Sheet

## 🚀 For Use During Online Lab Test

---

## Essential Imports

```python
# Core
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import time
import warnings
warnings.filterwarnings('ignore')

# Data
from sklearn.datasets import load_breast_cancer, load_diabetes, load_iris
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler

# Metrics
from sklearn.metrics import (accuracy_score, precision_score, recall_score, 
                            f1_score, roc_auc_score, mean_squared_error, r2_score)

# Ensemble
from sklearn.ensemble import (BaggingClassifier, RandomForestClassifier,
                             AdaBoostClassifier, GradientBoostingClassifier)
from sklearn.tree import DecisionTreeClassifier

# XGBoost
import xgboost as xgb
from xgboost import XGBClassifier, XGBRegressor
```

---

## Quick Data Setup

```python
# Load data
X, y = load_breast_cancer(return_X_y=True)

# Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Check
print(f"Train: {X_train.shape}, Test: {X_test.shape}")
print(f"Classes: {np.unique(y)}")
```

---

## Basic Model Training

```python
# Create model
model = XGBClassifier(
    n_estimators=100,
    max_depth=3,
    learning_rate=0.1,
    random_state=42
)

# Train
model.fit(X_train, y_train)

# Predict
y_pred = model.predict(X_test)

# Evaluate
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy:.4f}")
```

---

## Compare Multiple Models

```python
models = {
    'RF': RandomForestClassifier(n_estimators=100, random_state=42),
    'GB': GradientBoostingClassifier(n_estimators=100, random_state=42),
    'XGB': XGBClassifier(n_estimators=100, random_state=42)
}

results = []
for name, model in models.items():
    model.fit(X_train, y_train)
    score = model.score(X_test, y_test)
    results.append({'Model': name, 'Accuracy': score})
    print(f"{name}: {score:.4f}")

df = pd.DataFrame(results)
print(df.sort_values('Accuracy', ascending=False))
```

---

## Test Single Hyperparameter

```python
param_values = [50, 100, 200, 500]
results = []

for value in param_values:
    model = XGBClassifier(n_estimators=value, random_state=42)
    scores = cross_val_score(model, X_train, y_train, cv=5)
    results.append({
        'n_estimators': value,
        'mean_score': scores.mean(),
        'std_score': scores.std()
    })
    print(f"n_estimators={value}: {scores.mean():.4f} (+/- {scores.std():.4f})")

df = pd.DataFrame(results)
```

---

## XGBoost Configurations

```python
configs = {
    'Baseline': {'n_estimators': 100, 'max_depth': 3, 'learning_rate': 0.1},
    'Deep': {'n_estimators': 100, 'max_depth': 10, 'learning_rate': 0.1},
    'Slow': {'n_estimators': 1000, 'max_depth': 3, 'learning_rate': 0.01},
    'Regularized': {'n_estimators': 100, 'max_depth': 5, 'learning_rate': 0.1,
                   'reg_lambda': 10, 'gamma': 1.0}
}

for name, params in configs.items():
    model = XGBClassifier(**params, random_state=42)
    model.fit(X_train, y_train)
    score = model.score(X_test, y_test)
    print(f"{name}: {score:.4f}")
```

---

## Base Learner Comparison

```python
from sklearn.linear_model import LogisticRegression

base_learners = {
    'Stump': DecisionTreeClassifier(max_depth=1, random_state=42),
    'Tree': DecisionTreeClassifier(max_depth=5, random_state=42),
    'LogReg': LogisticRegression(random_state=42, max_iter=1000)
}

for name, base in base_learners.items():
    # Bagging
    bagging = BaggingClassifier(estimator=base, n_estimators=50, random_state=42)
    bagging.fit(X_train, y_train)
    score = bagging.score(X_test, y_test)
    print(f"{name} with Bagging: {score:.4f}")
```

---

## Quick Visualization

```python
# Bar plot
plt.figure(figsize=(10, 6))
plt.bar(df['Model'], df['Accuracy'])
plt.xlabel('Model')
plt.ylabel('Accuracy')
plt.title('Model Comparison')
plt.ylim([0.9, 1.0])  # Adjust as needed
plt.xticks(rotation=45)
for i, v in enumerate(df['Accuracy']):
    plt.text(i, v + 0.005, f'{v:.4f}', ha='center')
plt.tight_layout()
plt.savefig('comparison.png', dpi=150)
plt.show()
```

---

## Cross-Validation

```python
# Single model
scores = cross_val_score(model, X_train, y_train, cv=5)
print(f"CV: {scores.mean():.4f} (+/- {scores.std():.4f})")

# Multiple models
for name, model in models.items():
    scores = cross_val_score(model, X_train, y_train, cv=5)
    print(f"{name}: {scores.mean():.4f} (+/- {scores.std():.4f})")
```

---

## Check Overfitting

```python
train_acc = model.score(X_train, y_train)
test_acc = model.score(X_test, y_test)
gap = train_acc - test_acc

print(f"Train: {train_acc:.4f}")
print(f"Test:  {test_acc:.4f}")
print(f"Gap:   {gap:.4f}")

if gap > 0.1:
    print("⚠️  Overfitting detected!")
```

---

## Timing Code

```python
import time

start = time.time()
model.fit(X_train, y_train)
train_time = time.time() - start

print(f"Training time: {train_time:.2f} seconds")
```

---

## Performance Report

```python
from sklearn.metrics import classification_report

y_pred = model.predict(X_test)

print("Accuracy:", accuracy_score(y_test, y_pred))
print("Precision:", precision_score(y_test, y_pred, average='weighted'))
print("Recall:", recall_score(y_test, y_pred, average='weighted'))
print("F1:", f1_score(y_test, y_pred, average='weighted'))
print("\nDetailed Report:")
print(classification_report(y_test, y_pred))
```

---

## Parameter Sensitivity Plot

```python
param_values = [1, 2, 3, 5, 7, 10]
scores = []

for value in param_values:
    model = XGBClassifier(max_depth=value, n_estimators=100, random_state=42)
    cv_scores = cross_val_score(model, X_train, y_train, cv=5)
    scores.append(cv_scores.mean())

plt.figure(figsize=(10, 6))
plt.plot(param_values, scores, 'o-', linewidth=2, markersize=8)
plt.xlabel('max_depth')
plt.ylabel('Cross-Validation Accuracy')
plt.title('Effect of max_depth on Performance')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('sensitivity.png', dpi=150)
plt.show()
```

---

## Common XGBoost Hyperparameters

| Parameter | Typical Values | Effect |
|-----------|---------------|--------|
| `n_estimators` | 50, 100, 200, 500 | More = better fit (slower) |
| `max_depth` | 3, 5, 7, 10 | Higher = more complex |
| `learning_rate` | 0.01, 0.1, 0.3 | Lower = slower learning |
| `subsample` | 0.7, 0.8, 1.0 | Lower = more randomness |
| `colsample_bytree` | 0.7, 0.8, 1.0 | Lower = more randomness |
| `reg_lambda` | 0, 1, 10 | Higher = more regularization |
| `gamma` | 0, 0.5, 1, 5 | Higher = fewer splits |

---

## Quick Debugging

```python
# Check data
print("Shape:", X.shape)
print("Type:", type(X))
print("NaNs:", np.isnan(X).sum())
print("Classes:", np.unique(y))

# Check model
print("Model:", model)
print("Fitted:", hasattr(model, 'feature_importances_'))

# Check predictions
print("Predictions shape:", y_pred.shape)
print("Unique predictions:", np.unique(y_pred))
```

---

## Save Results

```python
# Save DataFrame
df_results.to_csv('results.csv', index=False)

# Save plot
plt.savefig('plot.png', dpi=150, bbox_inches='tight')

# Save model
import joblib
joblib.dump(model, 'model.pkl')

# Load model
model = joblib.load('model.pkl')
```

---

## Regression Version

```python
from sklearn.datasets import load_diabetes
from sklearn.metrics import mean_squared_error, r2_score
from xgboost import XGBRegressor
import numpy as np

# Load
X, y = load_diabetes(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train
model = XGBRegressor(n_estimators=100, max_depth=3, random_state=42)
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
r2 = r2_score(y_test, y_pred)

print(f"RMSE: {rmse:.4f}")
print(f"R²: {r2:.4f}")
```

---

## Emergency Template (Copy-Paste Ready)

```python
"""
EMERGENCY TEMPLATE - WORKS FOR MOST LAB TASKS
"""
import numpy as np
import pandas as pd
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt

# 1. Load data
X, y = load_breast_cancer(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 2. Define models
models = {
    'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42),
    'Gradient Boosting': GradientBoostingClassifier(n_estimators=100, random_state=42),
    'XGBoost': XGBClassifier(n_estimators=100, random_state=42)
}

# 3. Train and evaluate
results = []
for name, model in models.items():
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    results.append({'Model': name, 'Accuracy': acc})
    print(f"{name}: {acc:.4f}")

# 4. Show results
df = pd.DataFrame(results)
print("\nResults:")
print(df.sort_values('Accuracy', ascending=False))

# 5. Plot
plt.figure(figsize=(10, 6))
plt.bar(df['Model'], df['Accuracy'])
plt.xlabel('Model')
plt.ylabel('Accuracy')
plt.title('Model Comparison')
plt.ylim([0.9, 1.0])
plt.tight_layout()
plt.savefig('results.png', dpi=150)
plt.show()
```

---

## 🔥 Most Important Tips

1. **Always set `random_state=42`**
2. **Use cross-validation when comparing models**
3. **Check train vs test accuracy (overfitting)**
4. **Print intermediate results**
5. **Save your plots with `plt.savefig()`**
6. **Start with Template 1 from [05_Code_Templates.md](05_Code_Templates.md)**

---

## 📱 Quick Navigation

- **Full Templates**: [05_Code_Templates.md](05_Code_Templates.md)
- **XGBoost Details**: [01_XGBoost_Basics.md](01_XGBoost_Basics.md)
- **Tuning Guide**: [02_Hyperparameter_Tuning.md](02_Hyperparameter_Tuning.md)
- **Common Errors**: [06_Common_Pitfalls.md](06_Common_Pitfalls.md)

**Good luck! 🚀**
