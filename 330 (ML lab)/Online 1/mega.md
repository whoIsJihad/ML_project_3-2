
# Pandas Fundamentals for the Discerning Engineer

---

## 1. Core Structures

Pandas is built on two primary structures. For a CSE student, think of these as highly optimized, labeled containers that handle memory alignment for you.

### The Series (1D)

A **Series** is a labeled, one-dimensional array. It's essentially a NumPy array with an index.

- **Access:** By label (`s['a']`) or by integer position (`s[0]`).
- **Creation:**
	```python
	import pandas as pd
	s = pd.Series([10, 20], index=['x', 'y'])
	print(s)
	# x    10
	# y    20
	# dtype: int64
	```
- **Index:** The labels for each element. Can be strings, numbers, or dates.

#### More Examples
```python
# Creating a Series from a dictionary
data = {'a': 1, 'b': 2, 'c': 3}
s2 = pd.Series(data)
print(s2)
# a    1
# b    2
# c    3
# dtype: int64
```

### The DataFrame (2D)

A **DataFrame** is a tabular structure. In C++ terms, imagine a `std::map<string, std::vector<T>>` where all vectors are perfectly aligned by a shared index.

- **Creation:**
	```python
	data = {'Name': ['Alice', 'Bob'], 'Age': [25, 30]}
	df = pd.DataFrame(data)
	print(df)
	#     Name  Age
	# 0  Alice   25
	# 1    Bob   30
	```
- **Index:** Row labels (default: 0, 1, 2, ...)
- **Columns:** Column labels (strings, numbers, etc.)

#### More Examples
```python
# Creating a DataFrame from a list of dicts
data = [
	{'Name': 'Alice', 'Age': 25},
	{'Name': 'Bob', 'Age': 30}
]
df2 = pd.DataFrame(data)
print(df2)
```

---

## 2. Indexing and Selection

This is the primary source of logic errors. Use the correct tool for the job.

### `.iloc` (Integer-location)

Strictly zero-based integer indexing (like C/C++ arrays).

- `df.iloc[0]` → Returns the first row (as a Series)
- `df.iloc[:, 0]` → Returns the first column
- `df.iloc[-1]` → The stable way to access the last row regardless of size

**Example:**
```python
import pandas as pd
df = pd.DataFrame({'A': [10, 20, 30], 'B': [0.1, 0.2, 0.3]})
print(df.iloc[0])      # First row
print(df.iloc[:, 0])   # First column
print(df.iloc[-1])     # Last row
```

### `.loc` (Label-location)

Uses index labels and column names.

- `df.loc[0, 'A']` → Value at row label 0, column 'A'
- `df.loc[:, 'A']` → All rows, column 'A'
- `df.loc[1:2, ['A', 'B']]` → Rows 1 and 2, columns 'A' and 'B'

**Example:**
```python
df = pd.DataFrame({'Price': [1.5, 2.0, 3.0]}, index=['apple', 'banana', 'cherry'])
print(df.loc['banana', 'Price'])  # 2.0
print(df.loc[:, 'Price'])         # All prices
```

### Boolean Indexing (Filtering)

Functional filtering without the overhead of if statements.

- `df[df['Price'] > 0.5]` → Returns a view (or copy) of the DataFrame where the predicate is True.

**Example:**
```python
df = pd.DataFrame({'Price': [0.4, 0.8, 1.2], 'Item': ['A', 'B', 'C']})
filtered = df[df['Price'] > 0.5]
print(filtered)
#    Price Item
# 1   0.8    B
# 2   1.2    C
```

---

## 3. Handling Null / Missing Values (NaN)

### How Null Values Occur

Null (missing) values are common in real-world data. Here are the main ways they appear in Pandas:

#### 1. **Reading Data from External Sources**
When importing CSV, Excel, or database files, missing values are often represented as empty cells, `None`, `NA`, `N/A`, or other conventions.

