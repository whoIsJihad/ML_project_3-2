# Base Learners Comparison

## 🎯 What are Base Learners?

**Base Learner** (or **weak learner**): The individual model used in an ensemble method.

- **Bagging/Random Forest**: Uses Decision Trees as base learners
- **AdaBoost**: Can use any classifier, typically Decision Stumps (depth=1)
- **Gradient Boosting/XGBoost**: Typically uses Decision Trees

**Question**: What happens if we change the base learner?

---

## 🌲 Common Base Learners

### 1. Decision Trees (Most Common)
### 2. Linear Models (Logistic/Linear Regression)
### 3. SVM (Support Vector Machines)
### 4. K-Nearest Neighbors
### 5. Decision Stumps (depth=1 trees)

---

## 🔨 Implementation

### Setup

```python
from sklearn.ensemble import (
    BaggingClassifier, BaggingRegressor,
    AdaBoostClassifier, AdaBoostRegressor
)
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
from sklearn.linear_model import LogisticRegression, LinearRegression, Ridge
from sklearn.svm import SVC, SVR
from sklearn.neighbors import KNeighborsClassifier, KNeighborsRegressor
from sklearn.naive_bayes import GaussianNB

from sklearn.datasets import load_breast_cancer, load_diabetes
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score, mean_squared_error
import pandas as pd
import numpy as np
```

---

## 1️⃣ Bagging with Different Base Learners

### Classification Example

```python
# Load data
X, y = load_breast_cancer(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Define base learners
base_learners = {
    'Decision Tree (depth=3)': DecisionTreeClassifier(max_depth=3, random_state=42),
    'Decision Tree (depth=10)': DecisionTreeClassifier(max_depth=10, random_state=42),
    'Decision Tree (unlimited)': DecisionTreeClassifier(random_state=42),
    'Logistic Regression': LogisticRegression(random_state=42, max_iter=1000),
    'SVM': SVC(kernel='rbf', probability=True, random_state=42),
    'KNN (k=5)': KNeighborsClassifier(n_neighbors=5),
    'KNN (k=10)': KNeighborsClassifier(n_neighbors=10),
    'Naive Bayes': GaussianNB()
}

# Test each base learner in Bagging
results = []

for name, base_estimator in base_learners.items():
    # Single base learner
    base_estimator_clone = clone(base_estimator)
    base_estimator_clone.fit(X_train, y_train)
    base_score = base_estimator_clone.score(X_test, y_test)
    
    # Bagging ensemble
    bagging = BaggingClassifier(
        estimator=base_estimator,
        n_estimators=50,
        max_samples=0.8,
        max_features=0.8,
        random_state=42
    )
    bagging.fit(X_train, y_train)
    bagging_score = bagging.score(X_test, y_test)
    
    results.append({
        'Base Learner': name,
        'Single Model Accuracy': base_score,
        'Bagging Accuracy': bagging_score,
        'Improvement': bagging_score - base_score
    })
    
    print(f"{name}:")
    print(f"  Single: {base_score:.4f}")
    print(f"  Bagging: {bagging_score:.4f}")
    print(f"  Improvement: {bagging_score - base_score:.4f}\n")

# Create DataFrame
df_results = pd.DataFrame(results)
print("\nSummary:")
print(df_results.sort_values('Bagging Accuracy', ascending=False))
```

### Expected Output Pattern

```
Base Learner                  Single    Bagging   Improvement
Decision Tree (unlimited)     0.9298    0.9649    +0.0351    <- High variance, big gain
Decision Tree (depth=10)      0.9474    0.9649    +0.0175    <- Moderate gain
Decision Tree (depth=3)       0.9298    0.9474    +0.0176    <- Moderate gain
Logistic Regression           0.9561    0.9561    +0.0000    <- Stable, no gain
SVM                          0.9474    0.9649    +0.0175    <- Some gain
KNN (k=5)                    0.9298    0.9561    +0.0263    <- Good gain
Naive Bayes                  0.9386    0.9474    +0.0088    <- Small gain
```

**Key Insight**: Bagging helps most with **high-variance models** (deep trees, KNN). It doesn't help **stable models** (Logistic Regression).

---

## 2️⃣ AdaBoost with Different Base Learners

