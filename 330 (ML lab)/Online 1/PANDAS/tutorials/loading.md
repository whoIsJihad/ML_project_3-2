
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