```python
# CSV with missing values:
# Name,Age,Salary
# Alice,25,50000
# Bob,,65000      <- missing Age
# Charlie,30,
# -> Salary is missing

df = pd.read_csv('data.csv')
print(df)
#      Name   Age Salary
# 0  Alice  25.0  50000
# 1    Bob   NaN  65000
# 2  Charlie 30.0    NaN
```

#### 2. **Merging / Joining DataFrames**
When merging two DataFrames on a key, rows that don't match in the other table get `NaN` values.

```python
df1 = pd.DataFrame({'ID': [1, 2, 3], 'Name': ['A', 'B', 'C']})
df2 = pd.DataFrame({'ID': [1, 3, 4], 'Salary': [1000, 1200, 1500]})

merged = pd.merge(df1, df2, on='ID', how='outer')
print(merged)
#   ID Name  Salary
# 0   1    A  1000.0
# 1   2    B     NaN    <- no salary for ID 2
# 2   3    C  1200.0
# 3   4  NaN  1500.0    <- no name for ID 4
```

#### 3. **Reindexing or Reshaping**
When you reindex a Series or pivot a DataFrame, new indices may not have corresponding data.

```python
s = pd.Series([10, 20, 30], index=['a', 'b', 'c'])
s_reindexed = s.reindex(['a', 'b', 'c', 'd', 'e'])
print(s_reindexed)
# a    10.0
# b    20.0
# c    30.0
# d     NaN     <- new index, no data
# e     NaN     <- new index, no data
```

#### 4. **Type Conversions**
Converting a column to a numeric type when it contains non-numeric values may result in `NaN`.

```python
s = pd.Series(['1', '2', 'abc', '4'])
s_numeric = pd.to_numeric(s, errors='coerce')  # 'coerce' converts invalid to NaN
print(s_numeric)
# 0    1.0
# 1    2.0
# 2    NaN    <- 'abc' cannot be converted
# 3    4.0
```

#### 5. **Missing Data by Design**
Sometimes you explicitly insert `None` or `np.nan` to represent missing values.

```python
df = pd.DataFrame({'A': [1, None, 3], 'B': [4, 5, None]})
print(df)
#      A    B
# 0  1.0  4.0
# 1  NaN  5.0
# 2  3.0  NaN
```

---

### Detecting Null Values

#### **`.isna()` and `.isnull()`**
Check which cells contain `NaN`. (Both methods are identical in Pandas.)

```python
df = pd.DataFrame({'A': [1, None, 3], 'B': [4, 5, None]})
print(df.isna())
#        A      B
# 0  False  False
# 1   True  False
# 2  False   True
```

#### **Count Missing Values per Column**
```python
print(df.isna().sum())
# A    1
# B    1
# dtype: int64
```

#### **Count Missing Values per Row**
```python
print(df.isna().sum(axis=1))
# 0    0
# 1    1
# 2    1
# dtype: int64
```

#### **Check if Any Values are Missing**
```python
print(df.isna().any())
# A    True
# B    True
# dtype: bool

print(df.isna().any().any())  # any missing in entire DataFrame?
# True
```

#### **Get Rows with Missing Values**
```python
rows_with_null = df[df.isna().any(axis=1)]
print(rows_with_null)
#      A    B
# 1  NaN  5.0
# 2  3.0  NaN
```

---

### Handling Null Values

#### **1. Dropping (Removing) Rows or Columns with NaN**

**Drop rows with any NaN:**
```python
df_clean = df.dropna()
print(df_clean)
#    A  B
# 0  1.0  4.0
```

**Drop rows where a specific column has NaN:**
```python
df_clean = df.dropna(subset=['A'])
print(df_clean)
#      A    B
# 0  1.0  4.0
# 2  3.0  NaN
```

**Drop columns with any NaN:**
```python
df_clean = df.dropna(axis=1)
print(df_clean)
# Empty DataFrame  <- both columns have NaN, so both are dropped
```

**Drop only if all values in a row are NaN:**
```python
df_clean = df.dropna(how='all')
print(df_clean)
#      A    B
# 0  1.0  4.0
# 1  NaN  5.0
# 2  3.0  NaN
```

