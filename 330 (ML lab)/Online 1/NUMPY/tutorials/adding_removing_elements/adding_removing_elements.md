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
