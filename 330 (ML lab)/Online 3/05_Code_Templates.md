# Code Templates - Ready to Use# Ready-to-Use Code Templates





























































































































































































































































































































































































































































































































































































































































































- **Metrics**: See [04_Evaluation_Metrics.md](04_Evaluation_Metrics.md)- **Tuning**: See [02_Hyperparameter_Tuning.md](02_Hyperparameter_Tuning.md)- **Concepts**: See [01_XGBoost_Basics.md](01_XGBoost_Basics.md)## 🔗 Related Files---5. **Print intermediate results** - helps debug and shows progress4. **Save plots** - use `plt.savefig()` before `plt.show()`3. **Run section by section** - don't run everything at once2. **Modify the dataset loading section** for your specific data1. **Copy the template that matches your task**## 💡 Pro Tips---```print("✅ Learning curve saved!")plt.show()plt.savefig('learning_curve.png', dpi=300)plt.tight_layout()plt.grid(True, alpha=0.3)plt.legend(loc='best', fontsize=12)plt.title('Learning Curve', fontsize=14)plt.ylabel('Accuracy', fontsize=12)plt.xlabel('Training Set Size', fontsize=12)plt.fill_between(train_sizes, val_mean - val_std, val_mean + val_std, alpha=0.3)plt.plot(train_sizes, val_mean, 'o-', label='Validation Score', linewidth=2, markersize=8)plt.fill_between(train_sizes, train_mean - train_std, train_mean + train_std, alpha=0.3)plt.plot(train_sizes, train_mean, 'o-', label='Training Score', linewidth=2, markersize=8)plt.figure(figsize=(10, 6))# Plotval_std = val_scores.std(axis=1)val_mean = val_scores.mean(axis=1)train_std = train_scores.std(axis=1)train_mean = train_scores.mean(axis=1)# Calculate statistics)    n_jobs=-1    scoring='accuracy',    cv=5,    train_sizes=np.linspace(0.1, 1.0, 10),    model, X, y,train_sizes, train_scores, val_scores = learning_curve(# Generate learning curvemodel = XGBClassifier(n_estimators=100, max_depth=3, random_state=42)# Create modelX, y = load_breast_cancer(return_X_y=True)# Load datafrom xgboost import XGBClassifierfrom sklearn.datasets import load_breast_cancerfrom sklearn.model_selection import learning_curveimport matplotlib.pyplot as pltimport numpy as np"""Generate learning curves to analyze bias-variance"""```python## Template 5: Learning Curve Visualization---```print("\n", df.round(4))df = pd.DataFrame(results)# Show results    print(f"{name}: Acc={acc:.4f}, F1={f1:.4f}, Time={train_time:.2f}s")    results.append({'Model': name, 'Accuracy': acc, 'F1': f1, 'Time': train_time})        f1 = f1_score(y_test, y_pred, average='weighted')    acc = accuracy_score(y_test, y_pred)    y_pred = model.predict(X_test)        train_time = time.time() - start    model.fit(X_train, y_train)    start = time.time()for name, model in models.items():results = []# Train and evaluate}    'XGBoost': XGBClassifier(n_estimators=100, random_state=42)    'Gradient Boosting': GradientBoostingClassifier(n_estimators=100, random_state=42),    'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42),models = {# Define modelsX_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)X, y = load_breast_cancer(return_X_y=True)# Load dataimport timefrom sklearn.metrics import accuracy_score, f1_scorefrom xgboost import XGBClassifierfrom sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifierfrom sklearn.model_selection import train_test_splitfrom sklearn.datasets import load_breast_cancerimport pandas as pdimport numpy as np"""Quick comparison template - Use this during online test!"""```python## Template 4: Quick Comparison (For Time-Limited Labs)---```print("\n✅ Base learner comparison complete!")plt.show()plt.savefig('base_learner_comparison.png', dpi=300, bbox_inches='tight')plt.tight_layout()ax.grid(True, alpha=0.3, axis='y')ax.legend()ax.axhline(y=0, color='black', linestyle='-', linewidth=0.8)ax.set_xticklabels(df_results['Base Learner'], rotation=45, ha='right')ax.set_xticks(x)ax.set_title('Ensemble Improvement over Single Model')ax.set_ylabel('Accuracy Improvement')ax.set_xlabel('Base Learner')ax.bar(x + width/2, df_results['AdaBoost Gain'], width, label='AdaBoost Gain', alpha=0.8)ax.bar(x - width/2, df_results['Bagging Gain'], width, label='Bagging Gain', alpha=0.8)x = np.arange(len(df_results))ax = axes[1]# Plot 2: Improvement gainsax.grid(True, alpha=0.3, axis='y')ax.legend()ax.set_xticklabels(df_results['Base Learner'], rotation=45, ha='right')ax.set_xticks(x)ax.set_title('Accuracy Comparison')ax.set_ylabel('Accuracy')ax.set_xlabel('Base Learner')ax.bar(x + width, df_results['AdaBoost'], width, label='AdaBoost', alpha=0.8)ax.bar(x, df_results['Bagging'], width, label='Bagging', alpha=0.8)ax.bar(x - width, df_results['Single'], width, label='Single', alpha=0.8)width = 0.25x = np.arange(len(df_results))ax = axes[0]# Plot 1: Absolute scoresfig, axes = plt.subplots(1, 2, figsize=(15, 5))# =====================================================# VISUALIZATION# =====================================================print(df_results.round(4).to_string(index=False))print("="*80)print("SUMMARY")print("\n" + "="*80)df_results = pd.DataFrame(results)# =====================================================# RESULTS SUMMARY# =====================================================    })        'AdaBoost Gain': adaboost_score - single_score if not np.isnan(adaboost_score) else 0        'Bagging Gain': bagging_score - single_score if not np.isnan(bagging_score) else 0,        'AdaBoost': adaboost_score,        'Bagging': bagging_score,        'Single': single_score,        'Base Learner': name,    results.append({            print(f"  AdaBoost:     Failed")        adaboost_score = np.nan    except:        print(f"  AdaBoost:     {adaboost_score:.4f} (Δ: {adaboost_score - single_score:+.4f})")        adaboost_score = adaboost.score(X_test, y_test)        adaboost.fit(X_train, y_train)        )            random_state=42            n_estimators=50,            estimator=base_estimator,        adaboost = AdaBoostClassifier(    try:    # 3. AdaBoost            print(f"  Bagging:      Failed")        bagging_score = np.nan    except:        print(f"  Bagging:      {bagging_score:.4f} (Δ: {bagging_score - single_score:+.4f})")        bagging_score = bagging.score(X_test, y_test)        bagging.fit(X_train, y_train)        )            random_state=42            n_estimators=50,            estimator=base_estimator,        bagging = BaggingClassifier(    try:    # 2. Bagging        print(f"  Single Model: {single_score:.4f}")    single_score = single.score(X_test, y_test)    single.fit(X_train, y_train)    single = clone(base_estimator)    # 1. Single model        print("-" * 60)    print(f"\nTesting: {name}")for name, base_estimator in base_learners.items():results = []# =====================================================# TEST EACH BASE LEARNER# =====================================================}    'SVM': SVC(kernel='rbf', random_state=42),    'Logistic Regression': LogisticRegression(random_state=42, max_iter=1000),    'Deep Tree (depth=10)': DecisionTreeClassifier(max_depth=10, random_state=42),    'Shallow Tree (depth=3)': DecisionTreeClassifier(max_depth=3, random_state=42),    'Decision Stump (depth=1)': DecisionTreeClassifier(max_depth=1, random_state=42),base_learners = {# =====================================================# DEFINE BASE LEARNERS# =====================================================)    X, y, test_size=0.2, random_state=42X_train, X_test, y_train, y_test = train_test_split(X, y = load_breast_cancer(return_X_y=True)# Load dataimport matplotlib.pyplot as pltfrom sklearn.metrics import accuracy_scorefrom sklearn.base import clonefrom sklearn.svm import SVCfrom sklearn.linear_model import LogisticRegressionfrom sklearn.tree import DecisionTreeClassifierfrom sklearn.ensemble import BaggingClassifier, AdaBoostClassifierfrom sklearn.model_selection import train_test_splitfrom sklearn.datasets import load_breast_cancerimport pandas as pdimport numpy as np"""Compare different base learners in ensemble methods"""```python## Template 3: Base Learner Comparison---```print("\n✅ Hyperparameter tuning complete!")print(f"Overfitting Gap: {train_score - test_score:.4f}")print(f"Test Accuracy: {test_score:.4f}")print(f"Training Accuracy: {train_score:.4f}")print(f"\nFinal Model Performance:")test_score = final_model.score(X_test, y_test)train_score = final_model.score(X_train, y_train)final_model.fit(X_train, y_train)final_model = XGBClassifier(**best_config, random_state=42)print("="*60)print("TRAINING FINAL MODEL")print("\n" + "="*60)# =====================================================# TRAIN FINAL MODEL WITH BEST PARAMETERS# =====================================================    print(f"{param_name}: {best_value} (CV Score: {best_score:.4f})")    best_config[param_name] = best_value    best_score = df.loc[best_idx, 'Mean CV Score']    best_value = df.loc[best_idx, 'Value']    best_idx = df['Mean CV Score'].idxmax()    param_name = df['Parameter'].iloc[0]for df in all_results:best_config = {}print("="*60)print("BEST VALUES FOR EACH HYPERPARAMETER")print("\n" + "="*60)# =====================================================# FIND BEST CONFIGURATION# =====================================================plt.show()plt.savefig('hyperparameter_tuning.png', dpi=300, bbox_inches='tight')plt.tight_layout()    ax.legend()            label=f'Best: {best_value}')    ax.plot(best_value, best_score, 'r*', markersize=20,     ax.axvline(x=best_value, color='red', linestyle='--', alpha=0.5)    best_score = df.loc[best_idx, 'Mean CV Score']    best_value = df.loc[best_idx, 'Value']    best_idx = df['Mean CV Score'].idxmax()    # Mark best value        ax.grid(True, alpha=0.3)    ax.set_title(f'Effect of {param_name}')    ax.set_ylabel('Cross-Validation Accuracy')    ax.set_xlabel(param_name)                marker='o', capsize=5, linewidth=2, markersize=8)                yerr=df['Std CV Score'],    ax.errorbar(df['Value'], df['Mean CV Score'],         param_name = df['Parameter'].iloc[0]    ax = axes[idx // 2, idx % 2]for idx, df in enumerate(all_results[:4]):fig, axes = plt.subplots(2, 2, figsize=(15, 10))# =====================================================# VISUALIZE RESULTS# =====================================================all_results.append(results_subsample))    base_params={'n_estimators': 100, 'max_depth': 3, 'learning_rate': 0.1}    [0.5, 0.6, 0.7, 0.8, 0.9, 1.0],    'subsample',results_subsample = test_hyperparameter(print("="*60)print("Testing subsample")print("\n" + "="*60)# 4. subsampleall_results.append(results_lr))    base_params={'n_estimators': 200, 'max_depth': 3}    [0.01, 0.05, 0.1, 0.2, 0.3],    'learning_rate',results_lr = test_hyperparameter(print("="*60)print("Testing learning_rate")print("\n" + "="*60)# 3. learning_rateall_results.append(results_depth))    base_params={'n_estimators': 100, 'learning_rate': 0.1}    [2, 3, 4, 5, 6, 7, 8, 10],    'max_depth',results_depth = test_hyperparameter(print("="*60)print("Testing max_depth")print("\n" + "="*60)# 2. max_depthall_results.append(results_n_est))    base_params={'max_depth': 3, 'learning_rate': 0.1}    [50, 100, 200, 300, 500],    'n_estimators',results_n_est = test_hyperparameter(print("="*60)print("Testing n_estimators")print("\n" + "="*60)# 1. n_estimatorsall_results = []# =====================================================# TEST DIFFERENT HYPERPARAMETERS# =====================================================    return pd.DataFrame(results)            print(f"{param_name}={value}: {scores.mean():.4f} (+/- {scores.std():.4f})")                })            'Std CV Score': scores.std()            'Mean CV Score': scores.mean(),            'Value': value,            'Parameter': param_name,        results.append({                scores = cross_val_score(model, X_train, y_train, cv=5, scoring='accuracy')        model = XGBClassifier(**params)                params['random_state'] = 42        params[param_name] = value        params = base_params.copy()    for value in param_values:        results = []            base_params = {}    if base_params is None:    """Test different values of a hyperparameter"""def test_hyperparameter(param_name, param_values, base_params=None):# =====================================================# FUNCTION: Test single parameter# =====================================================)    X, y, test_size=0.2, random_state=42X_train, X_test, y_train, y_test = train_test_split(X, y = load_breast_cancer(return_X_y=True)# Load datafrom sklearn.model_selection import train_test_splitfrom sklearn.datasets import load_breast_cancerfrom sklearn.model_selection import cross_val_scorefrom xgboost import XGBClassifierimport matplotlib.pyplot as pltimport pandas as pdimport numpy as np"""Systematic hyperparameter tuning for XGBoost"""```python## Template 2: Hyperparameter Tuning for XGBoost---```print("\n✅ Analysis complete! Plot saved as 'ensemble_comparison.png'")plt.show()plt.savefig('ensemble_comparison.png', dpi=300, bbox_inches='tight')plt.tight_layout()ax.legend()ax.axvline(x=0.1, color='red', linestyle='--', label='High overfitting threshold')ax.set_title('Overfitting Analysis')ax.set_xlabel('Overfitting Gap (Train Acc - Test Acc)')ax.barh(df_results['Model'], df_results['Overfit Gap'], color=colors_overfit)colors_overfit = ['red' if x > 0.1 else 'green' for x in df_results['Overfit Gap']]ax = axes[1, 1]# Plot 4: Overfitting analysis    ax.text(row['Train Time (s)'] + 0.01, i, f"{row['Train Time (s)']:.2f}s", va='center')for i, (idx, row) in enumerate(df_results.iterrows()):ax.set_title('Training Time Comparison')ax.set_xlabel('Training Time (seconds)')ax.barh(df_results['Model'], df_results['Train Time (s)'], color='steelblue')ax = axes[1, 0]# Plot 3: Training timeax.grid(True, alpha=0.3, axis='y')ax.legend()ax.set_xticklabels(df_results['Model'], rotation=45, ha='right')ax.set_xticks(x + width * 1.5)ax.set_title('Multiple Metrics Comparison')ax.set_ylabel('Score')ax.set_xlabel('Models')    ax.bar(x + i*width, df_results[metric], width, label=metric)for i, metric in enumerate(metrics):width = 0.2x = np.arange(len(df_results))metrics = ['Accuracy', 'Precision', 'Recall', 'F1-Score']ax = axes[0, 1]# Plot 2: Multiple metrics    ax.text(row['Accuracy'] + 0.005, i, f"{row['Accuracy']:.4f}", va='center')for i, (idx, row) in enumerate(df_sorted.iterrows()):ax.set_xlim([df_sorted['Accuracy'].min() - 0.02, 1.0])ax.set_title('Model Accuracy Comparison')ax.set_xlabel('Accuracy')bars = ax.barh(df_sorted['Model'], df_sorted['Accuracy'], color=colors)colors = sns.color_palette('viridis', len(df_sorted))df_sorted = df_results.sort_values('Accuracy', ascending=False)ax = axes[0, 0]# Plot 1: Accuracy comparisonfig, axes = plt.subplots(2, 2, figsize=(15, 10))# =====================================================# 5. VISUALIZATIONS# =====================================================print("\nBest Model by Accuracy:", df_results.loc[df_results['Accuracy'].idxmax(), 'Model'])print(df_results.to_string(index=False))print("="*80)print("FINAL RESULTS")print("\n" + "="*80)df_results = df_results.round(4)df_results = pd.DataFrame(results)# =====================================================# 4. CREATE RESULTS DATAFRAME# =====================================================    print(f"{name} - Accuracy: {accuracy:.4f}, F1: {f1:.4f}, Time: {train_time:.2f}s")        })        'Pred Time (s)': pred_time        'Train Time (s)': train_time,        'Overfit Gap': train_accuracy - accuracy,        'Train Acc': train_accuracy,        'ROC-AUC': roc_auc,        'F1-Score': f1,        'Recall': recall,        'Precision': precision,        'Accuracy': accuracy,        'Model': name,    results.append({    # Store results        train_accuracy = model.score(X_train, y_train)    # Training accuracy (for overfitting check)            roc_auc = np.nan    else:        roc_auc = roc_auc_score(y_test, y_pred_proba)    if y_pred_proba is not None and len(np.unique(y)) == 2:    # ROC AUC (binary classification)        f1 = f1_score(y_test, y_pred, average='weighted')    recall = recall_score(y_test, y_pred, average='weighted')    precision = precision_score(y_test, y_pred, average='weighted')    accuracy = accuracy_score(y_test, y_pred)    # Calculate metrics            y_pred_proba = None    else:        y_pred_proba = model.predict_proba(X_test)[:, 1]    if hasattr(model, 'predict_proba'):    # Get probabilities (if available)        pred_time = time.time() - start_time    y_pred = model.predict(X_test)    start_time = time.time()    # Prediction time        train_time = time.time() - start_time    model.fit(X_train, y_train)    start_time = time.time()    # Training time        print(f"\nTraining {name}...")for name, model in models.items():results = []# =====================================================# 3. TRAIN AND EVALUATE ALL MODELS# =====================================================}    )        random_state=42        learning_rate=0.1,        max_depth=3,        n_estimators=100,    'XGBoost': xgb.XGBClassifier(        ),        random_state=42        learning_rate=0.1,        max_depth=3,        n_estimators=100,    'Gradient Boosting': GradientBoostingClassifier(        ),        random_state=42        learning_rate=1.0,        n_estimators=100,        estimator=DecisionTreeClassifier(max_depth=1, random_state=42),    'AdaBoost': AdaBoostClassifier(        ),        random_state=42        max_depth=10,        n_estimators=100,    'Random Forest': RandomForestClassifier(        ),        random_state=42        n_estimators=100,        estimator=DecisionTreeClassifier(random_state=42),    'Bagging': BaggingClassifier(models = {# =====================================================# 2. DEFINE MODELS# =====================================================print(f"Class distribution: {np.bincount(y_train)}")print(f"Test set: {X_test.shape}")print(f"Training set: {X_train.shape}")print(f"Dataset shape: {X.shape}")X_test_scaled = scaler.transform(X_test)X_train_scaled = scaler.fit_transform(X_train)scaler = StandardScaler()# Optional: Scale features (helps some models))    X, y, test_size=0.2, random_state=42X_train, X_test, y_train, y_test = train_test_split(# Split data#                           n_redundant=5, random_state=42)# X, y = make_classification(n_samples=1000, n_features=20, n_informative=15,# Option B: Generate synthetic dataX, y = load_breast_cancer(return_X_y=True)# Option A: Use built-in dataset# =====================================================# 1. LOAD AND PREPARE DATA# =====================================================warnings.filterwarnings('ignore')import warningsimport xgboost as xgb# XGBoostfrom sklearn.tree import DecisionTreeClassifier                             AdaBoostClassifier, GradientBoostingClassifier)from sklearn.ensemble import (BaggingClassifier, RandomForestClassifier,# Ensemble methods                            f1_score, roc_auc_score, classification_report)from sklearn.metrics import (accuracy_score, precision_score, recall_score, from sklearn.preprocessing import StandardScalerfrom sklearn.model_selection import train_test_split, cross_val_scorefrom sklearn.datasets import load_breast_cancer, load_wine, make_classification# Scikit-learnimport timeimport seaborn as snsimport matplotlib.pyplot as pltimport pandas as pdimport numpy as np"""Complete pipeline for comparing ensemble methods - Classification"""```python## Template 1: Complete Classification Pipeline---## 🚀 Quick Copy-Paste Solutions for Your Lab
## 🎯 Copy-Paste Templates for Lab

