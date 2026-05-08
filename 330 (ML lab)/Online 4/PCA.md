Below are simulation‑style PCA problems with detailed solutions. They are designed to help you practice the key steps: centering the data, computing the covariance matrix, finding eigenvalues and eigenvectors, and interpreting principal components. Work through each problem step by step.

---

## Problem 1: 2D Data – First Principal Component

You are given four 2‑dimensional data points:  
$$
(2,3),\;(5,4),\;(4,5),\;(1,2)
$$
  

**Tasks:**  
1. Center the data (subtract the mean).  
2. Compute the covariance matrix.  
3. Find the eigenvalues and eigenvectors of the covariance matrix.  
4. Determine the first principal component direction and the variance explained by it.

---

### Solution

#### Step 1: Center the data
Mean of $x$: $\bar{x} = (2+5+4+1)/4 = 12/4 = 3$  
Mean of $y$: $\bar{y} = (3+4+5+2)/4 = 14/4 = 3.5$  

Centered points (subtract mean):  
$$
\begin{aligned}
&(2-3,\;3-3.5) = (-1,\;-0.5) \\
&(5-3,\;4-3.5) = (2,\;0.5) \\
&(4-3,\;5-3.5) = (1,\;1.5) \\
&(1-3,\;2-3.5) = (-2,\;-1.5)
\end{aligned}
$$
  
Let $\mathbf{X}$ be the $4\times 2$ matrix of centered data (rows = points):  
$$
\mathbf{X} = \begin{pmatrix}
-1 & -0.5 \\
 2 &  0.5 \\
 1 &  1.5 \\
-2 & -1.5
\end{pmatrix}
$$

 
#### Step 2: Covariance matrix
$$
\Sigma = \frac{1}{n-1} \mathbf{X}^T \mathbf{X} \quad (\text{sample covariance})
$$
  
First compute $\mathbf{X}^T \mathbf{X}$:  
$$
\mathbf{X}^T \mathbf{X} = \begin{pmatrix}
-1 & 2 & 1 & -2 \\
-0.5 & 0.5 & 1.5 & -1.5
\end{pmatrix}
\begin{pmatrix}
-1 & -0.5 \\
 2 &  0.5 \\
 1 &  1.5 \\
-2 & -1.5
\end{pmatrix}
= \begin{pmatrix}
\sum x_i^2 & \sum x_i y_i \\
\sum x_i y_i & \sum y_i^2
\end{pmatrix}
$$
  
$$
\sum x_i^2 = (-1)^2 + 2^2 + 1^2 + (-2)^2 = 1+4+1+4 = 10
$$
  
$$
\sum y_i^2 = (-0.5)^2 + (0.5)^2 + (1.5)^2 + (-1.5)^2 = 0.25+0.25+2.25+2.25 = 5
$$
  
$$
\sum x_i y_i = (-1)(-0.5) + (2)(0.5) + (1)(1.5) + (-2)(-1.5) = 0.5 + 1 + 1.5 + 3 = 6
$$
  
Thus  
$$
\mathbf{X}^T \mathbf{X} = \begin{pmatrix}10 & 6 \\ 6 & 5\end{pmatrix}
$$
  
Now divide by $n-1 = 3$:  
$$
\Sigma = \frac{1}{3}\begin{pmatrix}10 & 6 \\ 6 & 5\end{pmatrix}
= \begin{pmatrix}
10/3 & 2 \\
2 & 5/3
\end{pmatrix}
\approx \begin{pmatrix}
3.3333 & 2 \\
2 & 1.6667
\end{pmatrix}
$$

 
#### Step 3: Eigenvalues and eigenvectors
Solve $\det(\Sigma - \lambda I)=0$:  
$$
\det\begin{pmatrix}
\frac{10}{3}-\lambda & 2 \\
2 & \frac{5}{3}-\lambda
\end{pmatrix}
= \left(\frac{10}{3}-\lambda\right)\left(\frac{5}{3}-\lambda\right) - 4 = 0
$$
  
Compute:  
$$
\left(\frac{10}{3}-\lambda\right)\left(\frac{5}{3}-\lambda\right) = \lambda^2 - 5\lambda + \frac{50}{9}
$$
  
So  
$$
\lambda^2 - 5\lambda + \frac{50}{9} - 4 = \lambda^2 - 5\lambda + \frac{50}{9} - \frac{36}{9} = \lambda^2 - 5\lambda + \frac{14}{9} = 0
$$
  
