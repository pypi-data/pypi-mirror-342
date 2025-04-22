# simplebins

**simplebins** is a lightweight Python utility that makes it easy to bin numeric values into equal-width intervals.  
It supports individual numbers, lists, `pandas.Series`, and `pandas.DataFrame`s.

---

## 🔧 Features

- Works with numbers, lists, `pandas.Series`, and `pandas.DataFrame`s  
- Returns either the bin index, floor, ceiling, midpoint, or a human-readable label  
- Clean and intuitive API  
- Handles missing values gracefully  
- Zero dependencies outside of `pandas` and `numpy`

---

## ❓ Why not `pandas.cut()`?

`pandas.cut()` is powerful but sometimes overkill.  
**simplebins** simplifies the common use case: fixed-width bins with predictable, numeric output – perfect for quick transformations.

---

## 🚀 Installation

```bash
pip install simplebins
```

---

## 📦 Usage

```python
from simplebins import cut
```

### Bin a single number
```python
cut(12, binwidth=5)
# Output: 10
```

### Bin a list of numbers
```python
cut([3, 7, 12], binwidth=5)
# Output: [0, 5, 10]
```

### Bin a pandas Series
```python
import pandas as pd
cut(pd.Series([3, 7, 12]), binwidth=5, output="label")
# Output: 
# 0     0 <= x < 5
# 1     5 <= x < 10
# 2    10 <= x < 15
# dtype: object
```

### Bin a DataFrame column-wise
```python
df = pd.DataFrame({"age": [21, 34, 65], "income": [2000, 3120, 4190]})
cut(df, binwidth=10)
```

---

## 🛠 Parameters

| Parameter    | Type                  | Default   | Description |
|--------------|-----------------------|-----------|-------------|
| `x`          | number, list, Series, DataFrame | –         | Input data to bin |
| `binwidth`   | `float`               | –         | Width of each bin (must be > 0) |
| `origin`     | `float`               | `0`       | Starting point for bins |
| `output`     | `str`                 | `"floor"` | One of: `"index"`, `"floor"`, `"ceiling"`, `"center"`, `"label"` |