---

## Template 1: Complete Ensemble Comparison

```python
"""
Template: Compare all ensemble methods on a dataset
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score, classification_report
from sklearn.datasets import load_breast_cancer

# Ensemble methods
from sklearn.ensemble import (
    BaggingClassifier,
    RandomForestClassifier,
    AdaBoostClassifier,
    GradientBoostingClassifier
)
from xgboost import XGBClassifier
import time
import warnings
warnings.filterwarnings('ignore')

# ============================================
# 1. LOAD DATA
# ============================================
print("Loading data...")
X, y = load_breast_cancer(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print(f"Training samples: {len(X_train)}")
print(f"Test samples: {len(X_test)}")

# ============================================
# 2. DEFINE MODELS
# ============================================
models = {
    'Bagging': BaggingClassifier(
        n_estimators=100,
        random_state=42
    ),
    'Random Forest': RandomForestClassifier(
        n_estimators=100,
        random_state=42
    ),
    'AdaBoost': AdaBoostClassifier(
        n_estimators=100,
        random_state=42
    ),
    'Gradient Boosting': GradientBoostingClassifier(
        n_estimators=100,
        learning_rate=0.1,
        random_state=42
    ),
    'XGBoost': XGBClassifier(
        n_estimators=100,
        learning_rate=0.1,
        random_state=42
    )
}

# ============================================
# 3. TRAIN AND EVALUATE
# ============================================
results = []

print("\n" + "="*60)
print("Training and Evaluating Models")
print("="*60)

for name, model in models.items():
    print(f"\nTraining {name}...")
    
    # Training time
    start_time = time.time()
    model.fit(X_train, y_train)
    train_time = time.time() - start_time
    
    # Prediction time
    start_time = time.time()
    y_pred = model.predict(X_test)
    pred_time = time.time() - start_time
    
    # Metrics
    accuracy = accuracy_score(y_test, y_pred)
    train_accuracy = model.score(X_train, y_train)
    
    # Cross-validation
    cv_scores = cross_val_score(model, X_train, y_train, cv=5)
    
    results.append({
        'Model': name,
        'Test Accuracy': accuracy,
        'Train Accuracy': train_accuracy,
        'CV Mean': cv_scores.mean(),
        'CV Std': cv_scores.std(),
        'Overfit Gap': train_accuracy - accuracy,
        'Train Time (s)': train_time,
        'Pred Time (s)': pred_time
    })
    
    print(f"  Test Accuracy: {accuracy:.4f}")
    print(f"  Train Accuracy: {train_accuracy:.4f}")
    print(f"  CV Accuracy: {cv_scores.mean():.4f} (+/- {cv_scores.std():.4f})")
    print(f"  Train Time: {train_time:.3f}s")

# ============================================
# 4. RESULTS TABLE
# ============================================
df_results = pd.DataFrame(results)
df_results = df_results.sort_values('Test Accuracy', ascending=False)

print("\n" + "="*60)
print("RESULTS SUMMARY")
print("="*60)
print(df_results.to_string(index=False))

# ============================================
# 5. VISUALIZATION
# ============================================
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Plot 1: Accuracy comparison
ax = axes[0, 0]
x_pos = np.arange(len(df_results))
ax.bar(x_pos, df_results['Test Accuracy'], alpha=0.7, label='Test')
ax.bar(x_pos, df_results['Train Accuracy'], alpha=0.5, label='Train')
ax.set_xticks(x_pos)
ax.set_xticklabels(df_results['Model'], rotation=45, ha='right')
ax.set_ylabel('Accuracy')
ax.set_title('Accuracy Comparison')
ax.legend()
ax.grid(True, alpha=0.3, axis='y')

# Plot 2: Training time
ax = axes[0, 1]
ax.barh(df_results['Model'], df_results['Train Time (s)'], color='steelblue')
ax.set_xlabel('Time (seconds)')
ax.set_title('Training Time')
ax.grid(True, alpha=0.3, axis='x')

# Plot 3: Overfitting analysis
ax = axes[1, 0]
ax.barh(df_results['Model'], df_results['Overfit Gap'], color='coral')
ax.axvline(x=0, color='red', linestyle='--', alpha=0.5)
ax.set_xlabel('Gap (Train - Test Accuracy)')
ax.set_title('Overfitting Analysis')
ax.grid(True, alpha=0.3, axis='x')

# Plot 4: CV scores with error bars
ax = axes[1, 1]
ax.errorbar(df_results['Model'], df_results['CV Mean'], 
           yerr=df_results['CV Std'], fmt='o', capsize=5, linewidth=2)
ax.set_xticklabels(df_results['Model'], rotation=45, ha='right')
ax.set_ylabel('Accuracy')
ax.set_title('Cross-Validation Scores')
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('ensemble_comparison.png', dpi=150, bbox_inches='tight')
plt.show()

print("\n✅ Analysis complete! Plot saved as 'ensemble_comparison.png'")
```