Multiply by 9: $9\lambda^2 - 45\lambda + 14 = 0$.  
Discriminant: $45^2 - 4\cdot9\cdot14 = 2025 - 504 = 1521 = 39^2$.  
Thus  
$$
\lambda = \frac{45 \pm 39}{18} \quad\Rightarrow\quad \lambda_1 = \frac{84}{18}= \frac{14}{3}\approx 4.6667,\quad \lambda_2 = \frac{6}{18}= \frac{1}{3}\approx 0.3333
$$
 

**Eigenvector for $\lambda_1 = 14/3$:**  
$$
\begin{pmatrix}
\frac{10}{3}-\frac{14}{3} & 2 \\
2 & \frac{5}{3}-\frac{14}{3}
\end{pmatrix}
\begin{pmatrix}v_1\\v_2\end{pmatrix}
= \begin{pmatrix}
-\frac{4}{3} & 2 \\
2 & -3
\end{pmatrix}
\begin{pmatrix}v_1\\v_2\end{pmatrix}=0
$$
  
From first row: $-\frac{4}{3}v_1 + 2v_2 = 0 \Rightarrow 2v_2 = \frac{4}{3}v_1 \Rightarrow v_2 = \frac{2}{3}v_1$.  
Choose $v_1 = 3$, then $v_2 = 2$. So eigenvector $\mathbf{v}_1 = (3,2)$ (or any multiple).  
Normalize: $\|\mathbf{v}_1\| = \sqrt{9+4}=\sqrt{13}$.  
Unit eigenvector: $\left(\frac{3}{\sqrt{13}},\frac{2}{\sqrt{13}}\right) \approx (0.832,0.555)$.

**Eigenvector for $\lambda_2 = 1/3$:**  
$$
\begin{pmatrix}
\frac{10}{3}-\frac{1}{3} & 2 \\
2 & \frac{5}{3}-\frac{1}{3}
\end{pmatrix}
= \begin{pmatrix}
3 & 2 \\
2 & \frac{4}{3}
\end{pmatrix}
$$
  
First row: $3v_1 + 2v_2 = 0 \Rightarrow v_2 = -\frac{3}{2}v_1$. Choose $v_1=2$, $v_2=-3$.  
Unit eigenvector: $\left(\frac{2}{\sqrt{13}},-\frac{3}{\sqrt{13}}\right) \approx (0.555,-0.832)$.
 
#### Step 4: First principal component and variance explained
The first principal component direction is the eigenvector corresponding to the largest eigenvalue: $\mathbf{v}_1 \approx (0.832,0.555)$.  
Variance explained by PC1:  
$$
\frac{\lambda_1}{\lambda_1+\lambda_2} = \frac{14/3}{14/3 + 1/3} = \frac{14}{15} \approx 0.9333 \; (93.33\%)
$$
  

**Answer:**  
- PC1 direction: $(0.832,0.555)$  
- Variance explained: $93.33\%$

---
 
## Problem 2: 2D Data – Both Principal Components

Consider the following three points:  
$$
(1,2),\;(3,3),\;(5,1)
$$
  

**Tasks:**  
1. Center the data.  
2. Compute the covariance matrix (use $n$ or $n-1$? – assume sample covariance with $n-1$).  
3. Find eigenvalues and eigenvectors.  
4. Write the two principal components as unit vectors.  
5. Compute the proportion of total variance explained by each PC.

---
 
### Solution

#### Step 1: Center the data
$\bar{x} = (1+3+5)/3 = 9/3 = 3$  
$\bar{y} = (2+3+1)/3 = 6/3 = 2$  

Centered points:  
$$
(1-3,2-2)=(-2,0),\quad (3-3,3-2)=(0,1),\quad (5-3,1-2)=(2,-1)
$$
  
Matrix $\mathbf{X}$ (rows):  
$$
\begin{pmatrix}
-2 & 0 \\
 0 & 1 \\
 2 & -1
\end{pmatrix}
$$


#### Step 2: Covariance matrix (sample)
$$
\mathbf{X}^T\mathbf{X} = \begin{pmatrix}
(-2)^2+0^2+2^2 & (-2)(0)+0\cdot1+2(-1) \\
(-2)(0)+0\cdot1+2(-1) & 0^2+1^2+(-1)^2
\end{pmatrix}
= \begin{pmatrix}
4+0+4 & 0+0-2 \\
0+0-2 & 0+1+1
\end{pmatrix}
= \begin{pmatrix}
8 & -2 \\
-2 & 2
\end{pmatrix}
$$
  
