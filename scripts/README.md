# 📜 Scripts Directory

This directory contains Python utility modules and automation scripts used to support the climate data analysis pipeline.

## 📁 Files

### [`eda_utils.py`](eda_utils.py)
A shared helper module that contains reusable functions for the Exploratory Data Analysis (EDA) notebooks. Using this module ensures consistency across all per-country analyses and eliminates code duplication.

**Key Functions:**
- `load_and_clean()`: Replaces sentinel values and parses dates.
- `profile_dataframe()`: Generates a standard data health report.
- `detect_outliers()`: Identifies extreme weather events using Z-scores.
- `plot_time_series()`: Generates professional monthly trend charts.
- `summary_statistics()`: Calculates key climate KPIs.

---

## 🛠️ Usage
In any Jupyter notebook, you can import these utilities using:
```python
import sys
sys.path.append('../')
from scripts.eda_utils import load_and_clean, profile_dataframe
```
