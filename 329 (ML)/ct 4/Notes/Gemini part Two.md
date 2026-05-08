# Study Guide 2: Semi-Supervised Learning & GMMs

## 1. Semi-Supervised Learning (SSL)

- **The Problem**: Labeled data is expensive/scarce (requires experts), while unlabeled data is cheap and abundant.
    
- **The Goal**: Use the structure of the massive unlabeled dataset to improve the decision boundary learned from the small labeled dataset.
    
- **Key Idea**: The distribution of $X$ (unlabeled) tells us where the "density" of the data lies, which often correlates with the class boundaries.
    

## 2. Gaussian Mixture Models (GMM)

GMM is a probabilistic model that assumes all data points are generated from a mixture of a finite number of Gaussian distributions with unknown parameters.

### GMM vs. K-Means

|Feature|K-Means|GMM|
|---|---|---|
|**Assignment**|Hard (1 or 0)|Soft (Probabilities/Weights)|
|**Cluster Shape**|Spherical (Circular)|Elliptical (Flexible)|
|**Parameters**|Mean only|Mean, Covariance (width/direction), and Weight|
|**Logic**|Distance-based|Density-based|

### Components of GMM

- $\mu$ **(Mean)**: The center of each Gaussian.
    
- $\Sigma$ **(Covariance)**: The shape and spread of each Gaussian.
    
- $w$ **(Mixing Weight)**: How much each Gaussian contributes to the overall population.
    

### Application of EM in GMM

- **E-step**: Calculate the probability that point $x$ comes from Gaussian $K$.
    
- **M-step**: Update Gaussian $K$'s mean and variance using the points, weighted by those probabilities.