Divide by $n-1 = 2$:  
$$
\Sigma = \frac{1}{2}\begin{pmatrix}8 & -2 \\ -2 & 2\end{pmatrix}
= \begin{pmatrix}
4 & -1 \\
-1 & 1
\end{pmatrix}
$$

 
#### Step 3: Eigenvalues and eigenvectors
Characteristic equation:  
$$
\det\begin{pmatrix}
4-\lambda & -1 \\
-1 & 1-\lambda
\end{pmatrix}
= (4-\lambda)(1-\lambda) - 1 = \lambda^2 -5\lambda +4 -1 = \lambda^2 -5\lambda +3 = 0
$$
  
$$
\lambda = \frac{5 \pm \sqrt{25-12}}{2} = \frac{5 \pm \sqrt{13}}{2}
$$
  
So $\lambda_1 = \frac{5+\sqrt{13}}{2} \approx 4.3028$, $\lambda_2 = \frac{5-\sqrt{13}}{2} \approx 0.6972$.

**Eigenvector for $\lambda_1$:**  
$$
\begin{pmatrix}
4-\lambda_1 & -1 \\
-1 & 1-\lambda_1
\end{pmatrix}
\begin{pmatrix}v_1\\v_2\end{pmatrix}=0
$$
  
Using first row: $(4-\lambda_1)v_1 - v_2 = 0 \Rightarrow v_2 = (4-\lambda_1)v_1$.  
Compute $4-\lambda_1 = 4 - \frac{5+\sqrt{13}}{2} = \frac{8-5-\sqrt{13}}{2} = \frac{3-\sqrt{13}}{2} \approx -0.3028$.  
Thus $v_2 \approx -0.3028\,v_1$. Choose $v_1=1$, then $v_2 \approx -0.3028$.  
Normalize: $\|\mathbf{v}_1\| = \sqrt{1 + (0.3028)^2} \approx \sqrt{1.0917}=1.0449$.  
Unit vector: $\left(1/1.0449,\; -0.3028/1.0449\right) \approx (0.9571,\; -0.2898)$.

**Eigenvector for $\lambda_2$:**  
Similarly, from $(4-\lambda_2)v_1 - v_2 = 0$ with $\lambda_2 = \frac{5-\sqrt{13}}{2}$.  
$4-\lambda_2 = 4 - \frac{5-\sqrt{13}}{2} = \frac{8-5+\sqrt{13}}{2} = \frac{3+\sqrt{13}}{2} \approx 3.3028$.  
So $v_2 = (3.3028)v_1$. Choose $v_1=1$, $v_2=3.3028$.  
Norm $\sqrt{1+10.908} \approx \sqrt{11.908}=3.451$.  
Unit vector: $(1/3.451,\;3.3028/3.451) \approx (0.2898,\;0.9571)$.  
Note that this is orthogonal to the first (dot product ≈ 0).
 
#### Step 4: PCs and variance explained
PC1 direction: $(0.9571,\,-0.2898)$  
PC2 direction: $(0.2898,\,0.9571)$  

Total variance = $\lambda_1+\lambda_2 = 5$ (sum of diagonal entries of $\Sigma$ is $4+1=5$, consistent).  
Proportion for PC1: $\lambda_1/5 \approx 4.3028/5 = 0.8606$ (86.06%)  
Proportion for PC2: $\lambda_2/5 \approx 0.6972/5 = 0.1394$ (13.94%)

**Answer:**  
- PC1: $(0.957,-0.290)$, explains 86.06% variance  
- PC2: $(0.290,0.957)$, explains 13.94% variance

---
 
## Problem 3: 3D Data – Covariance and Principal Components (Short)

Suppose you have centered data (already mean‑subtracted) for three points in 3D:  
$$
\mathbf{X} = \begin{pmatrix}
1 & 0 & 2 \\
-1 & 1 & 0 \\
0 & -1 & -2
\end{pmatrix}
$$
  
(rows are points, columns are features).

**Tasks:**  
1. Compute the covariance matrix (use $n-1$).  
2. Without fully solving the cubic, argue how many principal components you would keep if you want to retain 95% of the variance, given that the eigenvalues are $\lambda_1 = 4,\; \lambda_2 = 2,\; \lambda_3 = 0$.  
3. What does the zero eigenvalue indicate about the data?

---
 
### Solution

