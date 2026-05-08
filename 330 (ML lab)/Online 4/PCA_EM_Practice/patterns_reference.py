"""
KEY PATTERNS & SYNTAX - PCA and EM
Reference guide for common operations
"""

import numpy as np
from scipy.stats import multivariate_normal
from sklearn.decomposition import PCA as SklearnPCA
from sklearn.mixture import GaussianMixture


# ============ PCA PATTERNS ============

# Pattern 1: Center Data
X = np.random.randn(100, 5)
X_mean = X.mean(axis=0)          # shape: (n_features,)
X_centered = X - X_mean           # shape: (n_samples, n_features)
# Why: remove mean to make covariance centered at origin

# Pattern 2: Covariance Matrix (2 ways)
# Method A: np.cov (expects features as rows)
cov_matrix = np.cov(X_centered.T)  # shape: (n_features, n_features)

# Method B: Manual computation
cov_matrix = (X_centered.T @ X_centered) / (X.shape[0] - 1)  # shape: (n_features, n_features)

# Pattern 3: Eigendecomposition
eigenvalues, eigenvectors = np.linalg.eig(cov_matrix)
# Returns:
#   eigenvalues: shape (n_features,) - variance along each eigenvector
#   eigenvectors: shape (n_features, n_features) - columns are eigenvectors

# Pattern 4: Sort by Eigenvalues (Descending)
idx = np.argsort(eigenvalues)[::-1]       # Descending order indices
eigenvalues_sorted = eigenvalues[idx]     # shape: (n_features,)
eigenvectors_sorted = eigenvectors[:, idx] # shape: (n_features, n_features)

# Pattern 5: Select top k components
k = 2
components = eigenvectors_sorted[:, :k]  # shape: (n_features, k)
explained_var = eigenvalues_sorted[:k]   # shape: (k,)
explained_var_ratio = explained_var / eigenvalues_sorted.sum()  # normalized

# Pattern 6: Project onto components (Transform)
X_projected = X_centered @ components  # shape: (n_samples, k)
# Why dot product: projects each sample onto the component space

# Pattern 7: Reconstruct from components (optional)
X_reconstructed = X_projected @ components.T + X_mean
# Why: reverse the projection and add back the mean


# ============ EM / GMM PATTERNS ============

# Pattern 1: Multivariate Gaussian Likelihood
mu = np.array([0, 0])              # mean, shape: (n_features,)
sigma = np.eye(2)                  # covariance, shape: (n_features, n_features)
x_sample = np.array([0.5, 0.5])    # single sample, shape: (n_features,)

# Likelihood for single sample
likelihood = multivariate_normal.pdf(x_sample, mean=mu, cov=sigma)  # scalar

# Likelihood for multiple samples
X_samples = np.random.randn(10, 2)  # shape: (n_samples, n_features)
likelihoods = multivariate_normal.pdf(X_samples, mean=mu, cov=sigma)  # shape: (n_samples,)

# Pattern 2: Responsibilities (Posterior Probabilities)
# For K components, per-sample responsibility for component k:
# r_ik = (w_k * P(x_i | mu_k, Sigma_k)) / sum_j(w_j * P(x_i | mu_j, Sigma_j))

# Example with 2 components:
w = np.array([0.5, 0.5])           # weights, shape: (n_components,)
likelihoods_comp1 = multivariate_normal.pdf(X_samples, mean=mu1, cov=sigma1)  # (n_samples,)
likelihoods_comp2 = multivariate_normal.pdf(X_samples, mean=mu2, cov=sigma2)  # (n_samples,)

# Weighted likelihoods
weighted_likelihoods = np.column_stack([
    w[0] * likelihoods_comp1,
    w[1] * likelihoods_comp2
])  # shape: (n_samples, n_components)

# Normalize (E-step output)
responsibilities = weighted_likelihoods / weighted_likelihoods.sum(axis=1, keepdims=True)
# shape: (n_samples, n_components), each row sums to 1

# Pattern 3: Update Parameters (M-step)
responsibilities = np.array([[0.9, 0.1], [0.2, 0.8], [0.7, 0.3]])  # (n_samples=3, n_components=2)
X_samples = np.array([[1, 1], [0, 0], [1, 0]])  # (n_samples=3, n_features=2)

for k in range(2):  # for each component
    # Effective count
    Nk = responsibilities[:, k].sum()  # scalar - total responsibility for component k
    
    # Update mean
    mu_new = (responsibilities[:, k, np.newaxis] * X_samples).sum(axis=0) / Nk
    # mu_new shape: (n_features,)
    # Why: weighted average of samples by responsibility
    
    # Update covariance
    X_centered_k = X_samples - mu_new  # shape: (n_samples, n_features)
    cov_new = (responsibilities[:, k, np.newaxis, np.newaxis] * 
               (X_centered_k[:, :, np.newaxis] @ X_centered_k[:, np.newaxis, :])).sum(axis=0) / Nk
    # cov_new shape: (n_features, n_features)
    # Why: weighted outer product of centered samples
    
    # Update weight
    w_new = Nk / X_samples.shape[0]  # scalar in [0, 1]

# Pattern 4: Cluster Assignment (Prediction)
labels = np.argmax(responsibilities, axis=1)  # shape: (n_samples,)
# Why: assign to component with highest responsibility


# ============ SKLEARN VERSIONS (Reference) ============

print("\n--- PCA (Sklearn) ---")
X = np.random.randn(100, 5)
pca = SklearnPCA(n_components=2)
X_reduced = pca.fit_transform(X)
# Returns shape: (n_samples, n_components)
print(f"Explained variance ratio: {pca.explained_variance_ratio_}")
print(f"Components: {pca.components_.shape}")

print("\n--- GMM (Sklearn) ---")
gmm = GaussianMixture(n_components=2, random_state=42)
gmm.fit(X)
labels = gmm.predict(X)  # shape: (n_samples,)
proba = gmm.predict_proba(X)  # shape: (n_samples, n_components) - responsibilities
print(f"AIC: {gmm.aic(X)}")
print(f"Labels: {np.unique(labels)}")
