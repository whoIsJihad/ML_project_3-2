# Machine Learning Notes - Comprehensive Guide

## Table of Contents
1. [Unsupervised Learning](#unsupervised-learning)
2. [Clustering](#clustering)
3. [K-Means Algorithm](#k-means-algorithm)
4. [Dimensionality Reduction](#dimensionality-reduction)
5. [Principal Component Analysis (PCA)](#principal-component-analysis-pca)
6. [Learning Probabilistic Models](#learning-probabilistic-models)
7. [Bayesian Learning](#bayesian-learning)
8. [Maximum Likelihood Learning](#maximum-likelihood-learning)
9. [Expectation Maximization (EM)](#expectation-maximization-em)
10. [Gaussian Mixture Models (GMM)](#gaussian-mixture-models-gmm)
11. [Semi-Supervised Learning](#semi-supervised-learning)
12. [Self-Supervised Learning](#self-supervised-learning)

---

## Unsupervised Learning

### What is it?
Unsupervised learning is a type of machine learning where we have **input data but no corresponding output labels**. The algorithm must find patterns, structures, or relationships in the data on its own.

### Key Difference from Supervised Learning
- **Supervised**: You have pairs of (input, correct answer). Like a teacher giving you problems with solutions.
- **Unsupervised**: You only have inputs. Like exploring a new city without a map or guide.

### Why Use Unsupervised Learning?
1. **Labeled data is expensive** - Getting labels requires human effort
2. **Discover hidden patterns** - Find structures you didn't know existed
3. **Data exploration** - Understand your data before building models
4. **Preprocessing** - Prepare data for supervised learning

### Main Types
1. **Clustering** - Group similar data points together
2. **Dimensionality Reduction** - Compress data while keeping important information
3. **Anomaly Detection** - Find unusual patterns
4. **Association** - Discover rules that describe data (e.g., market basket analysis)

### Real-World Examples
- Customer segmentation in marketing
- Organizing large photo collections
- Discovering topics in documents
- Gene expression analysis
- Recommendation systems

---

## Clustering

### What is Clustering?
Clustering is the task of **grouping similar objects together**. Objects in the same group (cluster) should be more similar to each other than to objects in other groups.

### Intuition
Imagine you have a bag of different colored balls. Clustering is like sorting them into piles where each pile contains balls of similar colors.

### Key Concepts

#### 1. Similarity/Distance Metrics
How do we measure if two objects are similar?

**Common Distance Metrics:**

- **Euclidean Distance** (most common)
  - Straight-line distance between two points
  - Formula for 2D: $d = \sqrt{(x_1-x_2)^2 + (y_1-y_2)^2}$
  - In n dimensions: $d = \sqrt{\sum_{i=1}^{n}(x_i-y_i)^2}$

- **Manhattan Distance**
  - Sum of absolute differences
  - $d = |x_1-x_2| + |y_1-y_2|$
  - Like walking through city blocks

- **Cosine Similarity**
  - Measures angle between vectors
  - Good for text/document comparison
  - Range: -1 (opposite) to 1 (identical)

#### 2. Types of Clustering

**A. Partitional Clustering**
- Divides data into non-overlapping groups
- Each point belongs to exactly one cluster
- Example: K-Means

**B. Hierarchical Clustering**
- Creates a tree of clusters
- Can show nested groupings
- Two approaches:
  - **Agglomerative**: Bottom-up (merge small clusters)
  - **Divisive**: Top-down (split large clusters)

**C. Density-Based Clustering**
- Groups points that are close together in dense regions
- Can find arbitrary shapes
- Example: DBSCAN

**D. Model-Based Clustering**
- Assumes data comes from a mixture of probability distributions
- Example: Gaussian Mixture Models

#### 3. Evaluating Clusters

**Internal Metrics** (no ground truth labels needed):

- **Silhouette Score** (-1 to 1, higher is better)
  - Measures how similar a point is to its own cluster vs other clusters
  
- **Inertia/Within-Cluster Sum of Squares**
  - Sum of squared distances to cluster centers
  - Lower is better, but beware of overfitting

**External Metrics** (when you have true labels):
- Adjusted Rand Index
- Normalized Mutual Information

### Common Challenges
1. **Choosing number of clusters** - How many groups should there be?
2. **Different cluster shapes** - Some algorithms only find spherical clusters
3. **Scalability** - Some methods are slow on large datasets
4. **Outliers** - Unusual points can break clustering
5. **Feature scaling** - Different units can dominate distance calculations

---

## K-Means Algorithm

### What is K-Means?
K-Means is the most popular clustering algorithm. It partitions data into **K clusters** where each point belongs to the cluster with the nearest center (centroid).

### The Core Idea
1. Start with K random cluster centers
2. Assign each point to its nearest center
3. Move centers to the average of their assigned points
4. Repeat steps 2-3 until centers stop moving

### Step-by-Step Algorithm

**Input:** 
- Dataset: $X = \{x_1, x_2, ..., x_n\}$
- Number of clusters: K

**Steps:**

1. **Initialize** K cluster centers $\mu_1, \mu_2, ..., \mu_K$ (randomly or using smart methods)

2. **Assignment Step:**
   - For each point $x_i$, assign it to the nearest centroid:
   - $c_i = \arg\min_j ||x_i - \mu_j||^2$
   - This means: find which centroid $\mu_j$ is closest to point $x_i$

3. **Update Step:**
   - Recalculate each centroid as the mean of all points assigned to it:
   - $\mu_j = \frac{1}{|C_j|} \sum_{x_i \in C_j} x_i$
   - This means: average all the points in cluster j

4. **Repeat** steps 2-3 until:
   - Centroids don't change much, OR
   - Maximum iterations reached, OR
   - Assignments don't change

### Objective Function
K-Means minimizes the **Within-Cluster Sum of Squares (WCSS)**:

$$J = \sum_{j=1}^{K} \sum_{x_i \in C_j} ||x_i - \mu_j||^2$$

This means: sum up all the squared distances from points to their cluster centers.



### Choosing K: The Elbow Method

Plot WCSS vs number of clusters K:
- As K increases, WCSS decreases
- Look for an "elbow" - where the decrease slows down
- That's often a good K value
![[Pasted image 20260423093901.png]]


### Initialization Methods

**1. Random Initialization**
- Pick K random points as initial centers
- Problem: Can lead to poor results depending on starting points
- Solution: Run multiple times and pick best result

**2. K-Means++**
- Smarter initialization that spreads out initial centers
- First center: choose random point
- Next centers: choose points far from existing centers (probabilistically)
- Usually gives better results

### Advantages
✓ Simple to understand and implement
✓ Fast for large datasets
✓ Works well when clusters are spherical and similar size
✓ Guaranteed to converge

### Disadvantages
✗ Must specify K in advance
✗ Sensitive to initialization (use K-Means++)
✗ Assumes spherical clusters
✗ Sensitive to outliers
✗ Doesn't work well with different cluster sizes/densities
✗ Only finds linear boundaries

### Practical Tips
1. **Scale your features** - Normalize to same range
2. **Try multiple K values** - Use elbow method or silhouette score
3. **Run multiple times** - Different initializations give different results
4. **Remove outliers first** - They can skew centroids
5. **Consider alternatives** - If clusters aren't spherical, try other methods

---

## Dimensionality Reduction

### What is it?
Dimensionality reduction is the process of **reducing the number of features (variables)** in your dataset while **preserving as much important information as possible**.

### The Problem: Curse of Dimensionality

**What happens with many dimensions?**
1. **Sparse data** - Points become very far apart
2. **Computation** - Algorithms become slow
3. **Visualization** - Can't plot more than 3 dimensions
4. **Overfitting** - Models memorize noise
5. **Storage** - Takes more memory

**Example:**
- 100 points in 1D: Dense and informative
- Same 100 points in 100D: Extremely sparse and hard to learn from

### Why Reduce Dimensions?

**Benefits:**
1. **Visualization** - Plot high-dimensional data in 2D or 3D
2. **Speed** - Faster training and prediction
3. **Storage** - Less memory needed
4. **Remove noise** - Keep signal, discard noise
5. **Better performance** - Less overfitting
6. **Interpretability** - Fewer features to understand

### Two Main Approaches

#### 1. Feature Selection
**Keep a subset of original features, discard the rest**

**Methods:**
- Filter methods (correlation, variance threshold)
- Wrapper methods (forward/backward selection)
- Embedded methods (Lasso, decision trees)

**Pros:** Keep original features (interpretable)
**Cons:** May lose information

#### 2. Feature Extraction
**Create new features by combining original ones**

**Methods:**
- PCA (Principal Component Analysis)
- LDA (Linear Discriminant Analysis)
- t-SNE (for visualization)
- Autoencoders (neural networks)

**Pros:** Can capture complex relationships
**Cons:** New features may be hard to interpret

### Key Concepts

#### Intrinsic Dimensionality
The "true" number of dimensions needed to represent data.

**Example:** 
- Data lies on a 2D plane in 3D space
- 3D coordinates, but intrinsic dimension is 2

#### Information Preservation
How much of the original information do we keep?

**Measures:**
- Variance explained (PCA)
- Reconstruction error
- Downstream task performance

### Common Techniques Overview

**Linear Methods:**
- **PCA** - Finds directions of maximum variance
- **LDA** - Finds directions that separate classes (supervised)
- **ICA** - Finds independent components

**Nonlinear Methods:**
- **t-SNE** - Preserves local structure, great for visualization
- **UMAP** - Faster than t-SNE, preserves global structure better
- **Kernel PCA** - PCA in higher-dimensional space
- **Autoencoders** - Neural network-based

### When to Use What?

**Use PCA when:**
- Linear relationships in data
- Want to preserve global structure
- Need interpretable components
- Want fast computation

**Use t-SNE when:**
- Visualizing clusters
- Local structure matters
- Don't need to transform new data
- Have enough computation time

**Use Autoencoders when:**
- Complex nonlinear relationships
- Have lots of data
- Need to encode new data
- Willing to train neural networks

---

## Principal Component Analysis (PCA)

### What is PCA?
PCA is a technique that finds new axes (principal components) along which data varies the most. It transforms data to a new coordinate system where the first axis captures the most variance, the second captures the second most, and so on.

### The Big Idea

**Imagine:**
- You have photos of people's faces
- Each photo is a huge list of pixel values
- PCA finds patterns like "brightness", "smile intensity", "hair color"
- These patterns explain most of the variation in faces
- You can represent faces using just these few patterns

### Intuition with Visuals

**Original 2D data scattered diagonally:**
**PCA finds new axes aligned with the spread**
![[Pasted image 20260302120748.png|802]]
### How PCA Works: Step by Step

#### Step 1: Center the Data
Subtract the mean from each feature so the data is centered at origin.

For feature j: $x_j' = x_j - \bar{x}_j$

**Why?** PCA is about variance, which is measured from the mean.

#### Step 2: Compute Covariance Matrix
Covariance tells us how features vary together.

For features in matrix X (n samples × d features):
$$\Sigma = \frac{1}{n} X^T X$$

**What does covariance mean?**
- Positive: features increase together
- Negative: one increases, other decreases
- Zero: no linear relationship

#### Step 3: Find Eigenvectors and Eigenvalues

**Eigenvectors** = Principal components (the new axes)
**Eigenvalues** = How much variance each component captures

Solve: $\Sigma v = \lambda v$

Where:
- v is an eigenvector (direction)
- λ is an eigenvalue (magnitude of variance in that direction)

#### Step 4: Sort by Eigenvalues
Rank eigenvectors by their eigenvalues (largest to smallest).

**First principal component (PC1)** = eigenvector with largest eigenvalue
**Second principal component (PC2)** = eigenvector with second largest eigenvalue
And so on...

#### Step 5: Project Data
Transform original data onto principal components.

$$Z = X W$$

Where:
- X is centered original data (n × d)
- W is matrix of top k eigenvectors (d × k)
- Z is transformed data (n × k)

### Mathematical Perspective

**PCA solves this optimization:**

Maximize: $\text{Var}(Xw) = w^T \Sigma w$

Subject to: $||w|| = 1$ (unit vector)

**Translation:** Find direction w such that projecting data onto it gives maximum variance.

### Variance Explained

**How much information did we keep?**

Variance explained by component i:
$$\frac{\lambda_i}{\sum_{j=1}^{d} \lambda_j}$$

Cumulative variance explained by first k components:
$$\frac{\sum_{i=1}^{k} \lambda_i}{\sum_{j=1}^{d} \lambda_j}$$

**Rule of thumb:** Keep components that explain 90-95% of variance.

### Choosing Number of Components

**Method 1: Variance Threshold**
- Keep components until reaching target variance (e.g., 95%)

**Method 2: Scree Plot**
- Plot eigenvalues vs component number
- Look for "elbow" where decrease slows down

```
Eigenvalue
    |
    |\
    | \
    |  \___
    |      \____
    +-------------- Component
     1  2  3  4  5
        ↑ elbow
```

**Method 3: Kaiser Criterion**
- Keep components with eigenvalue > 1
- Works for standardized data

### PCA Example (Conceptual)

**Original data: 1000 dimensions**
- Images: 100×100 pixels = 10,000 dimensions
- Apply PCA

**Result:**
- PC1 might represent "overall brightness"
- PC2 might represent "horizontal vs vertical edges"
- PC3 might represent "contrast"
- First 50 PCs capture 95% of variance
- Reduced 10,000 → 50 dimensions!

### Important Properties

#### 1. Orthogonality
All principal components are perpendicular to each other.

**Why it matters:** No redundancy between components.

#### 2. Uncorrelated
Principal components have zero correlation.

$$\text{Cov}(PC_i, PC_j) = 0 \text{ for } i \neq j$$

#### 3. Ordered by Variance
Components are ranked by importance.

#### 4. Linear Transformation
PCA only finds linear combinations of original features.

**Limitation:** Can't capture nonlinear patterns.

### Data Standardization

**Should you standardize before PCA?**

**Standardize when:**
- Features have different units (meters, kilograms, etc.)
- Features have different scales
- You want each feature to contribute equally

**Don't standardize when:**
- Features already in same units/scale
- Larger variance is meaningful (e.g., all pixel values 0-255)

**How to standardize:**
$$x_{\text{standardized}} = \frac{x - \mu}{\sigma}$$

### Advantages
✓ Reduces dimensionality effectively
✓ Removes correlated features
✓ Fast computation
✓ Interpretable components
✓ No parameters to tune
✓ Works well as preprocessing step

### Disadvantages
✗ Assumes linear relationships
✗ Components may be hard to interpret
✗ Sensitive to scaling (must standardize)
✗ Assumes high variance = high importance (not always true)
✗ Can't capture complex nonlinear patterns

### Practical Applications

**1. Images**
- Face recognition (eigenfaces)
- Image compression
- Noise reduction

**2. Genetics**
- Gene expression analysis
- Population genetics
- Disease classification

**3. Finance**
- Risk modeling
- Portfolio optimization
- Market trend analysis

**4. Natural Language Processing**
- Topic modeling (with truncated SVD)
- Document similarity
- Semantic analysis

### Implementation Tips

1. **Always center data** - Subtract mean from each feature
2. **Consider standardizing** - If features have different scales
3. **Check variance explained** - Plot cumulative variance
4. **Watch for outliers** - They can dominate principal components
5. **Try different numbers of components** - Validate with downstream task
6. **Visualize first 2-3 PCs** - See if clusters/patterns emerge

---

## Learning Probabilistic Models

### What are Probabilistic Models?

Probabilistic models represent uncertainty using **probability distributions**. Instead of making hard predictions, they give probabilities.

**Deterministic model:** "This email IS spam"
**Probabilistic model:** "This email is spam with probability 0.87"

### Why Use Probability?

1. **Uncertainty is everywhere** - Measurements have noise, future is uncertain
2. **Quantify confidence** - Know when model is unsure
3. **Combine information** - Principled way to merge evidence
4. **Make better decisions** - Use probability to guide actions
5. **Model generating process** - Understand how data was created

### Key Probability Concepts

#### 1. Random Variables
A quantity that can take different values with certain probabilities.

**Notation:**
- X = random variable (capital letter)
- x = specific value (lowercase)

**Types:**
- **Discrete:** Can count values (dice roll: 1,2,3,4,5,6)
- **Continuous:** Infinite values in range (height: 150.2 cm, 151.8 cm, ...)

#### 2. Probability Distribution
Describes how probability is spread over possible values.

**For discrete X:**
$P(X=x)$ or just $P(x)$ = probability mass function

**For continuous X:**
$p(x)$ = probability density function (PDF)

**Properties:**
- All probabilities ≥ 0
- Sum/integral = 1

#### 3. Joint Probability
Probability of multiple events happening together.

$$P(X=x, Y=y)$$ or $$P(x,y)$$

**Example:** P(rainy, cold) = probability it's both rainy AND cold

#### 4. Conditional Probability
Probability of one event given another has occurred.

$$P(X=x | Y=y) = \frac{P(X=x, Y=y)}{P(Y=y)}$$

**Read as:** "Probability of X given Y"

**Example:** P(carry umbrella | rainy) = high

#### 5. Marginal Probability
Probability of one variable regardless of others.

$$P(X=x) = \sum_y P(X=x, Y=y)$$

**Example:** P(rainy) = P(rainy, cold) + P(rainy, warm)

#### 6. Independence
Two variables are independent if one doesn't affect the other.

$$P(X, Y) = P(X) \cdot P(Y)$$
$$P(X|Y) = P(X)$$

**Example:** Coin flips are independent.

#### 7. Bayes' Rule
The foundation of Bayesian reasoning:

$$P(Y|X) = \frac{P(X|Y) \cdot P(Y)}{P(X)}$$

Or more verbosely:
$$P(\text{hypothesis} | \text{data}) = \frac{P(\text{data} | \text{hypothesis}) \cdot P(\text{hypothesis})}{P(\text{data})}$$

**Terms:**
- **Prior:** P(Y) = belief before seeing data
- **Likelihood:** P(X|Y) = how probable is data if hypothesis is true
- **Evidence:** P(X) = total probability of data
- **Posterior:** P(Y|X) = belief after seeing data

### Types of Probabilistic Models

#### 1. Generative Models
Model how data is generated: P(X, Y)

**Process:**
1. Generate label Y from P(Y)
2. Generate features X from P(X|Y)

**Examples:**
- Naive Bayes
- Hidden Markov Models
- Gaussian Mixture Models
- Bayesian Networks

**Can do:**
- Classify: use Bayes rule to get P(Y|X)
- Generate new data: sample from P(X,Y)
- Handle missing data: marginalize

#### 2. Discriminative Models
Directly model the decision: P(Y|X)

**Process:**
- Learn boundary between classes
- Don't model how X is generated

**Examples:**
- Logistic Regression
- SVM
- Neural Networks
- Conditional Random Fields

**Trade-offs:**
- Usually better for classification
- Can't generate new data
- Often need less data

### Common Distributions

#### Discrete Distributions

**1. Bernoulli Distribution**
- Single binary trial
- P(X=1) = p, P(X=0) = 1-p
- Example: Coin flip

**2. Binomial Distribution**
- Number of successes in n trials
- Parameters: n (trials), p (success probability)
- Example: Number of heads in 10 coin flips

**3. Categorical Distribution**
- One outcome from K categories
- Parameters: [p₁, p₂, ..., pₖ] where Σpᵢ = 1
- Example: Die roll (6 categories)

#### Continuous Distributions

**1. Gaussian (Normal) Distribution**
$$p(x) = \frac{1}{\sqrt{2\pi\sigma^2}} \exp\left(-\frac{(x-\mu)^2}{2\sigma^2}\right)$$

- Parameters: μ (mean), σ² (variance)
- Bell curve shape
- Most common in ML

**2. Multivariate Gaussian**
$$p(\mathbf{x}) = \frac{1}{(2\pi)^{d/2}|\Sigma|^{1/2}} \exp\left(-\frac{1}{2}(\mathbf{x}-\boldsymbol{\mu})^T\Sigma^{-1}(\mathbf{x}-\boldsymbol{\mu})\right)$$

- Parameters: μ (mean vector), Σ (covariance matrix)
- Generalizes Gaussian to multiple dimensions

**3. Exponential Distribution**
- Time between events
- Parameter: λ (rate)
- Always positive values

### Latent Variable Models

**Latent variables** = Hidden variables not directly observed

**Why use them?**
- Represent underlying causes
- Simplify complex data
- Capture structure

**Example:**
- **Observed:** Student test scores
- **Latent:** Intelligence, effort, luck
- Model: Test scores depend on latent intelligence

**Common latent variable models:**
- Mixture models (GMM)
- Factor analysis
- Hidden Markov Models
- Topic models (LDA)

### Parameter Estimation

**Goal:** Learn model parameters from data

**Main approaches:**
1. **Maximum Likelihood Estimation (MLE)** - Find parameters that make data most likely
2. **Maximum A Posteriori (MAP)** - MLE + prior beliefs about parameters
3. **Bayesian Inference** - Full distribution over parameters

### Evaluation of Probabilistic Models

**1. Log-Likelihood**
- How probable is test data under the model?
- Higher log-likelihood = better
- $$\log P(D|\theta) = \sum_{i=1}^{n} \log P(x_i|\theta)$$

**2. Perplexity**
- Geometric mean of inverse probabilities
- Lower perplexity = better
- Common in language modeling

**3. Cross-Entropy**
- Measure of surprise
- Lower = better predictions

**4. Proper Scoring Rules**
- Brier score
- Log score
- Encourage honest probability estimates

---

## Bayesian Learning

### What is Bayesian Learning?

Bayesian learning is a framework where we **update our beliefs about model parameters as we see more data**, using Bayes' rule.

### The Core Philosophy

**Classical (Frequentist) View:**
- Parameters are fixed but unknown
- Estimate single best value
- Data is random

**Bayesian View:**
- Parameters are random variables with distributions
- Start with prior beliefs
- Update beliefs with data
- Never "know" exact value, but have probability distribution

### Bayes' Rule for Learning

$$P(\theta | D) = \frac{P(D | \theta) \cdot P(\theta)}{P(D)}$$

**Components:**

1. **Prior: P(θ)**
   - What we believe before seeing data
   - Can be informative (strong beliefs) or uninformative (weak beliefs)
   
2. **Likelihood: P(D|θ)**
   - How probable is observed data for parameter value θ
   - Same as in MLE
   
3. **Evidence: P(D)**
   - Total probability of data (normalizing constant)
   - $$P(D) = \int P(D|\theta) P(\theta) d\theta$$
   
4. **Posterior: P(θ|D)**
   - Updated belief after seeing data
   - This is what we want!

### Simple Example: Coin Flipping

**Problem:** Estimate probability p of heads for a biased coin

**Prior belief:**
- Beta distribution: P(p) = Beta(α, β)
- α=2, β=2 → slight belief that p ≈ 0.5 (fair coin)

**Data:**
- Flip 10 times: 7 heads, 3 tails

**Likelihood:**
- P(data|p) = Binomial(7 heads | 10 flips, p) = p⁷(1-p)³

**Posterior:**
- P(p|data) = Beta(α+7, β+3) = Beta(9, 5)
- Most likely value: around p ≈ 0.64

**As more data comes:**
- Prior becomes less important
- Data dominates
- Posterior concentrates around true value

### Sequential Updating

**Beautiful property:** Posterior from first batch of data becomes prior for next batch

```
Prior → [See Data 1] → Posterior₁
Posterior₁ → [See Data 2] → Posterior₂
Posterior₂ → [See Data 3] → Posterior₃
...
```

**Result:** Same as processing all data at once!

### Making Predictions

**Don't just use point estimate!** Use the full posterior distribution.

**Posterior Predictive Distribution:**
$$P(x_{\text{new}} | D) = \int P(x_{\text{new}} | \theta) P(\theta | D) d\theta$$

**What this means:**
- Average predictions over all possible parameter values
- Weight by how likely each parameter value is (posterior)
- Naturally accounts for uncertainty

**Example:**
- Posterior: p could be 0.5, 0.6, or 0.7 with different probabilities
- Prediction: "Next flip is heads" = weighted average
- More uncertainty in θ → more uncertainty in prediction

### Prior Selection

**Types of Priors:**

**1. Informative Prior**
- Strong beliefs about parameter values
- Useful when you have domain knowledge
- Example: "This coin is probably fair" → Beta(10, 10)

**2. Weakly Informative Prior**
- Gentle constraints
- Rules out unreasonable values
- Example: "Temperature is positive" → Half-Normal

**3. Non-informative Prior**
- Let data speak for itself
- Example: Uniform prior
- Warning: May not be truly "non-informative"

**4. Conjugate Prior**
- Mathematical convenience
- Posterior is same family as prior
- Example: Beta prior + Binomial likelihood → Beta posterior

### Conjugate Priors (Makes Math Easy)

| Likelihood | Conjugate Prior | Posterior |
|------------|----------------|-----------|
| Bernoulli | Beta | Beta |
| Binomial | Beta | Beta |
| Categorical | Dirichlet | Dirichlet |
| Gaussian (known σ²) | Gaussian | Gaussian |
| Gaussian (known μ) | Inverse-Gamma | Inverse-Gamma |
| Poisson | Gamma | Gamma |

**Why useful?**
- Closed-form updates (no approximation needed)
- Fast computation
- Interpretable

### Maximum A Posteriori (MAP) Estimation

**What if we need a single parameter value?**

**MAP estimate:**
$$\theta_{\text{MAP}} = \arg\max_{\theta} P(\theta | D)$$

**Using Bayes rule:**
$$\theta_{\text{MAP}} = \arg\max_{\theta} P(D | \theta) P(\theta)$$

**Relationship to MLE:**
- MLE: $\theta_{\text{MLE}} = \arg\max_{\theta} P(D | \theta)$
- MAP: $\theta_{\text{MAP}} = \arg\max_{\theta} P(D | \theta) P(\theta)$
- MAP = MLE + prior

**When they're similar:**
- Lots of data → prior becomes negligible → MAP ≈ MLE
- Uniform prior → MAP = MLE

### Bayesian vs Frequentist

| Aspect | Bayesian | Frequentist |
|--------|----------|-------------|
| Parameters | Random variables | Fixed unknowns |
| Inference | Probability distributions | Point estimates + confidence intervals |
| Prior knowledge | Incorporated naturally | Not used (or used indirectly) |
| Uncertainty | Credible intervals (direct probability) | Confidence intervals (long-run frequency) |
| Small data | Works well | Can struggle |
| Computation | Often harder | Often simpler |

### Advantages of Bayesian Learning

✓ Principled uncertainty quantification
✓ Incorporates prior knowledge
✓ Works well with small data
✓ Sequential updating is natural
✓ Prevents overfitting (through priors)
✓ Coherent decision-making framework

### Disadvantages

✗ Computationally expensive (often need approximations)
✗ Prior selection can be subjective
✗ Results depend on prior choice
✗ Requires more sophisticated tools
✗ Can be harder to interpret

### Computational Challenges

**Problem:** Computing posterior often intractable

$$P(\theta | D) = \frac{P(D | \theta) P(\theta)}{\int P(D | \theta) P(\theta) d\theta}$$

The integral in denominator is often impossible to compute!

**Solutions:**

**1. Conjugate Priors**
- Avoid the integral
- Limited to specific model families

**2. Numerical Integration**
- Grid approximation
- Only works in low dimensions

**3. Laplace Approximation**
- Approximate posterior as Gaussian
- Good for smooth, unimodal posteriors

**4. Markov Chain Monte Carlo (MCMC)**
- Sample from posterior
- Works in high dimensions
- Examples: Metropolis-Hastings, Gibbs sampling

**5. Variational Inference**
- Approximate with simpler distribution
- Faster than MCMC
- Trade accuracy for speed

### Applications

**1. Spam Filtering (Naive Bayes)**
- Prior: P(spam) = 0.3
- Update as you mark emails
- Personalizes to your patterns

**2. Medical Diagnosis**
- Prior: Disease prevalence
- Likelihood: Test accuracy
- Posterior: Probability you have disease

**3. A/B Testing**
- Prior: No difference between versions
- Update as results come in
- Decide when confident enough

**4. Robotics**
- Prior: Robot's believed location
- Likelihood: Sensor measurements
- Posterior: Updated location (Bayesian filtering)

**5. Machine Learning**
- Bayesian neural networks
- Gaussian processes
- Bayesian optimization

---

## Maximum Likelihood Learning

### What is Maximum Likelihood Estimation (MLE)?

MLE is a method to **estimate model parameters by finding values that make the observed data most probable**.

**Core idea:** Among all possible parameter values, pick the one that makes your data "most likely" to have occurred.

### The Intuition

**Imagine:**
- You see 10 coin flips: H H H T H H H H H T
- Question: What's the probability p of heads?
- MLE answer: p = 0.8 (because 8/10 were heads)
- Why? This value makes the observed sequence most likely

### Mathematical Formulation

**Given:**
- Data: $D = \{x_1, x_2, ..., x_n\}$
- Model with parameters: θ
- Probability of data given parameters: $P(D|\theta)$

**Goal:** Find θ that maximizes $P(D|\theta)$

$$\theta_{\text{MLE}} = \arg\max_{\theta} P(D | \theta)$$

### The Likelihood Function

**Likelihood:** $L(\theta) = P(D | \theta)$

**Key distinction:**
- **Probability:** Fix parameters, vary data
- **Likelihood:** Fix data, vary parameters

**For independent samples:**
$$L(\theta) = P(x_1, x_2, ..., x_n | \theta) = \prod_{i=1}^{n} P(x_i | \theta)$$

### Log-Likelihood

**Problem:** Products of small numbers → numerical underflow

**Solution:** Take logarithm!

$$\ell(\theta) = \log L(\theta) = \sum_{i=1}^{n} \log P(x_i | \theta)$$

**Why this works:**
- log is monotonic: max of L = max of log L
- Product → Sum
- Better numerical stability
- Easier derivatives

**So we maximize:**
$$\theta_{\text{MLE}} = \arg\max_{\theta} \ell(\theta)$$

### How to Find MLE

**Step 1: Write the likelihood**
- Based on your model/distribution
- Product over all data points

**Step 2: Take log-likelihood**
- Convert product to sum

**Step 3: Take derivative**
- Derivative with respect to each parameter

**Step 4: Set to zero and solve**
$$\frac{\partial \ell(\theta)}{\partial \theta} = 0$$

**Step 5: Verify it's a maximum**
- Check second derivative is negative

### Example 1: Gaussian Mean

**Setup:**
- Data: $x_1, ..., x_n$
- Model: $x_i \sim \mathcal{N}(\mu, \sigma^2)$ (known variance)
- Find: $\mu_{\text{MLE}}$

**Likelihood:**
$$L(\mu) = \prod_{i=1}^{n} \frac{1}{\sqrt{2\pi\sigma^2}} \exp\left(-\frac{(x_i-\mu)^2}{2\sigma^2}\right)$$

**Log-likelihood:**
$$\ell(\mu) = -\frac{n}{2}\log(2\pi\sigma^2) - \frac{1}{2\sigma^2}\sum_{i=1}^{n}(x_i-\mu)^2$$

**Derivative:**
$$\frac{\partial \ell}{\partial \mu} = \frac{1}{\sigma^2}\sum_{i=1}^{n}(x_i-\mu)$$

**Set to zero:**
$$\sum_{i=1}^{n}(x_i-\mu) = 0$$

$$\sum_{i=1}^{n}x_i = n\mu$$

**Result:**
$$\mu_{\text{MLE}} = \frac{1}{n}\sum_{i=1}^{n}x_i$$

**The sample mean!** This confirms our intuition.

### Example 2: Bernoulli Parameter

**Setup:**
- Data: $x_1, ..., x_n \in \{0,1\}$ (coin flips)
- Model: $P(x_i = 1) = p$
- Find: $p_{\text{MLE}}$

**Likelihood:**
$$L(p) = \prod_{i=1}^{n} p^{x_i}(1-p)^{1-x_i}$$

**Log-likelihood:**
$$\ell(p) = \sum_{i=1}^{n} [x_i \log p + (1-x_i) \log(1-p)]$$

$$= \left(\sum_{i=1}^{n} x_i\right) \log p + \left(n - \sum_{i=1}^{n} x_i\right) \log(1-p)$$

**Derivative:**
$$\frac{\partial \ell}{\partial p} = \frac{\sum x_i}{p} - \frac{n - \sum x_i}{1-p}$$

**Set to zero and solve:**
$$p_{\text{MLE}} = \frac{1}{n}\sum_{i=1}^{n} x_i$$

**The proportion of 1's!** Makes perfect sense.

### Properties of MLE

#### 1. Consistency
As n → ∞, $\theta_{\text{MLE}}$ converges to true θ

**Meaning:** With enough data, you'll find the right answer

#### 2. Asymptotic Normality
For large n, $\theta_{\text{MLE}}$ is approximately Gaussian

**Meaning:** You can compute confidence intervals

#### 3. Asymptotic Efficiency
MLE achieves lowest possible variance among unbiased estimators (for large n)

**Meaning:** Best use of data

#### 4. Invariance
If $\theta_{\text{MLE}}$ maximizes likelihood, then $g(\theta_{\text{MLE}})$ maximizes likelihood of g(θ)

**Example:** If $\sigma^2_{\text{MLE}} = 4$, then $\sigma_{\text{MLE}} = 2$

### MLE vs MAP vs Bayesian

**MLE:**
$$\theta_{\text{MLE}} = \arg\max_{\theta} P(D | \theta)$$
- No prior
- Single point estimate
- Can overfit with small data

**MAP:**
$$\theta_{\text{MAP}} = \arg\max_{\theta} P(D | \theta) P(\theta)$$
- Includes prior
- Single point estimate
- Prior acts as regularization

**Bayesian:**
$$P(\theta | D) = \frac{P(D | \theta) P(\theta)}{P(D)}$$
- Full posterior distribution
- No single estimate
- Quantifies uncertainty

**Relationship:**
- MAP = MLE + prior
- With uniform prior: MAP = MLE
- With lots of data: MAP ≈ MLE (prior becomes negligible)

### Advantages

✓ Intuitive and principled
✓ Strong theoretical properties
✓ Often has closed-form solution
✓ Works with many distributions
✓ No subjective prior needed
✓ Computationally efficient

### Disadvantages

✗ Can overfit with small data
✗ No uncertainty quantification
✗ Doesn't incorporate prior knowledge
✗ Assumes model is correct
✗ Can be biased (in small samples)

### Common Pitfalls

**1. Overfitting**
- MLE can perfectly fit small datasets
- Example: Gaussian MLE with n=1 has zero variance!

**2. Zero Probabilities**
- If event never observed, MLE assigns probability 0
- Problem for unseen events
- Solution: Smoothing (add-one, Laplace)

**3. Local Maxima**
- Non-convex problems have multiple peaks
- May find local maximum, not global
- Solution: Try multiple initializations

**4. Numerical Issues**
- Very small probabilities → underflow
- Solution: Work with log-probabilities

### Regularization as Prior

**Adding regularization ≈ Adding prior**

**L2 regularization (Ridge):**
$$\arg\min_{\theta} -\log P(D|\theta) + \lambda||\theta||^2$$
- Equivalent to MAP with Gaussian prior
- Prefers smaller parameter values

**L1 regularization (Lasso):**
$$\arg\min_{\theta} -\log P(D|\theta) + \lambda||\theta||_1$$
- Equivalent to MAP with Laplace prior
- Encourages sparsity

### Applications

**1. Statistical Modeling**
- Estimate means, variances, correlations
- Fit probability distributions to data

**2. Machine Learning**
- Logistic regression (maximize likelihood of labels)
- Naive Bayes (MLE for probabilities)

**3. Linear Regression**
- Minimize squared error = maximize Gaussian likelihood

**4. Clustering**
- Gaussian Mixture Models (EM algorithm)

**5. Time Series**
- ARMA models
- Hidden Markov Models

---

## Expectation Maximization (EM)

### What is EM?

EM is an iterative algorithm for **finding maximum likelihood estimates when we have missing or hidden data**.

**The problem:** Sometimes we can't directly optimize likelihood because some variables are unobserved (latent).

**The solution:** EM alternates between:
1. **E-step:** Guess the missing data
2. **M-step:** Optimize as if the guess was correct

### The Setting

**We have:**
- **Observed data:** X (what we can see)
- **Latent data:** Z (what we can't see but affects X)
- **Parameters:** θ (what we want to estimate)

**Complete data:** (X, Z) together


**Incomplete data:** Just X

**Goal:** Find θ that maximizes $P(X | \theta)$

**Challenge:** Can't compute $P(X | \theta)$ easily because Z is hidden!

$$P(X | \theta) = \sum_Z P(X, Z | \theta)$$

This sum/integral is often intractable.

### The EM Algorithm

**Initialize:** Start with random guess θ⁽⁰⁾

**Repeat until convergence:**

**E-Step (Expectation):**
Compute expected log-likelihood of complete data given current parameters.

$$Q(\theta | \theta^{(t)}) = \mathbb{E}_{Z|X,\theta^{(t)}}[\log P(X, Z | \theta)]$$

In words: "If θ⁽ᵗ⁾ were correct, what would we expect the complete data log-likelihood to be?"

**M-Step (Maximization):**
Find parameters that maximize this expected log-likelihood.

$$\theta^{(t+1)} = \arg\max_{\theta} Q(\theta | \theta^{(t)})$$

In words: "Find best parameters for our expected complete data"

**Update:** θ⁽ᵗ⁺¹⁾ becomes current parameters, repeat.

### Why Does EM Work?

**Key insight:** Each iteration increases (or keeps same) the likelihood!

$$P(X | \theta^{(t+1)}) \geq P(X | \theta^{(t)})$$

**Proof sketch:**
- E-step creates a lower bound on log-likelihood
- M-step maximizes that lower bound
- This pushes actual log-likelihood up

**Result:** Guaranteed to converge to a local maximum (or saddle point).

### Simple Intuition: The Coin Factory

**Scenario:**
- Two coin-flipping machines A and B with unknown biases pₐ and p_B
- Someone flips a random machine 5 times and tells you results
- But doesn't tell you which machine!
- Data: [H,H,T,H,T], machine unknown

**EM approach:**

**E-step (guess):**
- "If pₐ=0.4 and p_B=0.7, these flips probably came from B"
- Compute: P(machine = A | data, current params)

**M-step (update):**
- "If flips came from B with that probability, best estimate for p_B is..."
- Update parameters

**Iterate:**
- Better params → better guesses → better params → ...

### Detailed Example: Gaussian Mixture Model (Preview)

**Problem:** Data comes from mix of 2 Gaussian distributions

**Observed:** Data points X = {x₁, ..., xₙ}
**Hidden:** Which Gaussian each point came from

**Parameters:**
- θ = {π, μ₁, σ₁, μ₂, σ₂}
- π = mixing weight

**E-step:**
For each point xᵢ, compute probability it came from each Gaussian:

$$\gamma_{i1} = \frac{\pi \mathcal{N}(x_i | \mu_1, \sigma_1^2)}{\pi \mathcal{N}(x_i | \mu_1, \sigma_1^2) + (1-\pi) \mathcal{N}(x_i | \mu_2, \sigma_2^2)}$$

This is called the "responsibility" of component 1 for point i.

**M-step:**
Update parameters using the responsibilities as weights:

$$\mu_1^{\text{new}} = \frac{\sum_{i=1}^{n} \gamma_{i1} x_i}{\sum_{i=1}^{n} \gamma_{i1}}$$

Weighted average where points probably from component 1 count more.

### EM Properties

#### Convergence

**Guaranteed:**
- Likelihood never decreases
- Converges to a local maximum

**Not guaranteed:**
- Finding global maximum
- Speed of convergence

#### Sensitivity to Initialization

**Problem:** Different starting points → different local maxima

**Solutions:**
1. Run multiple times with different random initializations
2. Use smart initialization (e.g., K-means for GMM)
3. Try different numbers of components

#### Speed

**Can be slow:**
- Many iterations needed
- Each iteration can be expensive

**Speed-ups:**
- Early stopping (stop when change is small)
- Incremental EM (update on batches)
- Variational EM (approximations)

### Variants and Extensions

**1. Hard EM (K-means is an example)**
- E-step: Assign each point to most likely cluster (hard assignment)
- M-step: Update parameters
- Faster but less accurate

**2. Generalized EM**
- M-step: Just improve Q, don't necessarily maximize
- More flexible

**3. Stochastic EM**
- E-step: Sample latent variables instead of computing expectations
- Useful when E-step expectations are intractable

**4. Incremental EM**
- Update parameters after each data point
- Better for online learning

### When to Use EM

**Good for:**
- Missing data problems
- Mixture models
- Hidden Markov Models
- Collaborative filtering
- Image segmentation

**Not ideal when:**
- No latent variables (use direct MLE)
- Non-convex with many local maxima (try other methods)
- Need global optimum guarantees

### Advantages

✓ Guarantees likelihood improvement
✓ Simple to implement
✓ Often no other choice for latent variable models
✓ Interpretable iterations
✓ Can incorporate constraints easily

### Disadvantages

✗ Converges to local maxima
✗ Can be slow
✗ Sensitive to initialization
✗ Need to specify number of components
✗ Can get stuck in saddle points

### Practical Tips

1. **Initialize well** - Use domain knowledge or K-means
2. **Run multiple times** - Try different random starts
3. **Monitor likelihood** - Plot to check convergence
4. **Stop criteria** - When change < threshold or max iterations
5. **Validate** - Use held-out data to avoid overfitting
6. **Regularize** - Add priors to prevent degenerate solutions

---

## Gaussian Mixture Models (GMM)

### What is a GMM?

A Gaussian Mixture Model represents data as coming from a **mixture of multiple Gaussian (normal) distributions**.

**Core idea:** Your data has multiple "modes" or clusters, each shaped like a bell curve.

### The Motivation

**Problem with K-means:**
- Assumes spherical clusters
- Hard assignments (each point in exactly one cluster)
- Equal cluster sizes

**GMM advantages:**
- Handles elliptical clusters
- Soft assignments (probabilities)
- Different cluster sizes and shapes

### Mathematical Formulation

**A GMM is:**
$$P(x) = \sum_{k=1}^{K} \pi_k \mathcal{N}(x | \mu_k, \Sigma_k)$$

Where:
- K = number of components (clusters)
- πₖ = mixing weight for component k (πₖ ≥ 0, Σπₖ = 1)
- μₖ = mean of component k
- Σₖ = covariance matrix of component k
- $\mathcal{N}(x | \mu_k, \Sigma_k)$ = Gaussian PDF

**Interpretation:**
1. Pick component k with probability πₖ
2. Sample from that component's Gaussian

### Components Explained

#### 1. Mixing Weights (π)
Probability of each component.

**Example:** π = [0.3, 0.5, 0.2] for K=3
- 30% chance of component 1
- 50% chance of component 2
- 20% chance of component 3

**Constraints:**
- All πₖ ≥ 0
- Σπₖ = 1

#### 2. Means (μ)
Centers of each Gaussian.

**1D:** Just a number
**nD:** A vector [μ₁, μ₂, ..., μₙ]

#### 3. Covariances (Σ)
Shape and orientation of each Gaussian.

**Types:**

**Full covariance:** Each component has full covariance matrix
- Most flexible
- Most parameters
- Can represent any ellipse

**Diagonal covariance:** Only diagonal elements (no correlation)
- Axis-aligned ellipses
- Fewer parameters

**Spherical covariance:** σ²I (same variance in all directions)
- Circles/spheres
- Like K-means

**Tied covariance:** All components share same Σ
- Same shape, different locations
- Fewer parameters

### Visual Understanding

**1D GMM with K=2:**
```
        Peak 1       Peak 2
         /\           /\
        /  \         /  \
       /    \       /    \
      /      \     /      \
     /        \   /        \
    /          \ /          \
   /_____________X____________\
                ↑
        Overlap region
```

**2D GMM with K=3:**
```
        Component 1 (large, horizontal ellipse)
            ___________
           /           \
          |     O       |
           \___________/
    
    Component 2           Component 3
    (small circle)        (vertical ellipse)
         ___                  ___
        /   \                /   \
       | O   |              /  O  \
        \___/              \       /
                            \_____/
```

### Learning GMM with EM

**The problem:** Given data X, find parameters θ = {π, μ, Σ}

**Why EM?** We don't know which component generated each point (latent variable!)

#### E-Step: Compute Responsibilities

For each data point xᵢ and component k, compute "responsibility":

$$\gamma_{ik} = \frac{\pi_k \mathcal{N}(x_i | \mu_k, \Sigma_k)}{\sum_{j=1}^{K} \pi_j \mathcal{N}(x_i | \mu_j, \Sigma_j)}$$

**Meaning:** Probability that component k generated point xᵢ

**Properties:**
- 0 ≤ γᵢₖ ≤ 1
- Σₖ γᵢₖ = 1 for each i
- Soft assignment (unlike K-means)

**Intuition:**
- If xᵢ is close to μₖ → γᵢₖ is high
- If xᵢ is far from μₖ → γᵢₖ is low

#### M-Step: Update Parameters

**Effective number in each component:**
$$N_k = \sum_{i=1}^{n} \gamma_{ik}$$

**Update mixing weights:**
$$\pi_k^{\text{new}} = \frac{N_k}{n}$$

Proportion of data "assigned" to component k.

**Update means:**
$$\mu_k^{\text{new}} = \frac{1}{N_k} \sum_{i=1}^{n} \gamma_{ik} x_i$$

Weighted average of points, weighted by responsibility.

**Update covariances:**
$$\Sigma_k^{\text{new}} = \frac{1}{N_k} \sum_{i=1}^{n} \gamma_{ik} (x_i - \mu_k^{\text{new}})(x_i - \mu_k^{\text{new}})^T$$

Weighted covariance.

### Step-by-Step Algorithm

**Input:** Data X, number of components K

**Initialize:**
- Random or K-means initialization for μ
- Identity matrices for Σ
- Equal weights: π = [1/K, 1/K, ..., 1/K]

**Repeat:**

1. **E-Step:** Compute all γᵢₖ using current parameters

2. **M-Step:** Update all parameters using responsibilities

3. **Check convergence:** Stop if:
   - Log-likelihood change < threshold
   - Parameters don't change much
   - Maximum iterations reached

**Output:** Final parameters and responsibilities

### Choosing Number of Components K

**Problem:** K is a hyperparameter

**Methods:**

**1. Model Selection Criteria**

**Akaike Information Criterion (AIC):**
$$\text{AIC} = -2 \log L + 2p$$
- L = likelihood
- p = number of parameters
- Lower is better

**Bayesian Information Criterion (BIC):**
$$\text{BIC} = -2 \log L + p \log n$$
- Penalizes complexity more than AIC
- Lower is better

**2. Cross-Validation**
- Split data into train/validation
- Try different K
- Pick K with best validation log-likelihood

**3. Elbow Method**
- Plot likelihood vs K
- Look for elbow where improvement slows

**4. Domain Knowledge**
- Use prior knowledge about number of clusters

### GMM vs K-Means

| Aspect | K-Means | GMM |
|--------|---------|-----|
| Assignment | Hard (0 or 1) | Soft (probabilities) |
| Cluster shape | Spherical | Elliptical |
| Model | Geometric | Probabilistic |
| Speed | Faster | Slower |
| Parameters | Just means | Means + covariances + weights |
| Uncertainty | None | Probability for each cluster |

**Relationship:** K-means is special case of GMM with:
- Spherical covariances (σ²I)
- Hard assignments (γᵢₖ ∈ {0,1})

### Advantages

✓ Flexible cluster shapes (elliptical)
✓ Soft clustering (probabilities)
✓ Probabilistic framework
✓ Can model uncertainty
✓ Generative model (can sample new data)
✓ Handles different cluster sizes

### Disadvantages

✗ Must specify K
✗ Sensitive to initialization
✗ Can converge to local optima
✗ Computationally expensive
✗ Assumes data is Gaussian
✗ Struggles with very high dimensions

### Common Issues and Solutions

**1. Singularities**
- **Problem:** Covariance becomes nearly zero (one component fits single point)
- **Solution:** Regularize covariances: Σₖ + εI

**2. Poor Initialization**
- **Problem:** Random init leads to bad local optimum
- **Solution:** Initialize with K-means

**3. Choosing K**
- **Problem:** No clear "right" answer
- **Solution:** Try multiple K, use BIC/AIC

**4. High Dimensions**
- **Problem:** Many parameters, curse of dimensionality
- **Solution:** Use dimensionality reduction first (PCA), or constrain covariances

### Applications

**1. Image Segmentation**
- Each component = region color/texture
- Soft boundaries between regions

**2. Anomaly Detection**
- Model normal data with GMM
- Low probability regions = anomalies

**3. Speaker Recognition**
- Each speaker modeled by GMM
- Voice features cluster in different regions

**4. Background Subtraction (Video)**
- Each pixel's color history = GMM
- Detect foreground as deviations

**5. Density Estimation**
- Model complex probability distributions
- Better than single Gaussian

**6. Data Compression**
- Store only GMM parameters
- Reconstruct approximate data

### Extensions

**1. Bayesian GMM**
- Prior on parameters
- Automatic selection of K
- VBGMM, DPGMM (Dirichlet Process)

**2. Hidden Markov Models**
- GMM for emissions
- Sequence modeling

**3. Factor Analysis**
- GMM in latent space
- Dimensionality reduction

### Practical Implementation Tips

1. **Standardize data** - Scale features to similar ranges
2. **Initialize with K-means** - Much better than random
3. **Monitor log-likelihood** - Should always increase
4. **Regularize covariances** - Add small constant to diagonal
5. **Try different K** - Use BIC to select
6. **Check for empty components** - Reinitialize if needed
7. **Visualize results** - Project to 2D with PCA

---

## Semi-Supervised Learning

### What is Semi-Supervised Learning?

Semi-supervised learning uses **both labeled and unlabeled data** for training. Typically, you have a small amount of labeled data and a large amount of unlabeled data.

**The spectrum:**
- Supervised: All data labeled (expensive)
- Semi-supervised: Some data labeled, most unlabeled (realistic)
- Unsupervised: No data labeled (limited)

### Why Semi-Supervised?

**The reality:**
- **Labeled data is expensive** - Requires human effort
- **Unlabeled data is cheap** - Easy to collect
- **Example:** Medical images - millions available, few diagnosed

**The promise:**
- Use abundant unlabeled data to improve model
- Get closer to supervised performance with less labeling cost

### When Does It Help?

Semi-supervised learning works well when these assumptions hold:

#### 1. Smoothness Assumption
**If two points are close, their labels should be similar**

**Example:**
- Two similar images probably have same label
- Graph: nearby nodes likely same class

**What it means:**
- Decision boundary should be in low-density regions
- Don't put boundary through cluster of points

#### 2. Cluster Assumption
**Points in same cluster likely have same label**

**Example:**
- Customer segments have similar behavior
- Documents on same topic

**What it means:**
- If unlabeled point clusters with labeled points, assume same label

#### 3. Manifold Assumption
**Data lies on a low-dimensional manifold**

**Example:**
- Images of faces vary in few ways (pose, lighting)
- High-dimensional data has low intrinsic dimensionality

**What it means:**
- Points close on the manifold should have similar labels
- Even if far in original space

### Main Approaches

### 1. Self-Training (Bootstrap)

**Idea:** Model learns from its own predictions

**Algorithm:**
1. Train model on labeled data
2. Predict labels for unlabeled data
3. Add high-confidence predictions to training set
4. Retrain model
5. Repeat

**Example:**
```
Iteration 0: [100 labeled points]
→ Train model
→ Predict on 1000 unlabeled points
→ Add 50 predictions with confidence > 0.9

Iteration 1: [150 labeled points]
→ Train model
→ Predict on 950 unlabeled points
→ Add 40 more high-confidence predictions
...
```

**Pros:**
- Simple to implement
- Model-agnostic (works with any classifier)

**Cons:**
- Can amplify errors (feedback loop)
- Only helps if initial model is reasonable

### 2. Co-Training

**Idea:** Train multiple models on different "views" of data

**Algorithm:**
1. Split features into two independent views
2. Train model on each view (labeled data only)
3. Each model labels data for the other
4. Retrain with newly labeled data

**Example: Web page classification**
- View 1: Text content
- View 2: Hyperlinks
- Model 1 learns from text, labels based on links for Model 2
- Model 2 learns from links, labels based on text for Model 1

**Requirements:**
- Two conditionally independent views
- Each view sufficient for classification

### 3. Pseudo-Labeling

**Idea:** Treat predicted labels as true labels

**Algorithm:**
1. Train on labeled data
2. Predict all unlabeled data
3. Treat predictions as ground truth
4. Retrain on combined dataset

**Variant: Hard pseudo-labeling**
- Use predicted class directly

**Variant: Soft pseudo-labeling**
- Use predicted probabilities

**Modern approach: FixMatch**
- Only use high-confidence predictions
- Use data augmentation for consistency

### 4. Graph-Based Methods

**Idea:** Propagate labels through a graph

**Setup:**
- Nodes = data points (labeled + unlabeled)
- Edges = similarity between points
- Edge weights = how similar

**Label Propagation:**
1. Build graph from data
2. Initialize: Labeled nodes keep their labels
3. Iteratively: Each node averages neighbors' labels
4. Repeat until convergence

**Formula:**
$$f(x_i) = \frac{\sum_{j} w_{ij} f(x_j)}{\sum_{j} w_{ij}}$$

Label of xᵢ = weighted average of neighbors' labels

**Example:**
```
Labeled:  L1─────L2
           │      │
Unlabeled: U1────U2────U3
                  │
Labeled:         L3
```
U2 gets influenced by L2, L3 based on edge weights.

**Pros:**
- Intuitive
- Non-parametric
- Works well with manifold assumption

**Cons:**
- Requires choosing graph construction
- Doesn't scale well
- Transductive (can't easily label new points)

### 5. Generative Models

**Idea:** Model P(X, Y) jointly

**Approach:**
- Unlabeled data help model P(X)
- Better P(X) → better P(Y|X)

**Example: Semi-supervised Naive Bayes**
1. Use labeled data for P(Y) and P(X|Y)
2. Use all data (labeled + unlabeled) to better estimate P(X|Y)
3. EM algorithm:
   - E-step: Infer labels of unlabeled data
   - M-step: Update parameters with all data

**Example: Semi-supervised GMM**
- Fit GMM to all data (supervised + unsupervised)
- Labeled data guides cluster labels
- Unlabeled data improves cluster shapes

### 6. Consistency Regularization

**Idea:** Model should predict same label for augmented versions of same input

**Method:**
1. Take unlabeled example x
2. Create augmented version x'
3. Penalize if predictions differ: $\text{Loss} = D(f(x), f(x'))$

**Augmentations:**
- Images: rotation, crop, blur
- Text: synonym replacement, back-translation
- Generic: add noise

**Popular methods:**
- **Mean Teacher:** Student learns from teacher's predictions
- **UDA (Unsupervised Data Augmentation):** Consistency with strong augmentation
- **MixUp:** Mix two examples, predict mixed labels

### 7. Contrastive Learning (Modern)

**Idea:** Similar examples should have similar representations

**Method:**
1. Create multiple views of same data
2. Learn representations where same-instance views are close
3. Use these representations for downstream tasks

**Famous methods:**
- **SimCLR:** Contrastive learning for images
- **MoCo:** Momentum contrast
- These are often considered self-supervised (more below)

### Transductive vs Inductive

**Transductive:**
- See all unlabeled test data during training
- Goal: Label these specific unlabeled points
- Example: Graph-based methods

**Inductive:**
- Learn general model
- Can label new unseen data later
- Example: Self-training

### Practical Considerations

#### When to Use
✓ Labeled data is expensive
✓ Unlabeled data is abundant
✓ Assumptions (smoothness, cluster, manifold) hold
✓ Initial supervised model is reasonable

#### When to Avoid
✗ Unlabeled data is from different distribution
✗ Very little labeled data (may not help)
✗ Cheap to get labels
✗ High risk of error propagation

### Common Pitfalls

**1. Confirmation Bias**
- Model reinforces its own mistakes
- Solution: Use ensemble, require high confidence

**2. Distribution Mismatch**
- Unlabeled data from different distribution
- Solution: Check assumptions, weight examples

**3. Poor Initial Model**
- If supervised model is bad, semi-supervised makes it worse
- Solution: Ensure reasonable baseline first

### Evaluation Challenges

**Problem:** How much unlabeled data to use?

**Approach:**
- Learning curves: Plot performance vs. amount of labeled/unlabeled data
- Compare with supervised baseline

**Caveat:**
- Don't use test labels for any decisions
- Proper cross-validation tricky with unlabeled data

### Applications

**1. Web Content Classification**
- Few labeled pages, millions unlabeled
- Co-training on text + links

**2. Medical Image Analysis**
- Expensive to get expert labels
- Lots of unlabeled scans

**3. Speech Recognition**
- Transcription is expensive
- Raw audio is abundant

**4. Natural Language Processing**
- Most text is unlabeled
- Pre-training + fine-tuning paradigm

---

## Self-Supervised Learning

### What is Self-Supervised Learning?

Self-supervised learning creates **supervised tasks from unlabeled data** by using the data itself to generate labels.

**Key idea:** Design a task where labels come "for free" from the data structure.

### Supervised vs Self-Supervised

**Supervised:**
- Data: Images
- Labels: Human annotations (cat, dog, bird)
- Goal: Learn to classify

**Self-Supervised:**
- Data: Images
- Labels: Created automatically (which patch fits where, what's the rotation)
- Goal: Learn useful representations
- Then: Use representations for downstream tasks

### Why Self-Supervised?

**Advantages:**
1. **No expensive labels** - Automatically generated
2. **Unlimited data** - Can use all available data
3. **General representations** - Not specific to one task
4. **Pre-training** - Transfer to various downstream tasks

**Modern success:**
- Powers models like BERT, GPT, CLIP
- State-of-the-art in many domains
- Enables training on massive unlabeled datasets

### Core Principle: Pretext Tasks

A **pretext task** is an artificially created supervised task that helps the model learn useful representations.

**Good pretext tasks:**
- Labels are free/automatic
- Force model to understand data structure
- Transfer well to downstream tasks

### Pretext Tasks for Images

#### 1. Rotation Prediction
**Task:** Predict rotation angle (0°, 90°, 180°, 270°)

**How:**
1. Take image
2. Randomly rotate it
3. Model predicts rotation

**What it learns:**
- Object recognition
- Orientation understanding
- Spatial relationships

#### 2. Jigsaw Puzzle
**Task:** Reassemble shuffled image patches

**How:**
1. Divide image into 3×3 patches
2. Shuffle patches
3. Model predicts correct permutation

**What it learns:**
- Object parts relationships
- Context understanding
- Spatial structure

#### 3. Colorization
**Task:** Predict color of grayscale image

**How:**
1. Convert color image to grayscale
2. Model predicts colors in color space

**What it learns:**
- Object recognition (sky is blue, grass is green)
- Texture understanding
- Semantic knowledge

#### 4. Inpainting
**Task:** Fill in missing regions

**How:**
1. Mask out part of image
2. Model predicts masked content

**What it learns:**
- Context understanding
- Object completion
- Scene understanding

#### 5. Context Prediction
**Task:** Predict spatial relationship between patches

**How:**
1. Take two patches from image
2. Model predicts relative position

**What it learns:**
- Spatial relationships
- Object structure

### Contrastive Learning (Most Popular)

**Core idea:** Similar things should have similar representations, different things should be far apart.

#### SimCLR (Simple Contrastive Learning)

**Method:**
1. Take an image
2. Create two augmented versions (crop, color change, blur)
3. These are "positive pair" (should be similar)
4. Other images are "negative examples" (should be different)
5. Train model so positives are close, negatives are far

**Loss (InfoNCE):**
$$L = -\log \frac{\exp(sim(z_i, z_j)/\tau)}{\sum_{k=1}^{2N} \exp(sim(z_i, z_k)/\tau)}$$

Where:
- zᵢ, zⱼ = representations of positive pair
- sim = similarity (usually cosine)
- τ = temperature
- Sum over all negatives

**Intuition:** 
- Numerator: Make positive pair similar
- Denominator: Push away from negatives

**Key ingredients:**
- Strong data augmentation
- Large batch size (more negatives)
- Projection head
- Temperature parameter

#### MoCo (Momentum Contrast)

**Innovation:** Use a queue of negatives + momentum encoder

**Benefits:**
- Don't need huge batches
- More consistent negatives
- More efficient

#### BYOL (Bootstrap Your Own Latent)

**Surprising twist:** No negative examples needed!

**Method:**
- Two networks: online and target
- Online predicts target's output
- Target is slow-moving average of online

**Why it works:** Still debated, but it does!

### Pretext Tasks for Text

#### 1. Masked Language Modeling (BERT)
**Task:** Predict masked words

**Example:**
- Input: "The cat sat on the [MASK]"
- Target: "mat"

**What it learns:**
- Grammar
- Semantics
- Context understanding

#### 2. Next Sentence Prediction
**Task:** Predict if sentence B follows sentence A

**What it learns:**
- Discourse structure
- Sentence relationships

#### 3. Autoregressive Modeling (GPT)
**Task:** Predict next word

**Example:**
- Context: "The cat sat on the"
- Predict: "mat"

**What it learns:**
- Language generation
- Long-range dependencies

#### 4. Permutation Language Modeling (XLNet)
**Task:** Predict words in random order

**What it learns:**
- Bidirectional context
- Better than masked LM

### Pretext Tasks for Other Domains

**Audio:**
- Predict future frames from past
- Contrastive predictive coding (CPC)

**Video:**
- Predict frame order
- Verify frame rate
- Predict future frames

**Time Series:**
- Forecasting
- Transformation recognition

**Graphs:**
- Predict context (nearby nodes)
- Contrastive methods (GraphCL)

### Using Self-Supervised Models

**Typical workflow:**

**Phase 1: Pre-training (Self-Supervised)**
1. Large unlabeled dataset
2. Solve pretext task
3. Learn representations (encoder)

**Phase 2: Fine-tuning (Supervised)**
1. Small labeled dataset
2. Initialize with pre-trained encoder
3. Add task-specific head
4. Fine-tune on target task

**Phase 3: Evaluation**
- Test on target task

### Linear Evaluation Protocol

**Test:**
- Freeze pre-trained encoder
- Train only linear classifier on top
- Measures quality of representations

**Good representations:**
- High linear evaluation accuracy
- Features are already separable

### Self-Supervised vs Semi-Supervised

| Aspect | Self-Supervised | Semi-Supervised |
|--------|-----------------|-----------------|
| Goal | Learn representations | Improve classifier |
| Labeled data | Not needed for pretext | Some needed |
| Usage | Pre-train then transfer | Train on target directly |
| Flexibility | Very general | Task-specific |

**Relationship:**
- Can combine them!
- Self-supervised pre-training + semi-supervised fine-tuning

### Key Principles for Success

**1. Data Augmentation**
- Critical for contrastive methods
- Must preserve semantic content
- Different augmentations for different domains

**2. Architecture Matters**
- Deeper models often better
- Projection heads help
- Momentum encoders can stabilize

**3. Large Scale**
- More data generally helps
- Bigger batches for contrastive learning
- More compute → better representations

**4. Task Design**
- Pretext task should match eventual use
- Vision: spatial/appearance invariances
- Language: contextual understanding

### Recent Advances

**1. Vision Transformers (ViT) + Self-Supervised**
- MAE (Masked Autoencoders)
- Mask large patches, reconstruct
- Very effective

**2. Multimodal Learning**
- **CLIP:** Match images and text
- Train on image-caption pairs
- Zero-shot transfer

**3. Data2vec**
- Unified framework
- Same algorithm for vision, speech, text

**4. Scaling Laws**
- Bigger models + more data = better
- Self-supervised enables massive scale

### Advantages

✓ No labels needed
✓ Scales to unlimited data
✓ Learns general representations
✓ State-of-the-art performance
✓ Transfers to many tasks

### Disadvantages

✗ Requires large datasets
✗ Computationally expensive
✗ Pretext task design can be tricky
✗ May learn task-specific features
✗ Evaluation can be indirect

### Applications

**1. Computer Vision**
- Image classification
- Object detection
- Segmentation
- Pre-training for all vision tasks

**2. Natural Language Processing**
- BERT, GPT, RoBERTa
- Powers most modern NLP
- Pre-train once, use everywhere

**3. Speech and Audio**
- Wav2vec 2.0
- Low-resource language recognition
- Speaker identification

**4. Medicine**
- Learn from unlabeled medical images
- Transfer to diagnosis tasks

**5. Robotics**
- Learn from robot interactions
- Transfer to control tasks

### Practical Tips

1. **Choose right pretext task** - Match your domain
2. **Use strong augmentation** - Critical for contrastive learning
3. **Scale up** - More data and bigger models help
4. **Longer training** - Self-supervised needs more epochs
5. **Proper evaluation** - Test on multiple downstream tasks
6. **Consider compute** - Pre-training is expensive but reusable

---

## Summary and Connections

### The Big Picture

All these topics connect to help us learn from data, especially when labels are scarce:

**Unsupervised Learning** (no labels)
- Find patterns without guidance
- Clustering, dimensionality reduction

**Probabilistic Models** (principled uncertainty)
- Model data generation process
- Bayesian and MLE learning
- EM for hidden variables

**Mixture Models** (combine simple to model complex)
- GMM uses EM
- Soft clustering
- Density estimation

**Semi-Supervised** (few labels + lots of unlabeled)
- Leverage structure in unlabeled data
- Propagate labels

**Self-Supervised** (create labels automatically)
- Pre-train representations
- Transfer to supervised tasks

### Connections

- **PCA** can initialize **GMM**
- **K-Means** is hard EM for **GMM**
- **EM** used in **Semi-Supervised GMM**
- **Self-Supervised** can help **Semi-Supervised**
- **Bayesian** and **MLE** are different philosophies for all models

### When to Use What?

**No labels at all:**
- Clustering: K-Means or GMM
- Dimensionality Reduction: PCA
- Self-Supervised: Pre-train representations

**Few labels:**
- Semi-Supervised: Use all data
- Self-Supervised + Fine-tune: Often best

**Many labels:**
- Supervised learning (but that's another course!)

**Need probabilities:**
- Probabilistic models: Bayesian or MLE
- GMM for soft assignments

**Hidden structure:**
- EM algorithm
- Latent variable models

---

## Final Tips for Learning

1. **Build intuition first** - Understand concepts before math
2. **Implement from scratch** - Best way to truly understand
3. **Visualize everything** - Plot data, plot results
4. **Start simple** - 2D problems, small datasets
5. **Compare methods** - Try multiple approaches
6. **Read original papers** - See where ideas came from
7. **Practice on real data** - Theory meets reality
8. **Debug systematically** - Check each step
9. **Question assumptions** - When do methods fail?
10. **Teach others** - Best test of understanding

---

Good luck with your studies! These notes cover the fundamentals - now go explore and build amazing things! 🚀
