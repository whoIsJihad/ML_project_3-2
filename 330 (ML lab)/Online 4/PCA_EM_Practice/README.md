# PCA & EM Preparation Guide

Your test prep package includes these files:

## 1. **patterns_reference.py** 📚
Start here. Shows all key syntax & operations:
- Data centering, covariance matrices
- Eigendecomposition and sorting
- Projections, L responsibilities, M-step updates
- Sklearn equivalents (reference only)

**What you'll learn**: syntax patterns + expected shapes/return types

---

## 2. **pca_numpy.py** 🔧
Implement PCA from scratch (uncomment TODOs):
- `__init__`: Initialize attributes
- `fit()`: Covariance → eigendecomposition → select components
- `transform()`: Project data onto components
- `fit_transform()`: Convenience method

**Why this matters**: 
- Tests often ask: "compute PCA, project to 2D, return shape"
- You'll encounter eigendecomposition and matrix multiplication​
- Need to understand: centering, eigenvector selection, projection

**Tips**:
- Run `python pca_numpy.py` to test your implementation
- Check output shapes at each step
- Common mistake: forgetting to center data before covariance

---

## 3. **em_gmm_numpy.py** 🎲
Implement EM algorithm (Gaussian Mixture Model):
- `_initialize()`: Random component initialization
- `_e_step()`: Compute responsibilities (likelihoods × weights, then normalize)
- `_m_step()`: Update means, covariances, weights based on responsibilities
- `fit()`: Loop E-step → M-step until convergence
- `predict()`: Assign samples to best component

**Why this matters**:
- Tests ask: "Implement E-step", "update means", "compute responsibilities"
- Need to handle 3D arrays (covariances for all components)
- Broadcasting is critical for efficiency

**Tips**:
- E-step: likelihood (shape: n_samples × n_components) → responsibilities (same shape)
- M-step: use responsibilities to weight samples when computing new parameters
- Common mistake: forgetting to normalize responsibilities (rows should sum to 1)

---

## 4. **challenges.py** ⚡
Short, focused coding challenges (test-like):
1. **Variance explained**: Compute & normalize eigenvalues
2. **Projection shape**: (n, 20) data, (20, 5) components → (n, 5) output
3. **Responsibility matrix**: Create & normalize
4. **Weighted mean**: Key M-step operation
5. **Weighted covariance**: More complex M-step
6. **Loop pattern**: Update all K components
7. **Convergence check**: Compare log-likelihoods

**How to use**: Solve each in ~5 min. These are test-like problems.

---

## Study Strategy

### Day 1-2: Understand Patterns
- Read `patterns_reference.py` line-by-line
- Run it, understand output shapes
- Note key operations: `np.linalg.eig()`, `multivariate_normal.pdf()`, broadcasting

### Day 3: Implement PCA
- Work through `pca_numpy.py` step-by-step
- Fill in each TODO, test with `python pca_numpy.py`
- Understand why each step is needed

### Day 4: Implement EM
- Work through `em_gmm_numpy.py` step-by-step
- Start with E-step (easier), then M-step (trickier)
- Test convergence on synthetic data

### Day 5: Speed & Accuracy
- Solve `challenges.py` problems in 5-10 min each
- Time yourself—test will be ~2-3 hours
- Look for patterns: which operations appear most?

---

## Key Concepts Checklist

### PCA
- [ ] Data centering (subtract mean)
- [ ] Covariance matrix computation
- [ ] Eigendecomposition (eig vs eigh)
- [ ] Sorting eigenvalues (descending)
- [ ] Component selection (top-k eigenvectors)
- [ ] Projection via matrix multiplication
- [ ] Explained variance ratio (eigenvalues / sum)

### EM / GMM
- [ ] Initialize means, covariances, weights
- [ ] Multivariate Gaussian likelihood
- [ ] Responsibility computation (weighted likelihood / normalize)
- [ ] Update mean (weighted average)
- [ ] Update covariance (weighted outer products)
- [ ] Update weight (fraction of data assigned to component)
- [ ] Convergence (log-likelihood threshold)
- [ ] Prediction (argmax responsibility)

---

## Test Tips

1. **Shape debugging**: Print shapes at each step. Matrix dim mismatches cause 50% of errors.
2. **Normalization**: Check if values should sum to 1 (responsibilities, weights).
3. **Centering**: Always center before covariance/PCA. Easy to forget.
4. **Broadcasting**: Use `[:, np.newaxis]` to reshape (n,) → (n, 1) for multiplication.
5. **Eigendecomposition order**: `eig()` returns unsorted. Must sort by magnitude.
6. **Covariance symmetry**: Result should be symmetric. If not, you made a math error.

---

## Common Errors & Fixes

| Error | Cause | Fix |
|-------|-------|-----|
| `ValueError: shapes not aligned` | Wrong matrix dims | Print shapes before `@` |
| Responsibilities don't sum to 1 | Forgot normalization | Divide by row sum |
| Low explained variance | Didn't sort eigenvalues | Use `argsort()` with `[::-1]` |
| EM doesn't converge | Poor initialization | Use k-means++ or random seed |
| Covariance singular/NaN | Division by zero | Check Nk > 0 for each component |

---

Good luck! 🚀
