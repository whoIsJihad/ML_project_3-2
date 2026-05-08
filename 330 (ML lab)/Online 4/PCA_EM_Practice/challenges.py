"""
PRACTICE PROBLEMS - Mixed Challenges
Shorter snippets with specific TODOs (test-style)
"""
import numpy as np
from scipy.stats import multivariate_normal


# ============ CHALLENGE 1: PCA Variance Explained ============
def challenge_1_variance_explained():
    """
    Practice: Compute explained variance correctly
    """
    X = np.array([[1, 2, 3],
                  [4, 5, 6],
                  [7, 8, 9],
                  [10, 11, 12]])  # (4, 3)
    
    # Step 1: Center
    X_centered = X - X.mean(axis=0)
    
    # Step 2: Covariance
    cov = np.cov(X_centered.T)  # (3, 3)
    
    # Step 3: Eigendecomposition
    evals, evecs = np.linalg.eig(cov)
    
    # TODO: Sort by eigenvalues (descending)
    # TODO: Compute explained variance ratio (each eigenvalue / sum of all)
    # TODO: Print the ratio for each component
    # Expected: decreasing values that sum to ~1.0
    

# ============ CHALLENGE 2: PCA with Different n_components ============
def challenge_2_projection_mismatch():
    """
    Practice: Handle matrix shapes correctly
    Info: What shape should X_projected have if X is (100, 20) and we want 5 components?
    """
    X = np.random.randn(100, 20)
    
    # Simulate: we have components of shape (20, 5)
    components = np.random.randn(20, 5)
    
    # TODO: Project X onto components
    # Write the matrix multiplication
    # Expected shape: (100, 5)
    
    X_projected = None  # TODO: implement
    # print(f"X_projected shape: {X_projected.shape}")


# ============ CHALLENGE 3: EM Responsibilities Shape ============
def challenge_3_responsibility_shapes():
    """
    Practice: Understand responsibility matrix dimensions
    Key: responsibilities[i, k] = probability sample i belongs to component k
    """
    n_samples = 5
    n_components = 3
    n_features = 2
    
    # TODO: Create a responsibilities matrix (5, 3) where:
    #   - Each row represents a sample
    #   - Each column represents a component
    #   - Values are probabilities (0-1) that sum to 1 per row
    # Hint: use np.random.dirichlet
    
    responsibilities = None  # TODO: implement
    
    # TODO: Normalize to ensure rows sum to 1
    # If you used dirichlet, this should already be true
    
    # TODO: Find which component each sample belongs to
    # (argmax responsibility per sample)


# ============ CHALLENGE 4: Update Gaussian Mean ============
def challenge_4_weighted_mean():
    """
    Practice: Compute weighted mean (M-step key operation)
    """
    X = np.array([[1, 2],
                  [3, 4],
                  [5, 6]])  # (3, 2)
    
    responsibilities = np.array([0.8, 0.1, 0.2])  # (3,) - for one component
    
    # TODO: Compute weighted mean
    # Formula: mu = sum(r_i * x_i) / sum(r_i)
    # Hint: responsibilities[:, np.newaxis] expands to (3, 1) for broadcasting
    
    # Expected: roughly close to weighted average favoring sample 0
    

# ============ CHALLENGE 5: Covariance Update ============
def challenge_5_weighted_covariance():
    """
    Practice: Update covariance matrix (M-step)
    """
    X = np.array([[1, 2],
                  [3, 4],
                  [5, 6]])  # (3, 2)
    
    mu = np.array([2, 3])  # (2,) - component mean
    responsibilities = np.array([0.8, 0.1, 0.2])  # (3,) - for one component
    
    # TODO: Compute weighted covariance
    # Steps:
    # 1. Center data: X_centered = X - mu
    # 2. Compute weighted outer product: (X_centered[i].outer(X_centered[i]) * r_i)
    # 3. Sum and normalize by total responsibility
    
    # Hint for outer product of two vectors u, v:
    # u[:, np.newaxis] @ v[np.newaxis, :] gives (n, m) matrix
    

# ============ CHALLENGE 6: Multiple Components Loop ============
def challenge_6_loop_pattern():
    """
    Practice: Typical loop for updating all components at once
    """
    X = np.random.randn(20, 3)  # (20 samples, 3 features)
    responsibilities = np.random.rand(20, 4)  # (20 samples, 4 components)
    responsibilities /= responsibilities.sum(axis=1, keepdims=True)  # normalize
    
    n_components = 4
    n_features = 3
    
    means = np.zeros((n_components, n_features))
    covariances = np.zeros((n_components, n_features, n_features))
    weights = np.zeros(n_components)
    
    for k in range(n_components):
        # TODO: Extract responsibilities for component k: shape (20,)
        
        # TODO: Compute Nk = sum of responsibilities[k]
        
        # TODO: Update means[k]
        
        # TODO: Update covariances[k]
        
        # TODO: Update weights[k]


# ============ CHALLENGE 7: Convergence Check ============
def challenge_7_convergence():
    """
    Practice: Check if EM has converged
    """
    # Simulate old and new log-likelihoods from two successive iterations
    ll_old = -100.5
    ll_new = -100.4
    tol = 1e-4
    
    # TODO: Check if converged
    # Convergence: abs(ll_new - ll_old) < tol
    # Or: relative change: abs(ll_new - ll_old) / abs(ll_old) < tol


if __name__ == "__main__":
    print("Challenge 1: Variance Explained")
    challenge_1_variance_explained()
    print("\nChallenge 2: Projection Mismatch")
    challenge_2_projection_mismatch()
    # ... Add more as needed