**Use `inplace=True` to modify the original DataFrame:**
```python
df.dropna(inplace=True)
print(df)
```

---

#### **2. Filling (Imputing) Missing Values**

**Fill with a constant value:**
```python
df_filled = df.fillna(0)
print(df_filled)
#    A  B
# 0  1.0  4.0
# 1  0.0  5.0  <- NaN replaced with 0
# 2  3.0  0.0  <- NaN replaced with 0
```

**Fill with different values per column:**
```python
df_filled = df.fillna({'A': -1, 'B': 999})
print(df_filled)
#    A    B
# 0  1.0    4.0
# 1  -1.0   5.0  <- A filled with -1
# 2  3.0  999.0  <- B filled with 999
```

**Forward fill (propagate previous value down):**
```python
df_ffill = df.fillna(method='ffill')
print(df_ffill)
#    A  B
# 0  1.0  4.0
# 1  1.0  5.0   <- A filled with previous value (1.0)
# 2  3.0  5.0   <- B filled with previous value (5.0)
```

**Backward fill (propagate next value up):**
```python
df_bfill = df.fillna(method='bfill')
print(df_bfill)
#    A  B
# 0  1.0  4.0
# 1  3.0  5.0   <- A filled with next value (3.0)
# 2  3.0  NaN
```

**Fill with interpolated values (useful for time-series data):**
```python
s = pd.Series([1, None, None, 4])
s_interpolated = s.interpolate()
print(s_interpolated)
# 0    1.0
# 1    2.0   <- interpolated between 1 and 4
# 2    3.0   <- interpolated between 1 and 4
# 3    4.0
```

**Fill with column mean/median:**
```python
df_filled = df.fillna(df.mean())
print(df_filled)
#    A    B
# 0  1.0  4.0
# 1  2.0  5.0   <- A filled with mean of [1, 3] = 2.0
# 2  3.0  4.5   <- B filled with mean of [4, 5] = 4.5
```

---

#### **3. Custom Handling with `.where()` or `.mask()`**

**`.where()` keeps values where condition is True, replaces False with NaN (or specified value):**
```python
df_where = df.where(df > 2, other=-1)
print(df_where)
#    A    B
# 0  -1.0  -1.0  <- 1 and 4 are not > 2
# 1  -1.0   5.0
# 2   3.0  -1.0
```

**`.mask()` is the opposite (replaces where condition is True):**
```python
df_mask = df.mask(df < 3, other=0)
print(df_mask)
#    A  B
# 0  0.0  4.0   <- 1 is < 3
# 1  NaN  5.0
# 2  3.0  0.0   <- values < 3 are masked
```

---

#### **4. Using `.apply()` for Custom Logic**

```python
def custom_fill(col):
    return col.fillna(col.median())

df_custom = df.apply(custom_fill)
print(df_custom)
#    A    B
# 0  1.0  4.0
# 1  2.0  5.0   <- A filled with median, B filled with median
# 2  3.0  4.5
```

---

### Practical Strategy

**When should you drop vs fill?**

| Scenario | Action |
|----------|--------|
| Missing data is <5% of rows | Fill with mean/median or drop row |
| Missing data is >20% of column | Consider dropping the entire column |
| Missing is not random (structural) | Fill with domain knowledge or forward/backward fill |
| Time-series data | Use interpolation or forward fill |
| Categorical data | Use mode (most frequent value) or a placeholder like 'Unknown' |

**Example workflow:**
```python
import pandas as pd
import numpy as np

# Load data
df = pd.read_csv('data.csv')

# 1. Detect missing values
print(df.isna().sum())

# 2. Drop columns with >20% missing
missing_pct = (df.isna().sum() / len(df)) * 100
cols_to_drop = missing_pct[missing_pct > 20].index
df = df.drop(columns=cols_to_drop)

# 3. Fill remaining missing values
df['numeric_col'] = df['numeric_col'].fillna(df['numeric_col'].mean())
df['categorical_col'] = df['categorical_col'].fillna(df['categorical_col'].mode()[0])

# 4. Drop any rows still with missing values
df = df.dropna()

print(df.isna().sum())  # Verify all fixed
```