```python
# AdaBoost works best with weak learners

base_learners_ada = {
    'Decision Stump (depth=1)': DecisionTreeClassifier(max_depth=1, random_state=42),
    'Shallow Tree (depth=2)': DecisionTreeClassifier(max_depth=2, random_state=42),
    'Shallow Tree (depth=3)': DecisionTreeClassifier(max_depth=3, random_state=42),
    'Deep Tree (depth=10)': DecisionTreeClassifier(max_depth=10, random_state=42),
    'Logistic Regression': LogisticRegression(random_state=42, max_iter=1000),
    'SVM (linear)': SVC(kernel='linear', probability=True, random_state=42),
}

results_ada = []

for name, base_estimator in base_learners_ada.items():
    # Single base learner
    from sklearn.base import clone
    base_clone = clone(base_estimator)
    base_clone.fit(X_train, y_train)
    base_score = base_clone.score(X_test, y_test)
    
    # AdaBoost ensemble
    try:
        adaboost = AdaBoostClassifier(
            estimator=base_estimator,
            n_estimators=50,
            learning_rate=1.0,
            random_state=42
        )
        adaboost.fit(X_train, y_train)
        ada_score = adaboost.score(X_test, y_test)
        
        results_ada.append({
            'Base Learner': name,
            'Single Model': base_score,
            'AdaBoost': ada_score,
            'Improvement': ada_score - base_score
        })
        
        print(f"{name}:")
        print(f"  Single: {base_score:.4f}")
        print(f"  AdaBoost: {ada_score:.4f}")
        print(f"  Improvement: {ada_score - base_score:.4f}\n")
        
    except Exception as e:
        print(f"{name}: Error - {e}\n")

# Summary
df_ada = pd.DataFrame(results_ada)
print("\nSummary:")
print(df_ada.sort_values('AdaBoost', ascending=False))
```

### Expected Pattern

```
Base Learner               Single    AdaBoost  Improvement
Decision Stump (depth=1)   0.8947    0.9649    +0.0702    <- Weak learner, huge boost!
Shallow Tree (depth=2)     0.9298    0.9649    +0.0351    <- Good boost
Shallow Tree (depth=3)     0.9298    0.9561    +0.0263    <- Decent boost
Deep Tree (depth=10)       0.9474    0.9474    +0.0000    <- Already strong, no boost
Logistic Regression        0.9561    0.9649    +0.0088    <- Small boost
```

**Key Insight**: AdaBoost works best with **weak learners** (stumps, shallow trees). Strong learners (deep trees) don't benefit much.

---

## 3️⃣ Comparing Ensemble Methods with Same Base Learner

```python
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier

# Use Decision Trees (depth=3) as base learner for all
base_tree = DecisionTreeClassifier(max_depth=3, random_state=42)

# Single tree
single_tree = clone(base_tree)
single_tree.fit(X_train, y_train)
single_score = single_tree.score(X_test, y_test)

# Bagging
bagging = BaggingClassifier(
    estimator=base_tree,
    n_estimators=100,
    random_state=42
)
bagging.fit(X_train, y_train)
bagging_score = bagging.score(X_test, y_test)

# Random Forest (depth=3 trees)
rf = RandomForestClassifier(
    n_estimators=100,
    max_depth=3,
    random_state=42
)
rf.fit(X_train, y_train)
rf_score = rf.score(X_test, y_test)

# AdaBoost
adaboost = AdaBoostClassifier(
    estimator=base_tree,
    n_estimators=100,
    learning_rate=1.0,
    random_state=42
)
adaboost.fit(X_train, y_train)
ada_score = adaboost.score(X_test, y_test)

# Gradient Boosting (depth=3)
gb = GradientBoostingClassifier(
    n_estimators=100,
    max_depth=3,
    learning_rate=0.1,
    random_state=42
)
gb.fit(X_train, y_train)
gb_score = gb.score(X_test, y_test)

# XGBoost (depth=3)
import xgboost as xgb
xgb_model = xgb.XGBClassifier(
    n_estimators=100,
    max_depth=3,
    learning_rate=0.1,
    random_state=42
)
xgb_model.fit(X_train, y_train)
xgb_score = xgb_model.score(X_test, y_test)

# Compare
comparison = pd.DataFrame({
    'Method': ['Single Tree', 'Bagging', 'Random Forest', 
               'AdaBoost', 'Gradient Boosting', 'XGBoost'],
    'Accuracy': [single_score, bagging_score, rf_score, 
                 ada_score, gb_score, xgb_score]
})

comparison['Improvement vs Single'] = comparison['Accuracy'] - single_score

print(comparison.sort_values('Accuracy', ascending=False))

# Visualize
import matplotlib.pyplot as plt

plt.figure(figsize=(10, 6))
plt.barh(comparison['Method'], comparison['Accuracy'])
plt.xlabel('Accuracy')
plt.title('Comparison of Ensemble Methods (all using depth=3 trees)')
plt.xlim([comparison['Accuracy'].min() - 0.02, 1.0])
for i, v in enumerate(comparison['Accuracy']):
    plt.text(v + 0.005, i, f'{v:.4f}', va='center')
plt.tight_layout()
plt.show()
```