---

## Template 2: XGBoost Hyperparameter Comparison

```python
"""
Template: Compare XGBoost with different hyperparameters
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.datasets import load_breast_cancer
import time

# Load data
X, y = load_breast_cancer(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# ============================================
# HYPERPARAMETER CONFIGURATIONS
# ============================================
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
    'Many Shallow Trees': {
        'n_estimators': 500,
        'max_depth': 2,
        'learning_rate': 0.05
    },
    'Slow Learning': {
        'n_estimators': 1000,
        'max_depth': 3,
        'learning_rate': 0.01
    },
    'Regularized': {
        'n_estimators': 100,
        'max_depth': 5,
        'learning_rate': 0.1,
        'reg_lambda': 10,
        'gamma': 1.0
    },
    'With Subsampling': {
        'n_estimators': 100,
        'max_depth': 5,
        'learning_rate': 0.1,
        'subsample': 0.8,
        'colsample_bytree': 0.8
    }
}

# ============================================
# TRAIN AND EVALUATE
# ============================================
results = []

print("="*70)
print("XGBoost Hyperparameter Comparison")
print("="*70)

for name, params in configs.items():
    print(f"\nTesting: {name}")
    print(f"Params: {params}")
    
    # Create model
    model = XGBClassifier(**params, random_state=42)
    
    # Training time
    start = time.time()
    model.fit(X_train, y_train)
    train_time = time.time() - start
    
    # Evaluate
    train_acc = model.score(X_train, y_train)
    test_acc = model.score(X_test, y_test)
    
    # Cross-validation
    cv_scores = cross_val_score(model, X_train, y_train, cv=5)
    
    # Store results
    result = {
        'Configuration': name,
        'Test Accuracy': test_acc,
        'Train Accuracy': train_acc,
        'CV Mean': cv_scores.mean(),
        'CV Std': cv_scores.std(),
        'Overfit Gap': train_acc - test_acc,
        'Train Time (s)': train_time
    }
    result.update(params)
    results.append(result)
    
    print(f"  Test Accuracy: {test_acc:.4f}")
    print(f"  CV Accuracy: {cv_scores.mean():.4f} (+/- {cv_scores.std():.4f})")
    print(f"  Train Time: {train_time:.2f}s")

# ============================================
# RESULTS
# ============================================
df_results = pd.DataFrame(results)
df_results = df_results.sort_values('Test Accuracy', ascending=False)

print("\n" + "="*70)
print("RESULTS")
print("="*70)
print(df_results[['Configuration', 'Test Accuracy', 'CV Mean', 
                  'Overfit Gap', 'Train Time (s)']].to_string(index=False))

# ============================================
# VISUALIZATION
# ============================================
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Accuracy comparison
ax = axes[0]
x_pos = np.arange(len(df_results))
width = 0.35
ax.bar(x_pos - width/2, df_results['Test Accuracy'], width, 
       label='Test', alpha=0.8)
ax.bar(x_pos + width/2, df_results['Train Accuracy'], width, 
       label='Train', alpha=0.8)
ax.set_xticks(x_pos)
ax.set_xticklabels(df_results['Configuration'], rotation=45, ha='right')
ax.set_ylabel('Accuracy')
ax.set_title('Accuracy by Configuration')
ax.legend()
ax.grid(True, alpha=0.3, axis='y')

# Time vs Accuracy tradeoff
ax = axes[1]
scatter = ax.scatter(df_results['Train Time (s)'], df_results['Test Accuracy'],
                    s=200, alpha=0.6, c=range(len(df_results)), cmap='viridis')
for idx, row in df_results.iterrows():
    ax.annotate(row['Configuration'], 
               (row['Train Time (s)'], row['Test Accuracy']),
               fontsize=8, ha='center')
ax.set_xlabel('Training Time (seconds)')
ax.set_ylabel('Test Accuracy')
ax.set_title('Accuracy vs Training Time Tradeoff')
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('xgboost_hyperparameter_comparison.png', dpi=150, bbox_inches='tight')
plt.show()

print("\n✅ Complete! Plot saved.")
```