#### Step 1: Covariance matrix
$$
\mathbf{X}^T\mathbf{X} = \begin{pmatrix}
1 & -1 & 0 \\
0 & 1 & -1 \\
2 & 0 & -2
\end{pmatrix}
\begin{pmatrix}
1 & 0 & 2 \\
-1 & 1 & 0 \\
0 & -1 & -2
\end{pmatrix}
$$
  
Compute each entry:

- (1,1): $1^2 + (-1)^2 + 0^2 = 2$  
- (1,2): $1\cdot0 + (-1)\cdot1 + 0\cdot(-1) = -1$  
- (1,3): $1\cdot2 + (-1)\cdot0 + 0\cdot(-2) = 2$  
- (2,1): same as (1,2) = -1  
- (2,2): $0^2 + 1^2 + (-1)^2 = 2$  
- (2,3): $0\cdot2 + 1\cdot0 + (-1)\cdot(-2) = 2$  
- (3,1): same as (1,3) = 2  
- (3,2): same as (2,3) = 2  
- (3,3): $2^2 + 0^2 + (-2)^2 = 8$

So  
$$
\mathbf{X}^T\mathbf{X} = \begin{pmatrix}
2 & -1 & 2 \\
-1 & 2 & 2 \\
2 & 2 & 8
\end{pmatrix}
$$
  
Divide by $n-1 = 2$:  
$$
\Sigma = \frac{1}{2}\begin{pmatrix}
2 & -1 & 2 \\
-1 & 2 & 2 \\
2 & 2 & 8
\end{pmatrix}
= \begin{pmatrix}
1 & -0.5 & 1 \\
-0.5 & 1 & 1 \\
1 & 1 & 4
\end{pmatrix}
$$
 

#### Step 2: Variance explained with given eigenvalues
Given eigenvalues: $\lambda_1=4,\; \lambda_2=2,\; \lambda_3=0$.  
Total variance = $4+2+0 = 6$.  

Proportion of PC1: $4/6 \approx 66.7\%$  
Cumulative after PC2: $(4+2)/6 = 100\%$.  

To retain 95% variance, we need both PC1 and PC2 (since PC1 alone gives only 66.7%). The third component explains 0% variance and can be dropped.

#### Step 3: Interpretation of zero eigenvalue
A zero eigenvalue means the data lie exactly in a 2‑dimensional subspace of the original 3D space. Here, the three points are coplanar (or actually lie on a 2‑D plane). The third eigenvector corresponds to the direction orthogonal to that plane, and the data have no variation along that direction.

**Answer:**  
- Covariance matrix as above.  
- Keep 2 principal components to exceed 95% variance.  
- Zero eigenvalue indicates the data are perfectly confined to a 2‑D subspace (linear dependency among features).

---
 
## Projection onto Principal Components

Once you have the principal components (eigenvectors), you can **project** the centered data onto the PC space. This transforms your data from the original feature space into the reduced PC space.

### The Projection Formula

Given:
- Centered data matrix $\mathbf{X}$ (shape: $n \times d$, where $n$ = points, $d$ = features)
- Principal component matrix $\mathbf{V}$ (shape: $d \times k$, columns are unit eigenvectors, $k$ = number of PCs to keep)

The projected data (PC scores) is:
$$\mathbf{Z} = \mathbf{X} \mathbf{V}$$

Result: $\mathbf{Z}$ has shape $n \times k$ — each row is a point in PC space.
 
### Example: Project Problem 1 Data

From Problem 1, centered data:
$$\mathbf{X} = \begin{pmatrix}
-1 & -0.5 \\
 2 &  0.5 \\
 1 &  1.5 \\
-2 & -1.5
\end{pmatrix}$$

We found PC1 eigenvector: $\mathbf{v}_1 = (0.832, 0.555)$ (unit vector).

If we project onto **only PC1**, the matrix is:
$$\mathbf{V} = \begin{pmatrix} 0.832 \\ 0.555 \end{pmatrix}$$
(shape: $2 \times 1$)

Projection:
$$\mathbf{Z} = \mathbf{X} \mathbf{V} = \begin{pmatrix}
-1 & -0.5 \\
 2 &  0.5 \\
 1 &  1.5 \\
-2 & -1.5
\end{pmatrix}
\begin{pmatrix} 0.832 \\ 0.555 \end{pmatrix}$$

