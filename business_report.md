# Data Analytics Task-1 Business Report

## Executive Summary
This project analyzes a Kaggle Sample Superstore dataset to identify revenue trends, profitability drivers, customer/product performance, and strategic growth opportunities. The analysis covers data cleaning, exploratory analytics, SQL insight queries, KPI design, and dashboard planning for decision-makers.

## Problem Statement
The business needs a structured view of sales and profitability performance across time, products, customers, and regions to improve growth and reduce margin leakage.

## Dataset Overview
- Source: Kaggle (`himanshuuike/superstore-sales-dataset`)
- Records: 10,194
- Unique Orders: 5,111
- Unique Customers: 804
- Core fields: order dates, customer/segment, region/location, category/sub-category, sales, quantity, discount, profit

## Methodology
1. Loaded and profiled the raw CSV.
2. Standardized column names and formats.
3. Converted date/numeric columns and validated nulls/duplicates.
4. Flagged outliers via IQR (sales).
5. Performed EDA for trend, category, and distribution analysis.
6. Wrote reusable SQL for KPI and business questions.
7. Designed dashboard blueprints for business teams.

## Data Cleaning Summary
- Missing values: Checked all columns and documented null count.
- Duplicates: Checked and removed exact duplicates if present.
- Data types: Fixed date and numeric fields for reliable analysis.
- Standardization: Trimmed whitespace and normalized schema (snake_case).
- Outliers: Flagged extreme sales values (kept for business reality unless requested).

## Key KPI Results
- Total Revenue: 2,326,534.35
- Total Profit: 292,296.81
- Total Orders: 5,111
- Total Customers: 804
- Average Order Value (AOV): 455.20
- Overall Profit Margin: 12.56%

## EDA Findings
1. **Category Contribution**: Technology is the top revenue category, followed by Furniture and Office Supplies.
2. **Top Sub-Categories**: Chairs and Phones lead sales; these should remain strategic focus areas.
3. **Seasonality Signal**: Highest month in dataset timeline is 2026-11; lowest month is 2023-02.
4. **Long-tail Mix**: Fasteners and Labels contribute low revenue, indicating possible catalog optimization opportunities.
5. **Discount Risk**: Discount levels require closer control because aggressive discounting can hurt profit.

## Business Insights
### Key Trends
- Revenue concentration is visible in a few high-performing sub-categories (e.g., Chairs, Phones).
- Monthly performance varies significantly, indicating demand seasonality.

### Business Risks
- Margin leakage risk in categories/products with high sales but low/negative profit.
- Dependence on a small number of product lines can increase volatility.

### Growth Opportunities
- Expand winning categories through inventory and targeted campaigns.
- Increase cross-sell opportunities in Office Supplies bundles.
- Use regional personalization where conversion and profit are strongest.

### Actionable Recommendations
1. Set discount guardrails by product margin bands.
2. Run a quarterly profitability review at sub-category level.
3. Prioritize top 20% customers for retention programs.
4. Build demand forecasting for seasonal peaks and troughs.

## Final Conclusion
The business is healthy in topline terms, but sustained profit growth depends on better discount discipline, granular product profitability monitoring, and stronger customer retention strategy.