---

## Template 3: Single Hyperparameter Sensitivity Analysis

```python
"""
Template: Test effect of single hyperparameter
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from xgboost import XGBClassifier
from sklearn.model_selection import cross_val_score
from sklearn.datasets import load_breast_cancer

# Load data
X, y = load_breast_cancer(return_X_y=True)

# ============================================
# CHOOSE PARAMETER TO TEST
# ============================================
param_name = 'max_depth'  # CHANGE THIS
param_values = [1, 2, 3, 5, 7, 10, 15, 20]  # CHANGE THIS

# Base parameters (kept constant)
base_params = {
    'n_estimators': 100,
    'learning_rate': 0.1,
    'random_state': 42
}

# ============================================
# TEST PARAMETER
# ============================================
results = []

print(f"Testing parameter: {param_name}")
print(f"Values: {param_values}")
print("="*50)

for value in param_values:
    # Create model with this parameter value
    params = base_params.copy()
    params[param_name] = value
    
    model = XGBClassifier(**params)
    
    # Cross-validation
    scores = cross_val_score(model, X, y, cv=5, scoring='accuracy')
    
    results.append({
        param_name: value,
        'Mean Accuracy': scores.mean(),
        'Std': scores.std(),
        'Min': scores.min(),
        'Max': scores.max()
    })
    
    print(f"{param_name}={value:>6}: "
          f"{scores.mean():.4f} (+/- {scores.std():.4f})")

df_results = pd.DataFrame(results)

# ============================================
# FIND OPTIMAL VALUE
# ============================================
optimal_idx = df_results['Mean Accuracy'].idxmax()
optimal_value = df_results.loc[optimal_idx, param_name]
optimal_score = df_results.loc[optimal_idx, 'Mean Accuracy']

print("\n" + "="*50)
print(f"Optimal {param_name}: {optimal_value}")
print(f"Best Accuracy: {optimal_score:.4f}")
print("="*50)

# ============================================
# PLOT
# ============================================
plt.figure(figsize=(10, 6))

# Plot line with error bars
plt.errorbar(df_results[param_name], df_results['Mean Accuracy'],
            yerr=df_results['Std'], marker='o', capsize=5,
            linewidth=2, markersize=8)

# Highlight optimal
plt.axvline(x=optimal_value, color='red', linestyle='--', 
           label=f'Optimal: {param_name}={optimal_value}', alpha=0.7)

plt.xlabel(param_name, fontsize=12)
plt.ylabel('Cross-Validation Accuracy', fontsize=12)
plt.title(f'Effect of {param_name} on Model Performance', fontsize=14)
plt.grid(True, alpha=0.3)
plt.legend()

# Add value labels
for _, row in df_results.iterrows():
    plt.text(row[param_name], row['Mean Accuracy'] + 0.005,
            f"{row['Mean Accuracy']:.3f}", 
            ha='center', fontsize=9)

plt.tight_layout()
plt.savefig(f'{param_name}_sensitivity.png', dpi=150, bbox_inches='tight')
plt.show()

print(f"\n✅ Plot saved as '{param_name}_sensitivity.png'")
```

