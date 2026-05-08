"""
PCA from Scratch - NumPy Implementation
Complete the TODOs to implement PCA step-by-step
"""
import numpy as np


class PCA:
    def __init__(self, n_components):
        """
        Args:
            n_components (int): number of principal components to keep
        """
        # TODO: Initialize attributes (variance_explained, components, mean)
        pass
    
    def fit(self, X):
        """
        Fit PCA on data X
        
        Args:
            X (np.ndarray): shape (n_samples, n_features)
        
        Returns:
            self
        """
        # TODO: Center the data (subtract mean)
        # Hint: X_centered = X - X.mean(axis=0)
        
        # TODO: Compute covariance matrix (shape: n_features x n_features)
        # Hint: use np.cov(X_centered.T) or manual computation
        
        # TODO: Compute eigenvalues and eigenvectors
        # Hint: np.linalg.eig() returns (eigenvalues, eigenvectors)
        
        # TODO: Sort by eigenvalues (descending order)
        # Tip: use np.argsort() with negative values or [::-1]
        
        # TODO: Select top n_components eigenvectors (shape: n_features x n_components)
        
        # TODO: Store mean, components, and explained_variance
        # explained_variance should be normalized eigenvalues / sum(eigenvalues)
        
        return self
    
    def transform(self, X):
        """
        Project X onto principal components
        
        Args:
            X (np.ndarray): shape (n_samples, n_features)
        
        Returns:
            np.ndarray: shape (n_samples, n_components)
        """
        # TODO: Center data using stored mean
        
        # TODO: Project onto components using matrix multiplication
        # Hint: X_centered @ self.components
        
        pass
    
    def fit_transform(self, X):
        """Fit and transform in one call"""
        return self.fit(X).transform(X)


# ============ TEST ============
if __name__ == "__main__":
    # Generate sample data
    np.random.seed(42)
    X = np.random.randn(100, 5)
    
    # Create PCA with 2 components
    pca = PCA(n_components=2)
    X_reduced = pca.fit_transform(X)
    
    # Check shapes and properties
    print(f"Original shape: {X.shape}")
    print(f"Reduced shape: {X_reduced.shape}")
    print(f"Explained variance sum: {pca.variance_explained.sum():.4f}")
    print(f"Components shape: {pca.components.shape}")
