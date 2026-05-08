# XGBoost Basics: Implementation Guide

## 🎯 What is XGBoost?

**XGBoost** = **eX**treme **G**radient **Boost**ing

### The Simple Story

Imagine you're trying to predict house prices. Your first model (a simple decision tree) makes predictions, but it's not perfect - it makes errors. 

**Traditional approach**: Train one good model and hope it works.

**XGBoost approach**: 
1. Train a simple model → it makes some errors
2. Train a second model to **correct those errors**
3. Train a third model to correct **remaining errors**
4. Keep going, each new model fixing what previous ones got wrong
5. Final prediction = combine all models together

**Result**: Many "weak" models working together become one "strong" model!

### Why XGBoost is Special

**It's like assembling the Avengers**:
- Iron Man alone is strong, but not perfect
- Add Captain America → covers Iron Man's weaknesses  
- Add Thor → covers their combined weaknesses
- Together → much more powerful than any individual!

**XGBoost does this with models**:
- Model 1: Predicts roughly → makes some errors
- Model 2: Learns from Model 1's mistakes → reduces errors
- Model 3: Learns from combined mistakes → reduces more errors
- **Final model = Model 1 + Model 2 + Model 3 + ... = Very accurate!**

### Why It's Called "eXtreme"

XGBoost improves on regular Gradient Boosting by:

1. **Speed**: Optimized algorithms (10-100x faster)
2. **Regularization**: Built-in protection against overfitting
3. **Handles Missing Data**: Automatically learns best way to handle missing values
4. **Parallelization**: Uses multiple CPU cores
5. **Tree Pruning**: Smart about when to stop growing trees
6. **Hardware Optimization**: Cache-aware algorithms

**Bottom Line**: XGBoost is gradient boosting done right - faster, more accurate, and harder to overfit.

### Real-World Success

- **Kaggle**: Won majority of machine learning competitions (2015-2017)
- **Industry**: Used by companies like Airbnb, Uber, Microsoft
- **Problems**: Works for tabular data (spreadsheet-like data with rows/columns)

### What Problems Does XGBoost Solve?

✅ **Classification**: Is this email spam? Will customer churn? Is this a cat or dog?  
✅ **Regression**: What will house price be? How much will customer spend?  
✅ **Ranking**: What order should search results be shown?

❌ **Not for**: Images (use CNNs), Text/Language (use Transformers), Time-series (use RNNs/LSTMs)

---

## 🧠 The Core Concept: Sequential Error Correction

### Visualization

```
Data → [Model 1] → Predictions → Compare with Truth → Errors

        ↓ (Learn from errors)

Errors → [Model 2] → Better Predictions → Compare → Smaller Errors

        ↓ (Learn from remaining errors)

Smaller Errors → [Model 3] → Even Better Predictions → ...

Final Prediction = Sum of all models
```

### Example with Numbers

**Goal**: Predict house prices

| House | True Price | Model 1 | Error | Model 2 | Error | Model 3 | Final |
|-------|-----------|---------|-------|---------|-------|---------|-------|
| A | $300k | $250k | +$50k | +$40k | +$10k | +$8k | $298k ✓ |
| B | $500k | $480k | +$20k | +$15k | +$5k | +$4k | $499k ✓ |
| C | $200k | $220k | -$20k | -$15k | -$5k | -$4k | $201k ✓ |

- **Model 1**: Rough guess (baseline)
- **Model 2**: Corrects large errors from Model 1
- **Model 3**: Corrects remaining small errors
- **Final**: $250k + $40k + $8k = $298k (very close to $300k!)

Each model learns to predict the **errors** (residuals) of the previous models!

---

## 🆚 XGBoost vs Other Methods

| Method | How it Works | Strength | Weakness |
|--------|-------------|----------|----------|
| **Single Decision Tree** | One tree | Fast, interpretable | High variance (overfits) |
| **Random Forest** | Many trees in parallel, average results | Reduces variance | Doesn't reduce bias |
| **Gradient Boosting** | Trees in sequence, fix errors | Reduces bias | Slower, can overfit |
| **XGBoost** | Gradient Boosting + regularization + speed optimizations | Best accuracy, fast | Less interpretable, needs tuning |

