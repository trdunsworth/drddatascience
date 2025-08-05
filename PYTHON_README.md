# Python Support for Dr. D's Data Science

This site now supports both R and Python code execution and rendering in Quarto documents.

## Setup

1. **Install Python dependencies:**
   ```bash
   python setup_python.py
   ```
   
   Or manually:
   ```bash
   pip install -r requirements.txt
   ```

2. **Verify Quarto can find Python:**
   ```bash
   quarto check
   ```

## Using Python in Blog Posts

### Basic Python Code Block
```python
import pandas as pd
import numpy as np

# Your Python code here
data = pd.DataFrame({'x': [1, 2, 3], 'y': [4, 5, 6]})
print(data)
```

### Python Code Block with Options
```python
#| label: my-analysis
#| echo: true
#| eval: true
#| fig-cap: "My Figure Caption"

import matplotlib.pyplot as plt
plt.plot([1, 2, 3], [4, 5, 6])
plt.show()
```

## Common Code Block Options

- `#| echo: true/false` - Show/hide code
- `#| eval: true/false` - Execute/don't execute code  
- `#| output: true/false` - Show/hide output
- `#| warning: false` - Hide warnings
- `#| message: false` - Hide messages
- `#| fig-cap: "Caption"` - Add figure caption
- `#| fig-width: 8` - Set figure width
- `#| fig-height: 6` - Set figure height

## Python Utilities

The `python_utils.py` file contains Python equivalents of the R functions used in your analyses:

- `custom_summary()` - Comprehensive statistics (equivalent to your R function)
- `extract_datetime_features()` - Extract date/time components
- `create_response_time_plots()` - Generate analysis plots
- `create_geographic_map()` - Interactive maps with Folium
- `load_sql_data()` - Database connectivity

## Example Usage in a Blog Post

```python
#| label: load-utilities
from python_utils import custom_summary, create_response_time_plots
import pandas as pd

# Load your data
df = pd.read_csv('cardiac_arrests_cy.csv')

# Get comprehensive statistics
stats = custom_summary(df['call_entry_time'])
print(stats)

# Create visualizations
fig = create_response_time_plots(df, 'call_entry_time')
fig.show()
```

## Database Connections

For SQL Server connections (equivalent to your R setup):

```python
import sqlalchemy as sa
from python_utils import load_sql_data, CARDIAC_ARREST_CURRENT_YEAR

# Connection string for SQL Server
conn_str = "mssql+pyodbc://server/database?driver=ODBC+Driver+17+for+SQL+Server"

# Load data using your SQL queries
df = load_sql_data(conn_str, CARDIAC_ARREST_CURRENT_YEAR)
```

## Rendering

To render your site with Python support:

```bash
quarto render
```

To preview with live reload:

```bash
quarto preview
```

The site will automatically detect and execute both R and Python code blocks based on the language specified in the fenced code block.