---

## 4️⃣ Effect of Base Learner Complexity

### Experiment: Vary Tree Depth

```python
# Test how ensemble methods perform with different base learner depths
depths = [1, 2, 3, 5, 7, 10, 15]

results_depth = []

for depth in depths:
    # Bagging
    bagging = BaggingClassifier(
        estimator=DecisionTreeClassifier(max_depth=depth, random_state=42),
        n_estimators=50,
        random_state=42
    )
    bagging.fit(X_train, y_train)
    bagging_score = bagging.score(X_test, y_test)
    
    # AdaBoost
    adaboost = AdaBoostClassifier(
        estimator=DecisionTreeClassifier(max_depth=depth, random_state=42),
        n_estimators=50,
        random_state=42
    )
    adaboost.fit(X_train, y_train)
    ada_score = adaboost.score(X_test, y_test)
    
    # XGBoost
    xgb_model = xgb.XGBClassifier(
        max_depth=depth,
        n_estimators=50,
        random_state=42
    )
    xgb_model.fit(X_train, y_train)
    xgb_score = xgb_model.score(X_test, y_test)
    
    results_depth.append({
        'depth': depth,
        'Bagging': bagging_score,
        'AdaBoost': ada_score,
        'XGBoost': xgb_score
    })

df_depth = pd.DataFrame(results_depth)

# Plot
plt.figure(figsize=(12, 6))
plt.plot(df_depth['depth'], df_depth['Bagging'], 
         marker='o', label='Bagging', linewidth=2)
plt.plot(df_depth['depth'], df_depth['AdaBoost'], 
         marker='s', label='AdaBoost', linewidth=2)
plt.plot(df_depth['depth'], df_depth['XGBoost'], 
         marker='^', label='XGBoost', linewidth=2)
plt.xlabel('Tree Depth (Base Learner Complexity)')
plt.ylabel('Accuracy')
plt.title('Ensemble Performance vs Base Learner Complexity')
plt.legend()
plt.grid(True, alpha=0.3)
plt.xticks(depths)
plt.show()

print(df_depth)
```

### Expected Observations:

1. **Bagging**: Benefits from deeper trees (more variance to average out)
2. **AdaBoost**: Works best with shallow trees (weak learners)
3. **XGBoost**: More flexible, good with moderate depth (3-7)

---

## 5️⃣ Regression: Base Learner Comparison

```python
# Load regression data
X, y = load_diabetes(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Define base learners for regression
base_learners_reg = {
    'Decision Tree (depth=3)': DecisionTreeRegressor(max_depth=3, random_state=42),
    'Decision Tree (depth=10)': DecisionTreeRegressor(max_depth=10, random_state=42),
    'Linear Regression': LinearRegression(),
    'Ridge Regression': Ridge(alpha=1.0),
    'SVR': SVR(kernel='rbf'),
    'KNN (k=5)': KNeighborsRegressor(n_neighbors=5)
}

results_reg = []

for name, base_estimator in base_learners_reg.items():
    # Single model
    base_clone = clone(base_estimator)
    base_clone.fit(X_train, y_train)
    y_pred_base = base_clone.predict(X_test)
    base_mse = mean_squared_error(y_test, y_pred_base)
    base_rmse = np.sqrt(base_mse)
    
    # Bagging
    bagging_reg = BaggingRegressor(
        estimator=base_estimator,
        n_estimators=50,
        random_state=42
    )
    bagging_reg.fit(X_train, y_train)
    y_pred_bag = bagging_reg.predict(X_test)
    bag_mse = mean_squared_error(y_test, y_pred_bag)
    bag_rmse = np.sqrt(bag_mse)
    
    results_reg.append({
        'Base Learner': name,
        'Single RMSE': base_rmse,
        'Bagging RMSE': bag_rmse,
        'Improvement': base_rmse - bag_rmse
    })
    
    print(f"{name}:")
    print(f"  Single RMSE: {base_rmse:.4f}")
    print(f"  Bagging RMSE: {bag_rmse:.4f}")
    print(f"  Improvement: {base_rmse - bag_rmse:.4f}\n")

df_reg = pd.DataFrame(results_reg)
print("\nSummary (lower RMSE is better):")
print(df_reg.sort_values('Bagging RMSE'))
```

