# auditflow

`auditflow` is a lightweight, plug-and-play Python package that generates automated visual data quality audits for any tabular dataset (CSV or DataFrame). It's built with simplicity and real-world analytics workflows in mind.

## What It Does

- Detects missing values and visualizes them
- Highlights skewed numeric distributions
- Flags duplicates, constant columns, and high-cardinality categoricals
- Calculates memory usage and correlation heatmaps
- Auto-generates a clean HTML report with embedded visuals (no folders required)
- Writes a human-readable summary as a text report

Perfect for:
- Quick data onboarding
- Exploratory Data Analysis (EDA)
- Data validation in consulting and internal audit workflows

## Installation

```bash
pip install auditflow
```

## Usage

```python
from auditflow import run_audit
run_audit("your_dataset.csv")
```

Outputs:
- `audit_report.html`: portable report with embedded visuals
- `audit_summary.txt`: quick-glance data health insights
