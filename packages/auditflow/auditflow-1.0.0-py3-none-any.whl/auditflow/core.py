"""
core.py – Main logic for the auditflow package.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import skew
import os
import warnings
import datetime
import base64

warnings.filterwarnings("ignore")

def img_to_base64(img_path):
    with open(img_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode("utf-8")

def save_plot(fig, name):
    if not os.path.exists("audit_charts"):
        os.makedirs("audit_charts")
    fig.savefig(f"audit_charts/{name}", bbox_inches='tight')
    plt.close(fig)

def load_dataset(file_path):
    df = pd.read_csv(file_path)
    print(f"Loaded: {file_path} | Shape: {df.shape}")
    return df

def missing_values_analysis(df):
    nulls = df.isnull().sum()
    null_pct = (nulls / len(df)) * 100
    null_table = pd.DataFrame({
        "Missing Count": nulls,
        "Missing %": null_pct
    }).sort_values(by="Missing %", ascending=False)
    null_table_filtered = null_table[null_table["Missing Count"] > 0]

    fig, ax = plt.subplots(figsize=(10, 5))
    sns.heatmap(df.isnull(), cbar=False, cmap="viridis")
    ax.set_title("Heatmap of Missing Values")
    save_plot(fig, "missing_heatmap.png")

    fig, ax = plt.subplots(figsize=(10, 5))
    null_table_filtered["Missing %"].plot(kind='barh', ax=ax)
    ax.set_title("Percentage of Missing Values by Column")
    save_plot(fig, "missing_bar.png")

    return null_table_filtered

def general_quality_checks(df):
    results = {}
    results['duplicates'] = df.duplicated().sum()

    num_cols = df.select_dtypes(include=np.number).columns
    skews = df[num_cols].apply(skew).sort_values(ascending=False)
    results['skews'] = skews

    fig, ax = plt.subplots(figsize=(10, 5))
    skews.plot(kind='bar', ax=ax)
    ax.set_title("Skewness of Numeric Features")
    save_plot(fig, "skewness_plot.png")

    results['constants'] = [col for col in df.columns if df[col].nunique() == 1]
    results['cardinals'] = [col for col in df.columns if df[col].dtype == "object" and df[col].nunique() > 50]

    return results

def correlation_and_memory(df):
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(df.select_dtypes(include=np.number).corr(), annot=False, cmap="coolwarm")
    ax.set_title("Correlation Matrix")
    save_plot(fig, "correlation_matrix.png")

    memory_used = df.memory_usage(deep=True).sum() / 1024**2
    return memory_used

def generate_summary(nulls, general_results, memory_used):
    lines = []
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lines.append(f"Audit Summary Report - Generated on {timestamp}\n")

    if not nulls.empty:
        top_null = nulls.iloc[0]
        lines.append(f"- Column '{top_null.name}' has the highest missing percentage: {round(top_null['Missing %'], 2)}%.")

    if general_results['duplicates'] > 0:
        lines.append(f"- Dataset has {general_results['duplicates']} duplicate rows.")

    top_skew = general_results['skews'].abs().sort_values(ascending=False).head(1)
    for col, val in top_skew.items():
        lines.append(f"- Column '{col}' is highly skewed (Skewness = {round(val, 2)}).")

    if general_results['constants']:
        lines.append(f"- {len(general_results['constants'])} constant column(s): {', '.join(general_results['constants'])}")

    if general_results['cardinals']:
        lines.append(f"- High-cardinality columns (>50 unique values): {', '.join(general_results['cardinals'])}")

    lines.append(f"- Total memory usage: {round(memory_used, 2)} MB")

    with open("audit_summary.txt", "w") as f:
        for line in lines:
            f.write(line + "\n")

    return "\n".join(lines)

def export_html_report(summary_text):
    base64_missing_heatmap = img_to_base64("audit_charts/missing_heatmap.png")
    base64_missing_bar = img_to_base64("audit_charts/missing_bar.png")
    base64_skewness = img_to_base64("audit_charts/skewness_plot.png")
    base64_corr = img_to_base64("audit_charts/correlation_matrix.png")

    html_template = f"""<html><head><title>Audit Report</title><style>
    body {{ font-family: Arial; padding: 20px; }}
    h1 {{ color: #2c3e50; }}
    img {{ max-width: 100%; height: auto; margin: 10px 0; }}
    pre {{ background: #f8f8f8; padding: 10px; border: 1px solid #ddd; }}
    </style></head><body>
    <h1>Data Quality Audit Report</h1>
    <h2>Summary</h2>
    <pre>{summary_text}</pre>
    <h2>Visuals</h2>
    <h3>Missing Heatmap</h3><img src="data:image/png;base64,{base64_missing_heatmap}">
    <h3>Missing Bar Chart</h3><img src="data:image/png;base64,{base64_missing_bar}">
    <h3>Skewness</h3><img src="data:image/png;base64,{base64_skewness}">
    <h3>Correlation Matrix</h3><img src="data:image/png;base64,{base64_corr}">
    </body></html>"""
    with open("audit_report.html", "w", encoding="utf-8") as f:
        f.write(html_template)

def run_audit(file_path, save_dir="auditflow_output"):
    file_path = os.path.abspath(file_path)  # Fixed for Colab & PyPI compatibility

    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    os.chdir(save_dir)

    df = load_dataset(file_path)
    nulls = missing_values_analysis(df)
    general_results = general_quality_checks(df)
    memory_used = correlation_and_memory(df)
    summary = generate_summary(nulls, general_results, memory_used)
    export_html_report(summary)

    print("Audit complete. Outputs saved in:", save_dir)
