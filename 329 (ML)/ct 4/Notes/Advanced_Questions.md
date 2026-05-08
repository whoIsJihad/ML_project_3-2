# Machine Learning: 20 Advanced Conceptual Questions

## Level 6: Deep Dives into Clustering & GMM
21. **K-Means vs. GMM Geometric Assumptions:** Describe a scenario where a dataset has three clusters: one is a small tight circle, one is a large sparse circle, and one is a long thin ellipse. Explain why K-Means would struggle with this dataset and how GMM’s components (specifically weights and covariance) would resolve it.
22. **The Degeneracy Problem in GMM:** In a Gaussian Mixture Model, what happens if one Gaussian component "collapses" onto a single data point? Explain why this leads to an infinite likelihood problem and how we typically prevent it in practice.
23. **EM Convergence and Local Optima:** The EM algorithm is guaranteed to increase the log-likelihood at every step. However, this does not guarantee finding the "best" model. Explain the difference between local and global maxima in the context of EM and discuss two strategies for increasing the chance of finding the global maximum.
24. **Linkage Trade-offs in Hierarchical Clustering:** Compare and contrast "Single Linkage" and "Complete Linkage." In your answer, explain which is more robust to noise and which is more likely to create "compact" clusters, and why.

## Level 7: Dimensionality Reduction & PCA Nuances
25. **PCA vs. Information Loss:** PCA finds directions of maximum variance. Is it possible for the direction of maximum variance to contain *zero* useful information for a classification task? Provide a conceptual example.
26. **The "Curse of Dimensionality" in Clustering:** Explain why distance-based algorithms like K-Means become less effective as the number of features increases toward infinity. How does the ratio between the "nearest" and "farthest" neighbor change in high dimensions?
27. **PCA Reconstruction Error:** Explain the concept of "reconstruction error" in PCA. If you reduce a 100-dimensional dataset to 10 dimensions, how do you conceptually "reconstruct" the original data, and what is physically lost in the process?
28. **Kernel PCA Intuition:** Without using formulas, explain the "Kernel Trick" in the context of PCA. Why would we want to move data into a *higher* dimensional space before reducing it to a lower one?

## Level 8: Probabilistic Learning & Inference
29. **MLE and the "Zero Frequency" Problem:** In a categorical model (like a Naive Bayes spam filter), if a specific word never appears in the training data for "Spam," MLE will assign it a probability of zero. Explain why this is dangerous for future predictions and how "Smoothing" (a Bayesian idea) fixes this.
30. **MAP as a Regularizer:** Explain how Maximum A Posteriori (MAP) estimation acts as a bridge between MLE and Regularization (like L2/Ridge). How does changing the "strength" of our Prior belief affect the model’s complexity?
31. **Generative vs. Discriminative Models:** GMM is a generative model, while K-Means is often seen as a discriminative clustering approach. Explain the fundamental difference in how a generative model "views" the data creation process compared to a discriminative one.
32. **Sequential Bayesian Updating:** Describe the process of "Sequential Updating" in Bayesian Learning. How does the "Posterior" of today become the "Prior" of tomorrow, and why is this useful for real-time data streams?

## Level 9: Semi-Supervised Learning (SSL) Logic
33. **The Self-Training Feedback Loop:** In Self-Training (Pseudo-labeling), a model labels its own unlabeled data. Explain the "Confirmation Bias" or "Drift" problem—what happens if the model makes a confident but incorrect prediction early on?
34. **The Manifold Assumption:** Many SSL and Dimensionality Reduction algorithms rely on the "Manifold Assumption." Explain this concept using the analogy of a crumpled piece of paper in 3D space.
35. **Co-training Independence Assumption:** Co-training requires two "views" of the data that are conditionally independent. Explain what happens to the learning process if these two views are actually highly correlated (e.g., they both provide the same information).
36. **Consistency Regularization:** Modern SSL uses "Consistency Regularization." Explain the logic: why should a model’s prediction for an image of a cat remain the same even if we rotate, blur, or add noise to that image?

## Level 10: Model Selection & Evaluation
37. **BIC vs. AIC for GMM:** When choosing the number of clusters ($K$) for a GMM, we often use BIC (Bayesian Information Criterion) instead of just checking the Likelihood. Why do we need to "penalize" the model for having more components?
38. **Standardization in PCA:** If you have two features, "Age" (0–100) and "Income" (0–1,000,000), and you perform PCA without standardizing, which feature will the first Principal Component align with? Explain the "geometric" reason why.
39. **Interpretability of Principal Components:** Why are the new features created by PCA (the components) often harder for humans to interpret than the original features?
40. **Active Learning vs. Semi-Supervised Learning:** Both approaches deal with unlabeled data. Explain the conceptual difference between a model "using" unlabeled data (SSL) versus a model "asking" for specific labels (Active Learning).
