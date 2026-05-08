# Hyperparameter Tuning Guide

## 🎯 Goal

Find the best hyperparameters that maximize model performance on unseen data.

---

## 🔍 Three Main Approaches

### 1. Manual Search (Good for Understanding)
### 2. Grid Search (Exhaustive)
### 3. Random Search (Efficient)

---

## 1️⃣ Manual Search

**Best for**: Learning, small experiments, online tests (when you need to show work)

### Strategy: Vary One Parameter at a Time

```python
import numpy as np
import pandas as pd
from xgboost import XGBClassifier
from sklearn.model_selection import cross_val_score
import matplotlib.pyplot as plt

# Load data
X_train, X_test, y_train, y_test = ...  # your data

# Function to test a parameter
def test_parameter(param_name, param_values, base_params=None):
    """
    Test different values of a single parameter
    """
    if base_params is None:
        base_params = {'random_state': 42}
    
    results = []
    
    for value in param_values:
        # Create model with this parameter value
        params = base_params.copy()
        params[param_name] = value
        
        model = XGBClassifier(**params)
        
        # Cross-validation
        scores = cross_val_score(model, X_train, y_train, 
                                cv=5, scoring='accuracy')
        
        results.append({
            param_name: value,
            'mean_score': scores.mean(),
            'std_score': scores.std()
        })
        
        print(f"{param_name}={value}: {scores.mean():.4f} (+/- {scores.std():.4f})")
    
    return pd.DataFrame(results)
```

### Example 1: Tuning `n_estimators`

```python
# Test different numbers of trees
n_estimators_values = [50, 100, 200, 300, 500, 1000]

results_n_est = test_parameter(
    'n_estimators', 
    n_estimators_values,
    base_params={'max_depth': 3, 'learning_rate': 0.1, 'random_state': 42}
)

# Plot results
plt.figure(figsize=(10, 5))
plt.errorbar(results_n_est['n_estimators'], 
             results_n_est['mean_score'],
             yerr=results_n_est['std_score'],
             marker='o', capsize=5)
plt.xlabel('n_estimators')
plt.ylabel('Accuracy')
plt.title('Effect of n_estimators on Model Performance')
plt.grid(True, alpha=0.3)
plt.show()

# Best value
best_n_est = results_n_est.loc[results_n_est['mean_score'].idxmax(), 'n_estimators']
print(f"Best n_estimators: {best_n_est}")
```

### Example 2: Tuning `max_depth`

```python
# Test different tree depths
max_depth_values = [2, 3, 4, 5, 6, 7, 8, 10]

results_depth = test_parameter(
    'max_depth',
    max_depth_values,
    base_params={'n_estimators': 100, 'learning_rate': 0.1, 'random_state': 42}
)

# Plot
plt.figure(figsize=(10, 5))
plt.plot(results_depth['max_depth'], results_depth['mean_score'], 
         marker='o', linewidth=2)
plt.fill_between(results_depth['max_depth'],
                 results_depth['mean_score'] - results_depth['std_score'],
                 results_depth['mean_score'] + results_depth['std_score'],
                 alpha=0.3)
plt.xlabel('max_depth')
plt.ylabel('Accuracy')
plt.title('Effect of max_depth on Model Performance')
plt.grid(True, alpha=0.3)
plt.show()

best_depth = results_depth.loc[results_depth['mean_score'].idxmax(), 'max_depth']
print(f"Best max_depth: {best_depth}")
```

### Example 3: Tuning `learning_rate`

