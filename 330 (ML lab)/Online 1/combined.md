# Adding & Removing Elements

**Purpose:** Short, focused reference showing how to add and remove elements in NumPy arrays.

**Append**
- Syntax: `np.append(arr, values)`
- Returns a new array with `values` appended to the end of `arr`.

Example:
```python
import numpy as np
arr = np.array([1, 2, 3])
arr_appended = np.append(arr, [4, 5])
print(arr_appended)  # [1 2 3 4 5]
```

**Insert**
- Syntax: `np.insert(arr, index, values)`
- Inserts `values` into `arr` before `index` and returns a new array.

Example:
```python
arr = np.array([1, 2, 3])
arr_inserted = np.insert(arr, 2, 99)  # insert before index 2
print(arr_inserted)  # [ 1  2 99  3]
```

**Delete (rows / columns in 2D)**
- Syntax: `np.delete(arr, index, axis=0)` to remove a row; use `axis=1` to remove a column.
- Returns a new array with the specified row/column removed.

Example:
```python
arr2d = np.array([[10,11,12], [20,21,22], [30,31,32]])
# delete row 0
arr_row_deleted = np.delete(arr2d, 0, axis=0)
print(arr_row_deleted)
# delete column 1
arr_col_deleted = np.delete(arr2d, 1, axis=1)
print(arr_col_deleted)
```

**Notes & Best Practices**
- These functions return new arrays — they do not modify the original in-place.
- Repeatedly appending or inserting into large arrays is inefficient (O(n) copies). For performance:
  - Collect values in a Python list and convert once with `np.array(list)`.
  - Or preallocate an array and fill it when possible.
- Use these functions for convenience or small data; for heavy workloads, prefer preallocation or specialized structures.

---
File: `adding_removing_elements/adding_removing_elements.md` (placed next to `practice.ipynb` in the same folder)

### 1. The Input: `data.csv`

Imagine you have a file named `data.csv` sitting in your folder. It looks exactly like this:

```text
1.0, 2.0, 3.0
4.0, 5.0, 6.0

```

### 2. The Code: Loading the Data

You run this in your script:

```python
import numpy as np

# We tell NumPy to look for commas because it's a CSV
my_array = np.loadtxt('data.csv', delimiter=',')

print(my_array)

```

### 3. The Output: What `my_array` looks like

The output in your terminal will be a NumPy ndarray object:

```text
[[1. 2. 3.]
 [4. 5. 6.]]

```

NumPy has taken those strings, parsed them as floats, and mapped them into a 2D matrix.

---

### Comparison of Inputs and Outputs

| Feature | `loadtxt` / `genfromtxt` (Input) | `savetxt` (Output) |
| --- | --- | --- |
| **Source** | A `.txt` or `.csv` file on your SSD. | A NumPy array variable in your code. |
| **Result** | A NumPy array object in memory. | A new `.txt` or `.csv` file on your SSD. |
| **The "How"** | It reads line by line and splits by the `delimiter`. | It writes row by row and inserts the `delimiter`. |

### Example of `savetxt` (Going the other way)

If you have this array in Python:

```python
arr = np.array([[10, 20], [30, 40]])

# This creates a file called 'output.txt'
# fmt='%.0f' keeps it from looking like 10.000000
np.savetxt('output.txt', arr, delimiter=' ', fmt='%.0f')

```

**The resulting `output.txt` file will look like this:**

```text
10 20
30 40

```

### Why two functions for loading?

If your `data.csv` had a missing value like this: `1.0, , 3.0`, **`loadtxt`** would throw a tantrum and crash your program. **`genfromtxt`** would simply put a `nan` (Not a Number) in that spot and keep moving. Given your track record, you’ll probably be dealing with "broken" data often, so use `genfromtxt`.# NumPy Tutorial: Copying, Sorting, and Reshaping Arrays

This tutorial covers essential NumPy operations for copying, sorting, flattening, transposing, and reshaping arrays. Each function is explained with code examples and plain English descriptions, based on the reference image above.

---

## 1. Copying Arrays
- **`np.copy(arr)`**: Creates a new copy of the array in memory. Changes to the copy do not affect the original.
  ```python
  import numpy as np
  arr = np.array([1, 2, 3])
  arr_copy = np.copy(arr)
  arr_copy[0] = 99
  print('Original:', arr)      # [1 2 3]
  print('Copy:', arr_copy)     # [99 2 3]
  ```

## 2. Viewing Arrays
- **`arr.view(dtype)`**: Creates a new view of the array with a different data type (advanced usage).
  ```python
  arr = np.array([1, 2, 3], dtype=np.int32)
  arr_view = arr.view(np.float32)
  print('View:', arr_view)
  ```

## 3. Sorting Arrays
- **`arr.sort()`**: Sorts the array in-place (modifies the original array).
  ```python
  arr = np.array([3, 1, 2])
  arr.sort()
  print('Sorted:', arr)  # [1 2 3]
  ```
- **`arr.sort(axis=0)`**: Sorts along a specific axis (for 2D arrays).
  ```python
  arr2d = np.array([[3, 2], [1, 4]])
  arr2d.sort(axis=0)
  print(arr2d)  # [[1 2]
               #  [3 4]]
  ```

## 4. Flattening Arrays
- **`arr.flatten()`**: Flattens a multi-dimensional array to 1D.
  ```python
  arr2d = np.array([[1, 2], [3, 4]])
  flat = arr2d.flatten()
  print('Flattened:', flat)  # [1 2 3 4]
  ```

## 5. Transposing Arrays
- **`arr.T`**: Transposes the array (rows become columns and vice versa).
  ```python
  arr2d = np.array([[1, 2, 3], [4, 5, 6]])
  print('Transposed:\n', arr2d.T)
  # [[1 4]
  #  [2 5]
  #  [3 6]]
  ```

## 6. Reshaping Arrays
- **`arr.reshape(new_shape)`**: Returns a new array with the specified shape (must have the same number of elements).
  ```python
  arr = np.arange(12)
  reshaped = arr.reshape(3, 4)
  print('Reshaped:\n', reshaped)
  # [[ 0  1  2  3]
  #  [ 4  5  6  7]
  #  [ 8  9 10 11]]
  ```
- **`arr.resize(new_shape)`**: Changes the shape of the array in-place. If the new shape is larger, fills new values with 0.
  ```python
  arr = np.array([1, 2, 3, 4])
  arr.resize((2, 3))
  print('Resized:\n', arr)
  # [[1 2 3]
  #  [4 0 0]]
  ```

---

**Summary Table:**

| Operation   | Syntax Example                | Description                                      |
|-------------|------------------------------|--------------------------------------------------|
| Copy        | `np.copy(arr)`               | Copies array to new memory                       |
| View        | `arr.view(dtype)`            | Creates view with different dtype                |
| Sort        | `arr.sort()`                 | Sorts array in-place                             |
| Sort (axis) | `arr.sort(axis=0)`           | Sorts along a specific axis                      |
| Flatten     | `arr.flatten()`              | Flattens array to 1D                             |
| Transpose   | `arr.T`                      | Transposes array (rows <-> columns)              |
| Reshape     | `arr.reshape(3, 4)`          | Reshapes array without changing data             |
| Resize      | `arr.resize((5, 6))`         | Changes shape, fills new values with 0 if needed |

---

Try these examples in a Python environment to see how each operation works!
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