---

## Template 4: Base Learner Comparison

```python
"""
Template: Compare different base learners in ensemble
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import BaggingClassifier, AdaBoostClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.base import clone
import time

# Load data
X, y = load_breast_cancer(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# ============================================
# DEFINE BASE LEARNERS
# ============================================
base_learners = {
    'Decision Stump': DecisionTreeClassifier(max_depth=1, random_state=42),
    'Shallow Tree (depth=3)': DecisionTreeClassifier(max_depth=3, random_state=42),
    'Deep Tree (depth=10)': DecisionTreeClassifier(max_depth=10, random_state=42),
    'Logistic Regression': LogisticRegression(random_state=42, max_iter=1000),
    'KNN (k=5)': KNeighborsClassifier(n_neighbors=5)
}

# ============================================
# TEST WITH BAGGING
# ============================================
print("="*70)
print("BASE LEARNER COMPARISON WITH BAGGING")
print("="*70)

results = []

for name, base_est in base_learners.items():
    print(f"\nTesting: {name}")
    
    # Single base learner
    single = clone(base_est)
    single.fit(X_train, y_train)
    single_score = single.score(X_test, y_test)
    
    # Bagging
    bagging = BaggingClassifier(
        estimator=base_est,
        n_estimators=50,
        random_state=42
    )
    
    start = time.time()
    bagging.fit(X_train, y_train)
    train_time = time.time() - start
    
    bagging_score = bagging.score(X_test, y_test)
    
    # Cross-validation
    cv_scores = cross_val_score(bagging, X_train, y_train, cv=5)
    
    results.append({
        'Base Learner': name,
        'Single Model': single_score,
        'Bagging': bagging_score,
        'Improvement': bagging_score - single_score,
        'CV Mean': cv_scores.mean(),
        'CV Std': cv_scores.std(),
        'Train Time': train_time
    })
    
    print(f"  Single: {single_score:.4f}")
    print(f"  Bagging: {bagging_score:.4f}")
    print(f"  Improvement: {bagging_score - single_score:+.4f}")

# ============================================
# RESULTS
# ============================================
df_results = pd.DataFrame(results)
df_results = df_results.sort_values('Bagging', ascending=False)

print("\n" + "="*70)
print("RESULTS")
print("="*70)
print(df_results.to_string(index=False))

# ============================================
# VISUALIZATION
# ============================================
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Comparison plot
ax = axes[0]
x_pos = np.arange(len(df_results))
width = 0.35
ax.barh(x_pos - width/2, df_results['Single Model'], width, 
       label='Single Model', alpha=0.8)
ax.barh(x_pos + width/2, df_results['Bagging'], width, 
       label='Bagging', alpha=0.8)
ax.set_yticks(x_pos)
ax.set_yticklabels(df_results['Base Learner'])
ax.set_xlabel('Accuracy')
ax.set_title('Single vs Bagging Performance')
ax.legend()
ax.grid(True, alpha=0.3, axis='x')

# Improvement plot
ax = axes[1]
colors = ['green' if x > 0 else 'red' for x in df_results['Improvement']]
ax.barh(df_results['Base Learner'], df_results['Improvement'], color=colors, alpha=0.7)
ax.axvline(x=0, color='black', linestyle='-', linewidth=0.8)
ax.set_xlabel('Improvement (Bagging - Single)')
ax.set_title('Bagging Improvement by Base Learner')
ax.grid(True, alpha=0.3, axis='x')

plt.tight_layout()
plt.savefig('base_learner_comparison.png', dpi=150, bbox_inches='tight')
plt.show()

print("\n✅ Complete!")
```

