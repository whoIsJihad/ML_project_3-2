# Machine Learning: 20 Questions (No Derivations)

## Level 1: Foundational Concepts
1. **Unsupervised Learning:** What is the primary difference between Supervised and Unsupervised Learning regarding the data used?
2. **Clustering:** What is the fundamental goal of any clustering algorithm?
3. **Dimensionality Reduction:** Briefly explain the "Curse of Dimensionality" and why it is a problem for machine learning models.
4. **PCA Basics:** In Principal Component Analysis (PCA), what does a "Principal Component" represent?

## Level 2: Algorithm Mechanics
5. **K-Means Steps:** List the three iterative steps of the K-Means algorithm after initialization.
6. **EM Algorithm:** What do the "E" and "M" stand for in the EM algorithm, and what is the high-level task of each step?
7. **The Elbow Method:** How do you use the "Elbow Method" to determine the optimal number of clusters ($K$) for K-Means?
8. **PCA Process:** Why must we center the data (subtract the mean) before performing PCA?

## Level 3: Trade-offs and Comparisons
9. **K-Means vs. GMM:** Explain the difference between "Hard" and "Soft" cluster assignments. Which algorithm uses which?
10. **Initialization:** Why is it common practice to run the K-Means algorithm multiple times with different random initializations instead of just once?
11. **Standardization:** Why is it critical to scale or standardize features before performing PCA or K-Means?
12. **Semi-Supervised Learning (SSL):** Under what real-world circumstances is Semi-Supervised Learning more useful than standard Supervised Learning?

## Level 4: Theoretical Properties & Nuances
13. **Log-Likelihood:** In Maximum Likelihood Estimation (MLE), why do we maximize the *Log*-Likelihood instead of the raw Likelihood?
14. **Hierarchical Linkage:** Which linkage method in Hierarchical Clustering is most susceptible to the "Chaining" effect, and what does this look like?
15. **MLE vs. MAP:** Conceptually, what extra information does a Maximum A Posteriori (MAP) estimate consider that Maximum Likelihood Estimation (MLE) ignores?
16. **Orthogonality:** What does it mean for Principal Components to be "orthogonal," and why is this property useful?

## Level 5: Application and Complex Integration
17. **SSL with GMM:** Describe how the EM algorithm incorporates unlabeled data to improve a Gaussian Mixture Model in a semi-supervised setting.
18. **Cluster Geometry:** If a dataset contains elongated, elliptical clusters, why will K-Means likely perform poorly, and how does GMM's "Covariance" parameter address this?
19. **Co-training Requirements:** In the Co-training method for Semi-Supervised Learning, what are the two specific requirements for the "views" (feature sets) of the data?
20. **Interpreting PCA:** If your first two Principal Components explain 98% of the total variance in a 100-dimensional dataset, what does this tell you about the "Intrinsic Dimensionality" of your data?
