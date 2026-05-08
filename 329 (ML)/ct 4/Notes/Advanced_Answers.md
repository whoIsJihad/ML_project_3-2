# Machine Learning: 20 Advanced Answers

## Level 6: Deep Dives into Clustering & GMM
21. **Geometric Challenges:** K-Means assumes all clusters are spherical and equal in density. It would "cut" the ellipse in half or expand into the sparse circle’s space to try and make equal-sized spheres. GMM uses **Covariance** matrices to allow the ellipse to have its own orientation/length and **Mixing Weights** to account for different densities, fitting each cluster exactly as it is.
22. **Degeneracy:** If a Gaussian’s variance shrinks to zero to fit one point perfectly, its probability density at that point goes to infinity, making the Likelihood also infinite. This breaks the optimization. To prevent this, we add a tiny constant (regularization) to the diagonal of the **Covariance Matrix** so the variance never hits zero.
23. **Local vs. Global Maxima:** EM starts from a random point and "climbs the hill" of the likelihood function to the nearest peak. This peak might not be the highest one in the "mountain range" (global maximum). To fix this, we use **Multiple Random Restarts** (running the model several times) or use a smart initialization like **K-Means++**.
24. **Linkage Trade-offs:** **Single Linkage** (closest points) can merge very different clusters if a thin "bridge" of points connects them (Chaining). **Complete Linkage** (farthest points) forces clusters to be compact and similar in size, but it is extremely sensitive to **outliers**, as one far-away point can drastically increase the "distance" between two clusters.

## Level 7: Dimensionality Reduction & PCA Nuances
25. **PCA vs. Information Loss:** Yes. Imagine two clouds of points, "Class A" and "Class B," stacked vertically. The direction of maximum variance is horizontal. If you project onto that horizontal axis (PCA), both classes overlap completely, and you lose all ability to distinguish between them. PCA is "label-blind."
26. **High-Dimensional Distance:** In high dimensions, points become sparse. The distance between any two points starts to converge to the same value. K-Means (which relies on Euclidean distance) fails because it can no longer determine if a point is "significantly" closer to Centroid A than Centroid B—they all start to look equally far away.
27. **Reconstruction Error:** Reconstruction is the attempt to map the 10D projection back to the original 100D space. Because 90 dimensions were discarded, the reconstructed points won't match the originals perfectly. The "Reconstruction Error" measures the sum of the variance that was discarded during the reduction.
28. **Kernel PCA:** **Exam-ready answer (short, no formulas):**

	The kernel trick in PCA allows us to implicitly map data into a higher-dimensional space where nonlinear patterns become linear.
	
	We move data to a higher dimension because some structures (like curves or circles) cannot be captured by straight lines in the original space. In a higher-dimensional space, those curved patterns may become linear, making PCA able to detect meaningful directions of variation.
	
	The “trick” is that we do not actually compute the high-dimensional coordinates. Instead, we compute similarities between points as if they were mapped there, which makes the method computationally efficient.
	
	So, we temporarily go to a higher dimension to reveal hidden structure, then reduce back down to a lower dimension.

## Level 8: Probabilistic Learning & Inference
29. **Zero Frequency Problem:** If a word has zero probability, the entire likelihood product for that document becomes zero, regardless of other evidence. This is "Zero-frequency bias." **Laplace Smoothing** fixes this by adding 1 to every count (a Bayesian "Uniform Prior"), ensuring every outcome has at least a tiny probability.
30. **MAP as Regularizer:** In MAP, we add a "Prior" on the parameters. If we choose a Gaussian prior centered at zero, we are telling the model: "I prefer smaller weights unless the data strongly says otherwise." This is mathematically identical to **L2 (Ridge) Regularization**, where we penalize large parameter values to prevent overfitting.
31. **Generative vs. Discriminative:** A generative model (GMM) learns the joint probability $P(X, Y)$, meaning it learns "what each class looks like" so it can generate new samples. A discriminative model (K-Means/Logistic Regression) only learns $P(Y|X)$, meaning it only learns "where the boundary is" between classes.
32. **Sequential Bayesian Updating:** In Bayes' rule, the Posterior depends on the Prior and the Likelihood. When a new data batch arrives, we take our "old" Posterior (what we learned from batch 1) and use it as the "new" Prior for batch 2. This allows models to learn incrementally without needing to re-process all old data.

## Level 9: Semi-Supervised Learning (SSL) Logic
33. **Confirmation Bias:** If the model incorrectly labels an unlabeled point with high confidence, that point (and its error) is added to the training set. The model then retrains on its own mistake, becoming *even more* confident in its error. This "feedback loop" can lead to "model drift" away from the true decision boundary.
34. **Manifold Assumption:** This assumes that high-dimensional data actually lives on a simpler, lower-dimensional structure. A crumpled 2D paper in 3D space looks 3D, but it’s actually a 2D sheet. Algorithms like **Graph-based SSL** use this to "unroll" the paper and find labels by following the surface of the sheet rather than taking a shortcut through empty 3D space.
35. **Co-training Independence:** If the views are highly correlated, they are basically the same view. Model A will only confirm what Model B already knows, and neither will provide "new" informative labels to the other. The learning process will stall and fail to benefit from the unlabeled data.
36. **Consistency Regularization:** The logic is that the "identity" of an object is invariant to small perturbations. If a model changes its prediction just because we rotated the image by 5 degrees, it hasn't learned the "essence" of the object. SSL uses this to force the model to have a "smooth" decision boundary across the unlabeled data.

## Level 10: Model Selection & Evaluation
37. **BIC and Penalty:** As you add more clusters (K), the Likelihood will always increase because you have more parameters to "memorize" the data. **BIC** adds a penalty term based on the number of parameters and the size of the dataset. This prevents overfitting by choosing a simpler model unless the extra cluster provides a *massive* boost in fit.
38. **Standardization in PCA:** The first Principal Component will align almost perfectly with **Income**. Because PCA looks for maximum variance, and Income varies by millions while Age only varies by 100, the Income axis "looks" much larger to the algorithm. PCA will ignore Age entirely unless both are scaled to have a mean of 0 and variance of 1.
39. **Interpretability:** Principal Components are "mixtures" of all original features. PC1 might be `0.5*Age + 0.3*Income - 0.2*Height`. While this axis captures the most variance, it doesn't represent a single physical trait, making it hard to explain *why* a specific data point has a high value on that component.
40. **Active vs. SSL:** SSL is "passive"—it takes whatever unlabeled data is available and tries to find patterns. **Active Learning** is "proactive"—it identifies the specific unlabeled points that it is most confused about (e.g., points near the decision boundary) and asks a human to provide labels for *only those points* to maximize learning efficiency.