**When to Use XGBoost**:
- ✅ You have tabular/structured data (like CSV, Excel)
- ✅ You want best possible accuracy
- ✅ You're doing a Kaggle competition 😊
- ✅ You have time to tune hyperparameters

**When NOT to Use XGBoost**:
- ❌ You have image data (use CNNs instead)
- ❌ You have text data (use Transformers instead)
- ❌ You need a highly interpretable model (use logistic regression or single tree)
- ❌ You have very little data (<100 samples)

---

## 📦 Installation & Import

```python
# Install
pip install xgboost

# Import
import xgboost as xgb
from xgboost import XGBClassifier, XGBRegressor
```

---

## 🔨 Basic Usage

### Classification

```python
from xgboost import XGBClassifier
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Load data
X, y = load_breast_cancer(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Create model
model = XGBClassifier(
    n_estimators=100,      # Number of trees
    max_depth=3,           # Tree depth
    learning_rate=0.1,     # Step size (eta)
    random_state=42
)

# Train
model.fit(X_train, y_train)

# Predict
y_pred = model.predict(X_test)
y_pred_proba = model.predict_proba(X_test)  # Probabilities

# Evaluate
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy:.4f}")
```

### Regression

```python
from xgboost import XGBRegressor
from sklearn.datasets import load_diabetes
from sklearn.metrics import mean_squared_error, r2_score

# Load data
X, y = load_diabetes(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Create model
model = XGBRegressor(
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
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
print(f"MSE: {mse:.4f}, R²: {r2:.4f}")
```

---

## ⚙️ Key Hyperparameters (Must Know)

### 1. Number of Trees: `n_estimators`

**What**: Number of boosting rounds (trees to build)

```python
# Few trees (fast, might underfit)
model = XGBClassifier(n_estimators=50)

# Many trees (slow, might overfit)
model = XGBClassifier(n_estimators=500)

# Good starting point
model = XGBClassifier(n_estimators=100)
```

**Range to Try**: [50, 100, 200, 500, 1000]

**Effect**:
- ↑ More trees → Better training accuracy (but risk overfitting)
- ↓ Fewer trees → Faster training (but might underfit)

---

### 2. Tree Depth: `max_depth`

**What**: Maximum depth of each tree

```python
# Shallow (prevents overfitting, faster)
model = XGBClassifier(max_depth=3)

# Deep (can model complex patterns, slower)
model = XGBClassifier(max_depth=10)

# Default
model = XGBClassifier(max_depth=6)
```

**Range to Try**: [3, 5, 7, 10]

**Effect**:
- ↑ Deeper → Can learn complex interactions (but overfits)
- ↓ Shallower → More regularization (but might be too simple)

---

### 3. Learning Rate: `learning_rate` (or `eta`)

**What**: Step size shrinkage to prevent overfitting

```python
# Slow learning (needs more trees, but better generalization)
model = XGBClassifier(learning_rate=0.01, n_estimators=1000)

# Fast learning (fewer trees, but might overfit)
model = XGBClassifier(learning_rate=0.3, n_estimators=100)

# Default
model = XGBClassifier(learning_rate=0.1)
```

**Range to Try**: [0.01, 0.05, 0.1, 0.3]

**Effect**:
- ↓ Lower → Better generalization (but needs more trees, slower)
- ↑ Higher → Faster training (but risk overfitting)

**Rule of Thumb**: Lower learning rate + more trees = better results (if you have time)

---

### 4. Regularization: `reg_lambda` (L2) and `reg_alpha` (L1)

**What**: Penalty on leaf weights to prevent overfitting

```python
# No regularization
model = XGBClassifier(reg_lambda=0, reg_alpha=0)

# L2 regularization (Ridge)
model = XGBClassifier(reg_lambda=1.0)

# L1 regularization (Lasso, creates sparsity)
model = XGBClassifier(reg_alpha=1.0)

# Both
model = XGBClassifier(reg_lambda=1.0, reg_alpha=0.5)
```

**Range to Try**: [0, 0.01, 0.1, 1.0, 10.0]

