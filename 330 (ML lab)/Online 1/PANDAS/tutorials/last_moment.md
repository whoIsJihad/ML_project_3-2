
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


