# 📘 K-Means Clustering

## 1. Core Idea (Intuition)

**Goal:** Partition data into $K$ clusters (unknown labels).

**K-means approach:** Minimize **within-cluster variance** (points close to their cluster center).

**Key insight:** Iteratively assign points to nearest center, then recompute centers.

---

## 2. Objective Function

$$J = \sum_{i=1}^{n} \sum_{k=1}^{K} r_{ik} \| x_i - \mu_k \|^2$$

where:
- $r_{ik} = 1$ if point $i$ assigned to cluster $k$, else 0
- $\mu_k$: center of cluster $k$
- Sum of squared distances from points to their cluster center

**Goal:** Minimize $J$.

---

## 3. K-Means Algorithm

```
Initialize μ_1, μ_2, ..., μ_K (e.g., random points or K++ initialization)

For iteration t = 1, 2, ...:
  
  === Assignment Step ===
  For each point x_i:
    r_ik = 1 if k = argmin_k || x_i - μ_k ||²
    (assign to nearest center)
  
  === Update Step ===
  For each cluster k:
    μ_k = (1/N_k) Σ_i r_ik * x_i
    (center = mean of assigned points)
  
  If converged, return clusters
```

---

## 4. Convergence

**Theorem:** K-means converges in finite steps.

**Proof idea:**
- Assignment step: decreases (or keeps same) objective $J$
- Update step: decreases objective $J$ (optimal center is mean)
- Both decrease; finite states; must terminate

**In practice:** 10-100 iterations typical.

---

## 5. Initialization

### Random Initialization
Pick $K$ points randomly. **Problem:** May converge to bad local optimum.

### K-Means++ Initialization
1. Pick first center randomly
2. For remaining $K-1$ centers:
   - Pick point $x$ with probability proportional to $\min_k \|x - \mu_k\|^2$
   - (favors distant points; spreads out clusters)

**Effect:** Better initial clustering; often converges to better solution.

---

## 6. Choosing $K$

| Method | How |
|--------|-----|
| **Elbow method** | Plot $J$ vs. $K$; pick "elbow" (diminishing returns) |
| **Silhouette score** | Measure cluster tightness and separation |
| **Domain knowledge** | How many clusters make sense? |

---

## 7. Failure Cases / Limitations

| Problem | Why | Impact |
|---------|-----|--------|
| **Local optima** | Non-convex; initialization matters | Use K-means++ or multiple restarts |
| **Spherical clusters only** | Minimizes Euclidean distance | Fails on elongated clusters |
| **Outliers** | Mean affected by extreme points | Use K-medians or robust variants |
| **Hard assignment** | No uncertainty | Use GMM for soft clustering |

---

## 8. Complexity

- **Each iteration:** $O(nKd)$ (compute distance to each of $K$ centers for $n$ points in dimension $d$)
- **Total:** $O(nKdt)$ where $t$ is number of iterations

**Efficiency:** Linear in $n$; scales well to large datasets.

---

## 9. Applications

- **Image compression:** Reduce color palette (each pixel to nearest cluster center)
- **Customer segmentation:** Group customers by behavior
- **Document clustering:** Group documents by topic (before deep learning)
- **Dimensionality reduction:** K-means on high-dim data as preprocessing

---

## 10. Variants

| Variant | Change |
|---------|--------|
| **K-Medians** | Use median instead of mean; robust to outliers |
| **K-Medoids** | Use actual points as centers (not means) |
| **Mini-batch K-means** | Subsample for faster iteration |

---

## 11. K-Means vs. Alternatives

| Method | Soft/Hard | Scalable | Clusters | When Use |
|--------|----------|----------|----------|----------|
| **K-means** | Hard | Yes | Spherical | Quick baseline, large data |
| **GMM** | Soft | No | Ellipsoidal | Probability, small data |
| **Hierarchical** | No | No | Dendrogram | Interpretability, small data |
| **DBSCAN** | No | Partial | Arbitrary | Density-based, noise robust |

---

## 12. Exam Questions

### Conceptual
1. What does K-means minimize? Explain the objective function.
2. Why does K-means converge in finite steps?
3. What is K-means++ initialization? Why is it better?

### Practical
1. Apply K-means to 2D data (3 points, 2 clusters). Compute first iteration.
2. How to choose $K$? Compare elbow method vs. silhouette score.

### Trick Cases
1. K-means on elongated cluster. Why does it fail?
2. Outlier point far away. How does it affect center?

---

## 13. Key Takeaways

- **Objective:** Minimize within-cluster variance $J = \sum_i \sum_k r_{ik} \|x_i - \mu_k\|^2$
- **Algorithm:** Assignment (nearest center) + Update (mean)
- **Convergence:** Finite steps; converges to local optimum
- **K-means++:** Smart initialization; better final solution
- **Choosing K:** Elbow method, silhouette score, domain knowledge
- **Complexity:** $O(nKdt)$ per restart; scales well
- **Limitations:** Hard assignment, spherical clusters, sensitive to outliers
- **Modern alternatives:** DBSCAN (density), GMM (probabilistic), deep clustering

---