---

## Template 5: Quick Performance Report

```python
"""
Template: Generate quick performance report for a model
"""

def performance_report(model, X_train, X_test, y_train, y_test, model_name='Model'):
    """
    Generate comprehensive performance report
    """
    from sklearn.metrics import (accuracy_score, precision_score, recall_score,
                                f1_score, classification_report, confusion_matrix)
    from sklearn.model_selection import cross_val_score
    import time
    
    print("="*70)
    print(f"PERFORMANCE REPORT: {model_name}")
    print("="*70)
    
    # Training
    print("\n1. Training...")
    start = time.time()
    model.fit(X_train, y_train)
    train_time = time.time() - start
    print(f"   ✓ Training completed in {train_time:.2f} seconds")
    
    # Predictions
    print("\n2. Making predictions...")
    y_pred = model.predict(X_test)
    y_train_pred = model.predict(X_train)
    
    # Basic metrics
    print("\n3. Performance Metrics:")
    print(f"   Train Accuracy: {accuracy_score(y_train, y_train_pred):.4f}")
    print(f"   Test Accuracy:  {accuracy_score(y_test, y_pred):.4f}")
    print(f"   Precision:      {precision_score(y_test, y_pred, average='weighted'):.4f}")
    print(f"   Recall:         {recall_score(y_test, y_pred, average='weighted'):.4f}")
    print(f"   F1-Score:       {f1_score(y_test, y_pred, average='weighted'):.4f}")
    
    # Cross-validation
    print("\n4. Cross-Validation (5-fold):")
    cv_scores = cross_val_score(model, X_train, y_train, cv=5)
    print(f"   Scores: {cv_scores}")
    print(f"   Mean:   {cv_scores.mean():.4f}")
    print(f"   Std:    {cv_scores.std():.4f}")
    
    # Classification report
    print("\n5. Detailed Classification Report:")
    print(classification_report(y_test, y_pred))
    
    # Confusion matrix
    print("6. Confusion Matrix:")
    cm = confusion_matrix(y_test, y_pred)
    print(cm)
    
    # Overfitting check
    train_acc = accuracy_score(y_train, y_train_pred)
    test_acc = accuracy_score(y_test, y_pred)
    gap = train_acc - test_acc
    
    print("\n7. Overfitting Analysis:")
    print(f"   Gap (Train - Test): {gap:.4f}")
    if gap > 0.1:
        print("   ⚠️  Warning: Model may be overfitting!")
    elif gap < 0.02:
        print("   ✓ Model generalizes well")
    else:
        print("   ✓ Acceptable generalization")
    
    print("\n" + "="*70)

# Usage example
from xgboost import XGBClassifier
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split

X, y = load_breast_cancer(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = XGBClassifier(n_estimators=100, max_depth=5, random_state=42)
performance_report(model, X_train, X_test, y_train, y_test, model_name='XGBoost')
```

