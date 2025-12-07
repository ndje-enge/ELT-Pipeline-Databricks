CREATE OR REPLACE VIEW fmcg.gold.vw_fact_orders_enriched AS (
    SELECT 
        fo.date,
        fo.product_code,
        fo.customer_code,

        -- Date attributes
        dd.date_key,
        dd.year,
        dd.month_name,
        dd.month_short_name,
        dd.quarter,
        dd.year_quarter,

        -- Customer attributes
        dc.customer,
        dc.market,
        dc.platform,
        dc.channel,

        -- Product attributes
        dp.division,
        dp.category,
        dp.product,
        dp.variant,

        -- Metrics
        fo.sold_quantity,
        gp.price_inr,

        -- Derived Metric: Amount
        (fo.sold_quantity * gp.price_inr) AS total_amount_inr
    
    FROM fmcg.gold.fact_orders fo

    -- Join with Date Dimension
    LEFT JOIN fmcg.gold.dim_date dd
           ON fo.date = dd.month_start_date

    -- Join with Customers
    LEFT JOIN fmcg.gold.dim_customers dc 
           ON fo.customer_code = dc.customer_code

    -- Join with Products
    LEFT JOIN fmcg.gold.dim_products dp 
           ON fo.product_code = dp.product_code

    -- Join with Price (year-based)
    LEFT JOIN fmcg.gold.dim_gross_price gp 
           ON fo.product_code = gp.product_code
          AND YEAR(fo.date) = gp.year
);


-- Preview
SELECT * FROM fmcg.gold.vw_fact_orders_enriched;