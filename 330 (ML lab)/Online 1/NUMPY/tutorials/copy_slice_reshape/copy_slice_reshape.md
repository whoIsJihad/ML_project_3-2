# NumPy Tutorial: Copying, Sorting, and Reshaping Arrays

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