```python
# Test different learning rates
learning_rate_values = [0.01, 0.05, 0.1, 0.2, 0.3, 0.5]

# Note: Lower learning rates need more trees
results_lr = []

for lr in learning_rate_values:
    # Adjust n_estimators based on learning rate
    n_est = int(100 / lr)  # Inverse relationship
    
    model = XGBClassifier(
        n_estimators=n_est,
        learning_rate=lr,
        max_depth=3,
        random_state=42
    )
    
    scores = cross_val_score(model, X_train, y_train, cv=5)
    
    results_lr.append({
        'learning_rate': lr,
        'n_estimators': n_est,
        'mean_score': scores.mean(),
        'std_score': scores.std()
    })
    
    print(f"lr={lr}, n_est={n_est}: {scores.mean():.4f}")

df_lr = pd.DataFrame(results_lr)

# Plot
plt.figure(figsize=(10, 5))
plt.semilogx(df_lr['learning_rate'], df_lr['mean_score'], 
             marker='o', linewidth=2)
plt.xlabel('Learning Rate (log scale)')
plt.ylabel('Accuracy')
plt.title('Effect of Learning Rate on Model Performance')
plt.grid(True, alpha=0.3)
plt.show()
```

---

## 2️⃣ Grid Search

**Best for**: Finding optimal combination when you have limited parameters

### Basic Grid Search

```python
from sklearn.model_selection import GridSearchCV

# Define parameter grid
param_grid = {
    'n_estimators': [100, 200, 300],
    'max_depth': [3, 5, 7],
    'learning_rate': [0.01, 0.1, 0.3],
    'subsample': [0.8, 1.0],
    'colsample_bytree': [0.8, 1.0]
}

# Create model
model = XGBClassifier(random_state=42)

# Grid search
grid_search = GridSearchCV(
    model,
    param_grid,
    cv=5,                    # 5-fold cross-validation
    scoring='accuracy',      # or 'roc_auc', 'f1', etc.
    n_jobs=-1,              # Use all CPU cores
    verbose=2                # Show progress
)

# Fit
grid_search.fit(X_train, y_train)

# Best parameters
print("Best parameters:")
print(grid_search.best_params_)
print(f"\nBest cross-validation score: {grid_search.best_score_:.4f}")

# Best model
best_model = grid_search.best_estimator_

# Test on test set
test_score = best_model.score(X_test, y_test)
print(f"Test score: {test_score:.4f}")
```

### Analyzing Grid Search Results

```python
# Get all results
results_df = pd.DataFrame(grid_search.cv_results_)

# Show top 10 configurations
top_results = results_df.sort_values('rank_test_score')[
    ['params', 'mean_test_score', 'std_test_score', 'rank_test_score']
].head(10)

print(top_results)

# Plot parameter effects
import seaborn as sns

# Extract specific parameters for visualization
results_df['max_depth'] = results_df['params'].apply(lambda x: x['max_depth'])
results_df['learning_rate'] = results_df['params'].apply(lambda x: x['learning_rate'])

# Heatmap: max_depth vs learning_rate
pivot_table = results_df.pivot_table(
    values='mean_test_score',
    index='max_depth',
    columns='learning_rate',
    aggfunc='mean'
)

plt.figure(figsize=(10, 6))
sns.heatmap(pivot_table, annot=True, fmt='.4f', cmap='viridis')
plt.title('Mean Test Score: max_depth vs learning_rate')
plt.show()
```

---

## 3️⃣ Random Search

**Best for**: Large parameter spaces, limited time

```python
from sklearn.model_selection import RandomizedSearchCV
from scipy.stats import uniform, randint

# Define parameter distributions
param_distributions = {
    'n_estimators': randint(50, 500),           # Random integers
    'max_depth': randint(3, 10),
    'learning_rate': uniform(0.01, 0.3),        # Uniform distribution
    'subsample': uniform(0.6, 0.4),             # 0.6 to 1.0
    'colsample_bytree': uniform(0.6, 0.4),
    'gamma': uniform(0, 5),
    'reg_lambda': uniform(0, 10),
    'min_child_weight': randint(1, 10)
}

# Create model
model = XGBClassifier(random_state=42)

# Random search
random_search = RandomizedSearchCV(
    model,
    param_distributions,
    n_iter=50,              # Number of random combinations to try
    cv=5,
    scoring='accuracy',
    n_jobs=-1,
    verbose=2,
    random_state=42
)

# Fit
random_search.fit(X_train, y_train)

# Best parameters
print("Best parameters:")
print(random_search.best_params_)
print(f"\nBest score: {random_search.best_score_:.4f}")
```

