# Getting Started: Ensemble Learning & XGBoost Lab

## 📋 Overview

**Lab Topic**: Comparing ensemble learning with XGBoost using different hyperparameters and base learners

**What You'll Do**:
1. Implement various ensemble methods (Bagging, Random Forest, AdaBoost, Gradient Boosting)
2. Compare XGBoost with different hyperparameters
3. Test different base learners
4. Analyze and compare results

---

## 🛠️ Setup

### Required Libraries

```bash
# Install all required packages
pip install numpy pandas scikit-learn xgboost matplotlib seaborn
pip install torch torchvision  # If using PyTorch datasets
```

### Import Template

```python
# Data handling
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error

# Ensemble methods
from sklearn.ensemble import (
    BaggingClassifier, BaggingRegressor,
    RandomForestClassifier, RandomForestRegressor,
    AdaBoostClassifier, AdaBoostRegressor,
    GradientBoostingClassifier, GradientBoostingRegressor
)

# Base learners
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.svm import SVC, SVR
from sklearn.neighbors import KNeighborsClassifier

# XGBoost
import xgboost as xgb

# Visualization
import matplotlib.pyplot as plt
import seaborn as sns

# Utilities
import time
import warnings
warnings.filterwarnings('ignore')
```

---

## 📂 File Structure

```
Online 3/
├── 00_Getting_Started_Guide.md          (this file - start here)
├── 00a_What_Is_XGBoost.md              (what XGBoost is - read if new!)
├── 01_XGBoost_Basics.md                 (implementation details)
├── 02_Hyperparameter_Tuning.md          (tuning strategies)
├── 03_Base_Learners_Comparison.md       (different base models)
├── 04_Evaluation_Metrics.md             (how to compare)
├── 05_Code_Templates.md                 (ready-to-use code)
├── 06_Common_Pitfalls.md                (what to avoid)
├── 07_Quick_Reference_CheatSheet.md     (during-test reference)
└── Ensemble_Learning_Complete_Guide.md   (theory reference)
```

**📘 New to XGBoost?** Read [00a_What_Is_XGBoost.md](00a_What_Is_XGBoost.md) first! It explains what XGBoost is, why it exists, and how it actually works with simple examples and analogies.

---

## 🎯 Quick Start Workflow

### Step 1: Load Data
```python
# Example with sklearn datasets
from sklearn.datasets import load_breast_cancer, load_diabetes

# Classification
data = load_breast_cancer()
X, y = data.data, data.target

# Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
```

### Step 2: Train Basic Model
```python
# Start with basic XGBoost
model = xgb.XGBClassifier(random_state=42)
model.fit(X_train, y_train)
y_pred = model.predict(X_test)

# Evaluate
from sklearn.metrics import accuracy_score
print(f"Accuracy: {accuracy_score(y_test, y_pred):.4f}")
```

### Step 3: Compare Configurations
```python
# Try different hyperparameters
configs = [
    {'n_estimators': 50, 'max_depth': 3},
    {'n_estimators': 100, 'max_depth': 5},
    {'n_estimators': 200, 'max_depth': 7}
]

for config in configs:
    model = xgb.XGBClassifier(**config, random_state=42)
    model.fit(X_train, y_train)
    score = model.score(X_test, y_test)
    print(f"{config} -> Accuracy: {score:.4f}")
```

### Step 4: Store and Compare Results
```python
import pandas as pd

results = []
for name, model in models.items():
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    
    results.append({
        'Model': name,
        'Accuracy': accuracy_score(y_test, y_pred),
        'Time': time_taken
    })

df_results = pd.DataFrame(results)
print(df_results.sort_values('Accuracy', ascending=False))
```

---

## 🧪 Typical Lab Tasks

### Task 1: Compare Ensemble Methods
- Train: Bagging, Random Forest, AdaBoost, Gradient Boosting, XGBoost
- Same dataset, same test set
- Compare accuracy, training time, prediction time

### Task 2: Hyperparameter Sensitivity
- Pick one method (usually XGBoost)
- Vary one hyperparameter at a time:
  - `n_estimators`: [50, 100, 200, 500]
  - `max_depth`: [3, 5, 7, 10]
  - `learning_rate`: [0.01, 0.1, 0.3, 1.0]
- Plot: Hyperparameter value vs. Performance

### Task 3: Base Learner Comparison
- Use same ensemble method (e.g., Bagging or AdaBoost)
- Try different base learners:
  - Decision Tree (depth 1, 3, 5)
  - Logistic Regression / Linear Regression
  - SVM
  - KNN
- Compare results

### Task 4: Bias-Variance Analysis
- Plot learning curves
- Plot validation curves
- Analyze overfitting/underfitting

---

## 📊 Expected Outputs

You'll likely need to produce:

1. **Performance Table**
   ```
   | Model              | Accuracy | Precision | Recall | F1-Score | Time(s) |
   |--------------------|----------|-----------|--------|----------|---------|
   | XGBoost (default)  | 0.9532   | 0.9483    | 0.9621 | 0.9551   | 0.234   |
   | Random Forest      | 0.9474   | 0.9412    | 0.9586 | 0.9498   | 0.189   |
   | ...                | ...      | ...       | ...    | ...      | ...     |
   ```

2. **Hyperparameter Plots**
   - Line plots showing performance vs. hyperparameter value
   - Bar charts comparing different configurations

3. **Learning Curves**
   - Training vs. validation error over iterations
   - Shows overfitting behavior

4. **Feature Importance** (if asked)
   - Bar plot of top features

---

## ⚡ Pro Tips for Online Test

1. **Save Time with Templates**: Use the code templates from `05_Code_Templates.md`

2. **Use Default Random State**: Always set `random_state=42` for reproducibility

3. **Start Simple**: Get basic version working first, then optimize

4. **Print Intermediate Results**: Show your progress with prints

5. **Comment Your Code**: Helps you and graders understand

6. **Handle Errors Gracefully**:
   ```python
   try:
       model.fit(X_train, y_train)
   except Exception as e:
       print(f"Error: {e}")
   ```

7. **Time Your Code**:
   ```python
   import time
   start = time.time()
   model.fit(X_train, y_train)
   train_time = time.time() - start
   ```

8. **Create Reusable Functions**: Don't repeat code

---

## 📝 Checklist Before Test

- [ ] All libraries installed and importing correctly
- [ ] Understand basic XGBoost syntax
- [ ] Know how to tune at least 3 hyperparameters
- [ ] Can swap base learners in ensemble methods
- [ ] Can calculate and compare metrics
- [ ] Can create basic plots
- [ ] Have code templates ready
- [ ] Understand when to use classification vs. regression

---

## 🔗 Quick Navigation

- **Next**: Read [01_XGBoost_Basics.md](01_XGBoost_Basics.md) for implementation details
- **Theory**: Reference [Ensemble_Learning_Complete_Guide.md](Ensemble_Learning_Complete_Guide.md) for concepts
- **Code**: Jump to [05_Code_Templates.md](05_Code_Templates.md) for copy-paste ready code

---

Good luck! 🚀
