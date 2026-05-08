# Common Pitfalls & Troubleshooting

## ⚠️ Things That Can Go Wrong (and How to Fix Them)

---

## 1. Data Issues

### ❌ Problem: Forgot to split data properly

```python
# WRONG - Training and testing on same data
model.fit(X, y)
accuracy = model.score(X, y)  # This will be optimistically high!
```

```python
# CORRECT
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model.fit(X_train, y_train)
accuracy = model.score(X_test, y_test)  # True generalization performance
```

---

### ❌ Problem: Data leakage from scaling

```python
# WRONG - Scaling before split (test data leaks into training)
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)  # Sees all data!
X_train, X_test = train_test_split(X_scaled, ...)
```

```python
# CORRECT - Scale after split
X_train, X_test, y_train, y_test = train_test_split(X, y, ...)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)  # Fit only on training
X_test_scaled = scaler.transform(X_test)        # Transform test with same scaler
```

---

### ❌ Problem: Imbalanced class distribution

```python
# Check class distribution
import numpy as np
print("Class distribution:", np.bincount(y))
# Output: [900, 100] <- Highly imbalanced!
```

```python
# FIX 1: Use stratified split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)

# FIX 2: Use class weights
from xgboost import XGBClassifier

model = XGBClassifier(scale_pos_weight=9)  # ratio of negative to positive
model.fit(X_train, y_train)

# FIX 3: Use appropriate metrics (not just accuracy!)
from sklearn.metrics import f1_score, roc_auc_score
```

---

## 2. Model Configuration Issues

### ❌ Problem: Forgot to set random_state

```python
# BAD - Results will be different each time
model = XGBClassifier(n_estimators=100)
model.fit(X_train, y_train)
# Run 1: 0.95 accuracy
# Run 2: 0.93 accuracy
# Run 3: 0.96 accuracy  ← Not reproducible!
```

```python
# GOOD - Reproducible results
model = XGBClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)
# Every run: 0.95 accuracy ✓
```

---

### ❌ Problem: Wrong hyperparameters for the task

```python
# WRONG for XGBoost - These are Random Forest defaults!
model = XGBClassifier(
    max_depth=None,      # XGBoost expects integer, not None
    n_jobs=-1            # This parameter doesn't exist in XGBoost
)
```

```python
# CORRECT
model = XGBClassifier(
    max_depth=6,         # Integer value
    n_estimators=100,
    learning_rate=0.1,
    random_state=42
)
```

---

### ❌ Problem: AdaBoost with wrong base learner

```python
# INEFFECTIVE - AdaBoost with already strong learner
from sklearn.ensemble import AdaBoostClassifier
from sklearn.tree import DecisionTreeClassifier

model = AdaBoostClassifier(
    estimator=DecisionTreeClassifier(max_depth=20),  # Too deep!
    n_estimators=50
)
# AdaBoost won't improve much because base is already strong
```

```python
# BETTER - Use weak learner
model = AdaBoostClassifier(
    estimator=DecisionTreeClassifier(max_depth=1),  # Decision stump
    n_estimators=50
)
# AdaBoost can make significant improvements
```

---

## 3. Evaluation Mistakes

### ❌ Problem: Using wrong metric for imbalanced data

```python
# Dataset: 95% class 0, 5% class 1
# Naive model that always predicts 0

from sklearn.metrics import accuracy_score
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy:.4f}")  # 0.95 - Looks great but useless!
```

```python
# CORRECT - Use appropriate metrics
from sklearn.metrics import precision_score, recall_score, f1_score, roc_auc_score

print(f"Accuracy: {accuracy_score(y_test, y_pred):.4f}")
print(f"Precision: {precision_score(y_test, y_pred):.4f}")
print(f"Recall: {recall_score(y_test, y_pred):.4f}")      # Will be 0!
print(f"F1-Score: {f1_score(y_test, y_pred):.4f}")        # Will be low
print(f"ROC-AUC: {roc_auc_score(y_test, y_pred_proba):.4f}")
```

---

### ❌ Problem: Not using cross-validation

```python
# RISKY - Single split might be lucky/unlucky
model.fit(X_train, y_train)
score = model.score(X_test, y_test)
print(f"Accuracy: {score:.4f}")  # Might not generalize!
```

```python
# BETTER - Use cross-validation
from sklearn.model_selection import cross_val_score

scores = cross_val_score(model, X_train, y_train, cv=5)
print(f"CV Accuracy: {scores.mean():.4f} (+/- {scores.std():.4f})")

# Then test on held-out test set
model.fit(X_train, y_train)
test_score = model.score(X_test, y_test)
print(f"Test Accuracy: {test_score:.4f}")
```