---


# 0. Mental model (VERY IMPORTANT)

**Pandas = Excel + SQL + Python**

* **Series** → one column with index
* **DataFrame** → table (rows + columns)
* Almost everything is:
  **select → filter → compute → group → transform → join**

If you understand this pipeline, Pandas becomes predictable.

---

# 1. Creating DataFrames (you already know basics, still recap)

```python
import pandas as pd

df = pd.DataFrame({
    "name": ["A", "B", "C"],
    "age": [20, 21, 22],
    "cgpa": [3.5, 3.7, 3.9]
})
```

From CSV (VERY COMMON IN TESTS):

```python
df = pd.read_csv("data.csv")
```

Quick inspection (MEMORIZE THESE):

```python
df.head()
df.tail()
df.shape        # (rows, cols)
df.columns
df.dtypes
df.info()
df.describe()
```

---

# 2. Selecting data (THIS IS HUGE)

### Column selection

```python
df["age"]              # Series
df[["age", "cgpa"]]    # DataFrame
```

### Row selection (index-based)

```python
df.iloc[0]        # first row
df.iloc[0:3]      # slice
df.iloc[0, 1]     # row 0, col 1
```

### Label-based

```python
df.loc[0]                     
df.loc[0:2, ["age", "cgpa"]]
```

---

# **LOC vs ILOC**

| Feature            | `.loc`                                              | `.iloc`                              |
| ------------------ | --------------------------------------------------- | ------------------------------------ |
| **Selection type** | Label-based                                         | Position-based (integer index)       |
| **Rows & Columns** | Use actual row/column labels                        | Use integer positions (0,1,2…)       |
| **Slicing**        | Inclusive of **end label**                          | Exclusive of **end index**           |
| **Example**        | `df.loc[2, "Age"]` → row with label 2, column "Age" | `df.iloc[2,1]` → 3rd row, 2nd column |

---

### **1. Row selection**

```python
# loc → label
df.loc[0]       # row with index 0 (if index is 0,1,2…)
df.loc[0:2]     # rows with labels 0,1,2 → inclusive

# iloc → integer position
df.iloc[0]      # first row
df.iloc[0:2]    # first 2 rows → 0 and 1 (exclusive of 2)
```

---

### **2. Column selection**

```python
df.loc[:, "Age"]           # all rows, column "Age"
df.loc[:, ["Age","CGPA"]]  # multiple columns by name

df.iloc[:, 1]              # all rows, second column
df.iloc[:, 1:3]            # second and third columns
```

---

### **3. Row + Column together**

```python
df.loc[0, "Age"]     # row with label 0, column "Age"
df.iloc[0, 1]        # first row, second column
```

---

### **Rule to remember (trick)**

* **LOC** = **Labels you see**
* **ILOC** = **Integer positions like arrays**
* Slice with **LOC → end included**, **ILOC → end excluded**

---

**Rule**

* `iloc` → position
* `loc` → label + conditions

---

# 3. Filtering rows (MOST ASKED)

```python
df[df["age"] > 20]
df[df["cgpa"] >= 3.7]
```

Multiple conditions (**USE & | NOT and/or**):

```python
df[(df["age"] > 20) & (df["cgpa"] >= 3.7)]
```

String conditions:

```python
df[df["name"] == "A"]
df[df["name"].isin(["A", "C"])]
```

---

# **Adding Rows in Pandas (Recommended: `pd.concat`)**

Pandas **DataFrames are immutable**, so you don’t truly “insert” a row—you **create a new DataFrame** by concatenating the old one with the new row(s).

---

## **1. Adding a single row**