---

## 6️⃣ Complete Comparison Function

```python
def compare_base_learners(X_train, X_test, y_train, y_test, 
                         task_type='classification'):
    """
    Complete comparison of different base learners in ensemble methods
    """
    from sklearn.base import clone
    import time
    
    if task_type == 'classification':
        base_learners = {
            'Stump (depth=1)': DecisionTreeClassifier(max_depth=1, random_state=42),
            'Tree (depth=3)': DecisionTreeClassifier(max_depth=3, random_state=42),
            'Tree (depth=10)': DecisionTreeClassifier(max_depth=10, random_state=42),
            'Logistic Reg': LogisticRegression(random_state=42, max_iter=1000),
        }
        metric = accuracy_score
        metric_name = 'Accuracy'
    else:
        base_learners = {
            'Stump (depth=1)': DecisionTreeRegressor(max_depth=1, random_state=42),
            'Tree (depth=3)': DecisionTreeRegressor(max_depth=3, random_state=42),
            'Tree (depth=10)': DecisionTreeRegressor(max_depth=10, random_state=42),
            'Linear Reg': LinearRegression(),
        }
        metric = lambda y_true, y_pred: -np.sqrt(mean_squared_error(y_true, y_pred))
        metric_name = 'Neg RMSE'
    
    results = []
    
    for base_name, base_est in base_learners.items():
        print(f"\nTesting: {base_name}")
        
        # Single model
        start = time.time()
        single = clone(base_est)
        single.fit(X_train, y_train)
        y_pred = single.predict(X_test)
        single_score = metric(y_test, y_pred)
        single_time = time.time() - start
        
        # Bagging
        start = time.time()
        if task_type == 'classification':
            bag = BaggingClassifier(estimator=base_est, n_estimators=50, random_state=42)
        else:
            bag = BaggingRegressor(estimator=base_est, n_estimators=50, random_state=42)
        bag.fit(X_train, y_train)
        y_pred = bag.predict(X_test)
        bag_score = metric(y_test, y_pred)
        bag_time = time.time() - start
        
        # AdaBoost
        start = time.time()
        if task_type == 'classification':
            ada = AdaBoostClassifier(estimator=base_est, n_estimators=50, random_state=42)
        else:
            ada = AdaBoostRegressor(estimator=base_est, n_estimators=50, random_state=42)
        ada.fit(X_train, y_train)
        y_pred = ada.predict(X_test)
        ada_score = metric(y_test, y_pred)
        ada_time = time.time() - start
        
        results.append({
            'Base Learner': base_name,
            f'Single {metric_name}': single_score,
            f'Bagging {metric_name}': bag_score,
            f'AdaBoost {metric_name}': ada_score,
            'Single Time': single_time,
            'Bagging Time': bag_time,
            'AdaBoost Time': ada_time
        })
    
    return pd.DataFrame(results)

# Usage
df_comparison = compare_base_learners(X_train, X_test, y_train, y_test, 
                                     task_type='classification')
print(df_comparison)
```

---

## 💡 Key Takeaways

### When to Use Which Base Learner?

| Ensemble Method | Best Base Learner | Why |
|----------------|-------------------|-----|
| **Bagging** | Deep trees, high-variance models | More variance to average out |
| **Random Forest** | Deep trees | Same as bagging, built for trees |
| **AdaBoost** | Weak learners (stumps, shallow trees) | Boosting makes them strong |
| **Gradient Boosting** | Shallow-medium trees (depth 3-6) | Sequential correction of errors |
| **XGBoost** | Shallow-medium trees (depth 3-7) | Regularized, handles complexity well |

### General Rules:

1. **High Bias Base Learner** (stump, linear model)
   - → Use Boosting (AdaBoost, Gradient Boosting)
   - Boosting reduces bias

2. **High Variance Base Learner** (deep tree, KNN)
   - → Use Bagging/Random Forest
   - Averaging reduces variance

3. **Stable Base Learner** (already low variance)
   - → Ensemble won't help much
   - Example: Logistic Regression with Bagging = no improvement

---

## 🔗 Next Steps

- **Evaluation**: See [04_Evaluation_Metrics.md](04_Evaluation_Metrics.md)
- **Templates**: See [05_Code_Templates.md](05_Code_Templates.md)
