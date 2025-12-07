# Databricks notebook source
# MAGIC %md
# MAGIC **Import Required Libraries**

# COMMAND ----------

from pyspark.sql import functions as F

# COMMAND ----------

# MAGIC %md
# MAGIC **Define start and end dates**

# COMMAND ----------

# start date and end date
start_date = "2024-01-01"
end_date   = "2025-12-01"

# COMMAND ----------

# 1️⃣ Generate one row per month start between start_date and end_date
df = (
    spark.sql(f"""
        SELECT explode(
            sequence(
                to_date('{start_date}'),
                to_date('{end_date}'),
                interval 1 month
            )
        ) AS month_start_date
    """)
)


# 2️⃣ Add useful analytics columns
df = (
    df
    # Surrogate key at month grain
    .withColumn("date_key", F.date_format("month_start_date", "yyyyMM").cast("int"))
    .withColumn("year", F.year("month_start_date"))
    .withColumn("month_name", F.date_format("month_start_date", "MMMM"))
    .withColumn("month_short_name", F.date_format("month_start_date", "MMM"))
    .withColumn("quarter", F.concat(F.lit("Q"), F.quarter("month_start_date")))
    .withColumn("year_quarter", F.concat(F.col("year"), F.lit("-Q"), F.quarter("month_start_date")))
)

# COMMAND ----------

display(df)

# COMMAND ----------

# Save as a table
df.write \
    .mode("overwrite") \
    .format("delta") \
    .saveAsTable("fmcg.gold.dim_date")