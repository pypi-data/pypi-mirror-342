"""
core.py – Main logic for the datainsightx package.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import base64
import warnings
import datetime
import json

warnings.filterwarnings("ignore")


def img_to_base64(img_path):
    with open(img_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode("utf-8")


def save_plot(fig, name, charts_dir="insight_charts"):
    os.makedirs(charts_dir, exist_ok=True)
    fig.savefig(os.path.join(charts_dir, name), bbox_inches="tight")
    plt.close(fig)


def load_dataset(file_path):
    df = pd.read_csv(file_path)
    print("Loaded:", file_path, "| Shape:", df.shape)
    return df


def infer_columns(df):
    date_col, value_col, category_col = None, None, None

    for col in df.columns:
        if 'date' in col.lower() or 'time' in col.lower():
            try:
                df[col] = pd.to_datetime(df[col])
                date_col = col
                break
            except:
                continue

    num_cols = df.select_dtypes(include=np.number).columns
    if len(num_cols) >= 1:
        value_col = num_cols[0]

    for col in df.select_dtypes(include='object').columns:
        if df[col].nunique() < 50:
            category_col = col
            break

    return df, date_col, value_col, category_col


def compute_kpis(df, date_col, value_col, category_col):
    kpis = {}
    df = df.sort_values(by=date_col).copy()
    df.set_index(date_col, inplace=True)

    df_monthly = df[value_col].resample("M").sum()
    df_yoy = df[value_col].resample("Y").sum()

    kpis["total_value"] = round(df[value_col].sum(), 2)
    kpis["monthly_average"] = round(df_monthly.mean(), 2)
    kpis["max_month"] = str(df_monthly.idxmax().date())
    kpis["max_month_value"] = round(df_monthly.max(), 2)

    if df_monthly.shape[0] > 2:
        kpis["avg_mom_pct_change"] = round(df_monthly.pct_change().mean() * 100, 2)
    if df_yoy.shape[0] > 1:
        kpis["avg_yoy_pct_change"] = round(df_yoy.pct_change().mean() * 100, 2)

    if category_col:
        top = df.groupby(category_col)[value_col].sum().sort_values(ascending=False).head(5)
        kpis[f"top_5_{category_col}"] = top.to_dict()

    return kpis, df_monthly, df, category_col


def plot_monthly_trend(df_monthly, value_col):
    fig, ax = plt.subplots(figsize=(10, 5))
    df_monthly.plot(ax=ax, marker='o')
    ax.set_title("Monthly Trend")
    ax.set_ylabel(value_col)
    ax.grid(True)
    save_plot(fig, "monthly_trend.png")


def plot_category_bar(df, category_col, value_col):
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(data=df.reset_index(), x=category_col, y=value_col, estimator=np.sum, ci=None, ax=ax)
    ax.set_title(f"{value_col} by {category_col}")
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
    save_plot(fig, "category_plot.png")


def export_summary_txt(kpis):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lines = [f"# KPI Summary (Generated on {timestamp})\n"]

    for key, val in kpis.items():
        if isinstance(val, dict):
            lines.append(f"- {key}:")
            for subk, subv in val.items():
                lines.append(f"    • {subk}: {round(subv, 2)}")
        else:
            lines.append(f"- {key}: {val}")

    with open("insight_summary.txt", "w") as f:
        f.write("\n".join(lines))

    return "\n".join(lines)


def export_json(kpis):
    def convert(o):
        if isinstance(o, (np.integer, np.floating)):
            return o.item()
        elif isinstance(o, np.ndarray):
            return o.tolist()
        elif isinstance(o, datetime.date):
            return o.isoformat()
        return str(o)

    cleaned_kpis = json.loads(json.dumps(kpis, default=convert))
    with open("insight_kpis.json", "w") as f:
        json.dump(cleaned_kpis, f, indent=4)


def export_html(summary_text):
    trend_img = img_to_base64("insight_charts/monthly_trend.png")
    cat_img = img_to_base64("insight_charts/category_plot.png") if os.path.exists("insight_charts/category_plot.png") else ""

    html = f"""
    <html><head><title>Insight Report</title><style>
    body {{ font-family: Arial; padding: 20px; }}
    h1, h2 {{ color: #2c3e50; }}
    img {{ max-width: 100%; margin: 10px 0; }}
    pre {{ background: #f8f8f8; padding: 10px; border: 1px solid #ddd; }}
    </style></head><body>
    <h1>Data Insight Report</h1>
    <h2>Summary</h2>
    <pre>{summary_text}</pre>
    <h2>Visuals</h2>
    <h3>Monthly Trend</h3>
    <img src="data:image/png;base64,{trend_img}">
    {"<h3>Top Categories</h3><img src='data:image/png;base64," + cat_img + "'>" if cat_img else ""}
    </body></html>
    """
    with open("insight_report.html", "w", encoding="utf-8") as f:
        f.write(html)


def run_insight(file_path, save_dir="insightx_output"):
    file_path = os.path.abspath(file_path)

    os.makedirs(save_dir, exist_ok=True)
    os.chdir(save_dir)

    df = load_dataset(file_path)
    df, date_col, value_col, category_col = infer_columns(df)

    if not all([date_col, value_col]):
        print("Error: Required columns not found. Ensure your data has at least one date column and one numeric column.")
        return

    kpis, df_monthly, df_sorted, cat_col = compute_kpis(df, date_col, value_col, category_col)
    plot_monthly_trend(df_monthly, value_col)
    if cat_col:
        plot_category_bar(df_sorted, cat_col, value_col)

    summary_text = export_summary_txt(kpis)
    export_json(kpis)
    export_html(summary_text)

    print("Insight report generated. Files saved in:", save_dir)