```python
import pandas as pd

# Original DataFrame
df = pd.DataFrame({
    "Name": ["A", "B"],
    "Age": [20, 21],
    "CGPA": [3.5, 3.7]
})

# New row as a DataFrame
new_row = pd.DataFrame({"Name": ["C"], "Age": [22], "CGPA": [3.9]})

# Concatenate
df = pd.concat([df, new_row], ignore_index=True)

print(df)
```

**Output:**

```
  Name  Age  CGPA
0    A   20   3.5
1    B   21   3.7
2    C   22   3.9
```

✅ Key points:

* `ignore_index=True` → re-numbers the index (important!)
* `new_row` must be a **DataFrame**, not Series.

---

## **2. Adding multiple rows at once**

```python
more_rows = pd.DataFrame({
    "Name": ["D", "E"],
    "Age": [23, 24],
    "CGPA": [4.0, 3.8]
})

df = pd.concat([df, more_rows], ignore_index=True)
```

**Output:**

```
  Name  Age  CGPA
0    A   20   3.5
1    B   21   3.7
2    C   22   3.9
3    D   23   4.0
4    E   24   3.8
```

---

## **3. Important Tips / Tricks**

1. **Column order matters**:
   Pandas aligns by **column names**, not positions. Missing columns → `NaN`.

```python
new_row = pd.DataFrame({"Name": ["F"], "CGPA": [3.6]})
df = pd.concat([df, new_row], ignore_index=True)
# Age will be NaN for this row
```

2. **Resetting index is crucial**:
   If you skip `ignore_index=True`, old indexes are kept → duplicate or messy indexes.

3. **Can append at top or middle**:

   * Top: `df = pd.concat([new_row, df], ignore_index=True)`
   * Middle → split + concat (rarely needed in tests).

4. **Do not use `append` in new Pandas versions**:

   * `df.append()` is deprecated in ≥2.0

---

### ✅ **Summary: Exam Cheat Version**

```python
df = pd.concat([df, pd.DataFrame(new_row_dict)], ignore_index=True)
```

* `new_row_dict` can contain **one row or multiple rows**.
* Always `ignore_index=True` unless you intentionally want old indexes.

---



# 4. Adding / modifying columns

```python
df["passed"] = df["cgpa"] >= 3.0
df["age_plus_1"] = df["age"] + 1
```

Using conditions:

```python
df["grade"] = "Average"
df.loc[df["cgpa"] >= 3.7, "grade"] = "Excellent"
```

---

# 5. Dropping stuff

```python
df.drop("age", axis=1)          # drop column
df.drop(0, axis=0)              # drop row
df.drop(columns=["age"])
df.drop(index=[0, 1])
```

⚠️ By default it **does NOT modify original**
Use:

```python
df = df.drop("age", axis=1)
# or
df.drop("age", axis=1, inplace=True)
```

---

# 6. Missing values (VERY COMMON)

```python
df.isna()
df.isna().sum()
```

Drop missing:

```python
df.dropna()
```

Fill missing:

```python
df.fillna(0)
df["cgpa"].fillna(df["cgpa"].mean())
```

---

# 7. Sorting

```python
df.sort_values("cgpa")
df.sort_values("cgpa", ascending=False)
df.sort_values(["age", "cgpa"])
```

---

# 8. GroupBy (THIS IS CRITICAL)

Think: **SQL GROUP BY**

```python
df.groupby("age")["cgpa"].mean()
```

Multiple aggregations:

```python
df.groupby("age").agg({
    "cgpa": ["mean", "max"],
    "name": "count"
})
```

Common ones:

* `mean`
* `sum`
* `count`
* `max`
* `min`

---

# 9. Value counts (EXAM FAVORITE)

```python
df["age"].value_counts()
```

Normalized (percent):

```python
df["age"].value_counts(normalize=True)
```

---

# 10. Apply vs Map (simple rule)

### map → Series only

```python
df["cgpa"] = df["cgpa"].map(lambda x: x * 10)
```

### apply → Series or DataFrame

```python
df["status"] = df["cgpa"].apply(lambda x: "Good" if x >= 3.7 else "Ok")
```

Avoid `apply` if vectorized ops exist.

---

