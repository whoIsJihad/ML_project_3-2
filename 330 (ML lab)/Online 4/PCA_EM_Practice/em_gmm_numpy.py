"""
EM Algorithm - Gaussian Mixture Model from NumPy
Complete the TODOs to implement EM (E-step and M-step)
"""
import numpy as np
from scipy.stats import multivariate_normal


class GaussianMixtureModel:
    def __init__(self, n_components, max_iter=100, tol=1e-4, random_state=None):
        """
        Args:
            n_components (int): number of Gaussian components
            max_iter (int): maximum iterations
            tol (float): convergence tolerance
        """
        self.n_components = n_components
        self.max_iter = max_iter
        self.tol = tol
        self.random_state = random_state
        
        # TODO: Initialize placeholders for means, covariances, weights
        # These should be set in fit()
    
    def _initialize(self, X):
        """Initialize parameters randomly"""
        n_samples, n_features = X.shape
        
        if self.random_state:
            np.random.seed(self.random_state)
        
        # TODO: Initialize means by randomly selecting n_components samples from X
        # Hint: use np.random.choice(n_samples, n_components, replace=False)
        
        # TODO: Initialize covariances as identity matrix * 1.0 for each component
        # Shape: (n_components, n_features, n_features)
        
        # TODO: Initialize weights uniformly (1/n_components for each)
        # Shape: (n_components,)
    
    def _e_step(self, X):
        """
        E-step: compute responsibilities (posterior probabilities)
        
        Args:
            X (np.ndarray): shape (n_samples, n_features)
        
        Returns:
            responsibilities: shape (n_samples, n_components)
        """
        n_samples = X.shape[0]
        responsibilities = np.zeros((n_samples, self.n_components))
        
        # TODO: For each component k:
        #   - Compute likelihood P(X | mu_k, Sigma_k) using multivariate_normal.pdf
        #   - Multiply by weight P(k)
        #   - Store in responsibilities after normalization
        
        # TODO: Normalize responsibilities by rows (sum to 1 for each sample)
        # Hint: responsibilities /= responsibilities.sum(axis=1, keepdims=True)
        
        return responsibilities
    
    def _m_step(self, X, responsibilities):
        """
        M-step: update parameters based on responsibilities
        
        Args:
            X (np.ndarray): shape (n_samples, n_features)
            responsibilities (np.ndarray): shape (n_samples, n_components)
        """
        n_samples, n_features = X.shape
        
        # TODO: For each component k:
        #   - Compute effective count: Nk = sum of responsibilities for component k
        #   - Update mean: mu_k = sum(responsibilities[k] * X) / Nk
        #   - Update covariance: Sigma_k = weighted covariance matrix
        #   - Update weight: weights[k] = Nk / n_samples
        
        pass
    
    def fit(self, X):
        """
        Fit GMM using EM algorithm
        
        Args:
            X (np.ndarray): shape (n_samples, n_features)
        
        Returns:
            self
        """
        self._initialize(X)
        
        for iteration in range(self.max_iter):
            # TODO: Run E-step
            
            # TODO: Run M-step
            
            # TODO: Check convergence (optional: compute log-likelihood)
            # If converged (change < tol), break
            
            if iteration % 10 == 0:
                print(f"Iteration {iteration}")
        
        return self
    
    def predict(self, X):
        """
        Predict cluster assignments
        
        Args:
            X (np.ndarray): shape (n_samples, n_features)
        
        Returns:
            np.ndarray: cluster labels, shape (n_samples,)
        """
        # TODO: Use responsibilities (E-step) and assign each sample to cluster with highest responsibility
        # Hint: np.argmax(responsibilities, axis=1)
        
        pass


# ============ TEST ============
if __name__ == "__main__":
    # Generate sample data (2 Gaussians)
    np.random.seed(42)
    X1 = np.random.randn(50, 2) + np.array([2, 2])
    X2 = np.random.randn(50, 2) + np.array([-2, -2])
    X = np.vstack([X1, X2])
    
    # Fit GMM
    gmm = GaussianMixtureModel(n_components=2, max_iter=50, random_state=42)
    gmm.fit(X)
    
    # Predict
    labels = gmm.predict(X)
    
    print(f"Data shape: {X.shape}")
    print(f"Predicted labels: {np.unique(labels)}")
    print(f"Label distribution: {np.bincount(labels)}")