---

## Template 6: Learning Curve Plotter

```python
"""
Template: Plot learning curves for multiple models
"""

import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import learning_curve

def plot_learning_curves(models_dict, X, y, cv=5):
    """
    Plot learning curves for multiple models
    
    models_dict: {'Model Name': model_object}
    """
    n_models = len(models_dict)
    fig, axes = plt.subplots(1, n_models, figsize=(6*n_models, 5))
    
    if n_models == 1:
        axes = [axes]
    
    for idx, (name, model) in enumerate(models_dict.items()):
        print(f"Computing learning curve for {name}...")
        
        # Generate learning curve
        train_sizes, train_scores, val_scores = learning_curve(
            model, X, y,
            train_sizes=np.linspace(0.1, 1.0, 10),
            cv=cv,
            scoring='accuracy',
            n_jobs=-1
        )
        
        # Calculate statistics
        train_mean = train_scores.mean(axis=1)
        train_std = train_scores.std(axis=1)
        val_mean = val_scores.mean(axis=1)
        val_std = val_scores.std(axis=1)
        
        # Plot
        ax = axes[idx]
        ax.plot(train_sizes, train_mean, 'o-', label='Training', linewidth=2)
        ax.fill_between(train_sizes, train_mean - train_std, 
                       train_mean + train_std, alpha=0.3)
        
        ax.plot(train_sizes, val_mean, 'o-', label='Validation', linewidth=2)
        ax.fill_between(train_sizes, val_mean - val_std, 
                       val_mean + val_std, alpha=0.3)
        
        ax.set_xlabel('Training Set Size')
        ax.set_ylabel('Accuracy')
        ax.set_title(f'Learning Curve: {name}')
        ax.legend(loc='best')
        ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('learning_curves.png', dpi=150, bbox_inches='tight')
    plt.show()
    print("✅ Saved as 'learning_curves.png'")

# Usage
from xgboost import XGBClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import load_breast_cancer

X, y = load_breast_cancer(return_X_y=True)

models = {
    'XGBoost': XGBClassifier(n_estimators=100, random_state=42),
    'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42)
}

plot_learning_curves(models, X, y, cv=5)
```

---

## 💡 Quick Tips

### How to Use These Templates:

1. **Copy the entire template** you need
2. **Modify the data loading** section for your dataset
3. **Adjust parameters** in the configuration section
4. **Run and get results**

### Common Modifications:

```python
# Change dataset
from sklearn.datasets import load_iris  # or load_digits, load_wine, etc.
X, y = load_iris(return_X_y=True)

# Change to regression
from sklearn.datasets import load_diabetes
from xgboost import XGBRegressor
from sklearn.metrics import mean_squared_error, r2_score

# Change test size
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42  # 30% test
)

# Change CV folds
cv_scores = cross_val_score(model, X_train, y_train, cv=10)  # 10-fold

# Add more models
models['My Custom Model'] = MyCustomClassifier(params)
```

---

## 🔗 Navigation

- **Back to Start**: [00_Getting_Started_Guide.md](00_Getting_Started_Guide.md)
- **Common Issues**: [06_Common_Pitfalls.md](06_Common_Pitfalls.md)