Compute each row's dot product with $\mathbf{v}_1$:
- Row 1: $(-1)(0.832) + (-0.5)(0.555) = -0.832 - 0.278 = -1.110$  
- Row 2: $(2)(0.832) + (0.5)(0.555) = 1.664 + 0.278 = 1.942$  
- Row 3: $(1)(0.832) + (1.5)(0.555) = 0.832 + 0.833 = 1.665$  
- Row 4: $(-2)(0.832) + (-1.5)(0.555) = -1.664 - 0.833 = -2.497$  

So the projected data (4 points in 1D PC space):
$$\mathbf{Z} = \begin{pmatrix} -1.110 \\ 1.942 \\ 1.665 \\ -2.497 \end{pmatrix}$$

Each value is a **PC score** — the coordinate of that original point along the PC1 direction.
 
### Key Points

- **Projection captures variance along the PC directions.** It tells you where points lie relative to the principal components.
- **If keeping $k < d$ PCs**, you're compressing: $\mathbf{Z}$ is $n \times k$ instead of $n \times d$. You lose variance but reduce dimensions.
- **In practice**: Standardize first (center and scale), compute covariance/correlation, find eigenvectors, then project.

### Why Center Before Projecting?

**Simple answer:** Think of centering as **setting a reference point**.

Imagine you want to measure which direction your data is stretched. If you measure from the original location (off-center), your measurement is off. **Center the data first** = measure from the middle = you get the true pattern.

**Example:** If your data points are at $(1, 2), (3, 4), (5, 6)$ with mean $(3, 4)$:
- **Without centering**: The first principal component points toward the global position $(3, 4)$ — not useful.
- **With centering**: The points become $(-2, -2), (0, 0), (2, 2)$. Now the PC clearly shows the direction they spread: along the line $y = x$.

**Don't worry about losing the mean:** You keep it! When you need the original form back, just add the mean:
$$\text{reconstructed} = \mathbf{Z} \mathbf{V}^T + \text{mean}$$
 
