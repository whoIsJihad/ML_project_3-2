# NumPy Slicing & Indexing — Detailed Guide (for C++ programmers)

**Overview**
- **Purpose:** Explain NumPy indexing and slicing clearly, with many examples and comparisons to C/C++ array access, targeted at non-expert Python users.
- **Audience:** Programmers familiar with C/C++ arrays and pointers who need to understand NumPy's memory model, indexing semantics, views vs. copies, and common patterns.

**Quick note about terminology**
- **Array / ndarray:** Use `ndarray` or `array` to mean a NumPy n-dimensional array.
- **View:** A new Python `ndarray` object that shares the same memory buffer as the original — changes to one may reflect in the other.
- **Copy:** A new `ndarray` with its own memory buffer; changes do not affect the other.

**1. Basic 1D indexing and slicing (familiar ground)**
- Access elements by integer index like C++: `a[2]` (0-based).
- Negative indices count from the end: `a[-1]` is the last element.

Examples:
```python
import numpy as np
a = np.array([10, 20, 30, 40, 50])
print(a[0])   # 10
print(a[-1])  # 50
```

- Slicing syntax is `a[start:stop:step]` (like Python lists). `start` inclusive, `stop` exclusive.
- Omitting an index uses defaults: `start=0`, `stop=len(a)`, `step=1`.

Examples:
```python
print(a[1:4])     # [20 30 40] (elements at indices 1,2,3)
print(a[:3])      # [10 20 30]
print(a[3:])      # [40 50]
print(a[::2])     # [10 30 50] (every 2nd element)
print(a[::-1])    # [50 40 30 20 10] (reversed)
```

**Key difference vs C++**: slices return views (not copies) when possible — modifying a slice may modify the original array (see section 3).

**2. Multi-dimensional indexing**
- For a 2D array `A`, use `A[i, j]` to access the element at row `i` and column `j` (similar to `A[i][j]` but faster and more direct).

Example:
```python
A = np.array([[1,2,3],[4,5,6],[7,8,9]])
print(A[1,2])    # 6 (row 1, col 2)
# Equivalent (but slightly slower): A[1][2]
```

- Slicing across axes uses commas: `A[row_slice, col_slice]`.

Examples:
```python
print(A[0:2, 1:3])  # rows 0..1, cols 1..2 -> [[2,3],[5,6]]
print(A[:, 0])      # all rows, column 0 -> [1,4,7]
print(A[1, :])      # row 1 -> [4,5,6]
```

**3. Views vs Copies (crucial)**
- Most slicing operations return a **view** (a window into the same memory). Assignment to the view affects the original array.

Example (1D):
```python
x = np.arange(6)      # [0 1 2 3 4 5]
s = x[2:5]            # view referencing x's memory
s[0] = 99
print(x)              # [ 0  1 99  3  4  5]  <- x changed
```

Example (2D):
```python
B = np.arange(9).reshape(3,3)
sub = B[0:2, 0:2]
sub[:] = -1
print(B)
# [[-1 -1  2]
#  [-1 -1  5]
#  [ 6  7  8]]  <- B changed in the slice region
```

- When does NumPy return a copy instead of a view? Common cases:
  - Using non-contiguous slicing with steps that break memory layout (e.g., `a[::-1]` often returns a view, but some advanced operations return copies).
  - Fancy indexing (integer array indexing) and boolean indexing always return a copy.

**4. Fancy indexing (integer array indexing)**
- Use integer arrays to pick arbitrary elements: `a[[2,0,3]]`.
- Important: fancy indexing always returns a copy (not a view).

Example:
```python
a = np.array([10,20,30,40,50])
sel = a[[3,1,4]]
sel[0] = 999
print(a)   # original unchanged
```

- For 2D arrays, you can index rows and columns with integer arrays: `A[[0,2],[1,2]]` picks elements `(0,1)` and `(2,2)` (pairwise).
- To get the Cartesian product (all combinations), use `np.ix_()`:
```python
rows = np.array([0,2])
cols = np.array([1,2])
print(A[np.ix_(rows, cols)])  # submatrix with rows 0,2 and cols 1,2
```

**5. Boolean indexing (masking)**
- Create a boolean mask of same shape and use it to select elements. Result is a 1D copy of selected elements.

Example:
```python
x = np.array([1,2,3,4,5])
mask = x % 2 == 0  # [False, True, False, True, False]
print(x[mask])     # [2 4]
# assignment to masked positions
x[mask] = -1
print(x)           # [ 1 -1  3 -1  5]
```

**6. Combining indexing types**
- You can mix slices, integer arrays, and masks: `A[mask, 2]` or `A[1:3, [0,2]]`.
- Be mindful: if you use fancy indexing anywhere in the indexing expression, the result is a copy.

Example:
```python
A = np.arange(12).reshape(3,4)
# slice rows 0:2, pick columns 1 and 3 -> copy because of fancy indexing
res = A[0:2, [1,3]]
```

**7. Assignment with fancy indexing and masks**
- Fancy indexing yields a copy, so assignment via fancy indexing works differently. For assignment to original array, use `np.put_along_axis` or mask-based assignment.

Example (mask assignment preferred):
```python
A = np.arange(6)
mask = A % 2 == 0
A[mask] = -100  # correct: writes back to original where mask True
```