---

## 🎨 Systematic Tuning Strategy

### Step-by-Step Tuning Process

```python
# Step 1: Fix learning rate and tune tree parameters
print("Step 1: Tuning tree parameters...")
param_grid_step1 = {
    'max_depth': [3, 5, 7, 9],
    'min_child_weight': [1, 3, 5]
}

grid1 = GridSearchCV(
    XGBClassifier(learning_rate=0.1, n_estimators=100, random_state=42),
    param_grid_step1,
    cv=5,
    scoring='accuracy',
    n_jobs=-1
)
grid1.fit(X_train, y_train)

best_depth = grid1.best_params_['max_depth']
best_min_child = grid1.best_params_['min_child_weight']
print(f"Best max_depth: {best_depth}, min_child_weight: {best_min_child}")


# Step 2: Tune gamma
print("\nStep 2: Tuning gamma...")
param_grid_step2 = {
    'gamma': [0, 0.1, 0.2, 0.5, 1.0, 2.0]
}

grid2 = GridSearchCV(
    XGBClassifier(
        learning_rate=0.1, 
        n_estimators=100,
        max_depth=best_depth,
        min_child_weight=best_min_child,
        random_state=42
    ),
    param_grid_step2,
    cv=5,
    scoring='accuracy',
    n_jobs=-1
)
grid2.fit(X_train, y_train)

best_gamma = grid2.best_params_['gamma']
print(f"Best gamma: {best_gamma}")


# Step 3: Tune subsample and colsample_bytree
print("\nStep 3: Tuning subsample and colsample_bytree...")
param_grid_step3 = {
    'subsample': [0.6, 0.7, 0.8, 0.9, 1.0],
    'colsample_bytree': [0.6, 0.7, 0.8, 0.9, 1.0]
}

grid3 = GridSearchCV(
    XGBClassifier(
        learning_rate=0.1,
        n_estimators=100,
        max_depth=best_depth,
        min_child_weight=best_min_child,
        gamma=best_gamma,
        random_state=42
    ),
    param_grid_step3,
    cv=5,
    scoring='accuracy',
    n_jobs=-1
)
grid3.fit(X_train, y_train)

best_subsample = grid3.best_params_['subsample']
best_colsample = grid3.best_params_['colsample_bytree']
print(f"Best subsample: {best_subsample}, colsample: {best_colsample}")


# Step 4: Tune regularization
print("\nStep 4: Tuning regularization...")
param_grid_step4 = {
    'reg_lambda': [0, 0.1, 1, 10, 100],
    'reg_alpha': [0, 0.01, 0.1, 1, 10]
}

grid4 = GridSearchCV(
    XGBClassifier(
        learning_rate=0.1,
        n_estimators=100,
        max_depth=best_depth,
        min_child_weight=best_min_child,
        gamma=best_gamma,
        subsample=best_subsample,
        colsample_bytree=best_colsample,
        random_state=42
    ),
    param_grid_step4,
    cv=5,
    scoring='accuracy',
    n_jobs=-1
)
grid4.fit(X_train, y_train)

best_lambda = grid4.best_params_['reg_lambda']
best_alpha = grid4.best_params_['reg_alpha']
print(f"Best reg_lambda: {best_lambda}, reg_alpha: {best_alpha}")


# Step 5: Lower learning rate and increase n_estimators
print("\nStep 5: Final tuning with lower learning rate...")
param_grid_step5 = {
    'learning_rate': [0.01, 0.05, 0.1],
    'n_estimators': [100, 200, 500, 1000]
}

grid5 = GridSearchCV(
    XGBClassifier(
        max_depth=best_depth,
        min_child_weight=best_min_child,
        gamma=best_gamma,
        subsample=best_subsample,
        colsample_bytree=best_colsample,
        reg_lambda=best_lambda,
        reg_alpha=best_alpha,
        random_state=42
    ),
    param_grid_step5,
    cv=5,
    scoring='accuracy',
    n_jobs=-1
)
grid5.fit(X_train, y_train)

print("\nFinal best parameters:")
print(grid5.best_params_)

# Final model
final_model = grid5.best_estimator_
test_score = final_model.score(X_test, y_test)
print(f"\nFinal test score: {test_score:.4f}")
```