---

### ❌ Problem: Not checking for overfitting

```python
# Only looking at test accuracy
test_acc = model.score(X_test, y_test)
print(f"Test: {test_acc:.4f}")  # 0.85 - Is this good or bad?
```

```python
# CORRECT - Compare train and test
train_acc = model.score(X_train, y_train)
test_acc = model.score(X_test, y_test)

print(f"Train: {train_acc:.4f}")
print(f"Test:  {test_acc:.4f}")
print(f"Gap:   {train_acc - test_acc:.4f}")

if train_acc - test_acc > 0.1:
    print("⚠️  Warning: Model is overfitting!")
```

---

## 4. XGBoost Specific Issues

### ❌ Problem: Learning rate too high

```python
# Too aggressive
model = XGBClassifier(learning_rate=1.0, n_estimators=50)
# Model might overfit quickly or be unstable
```

```python
# BETTER - Lower learning rate with more trees
model = XGBClassifier(learning_rate=0.1, n_estimators=200)
# Or even slower for best results
model = XGBClassifier(learning_rate=0.01, n_estimators=1000)
```

---

### ❌ Problem: Not using early stopping

```python
# Training for fixed number of rounds
model = XGBClassifier(n_estimators=1000)  # Might overfit!
model.fit(X_train, y_train)
```

```python
# BETTER - Use early stopping
X_train_split, X_val, y_train_split, y_val = train_test_split(
    X_train, y_train, test_size=0.2, random_state=42
)

model = XGBClassifier(n_estimators=1000, early_stopping_rounds=10)
model.fit(
    X_train_split, y_train_split,
    eval_set=[(X_val, y_val)],
    verbose=False
)
print(f"Best iteration: {model.best_iteration}")
```

---

### ❌ Problem: Too deep trees

```python
# Overfitting risk
model = XGBClassifier(max_depth=15, n_estimators=100)
```

```python
# BETTER - Shallower trees
model = XGBClassifier(
    max_depth=3,          # or 5, 7
    n_estimators=200,     # Increase number instead
    learning_rate=0.1
)
```

---

## 5. Comparison Issues

### ❌ Problem: Comparing with different random states

```python
# WRONG - Each model uses different random split
model1 = RandomForestClassifier(random_state=1)
model2 = XGBClassifier(random_state=2)
model3 = GradientBoostingClassifier(random_state=3)

# They might be seeing slightly different data patterns!
```

```python
# CORRECT - Same random state for fair comparison
model1 = RandomForestClassifier(random_state=42)
model2 = XGBClassifier(random_state=42)
model3 = GradientBoostingClassifier(random_state=42)

# Or use cross-validation (even better)
for name, model in models.items():
    scores = cross_val_score(model, X, y, cv=5, random_state=42)
    print(f"{name}: {scores.mean():.4f}")
```

---

### ❌ Problem: Not controlling for computation time

```python
# UNFAIR - Different number of trees
model1 = RandomForestClassifier(n_estimators=500)
model2 = XGBClassifier(n_estimators=50)

# RF has 10x more trees, of course it might be better!
```

```python
# FAIRER - Same number of trees or same training time
# Option 1: Same n_estimators
model1 = RandomForestClassifier(n_estimators=100)
model2 = XGBClassifier(n_estimators=100)

# Option 2: Control for time
import time

for name, model in models.items():
    start = time.time()
    model.fit(X_train, y_train)
    train_time = time.time() - start
    score = model.score(X_test, y_test)
    print(f"{name}: {score:.4f} (Time: {train_time:.2f}s)")
```

---

## 6. Code Errors

### ❌ Problem: Import errors

```python
# WRONG
from xgboost import XGBoost  # No such class!
```

```python
# CORRECT
from xgboost import XGBClassifier, XGBRegressor
# or
import xgboost as xgb
model = xgb.XGBClassifier()
```

---

### ❌ Problem: Shape mismatch

```python
# WRONG - Predicting on wrong shape
model.fit(X_train, y_train)
y_pred = model.predict(X_train[0])  # Single sample without reshape!
# Error: Expected 2D array, got 1D array
```

```python
# CORRECT - Reshape single sample
single_sample = X_train[0].reshape(1, -1)
y_pred = model.predict(single_sample)

# Or for single prediction
y_pred = model.predict(X_train[[0]])  # Double bracket keeps 2D
```

---

### ❌ Problem: Mixing numpy and pandas

