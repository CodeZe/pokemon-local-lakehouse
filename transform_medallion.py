import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, explode

# Spark Session fully optimized with the matching 1.5.2 runtime package string
spark = SparkSession.builder \
    .appName("PokemonMedallion") \
    .master("local[*]") \
    .config("spark.driver.memory", "2g") \
    .config("spark.jars.packages", "org.apache.iceberg:iceberg-spark-runtime-3.5_2.12:1.5.2") \
    .config("spark.sql.extensions", "org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions") \
    .config("spark.sql.catalog.local_catalog", "org.apache.iceberg.spark.SparkCatalog") \
    .config("spark.sql.catalog.local_catalog.type", "hadoop") \
    .config("spark.sql.catalog.local_catalog.warehouse", "./data/iceberg_warehouse") \
    .getOrCreate()

print("Spark initialized. Reading Bronze Layer...")

# Read Bronze JSON Files
raw_df = spark.read.option("multiline", "true").json("data/bronze")

# TRANSFORM TO SILVER (Flatten and Clean)
silver_df = raw_df.select(
    col("id").alias("pokemon_id"),
    col("name"),
    col("base_experience"),
    col("height"),
    col("weight")
)

# Save as Silver Iceberg Table
silver_df.write.format("iceberg").mode("overwrite").saveAsTable("local_catalog.default.silver_pokemon")
print("Silver Layer saved to Iceberg!")

# TRANSFORM TO GOLD (Dimensions & Facts Star Schema)
types_df = raw_df.select(
    col("id").alias("pokemon_id"),
    explode("types").alias("type_entry")
).select(
    col("pokemon_id"),
    col("type_entry.type.name").alias("type_name")
)

types_df.write.format("iceberg").mode("overwrite").saveAsTable("local_catalog.default.dim_pokemon_types")

fact_df = silver_df.select("pokemon_id", "base_experience", "height", "weight")
fact_df.write.format("iceberg").mode("overwrite").saveAsTable("local_catalog.default.fct_pokemon_metrics")

print("Gold Layer Star Schema saved to Iceberg!")
spark.stop()