**Effect**:
- ↑ Higher → More regularization, prevents overfitting
- Especially useful with deep trees or many features

---

### 5. Subsampling: `subsample` and `colsample_bytree`

**What**: Use subset of data/features per tree (like Random Forest)

```python
# Use all data and features
model = XGBClassifier(subsample=1.0, colsample_bytree=1.0)

# Use 80% of samples and 80% of features per tree
model = XGBClassifier(subsample=0.8, colsample_bytree=0.8)

# Aggressive subsampling (more randomness, less overfitting)
model = XGBClassifier(subsample=0.5, colsample_bytree=0.5)
```

**Range to Try**: [0.5, 0.7, 0.8, 1.0]

**Effect**:
- ↓ Lower → More randomness, prevents overfitting, faster
- Creates diversity like Random Forest

---

### 6. Minimum Child Weight: `min_child_weight`

**What**: Minimum sum of instance weight (hessian) in a child

```python
# Allow very small leaves (might overfit)
model = XGBClassifier(min_child_weight=1)

# Require substantial data in each leaf (more conservative)
model = XGBClassifier(min_child_weight=5)
```

**Range to Try**: [1, 3, 5, 10]

**Effect**:
- ↑ Higher → More conservative splits, prevents overfitting
- Similar to `min_samples_leaf` in sklearn trees

---

### 7. Gamma: `gamma` (min_split_loss)

**What**: Minimum loss reduction required to make a split

```python
# Allow any beneficial split
model = XGBClassifier(gamma=0)

# Require substantial gain to split
model = XGBClassifier(gamma=1.0)
```

**Range to Try**: [0, 0.1, 0.5, 1.0, 5.0]

**Effect**:
- ↑ Higher → Fewer splits, more regularization
- Directly controls tree growth

---

## 📊 Hyperparameter Summary Table

| Parameter | Default | Range to Try | Effect | When to Increase |
|-----------|---------|--------------|--------|------------------|
| `n_estimators` | 100 | [50, 100, 200, 500] | More trees = better fit | When underfitting |
| `max_depth` | 6 | [3, 5, 7, 10] | Deeper = more complex | When underfitting |
| `learning_rate` | 0.3 | [0.01, 0.1, 0.3] | Lower = better generalization | When overfitting (and increase n_estimators) |
| `subsample` | 1.0 | [0.5, 0.7, 0.8, 1.0] | Lower = more randomness | When overfitting |
| `colsample_bytree` | 1.0 | [0.5, 0.7, 0.8, 1.0] | Lower = more diversity | When overfitting |
| `reg_lambda` | 1.0 | [0, 0.1, 1.0, 10] | Higher = more regularization | When overfitting |
| `reg_alpha` | 0 | [0, 0.1, 1.0, 10] | Higher = more regularization | When overfitting |
| `gamma` | 0 | [0, 0.1, 1.0, 5.0] | Higher = fewer splits | When overfitting |
| `min_child_weight` | 1 | [1, 3, 5, 10] | Higher = more conservative | When overfitting |

---

## 🎨 Training with Validation Set

**Pro Tip**: Use `eval_set` to monitor validation performance during training

```python
# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Further split training into train and validation
X_train, X_val, y_train, y_val = train_test_split(
    X_train, y_train, test_size=0.2, random_state=42
)

# Train with validation monitoring
model = XGBClassifier(n_estimators=1000, learning_rate=0.1)

model.fit(
    X_train, y_train,
    eval_set=[(X_train, y_train), (X_val, y_val)],
    eval_metric='logloss',  # or 'error', 'auc', 'rmse', etc.
    verbose=50  # Print every 50 rounds
)

# Get evaluation results
results = model.evals_result()
train_loss = results['validation_0']['logloss']
val_loss = results['validation_1']['logloss']

# Plot learning curves
import matplotlib.pyplot as plt
plt.plot(train_loss, label='Train')
plt.plot(val_loss, label='Validation')
plt.xlabel('Boosting Round')
plt.ylabel('Log Loss')
plt.legend()
plt.show()
```

---

## 🛑 Early Stopping

