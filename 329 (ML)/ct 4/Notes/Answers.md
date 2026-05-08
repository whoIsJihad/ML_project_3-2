# Machine Learning: 20 Answers

## Level 1: Foundational Concepts
1. **Unsupervised vs. Supervised:** Supervised learning uses labeled data (input-output pairs). Unsupervised learning uses data with only features and no corresponding target labels.
2. **Goal of Clustering:** To group similar data points together so that points in the same cluster are more similar to each other than to those in other clusters.
3. **Curse of Dimensionality:** As dimensions increase, data becomes extremely sparse, and distances between points become almost equal. This makes it hard to find patterns and causes models to overfit more easily.
4. **Principal Component:** A Principal Component is a new axis (a linear combination of the original features) that captures the direction of maximum variance in the data.

## Level 2: Algorithm Mechanics
5. **K-Means Steps:**
   1. **Assignment:** Assign each point to the nearest cluster centroid.
   2. **Update:** Recalculate each centroid as the average (mean) of all points assigned to it.
   3. **Check Convergence:** Repeat until centroids stop moving significantly.
6. **EM Algorithm Steps:**
   - **Expectation (E):** "Guess" the hidden labels or responsibilities (the probability that each point belongs to each cluster).
   - **Maximization (M):** Update the model parameters (means, variances, weights) to maximize the likelihood given those guesses.
5. **The Elbow Method:** Plot the Within-Cluster Sum of Squares (WCSS) against the number of clusters $K$. The "elbow" point is where the rate of decrease significantly slows down, suggesting the optimal $K$.![[Pasted image 20260303235514.png]]
8. **PCA Centering:** 
- **Formal Explanation (for Exam):** PCA identifies directions that maximize **variance**. Mathematically, variance is defined as the spread of data points **relative to their mean**. If data is not centered (mean $\neq$ 0), the first Principal Component (PC1) will likely align with the vector pointing from the origin to the data's center, rather than the direction of maximum internal spread. Centering ensures that the resulting components describe the **internal structure and correlations** of the data points, independent of their absolute location in the feature space.
- **Intuition:** Imagine you are measuring the height of 10 skyscrapers. They are all around 500 meters tall, but differ by only a few centimeters. Without centering, PCA will see the number "500" and think the most important thing is "Everything is 500 meters tall." Centering forces PCA to ignore the shared 500m height and focus entirely on the **tiny differences** between the buildings. That is where the real "pattern" is!

## Level 3: Trade-offs and Comparisons
9. **Hard vs. Soft Assignment:** "Hard" assignment (K-Means) assigns a point 100% to one cluster. "Soft" assignment (GMM) gives a probability for each cluster, allowing points to belong partially to multiple groups.
10. **Initialization Sensitivity:** K-Means is sensitive to its starting points. Because it only finds a **local optimum**, starting with "bad" random centroids can lead to a poor final clustering. By running the algorithm multiple times (Random Restarts) and choosing the version with the lowest **Within-Cluster Sum of Squares (WCSS)**, we increase our chances of finding the global optimum (the best possible clustering).
11. **Standardization Significance:** Both K-Means (distance-based) and PCA (variance-based) are sensitive to scale. If one feature has values from 0-1 and another from 0-10,000, the larger feature will dominate the calculations.
12. **SSL Usefulness:** Semi-Supervised Learning is best when labeled data is very expensive or slow to produce (like medical diagnoses) but unlabeled data is cheap and abundant (like raw medical images).

## Level 4: Theoretical Properties & Nuances
13. **Log-Likelihood Choice:** The Likelihood function involves a product of many small probabilities, which can lead to numerical underflow. Logarithms turn products into sums, which are numerically stable and easier to differentiate for optimization.
14. **Chaining Effect:** Single Linkage is most prone to chaining. It merges clusters based on the two closest individual points, potentially "chaining" together two distinct clusters if a thin trail of points lies between them.
15. **MLE vs. MAP:** MLE only considers the observed data. MAP considers both the data *and* a "Prior" (pre-existing belief about the distribution of the parameters) based on domain knowledge.
16. **Orthogonality:** Orthogonal components are mathematically perpendicular (uncorrelated). This ensures that each Principal Component captures unique, non-redundant information.

## Level 5: Application and Complex Integration
17. **SSL with GMM:** In the E-step, the model uses its current parameters to predict labels for the unlabeled data. In the M-step, it treats those predictions as "soft" labels, combined with the true labels of the labeled data, to update its means and variances.
18. **Cluster Geometry (Compass vs. Balloon):**
- **Formal Explanation:** K-Means uses Euclidean distance, which mathematically assumes clusters are **spherical (circular)** and equal in size. If a cluster is elongated (elliptical), K-Means will fail to capture its true shape and often "splits" it incorrectly. GMM solves this using the **Covariance** parameter, which models the spread and orientation of each cluster, allowing it to fit any elliptical shape.
- **Intuition:** Think of **K-Means** as a **Compass**. It can only draw perfect circles. If your data cluster is shaped like a long cigar, a circle won't fit it. Think of **GMM** as a **Balloon**. The **Covariance** parameter allows the balloon to "stretch" (become long) and "tilt" (rotate) to perfectly fit the shape of the data, no matter how elongated it is.
19. **Co-training Views:** 1) Each view must be sufficient to train a good classifier on its own. 2) The two views must be conditionally independent (meaning they don't share information that isn't related to the class label).
20. **Intrinsic Dimensionality:** It tells you that although the data is represented in 100 dimensions, its "true" or intrinsic dimensionality is likely 2. The remaining 98 dimensions are mostly noise or redundant information.
