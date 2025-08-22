---
title: "Python Test"
author: "Tony Dunsworth, Ph.D."
date: "2025-08-13"
execute: 
  eval: true
---

Testing Python execution:

::: {#88fba72c .cell execution_count=1}
``` {.python .cell-code}
import pandas as pd
import numpy as np

# Test basic functionality
print("Python is working!")
print(f"Pandas version: {pd.__version__}")
print(f"NumPy version: {np.__version__}")

# Create a simple DataFrame
data = {'x': [1, 2, 3, 4, 5], 'y': [2, 4, 6, 8, 10]}
df = pd.DataFrame(data)
print("\nSample DataFrame:")
print(df)
```

::: {.cell-output .cell-output-stdout}
```
Python is working!
Pandas version: 2.3.1
NumPy version: 2.2.6

Sample DataFrame:
   x   y
0  1   2
1  2   4
2  3   6
3  4   8
4  5  10
```
:::
:::


