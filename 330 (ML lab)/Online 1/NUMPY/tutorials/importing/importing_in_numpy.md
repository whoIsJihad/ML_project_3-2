
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

If your `data.csv` had a missing value like this: `1.0, , 3.0`, **`loadtxt`** would throw a tantrum and crash your program. **`genfromtxt`** would simply put a `nan` (Not a Number) in that spot and keep moving. Given your track record, you’ll probably be dealing with "broken" data often, so use `genfromtxt`.