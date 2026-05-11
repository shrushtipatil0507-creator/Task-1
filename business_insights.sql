-- Superstore SQL pack (works on table: superstore_sales)
-- Recommended schema uses snake_case columns matching cleaned CSV.

-- 1) Total Revenue and Profit
SELECT
    SUM(sales) AS total_revenue,
    SUM(profit) AS total_profit,
    ROUND((SUM(profit) / NULLIF(SUM(sales), 0)) * 100, 2) AS profit_margin_pct
FROM superstore_sales;

-- 2) Total Orders, Total Customers, AOV
SELECT
    COUNT(DISTINCT order_id) AS total_orders,
    COUNT(DISTINCT customer_id) AS total_customers,
    ROUND(SUM(sales) / NULLIF(COUNT(DISTINCT order_id), 0), 2) AS average_order_value
FROM superstore_sales;

-- 3) Monthly Revenue Trend
SELECT
    DATE_TRUNC('month', order_date) AS order_month,
    SUM(sales) AS monthly_revenue,
    SUM(profit) AS monthly_profit
FROM superstore_sales
GROUP BY 1
ORDER BY 1;

-- 4) Top 10 Customers by Revenue
SELECT
    customer_id,
    customer_name,
    SUM(sales) AS customer_revenue,
    SUM(profit) AS customer_profit
FROM superstore_sales
GROUP BY customer_id, customer_name
ORDER BY customer_revenue DESC
LIMIT 10;

-- 5) Top 10 Products by Revenue
SELECT
    product_id,
    product_name,
    category,
    sub_category,
    SUM(sales) AS product_revenue,
    SUM(profit) AS product_profit
FROM superstore_sales
GROUP BY product_id, product_name, category, sub_category
ORDER BY product_revenue DESC
LIMIT 10;

-- 6) Category Performance
SELECT
    category,
    SUM(sales) AS revenue,
    SUM(profit) AS profit,
    ROUND((SUM(profit) / NULLIF(SUM(sales), 0)) * 100, 2) AS profit_margin_pct
FROM superstore_sales
GROUP BY category
ORDER BY revenue DESC;

-- 7) Sub-category Risk View (high revenue but low/negative profit)
SELECT
    sub_category,
    SUM(sales) AS revenue,
    SUM(profit) AS profit
FROM superstore_sales
GROUP BY sub_category
HAVING SUM(sales) > 50000
ORDER BY profit ASC;

-- 8) Region Performance
SELECT
    region,
    SUM(sales) AS revenue,
    SUM(profit) AS profit,
    COUNT(DISTINCT order_id) AS orders
FROM superstore_sales
GROUP BY region
ORDER BY revenue DESC;

-- 9) Discount Impact on Profitability
SELECT
    ROUND(discount, 2) AS discount_band,
    AVG(profit) AS avg_profit,
    SUM(sales) AS sales_volume,
    COUNT(*) AS line_items
FROM superstore_sales
GROUP BY ROUND(discount, 2)
ORDER BY discount_band;

-- 10) Month-over-Month Growth in Revenue
WITH monthly AS (
    SELECT
        DATE_TRUNC('month', order_date) AS order_month,
        SUM(sales) AS revenue
    FROM superstore_sales
    GROUP BY 1
)
SELECT
    order_month,
    revenue,
    LAG(revenue) OVER (ORDER BY order_month) AS previous_month_revenue,
    ROUND(
        ((revenue - LAG(revenue) OVER (ORDER BY order_month))
        / NULLIF(LAG(revenue) OVER (ORDER BY order_month), 0)) * 100,
        2
    ) AS mom_growth_pct
FROM monthly
ORDER BY order_month;
