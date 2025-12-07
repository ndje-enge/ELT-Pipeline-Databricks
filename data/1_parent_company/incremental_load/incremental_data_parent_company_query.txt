COPY INTO fmcg.gold.fact_orders
FROM (
  SELECT 
    CAST(date AS DATE) AS date,
    product_code,
    customer_code,
    CAST(sold_quantity AS BIGINT) AS sold_quantity
  FROM '/Volumes/fmcg/gold/parent_incremental_data/fact_orders.csv'
)
FILEFORMAT = CSV
FORMAT_OPTIONS ('header' = 'true');