**For training vs. test:**
- Train: center by train mean, compute PCs, project.
- Test: center by **same train mean** (don't recompute), then project.

No information is lost—centering is just a shift that makes PCA work correctly.

---

## Training vs. Testing in PCA

**What are V and Z?**

- **$\mathbf{V}$** = The **eigenvectors** (principal components). These are *learned* during training. Think of them as "directions" you discovered in your training data.
  
- **$\mathbf{Z}$** = The **projected data** (PC scores). These are your data points *expressed in the new PC directions*.

### Training Phase (Learning the Directions)

You have training data $\mathbf{X}_{\text{train}}$ (say, 1000 samples × 10 features).

1. **Compute the mean** of training data: $\mu = \text{mean}(\mathbf{X}_{\text{train}})$
2. **Center the data**: $\mathbf{X}_{\text{centered}} = \mathbf{X}_{\text{train}} - \mu$
3. **Find covariance matrix**: $\Sigma = \frac{1}{n-1} \mathbf{X}_{\text{centered}}^T \mathbf{X}_{\text{centered}}$
4. **Find eigenvectors**: Solve for $\mathbf{V}$ (the directions of max variance)
5. **Project training data**: $\mathbf{Z}_{\text{train}} = \mathbf{X}_{\text{centered}} \mathbf{V}$ (now 1000 samples × fewer dimensions)
6. **Train your model on $\mathbf{Z}_{\text{train}}$** — the reduced-dimensional data (not the original!)
 
**After training, you store:**
- $\mu$ (the training mean)
- $\mathbf{V}$ (the eigenvectors you found)

### Testing Phase (Using the Directions)

You have test data $\mathbf{X}_{\text{test}}$ (say, 200 samples × 10 features).

1. **Center using training mean** (NOT test mean): $\mathbf{X}_{\text{test, centered}} = \mathbf{X}_{\text{test}} - \mu$
2. **Project onto the learned directions**: $\mathbf{Z}_{\text{test}} = \mathbf{X}_{\text{test, centered}} \mathbf{V}$ (now 200 samples × fewer dimensions)
3. **Feed $\mathbf{Z}_{\text{test}}$ to your trained model** — the model expects the same dimensionality and space as training

Now $\mathbf{Z}_{\text{test}}$ has the *same PC space* as $\mathbf{Z}_{\text{train}}$. Your model can make predictions.
 
### Concrete Example

**Training data:** 3 points × 2 features
$$\mathbf{X}_{\text{train}} = \begin{pmatrix} 1 & 2 \\ 3 & 4 \\ 5 & 6 \end{pmatrix}$$

**Step 1: Mean & center**
$$\mu = (3, 4), \quad \mathbf{X}_{\text{centered}} = \begin{pmatrix} -2 & -2 \\ 0 & 0 \\ 2 & 2 \end{pmatrix}$$

**Step 2: Find eigenvectors** (imagine you computed them)
$$\mathbf{V} = \begin{pmatrix} 0.707 \\ 0.707 \end{pmatrix} \quad \text{(first PC, 1D for simplicity)}$$

**After training: Store $\mu = (3, 4)$ and $\mathbf{V}$.**

---
 
**Test data:** 2 new points × 2 features
$$\mathbf{X}_{\text{test}} = \begin{pmatrix} 2 & 3 \\ 4 & 5 \end{pmatrix}$$

**Step 1: Center using training mean** (crucial!)
$$\mathbf{X}_{\text{test, centered}} = \begin{pmatrix} 2 & 3 \\ 4 & 5 \end{pmatrix} - (3, 4) = \begin{pmatrix} -1 & -1 \\ 1 & 1 \end{pmatrix}$$

**Step 2: Project onto $\mathbf{V}$**
$$\mathbf{Z}_{\text{test}} = \begin{pmatrix} -1 & -1 \\ 1 & 1 \end{pmatrix} \begin{pmatrix} 0.707 \\ 0.707 \end{pmatrix} = \begin{pmatrix} -1.414 \\ 1.414 \end{pmatrix}$$

**Result:** Your test points are now in PC space: $(-1.414, 1.414)$ (1D values).

### Why not recompute on test data?

If you recomputed the eigenvectors from test data, you'd get a *different* basis—test points wouldn't be comparable to training points. **You must use the *same* $\mu$ and $\mathbf{V}$ from training.**

---
 
### The Big Picture: Why Compute Eigenvectors?

**You compute eigenvectors specifically to PROJECT and reduce dimensions.**

| Step | What | Why |
|------|------|-----|
| Find $\mathbf{V}$ (eigenvectors) | Directions of max variance | These tell you which directions to compress into |
| Project: $\mathbf{Z}_{\text{train}} = \mathbf{X}_{\text{centered}} \mathbf{V}$ | Transform 1000×10 → 1000×(fewer dims) | **This** is your reduced-dimensional data |
| Train model on $\mathbf{Z}_{\text{train}}$ | Use projected data, NOT original | Fewer features = faster, simpler models |
| Project test: $\mathbf{Z}_{\text{test}} = \mathbf{X}_{\text{test, centered}} \mathbf{V}$ | Same transformation | Keep test data in the same space as training |
| Predict on $\mathbf{Z}_{\text{test}}$ | Use projected test data | Model recognizes it as the same PC space |

**So the eigenvalues and eigenvectors are tools to compress your data before feeding it to your model.**

---

### Do You Get the "Actual" Result?

**Yes.** The model's output (classification, regression, etc.) is your actual result. Projection is just preprocessing.

**Example:**
- Original test data: 200 samples × 10 features
- Project it: 200 samples × 3 PCs (compressed)
- Train a classifier on training PCs → outputs: class labels or probabilities
- Test on test PCs → **these predictions ARE your actual result**

**You lost 7 features, but you only kept 3 PCs that explained 95% of variance. The model still works because the important patterns are preserved.**

---
 
### (Optional) Can You Reconstruct the Original Features?

If you want to reverse the projection (transform back to original 10 features):
$$\mathbf{X}_{\text{reconstructed}} = \mathbf{Z} \mathbf{V}^T + \mu$$

**But:** You only have 3 PCs, so you can only reconstruct along those 3 directions. The 7 dropped dimensions are gone — you get an approximation, not the exact original.

**When to reconstruct:** 
- For visualization
- For anomaly detection (check if reconstruction error is large)
- Usually NOT needed for predictions — the model already works on $\mathbf{Z}$

---

## Practice Tips for Your Test

- **Always start by centering the data.** PCA is sensitive to the mean.  
- Use **sample covariance** (divide by $n-1$) unless the problem explicitly says “population covariance” (divide by $n$).  
- For eigenvalue problems, you may be given a small dataset so that you can compute by hand. Practice solving 2×2 characteristic equations quickly.  
- Remember that **eigenvectors are directions**; unit vectors are the principal components.  
- Variance explained = $\lambda_i / \sum \lambda_j$.  
- In a 30‑minute test, expect a 2D or small 3D dataset. Focus on clear, step‑by‑step calculations.