# 11. String operations (SUPER COMMON)

```python
df["name"].str.lower()
df["name"].str.upper()
df["name"].str.contains("a")
df["name"].str.len()
```

---

# 12. Renaming columns

```python
df.rename(columns={"cgpa": "CGPA"})
```

---

# 13. Merging / Joining (IMPORTANT)

```python
pd.merge(df1, df2, on="id")
pd.merge(df1, df2, how="left", on="id")
```

`how`:

* inner
* left
* right
* outer

---

# 14. Index basics (don’t overthink)

```python
df.set_index("name")
df.reset_index()
```

---

# 15. Common traps (READ THIS)

❌ `and / or` → use `& |`
❌ Forget parentheses in conditions
❌ Confuse `loc` and `iloc`
❌ Expect inplace change without assignment

---

# 16. Absolute minimum checklist (memorize)

If you remember ONLY this, you’ll survive:

* `read_csv`
* `head`, `info`, `describe`
* `df["col"]`, `df[["c1","c2"]]`
* `loc`, `iloc`
* filtering with conditions
* `groupby().agg()`
* `value_counts`
* `fillna`, `dropna`
* `sort_values`
* `merge`

---



---

# **1. Basic CSV loading**

```python
import pandas as pd

df = pd.read_csv("data.csv")
```

* Default separator: `,`
* Assumes **first row is header**

---

# **2. CSV with no header**

```python
df = pd.read_csv("data.csv", header=None)
```

* Pandas will auto-assign column names as 0,1,2…
* You can rename later with `names`:

```python
df = pd.read_csv("data.csv", header=None, names=["Name","Age","CGPA"])
```

---

# **3. Different delimiter / separator**

```python
df = pd.read_csv("data.txt", sep="\t")        # tab-separated
df = pd.read_csv("data.txt", sep="|")        # pipe-separated
df = pd.read_csv("data.txt", sep=";")        # semicolon-separated
```

---

# **4. Only load certain columns**

```python
df = pd.read_csv("data.csv", usecols=["Name", "CGPA"])
# or by index
df = pd.read_csv("data.csv", usecols=[0,2])
```

---

# **5. Skip rows / load partial file**

```python
df = pd.read_csv("data.csv", skiprows=2)      # skip first 2 rows
df = pd.read_csv("data.csv", nrows=5)        # load only first 5 rows
```

---

# **6. Handle missing values on load**

```python
df = pd.read_csv("data.csv", na_values=["NA", "Missing", "?"])
```

* Converts specified strings to `NaN`

---

# **7. Set a column as index**

```python
df = pd.read_csv("data.csv", index_col="Name")
```

* Then you can do `df.loc["Alice"]` directly

---

# **8. Encoding issues**

```python
df = pd.read_csv("data.csv", encoding="utf-8")           # default
df = pd.read_csv("data.csv", encoding="latin1")          # if utf-8 fails
```

---

# **9. Skip footer lines**

```python
df = pd.read_csv("data.csv", skipfooter=2, engine="python")
```

* `skipfooter` requires `engine="python"`

---

# **10. Quick options cheat sheet**

| Option       | Use Case                  |
| ------------ | ------------------------- |
| `sep`        | delimiter not comma       |
| `header`     | file has no header row    |
| `names`      | assign column names       |
| `usecols`    | only load certain columns |
| `skiprows`   | skip top rows             |
| `nrows`      | load first N rows         |
| `index_col`  | set column as index       |
| `na_values`  | convert strings to NaN    |
| `encoding`   | handle non-UTF text       |
| `skipfooter` | skip last rows            |

---

# **BONUS: read other text formats**

* **TSV** → `pd.read_csv("data.tsv", sep="\t")`
* **Space-separated** → `pd.read_csv("data.txt", delim_whitespace=True)`
* **Excel** → `pd.read_excel("data.xlsx")`
* **JSON** → `pd.read_json("data.json")`

---

✅ After loading, always inspect:

```python
df.head()
df.info()
df.describe()
```

---