Example (danger with fancy indexing):
```python
idx = np.array([0,1,2])
b = A[idx]
b[:] = 0
# A unchanged because b is a copy
```

**8. Advanced slicing features**
- `Ellipsis` (`...`) matches full slices on remaining axes: `A[0,...]` equals `A[0,:,:,...]` depending on ndim.
- `np.newaxis` (or `None`) adds an axis: `a[np.newaxis, :]` changes shape from `(N,)` to `(1,N)`; useful for broadcasting.

Examples:
```python
C = np.ones((4,5))
print(C[0,...].shape)        # (5,)
v = np.array([1,2,3])
print(v[np.newaxis, :].shape) # (1,3)
print(v[:, np.newaxis].shape) # (3,1)
```

**9. Slice objects and `slice()` constructor**
- `a[2:10:2]` is syntactic sugar for `a[slice(2,10,2)]`. Useful when building indices programmatically.

Example:
```python
s = slice(2, None, -1)
print(a[s])
```

**10. Performance considerations & memory layout**
- NumPy arrays have `dtype`, `shape`, and `strides`. `strides` describe how many bytes to skip to move by one index in each dimension.
- Views share the same buffer but may have different `shape` and `strides`.
- Contiguous arrays (C-order) are faster for many operations. Use `.copy()` to force a contiguous copy when needed: `b = a.copy()`.

Check properties:
```python
print(a.flags)     # shows C_CONTIGUOUS, F_CONTIGUOUS, etc.
print(a.strides)
```

**11. Useful helper functions**
- `np.take(a, indices, axis=...)` — like fancy indexing but with options for out-of-bounds behavior.
- `np.put(a, indices, values)` — write into flattened array (use with care).
- `np.where(condition, x, y)` — choose elements from `x` or `y` depending on `condition`.
- `np.nonzero(a)` or `np.where(a)` — indices of non-zero/True elements.

Examples:
```python
vals = np.array([10,20,30,40])
print(np.take(vals, [3,0]))
```

**12. Common idioms and examples**
- Reverse rows in a 2D array:
```python
A = np.arange(12).reshape(3,4)
A_rev_rows = A[::-1, :]
```
- Extract diagonal-like elements or stride-based patterns with slicing and `stride_tricks` (advanced): `A[::2, ::2]`.
- Replace all negative values with 0:
```python
A[A < 0] = 0
```
- Broadcast a 1D vector to subtract a row-wise mean:
```python
M = np.random.rand(100, 200)
row_mean = M.mean(axis=1)          # shape (100,)
M_centered = M - row_mean[:, None] # use newaxis to broadcast
```

**13. How to think about indexing if you come from C++**
- C++: multi-dimensional arrays are often contiguous blocks with manual index arithmetic. In NumPy:
  - The raw memory is also a contiguous block (unless using Fortran-order), but `strides` control how indices map to memory.
  - `A[i,j]` is syntactic sugar that computes offset = base + i*stride0 + j*stride1 and reads/writes memory.
  - Unlike raw pointers, NumPy slices can return a view with different strides but the same base buffer.
- Example: `A[:, ::-1]` does not copy memory — it creates a view with negative stride for the second axis.

**14. Debugging tips**
- When a change to a slice unexpectedly modifies the original, it's a view issue — check whether you intended a copy. Use `.copy()` to avoid surprises.
- When masked/fancy indexing assignments don't update the original, remember those indexing styles return copies — use boolean masks or in-place functions.
- When performance is poor, check `a.flags['C_CONTIGUOUS']` and consider `a.copy()` to make layout contiguous.

**15. Short reference (cheat-sheet)**
- `a[i]` : scalar element
- `a[i:j]` : slice view (usually)
- `a[:, k]` : column (view)
- `a[[i,j]]` : fancy indexing (copy)
- `a[mask]` : boolean indexing (copy of selected elements)
- `a.reshape(...)` : view when possible, else copy
- `a.astype(dtype)` : copy with new dtype

**16. Examples you can run (copy–paste)**
```python
import numpy as np
# Setup
A = np.arange(12).reshape(3,4)
print('A:\n', A)
# slice view
s = A[0:2, 1:3]
print('s (view):\n', s)
s[0,0] = 999
print('A after modifying s:\n', A)
# fancy indexing (copy)
b = A[[0,2], [1,3]]
print('b (copy):', b)
# boolean masking
mask = A % 2 == 0
print('even values:', A[mask])
# reshape with inferred dimension
print('reshape to (2,-1):\n', A.reshape(2, -1))
# broadcast example
v = np.array([1,2,3,4])
print('subtract row mean example:')
M = A.astype(float)
M_centered = M - M.mean(axis=1)[:, None]
print(M_centered)
```

**17. Further reading and references**
- NumPy indexing documentation: https://numpy.org/doc/stable/reference/arrays.indexing.html
- Strides and memory layout: https://numpy.org/doc/stable/reference/arrays.ndarray.html#internal-memory-layout
- `np.ix_`, `np.take`, `np.put`, `np.where` — see NumPy docs for these utilities.

---
File: `slicing_indexing_detailed.md` created in the `tutorials/slicing_indexing` folder.