**Automatically stop when validation performance stops improving**

```python
model = XGBClassifier(n_estimators=1000, learning_rate=0.1)

model.fit(
    X_train, y_train,
    eval_set=[(X_val, y_val)],
    eval_metric='logloss',
    early_stopping_rounds=10,  # Stop if no improvement for 10 rounds
    verbose=False
)

print(f"Best iteration: {model.best_iteration}")
print(f"Best score: {model.best_score}")
```

---

## 🌳 Feature Importance

```python
# Train model
model = XGBClassifier()
model.fit(X_train, y_train)

# Get feature importance
importance = model.feature_importances_
feature_names = [f'Feature {i}' for i in range(len(importance))]

# Plot
import matplotlib.pyplot as plt
plt.barh(feature_names, importance)
plt.xlabel('Importance')
plt.title('Feature Importance')
plt.show()

# Or use built-in plot
from xgboost import plot_importance
plot_importance(model, max_num_features=10)
plt.show()
```

**Types of Importance**:
- `weight`: Number of times feature is used to split
- `gain`: Average gain when feature is used (default)
- `cover`: Average coverage (samples affected)

```python
# Get different importance types
model.get_booster().get_score(importance_type='weight')
model.get_booster().get_score(importance_type='gain')
model.get_booster().get_score(importance_type='cover')
```

---

## 🔄 Comparing XGBoost Configurations

```python
import pandas as pd
from sklearn.metrics import accuracy_score
import time

# Define configurations to test
configs = {
    'Baseline': {
        'n_estimators': 100,
        'max_depth': 3,
        'learning_rate': 0.1
    },
    'Deep Trees': {
        'n_estimators': 100,
        'max_depth': 10,
        'learning_rate': 0.1
    },
    'Many Shallow': {
        'n_estimators': 500,
        'max_depth': 2,
        'learning_rate': 0.05
    },
    'Regularized': {
        'n_estimators': 100,
        'max_depth': 5,
        'learning_rate': 0.1,
        'reg_lambda': 10,
        'gamma': 1.0
    }
}

# Train and evaluate each
results = []

for name, params in configs.items():
    # Create model
    model = XGBClassifier(**params, random_state=42)
    
    # Time training
    start = time.time()
    model.fit(X_train, y_train)
    train_time = time.time() - start
    
    # Predict
    y_pred = model.predict(X_test)
    
    # Evaluate
    accuracy = accuracy_score(y_test, y_pred)
    
    # Store results
    results.append({
        'Configuration': name,
        'Accuracy': accuracy,
        'Training Time (s)': train_time,
        **params  # Include all parameters
    })

# Create DataFrame
df_results = pd.DataFrame(results)
print(df_results.sort_values('Accuracy', ascending=False))
```

---

## 💡 Quick Tips

1. **Start with defaults**: XGBoost defaults are pretty good!

2. **Typical good configuration**:
   ```python
   model = XGBClassifier(
       n_estimators=200,
       max_depth=5,
       learning_rate=0.1,
       subsample=0.8,
       colsample_bytree=0.8,
       random_state=42
   )
   ```

3. **If overfitting**:
   - Decrease `max_depth` (e.g., 3-5)
   - Decrease `n_estimators`
   - Decrease `learning_rate` and increase `n_estimators`
   - Increase `reg_lambda`, `reg_alpha`, `gamma`
   - Decrease `subsample`, `colsample_bytree` (0.7-0.8)
   - Increase `min_child_weight`

4. **If underfitting**:
   - Increase `max_depth` (e.g., 7-10)
   - Increase `n_estimators`
   - Decrease regularization

5. **For fast experimentation**:
   - Use small `n_estimators` (50-100)
   - Use `subsample=0.5` (trains 2x faster)

---

## 🔗 Next Steps

- **Hyperparameter Tuning**: See [02_Hyperparameter_Tuning.md](02_Hyperparameter_Tuning.md)
- **Base Learners**: See [03_Base_Learners_Comparison.md](03_Base_Learners_Comparison.md)
- **Code Templates**: See [05_Code_Templates.md](05_Code_Templates.md)