```python
# Be careful with indices
import pandas as pd
df = pd.DataFrame(X)
df_train, df_test = train_test_split(df, test_size=0.2)

# Indices might not be 0, 1, 2, ... anymore!
y_pred = model.predict(df_test)
accuracy = accuracy_score(y_test, y_pred)  # Might have index mismatch!
```

```python
# FIX - Reset index or use .values
df_train.reset_index(drop=True, inplace=True)
df_test.reset_index(drop=True, inplace=True)

# Or convert to numpy
X_test_array = df_test.values
```

---

## 7. Performance Issues

### ❌ Problem: Very slow training

```python
# TOO MANY parameters to search
from sklearn.model_selection import GridSearchCV

param_grid = {
    'n_estimators': [50, 100, 200, 300, 500],
    'max_depth': [3, 5, 7, 10, 15, 20],
    'learning_rate': [0.01, 0.05, 0.1, 0.2, 0.3],
    'subsample': [0.6, 0.7, 0.8, 0.9, 1.0],
    'colsample_bytree': [0.6, 0.7, 0.8, 0.9, 1.0]
}
# This is 5×6×5×5×5 = 3750 combinations! Will take forever!
```

```python
# BETTER - Tune sequentially or use RandomizedSearchCV
from sklearn.model_selection import RandomizedSearchCV

# Only test 50 random combinations
random_search = RandomizedSearchCV(
    model, param_distributions=param_grid,
    n_iter=50,  # Much faster!
    cv=5,
    random_state=42
)

# Or tune one parameter at a time (manual)
```

---

### ❌ Problem: Not using parallel processing

```python
# SLOW - Single core
model = XGBClassifier(n_estimators=1000)
scores = cross_val_score(model, X, y, cv=5)  # Takes 5x longer
```

```python
# FAST - Use all cores
model = XGBClassifier(n_estimators=1000, n_jobs=-1)
scores = cross_val_score(model, X, y, cv=5, n_jobs=-1)
```

---

## 8. Interpretation Mistakes

### ❌ Problem: Confusing correlation with causation

Just because a feature has high importance doesn't mean it *causes* the outcome!

```python
# Feature importance shows correlation, not causation
importance = model.feature_importances_
# "Income" has high importance in predicting "owns_yacht"
# But yacht doesn't cause income!
```

---

### ❌ Problem: Overstating model confidence

```python
# Your model's 95% accuracy on test set doesn't mean
# it will be 95% accurate in production!

# Real-world data might:
# - Have different distribution
# - Include edge cases not in training data
# - Change over time (concept drift)
```

---

## 🔧 Quick Debugging Checklist

When something goes wrong, check:

- [ ] Data split correctly (train/test)?
- [ ] Random state set (reproducibility)?
- [ ] Correct shapes (2D arrays)?
- [ ] No data leakage (scaling after split)?
- [ ] Appropriate metric for your problem?
- [ ] Cross-validation used?
- [ ] Train vs test performance compared (overfitting)?
- [ ] Sensible hyperparameters?
- [ ] Correct imports?
- [ ] Latest library versions?

---

## 💡 Best Practices Summary

### ✅ DO:
- Set `random_state=42` everywhere
- Use cross-validation
- Check for overfitting (compare train vs test)
- Use appropriate metrics
- Scale features when needed (but after split!)
- Start simple, then increase complexity
- Time your experiments
- Plot your results
- Use early stopping with XGBoost

### ❌ DON'T:
- Train and test on same data
- Scale before splitting
- Use only accuracy for imbalanced data
- Forget to check class distribution
- Use very deep trees without regularization
- Compare models with different random states
- Blindly trust feature importance
- Ignore computational cost

---

## 🆘 Common Error Messages

### Error: "ValueError: Input contains NaN"
```python
# Check for missing values
print(X.isna().sum())

# Fix: Fill or remove
X = X.fillna(X.mean())  # Fill with mean
# or
X = X.dropna()  # Remove rows
```

### Error: "ValueError: Unknown label type"
```python
# XGBoost expects labels to be 0, 1, 2, ... for classification

# If you have -1, 1, convert to 0, 1
from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()
y = le.fit_transform(y)
```

### Error: "KeyError: 'xxx' not found in axis"
```python
# Column doesn't exist in DataFrame
# Check column names
print(df.columns)
```

---

## 🔗 Need More Help?

- **Basics**: [01_XGBoost_Basics.md](01_XGBoost_Basics.md)
- **Tuning**: [02_Hyperparameter_Tuning.md](02_Hyperparameter_Tuning.md)
- **Templates**: [05_Code_Templates.md](05_Code_Templates.md)
