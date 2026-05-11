"""Data cleaning + EDA pipeline for Sample Superstore dataset."""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def load_data(input_path: Path) -> pd.DataFrame:
    """Load CSV data with robust encoding handling."""
    try:
        return pd.read_csv(input_path, encoding="latin1")
    except FileNotFoundError as exc:
        raise FileNotFoundError(f"Input file not found: {input_path}") from exc


def standardize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Normalize column names for easier analysis and SQL alignment."""
    rename_map = {
        "Row ID": "row_id",
        "Order ID": "order_id",
        "Order Date": "order_date",
        "Ship Date": "ship_date",
        "Ship Mode": "ship_mode",
        "Customer ID": "customer_id",
        "Customer Name": "customer_name",
        "Segment": "segment",
        "Country/Region": "country_region",
        "City": "city",
        "State/Province": "state_province",
        "Postal Code": "postal_code",
        "Region": "region",
        "Product ID": "product_id",
        "Category": "category",
        "Sub-Category": "sub_category",
        "Product Name": "product_name",
        "Sales": "sales",
        "Quantity": "quantity",
        "Discount": "discount",
        "Profit": "profit",
    }
    return df.rename(columns=rename_map)


def clean_data(df: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    """Apply cleaning rules and return cleaned data + quality summary."""
    qc = {}
    qc["shape_before"] = tuple(df.shape)

    # Strip whitespace in text columns to remove formatting inconsistencies.
    obj_cols = df.select_dtypes(include=["object", "string"]).columns
    for col in obj_cols:
        df[col] = df[col].astype(str).str.strip()

    # Date conversion.
    df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")
    df["ship_date"] = pd.to_datetime(df["ship_date"], errors="coerce")

    # Numeric conversion.
    for col in ["sales", "quantity", "discount", "profit", "postal_code"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    qc["null_summary"] = df.isna().sum().to_dict()

    # Drop exact duplicates.
    duplicates = int(df.duplicated().sum())
    df = df.drop_duplicates().copy()
    qc["duplicates_removed"] = duplicates

    # Fill limited missing values with business-safe defaults.
    df["postal_code"] = df["postal_code"].fillna(0).astype("int64")
    df["ship_mode"] = df["ship_mode"].fillna("Unknown")

    # Outlier detection by IQR (flag only, do not remove by default).
    q1 = df["sales"].quantile(0.25)
    q3 = df["sales"].quantile(0.75)
    iqr = q3 - q1
    lower, upper = q1 - 1.5 * iqr, q3 + 1.5 * iqr
    df["sales_outlier_flag"] = ((df["sales"] < lower) | (df["sales"] > upper)).astype(int)
    qc["sales_outliers"] = int(df["sales_outlier_flag"].sum())

    # Build monthly fields for trend analysis.
    df["order_year"] = df["order_date"].dt.year
    df["order_month"] = df["order_date"].dt.to_period("M").astype(str)

    qc["shape_after"] = tuple(df.shape)
    return df, qc


def eda_outputs(df: pd.DataFrame, output_dir: Path) -> dict:
    """Create EDA summaries and save visuals."""
    output_dir.mkdir(parents=True, exist_ok=True)
    plots_dir = output_dir / "plots"
    plots_dir.mkdir(parents=True, exist_ok=True)

    kpis = {}
    kpis["total_revenue"] = float(df["sales"].sum())
    kpis["total_profit"] = float(df["profit"].sum())
    kpis["total_orders"] = int(df["order_id"].nunique())
    kpis["total_customers"] = int(df["customer_id"].nunique())
    kpis["average_order_value"] = float(df.groupby("order_id")["sales"].sum().mean())
    kpis["profit_margin_pct"] = float((df["profit"].sum() / df["sales"].sum()) * 100)

    monthly = df.groupby("order_month", as_index=False).agg(
        revenue=("sales", "sum"), profit=("profit", "sum")
    )
    category = df.groupby("category", as_index=False).agg(
        revenue=("sales", "sum"), profit=("profit", "sum")
    )
    top_products = (
        df.groupby(["product_id", "product_name"], as_index=False)
        .agg(revenue=("sales", "sum"), profit=("profit", "sum"))
        .sort_values("revenue", ascending=False)
        .head(10)
    )

    monthly.to_csv(output_dir / "monthly_revenue_profit.csv", index=False)
    category.to_csv(output_dir / "category_performance.csv", index=False)
    top_products.to_csv(output_dir / "top_products.csv", index=False)

    sns.set_theme(style="whitegrid")

    plt.figure(figsize=(12, 5))
    plt.plot(monthly["order_month"], monthly["revenue"], marker="o")
    plt.xticks(rotation=60)
    plt.title("Monthly Revenue Trend")
    plt.tight_layout()
    plt.savefig(plots_dir / "monthly_revenue_trend.png", dpi=150)
    plt.close()

    plt.figure(figsize=(8, 5))
    sns.barplot(data=category.sort_values("revenue", ascending=False), x="category", y="revenue")
    plt.title("Revenue by Category")
    plt.tight_layout()
    plt.savefig(plots_dir / "category_revenue.png", dpi=150)
    plt.close()

    plt.figure(figsize=(8, 5))
    sns.histplot(df["sales"], bins=40, kde=True)
    plt.title("Sales Distribution")
    plt.tight_layout()
    plt.savefig(plots_dir / "sales_distribution.png", dpi=150)
    plt.close()

    return kpis


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    input_csv = root / "data" / "raw" / "samplesuperstore.csv"
    processed_dir = root / "data" / "processed"
    reports_dir = root / "reports"

    df = load_data(input_csv)
    df = standardize_columns(df)
    cleaned_df, qc_summary = clean_data(df)

    processed_dir.mkdir(parents=True, exist_ok=True)
    cleaned_df.to_csv(processed_dir / "superstore_cleaned.csv", index=False)

    kpi_summary = eda_outputs(cleaned_df, reports_dir)

    (reports_dir / "data_quality_summary.json").write_text(
        json.dumps(qc_summary, indent=2), encoding="utf-8"
    )
    (reports_dir / "kpi_summary.json").write_text(json.dumps(kpi_summary, indent=2), encoding="utf-8")

    print("Pipeline complete. Cleaned data and reports generated.")


if __name__ == "__main__":
    main()