---

## 📊 Comparing Effects of Multiple Hyperparameters

```python
# Create a comparison across multiple dimensions
configs = []

# Vary n_estimators
for n_est in [50, 100, 200]:
    model = XGBClassifier(n_estimators=n_est, random_state=42)
    scores = cross_val_score(model, X_train, y_train, cv=5)
    configs.append({
        'varied_param': 'n_estimators',
        'value': n_est,
        'mean_score': scores.mean(),
        'std_score': scores.std()
    })

# Vary max_depth
for depth in [3, 5, 7]:
    model = XGBClassifier(max_depth=depth, random_state=42)
    scores = cross_val_score(model, X_train, y_train, cv=5)
    configs.append({
        'varied_param': 'max_depth',
        'value': depth,
        'mean_score': scores.mean(),
        'std_score': scores.std()
    })

# Vary learning_rate
for lr in [0.01, 0.1, 0.3]:
    model = XGBClassifier(learning_rate=lr, n_estimators=200, random_state=42)
    scores = cross_val_score(model, X_train, y_train, cv=5)
    configs.append({
        'varied_param': 'learning_rate',
        'value': lr,
        'mean_score': scores.mean(),
        'std_score': scores.std()
    })

# Create DataFrame
df_comparison = pd.DataFrame(configs)

# Plot all comparisons
fig, axes = plt.subplots(1, 3, figsize=(15, 4))

for idx, param in enumerate(['n_estimators', 'max_depth', 'learning_rate']):
    data = df_comparison[df_comparison['varied_param'] == param]
    
    axes[idx].errorbar(data['value'], data['mean_score'], 
                       yerr=data['std_score'], 
                       marker='o', capsize=5, linewidth=2)
    axes[idx].set_xlabel(param)
    axes[idx].set_ylabel('Accuracy')
    axes[idx].set_title(f'Effect of {param}')
    axes[idx].grid(True, alpha=0.3)

plt.tight_layout()
plt.show()
```

---

## 💡 Tips for Lab

1. **Start Simple**: Test one parameter at a time first

2. **Use Cross-Validation**: Always use CV, not just train-test split

3. **Plot Results**: Visualizations show trends clearly

4. **Document Everything**: Save results in DataFrames

5. **Time Constraints**: In online test, use manual search with 3-5 values per parameter

6. **Quick Template for Lab**:

```python
# Quick parameter comparison for lab
params_to_test = {
    'n_estimators': [50, 100, 200],
    'max_depth': [3, 5, 7],
    'learning_rate': [0.01, 0.1, 0.3]
}

results = []

for param_name, values in params_to_test.items():
    for value in values:
        # Create model with this parameter
        params = {'random_state': 42, param_name: value}
        model = XGBClassifier(**params)
        
        # Cross-validate
        scores = cross_val_score(model, X_train, y_train, cv=5)
        
        results.append({
            'Parameter': param_name,
            'Value': value,
            'Mean Accuracy': scores.mean(),
            'Std': scores.std()
        })

# Show results
df_results = pd.DataFrame(results)
print(df_results.sort_values('Mean Accuracy', ascending=False))
```

---

## 🔗 Next Steps

- **Base Learners**: See [03_Base_Learners_Comparison.md](03_Base_Learners_Comparison.md)
- **Evaluation**: See [04_Evaluation_Metrics.md](04_Evaluation_Metrics.md)
- **Ready Code**: See [05_Code_Templates.md](05_Code_Templates.md)
