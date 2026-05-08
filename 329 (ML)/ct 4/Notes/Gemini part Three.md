# Study Guide 3: Clustering & Dimensionality Reduction

## 1. K-Means Clustering: The Iterative Partitioning

K-Means aims to partition $n$ observations into $K$ clusters in which each observation belongs to the cluster with the nearest mean.

### The Objective Function (Distortion)

K-Means tries to minimize the **Within-Cluster Sum of Squares (WCSS)**, also known as Inertia or Distortion:

$$J = \sum_{i=1}^{K} \sum_{x \in C_i} ||x - \mu_i||^2$$

Where $\mu_i$ is the centroid of cluster $C_i$.

### The Lloyd's Algorithm Mechanics

1. **Assignment Step**: Assign each observation to the cluster whose centroid has the least squared Euclidean distance.
    
2. **Update Step**: Calculate the new means (centroids) to be the centroids of the observations in the new clusters.
    
3. **Convergence**: The algorithm converges when assignments no longer change. Note that it finds a **local optimum**, not necessarily the global one.
    

### Critical Nuances

- **The "Elbow" Method**: Since $K$ must be specified, we plot WCSS against $K$. The "elbow" point (where the rate of decrease sharply slows) suggests an optimal $K$.
    
- **Initialization Sensitivity**: Poor initial centroids lead to poor local minima. **K-Means++** is a common initialization technique that spreads out initial centroids to improve convergence.
    
- **Scalability**: It is computationally efficient ($O(n \cdot K \cdot I)$ where $I$ is iterations), making it suitable for large datasets.
    

## 2. Hierarchical Clustering: Building the Dendrogram

This method seeks to build a hierarchy of clusters without assuming a fixed $K$ upfront.

### Agglomerative (Bottom-Up) Process

Every point starts as a singleton cluster. At each step, the two "closest" clusters are merged until only one cluster remains. This results in a **Dendrogram**, where the height of the "branches" represents the distance between merged clusters.

### Linkage Metrics: Defining "Closeness"

How we measure the distance between two _sets_ of points significantly changes the resulting shape:

- **Single Linkage (Minimum Distance)**: Uses the distance between the two closest points. Pros: Can handle non-elliptical shapes. Cons: Susceptible to **Chaining** (clusters being merged because of a single trail of points).
    
- **Complete Linkage (Maximum Distance)**: Uses the distance between the two farthest points. Pros: Produces compact, even-sized clusters. Cons: Sensitive to outliers.
    
- **Average Linkage**: Uses the average distance between all pairs. More robust to noise than single/complete linkage.
    
- **Ward's Method**: Minimizes the increase in total within-cluster variance after merging. Usually produces the most "natural" looking clusters.
    

## 3. Dimensionality Reduction: PCA

Principal Component Analysis (PCA) is a linear transformation that converts data to a new coordinate system.

### The Optimization Goal

PCA finds directions (Principal Components) that:

1. Maximize the **Variance** of the projected data.
    
2. Minimize the **Reconstruction Error** (the distance between original points and their projections).
    

### Mathematical Logic (Conceptual)

- **Eigen-decomposition**: PCA is performed by calculating the eigenvectors and eigenvalues of the data's **Covariance Matrix**.
    
- **Eigenvectors**: These are the Principal Components (PCs). They are orthogonal (at 90 degrees) to each other.
    
- **Eigenvalues**: These represent the amount of variance explained by each PC. We sort these from highest to lowest.
    

### Components and Selection

- **PC1**: The vector that accounts for the largest possible variance in the dataset.
    
- **PC2**: The vector that accounts for the second-largest variance, while being orthogonal to PC1.
    
- **Screen Plot**: A graph showing the proportion of variance explained by each PC. We keep enough PCs to cover a target percentage (e.g., 95%) of the total variance.
    

### When to use PCA?

- **Curse of Dimensionality**: High-dimensional spaces are sparse; PCA reduces dimensions to make patterns more visible.
    
- **Multicollinearity**: If features are highly correlated, PCA creates new, uncorrelated features.
    
- **Preprocessing**: Often used before clustering (to remove noise) or before classification (to speed up training).