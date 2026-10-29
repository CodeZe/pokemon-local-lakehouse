import duckdb

# Connect to a temporary local memory database
con = duckdb.connect()

# Crucial: Install and load the extension so DuckDB knows how to parse Iceberg metadata
con.execute("INSTALL iceberg; LOAD iceberg;")

print("Querying and Joining Local Iceberg Fact & Dimension Tables...\n")

# This standard SQL query joins the two physical directories on disk using iceberg_scan
query = """
    SELECT 
        t.type_name AS pokemon_type,
        COUNT(DISTINCT f.pokemon_id) AS total_pokemon,
        ROUND(AVG(f.base_experience), 1) AS avg_base_experience,
        ROUND(AVG(f.weight), 1) AS avg_weight
    FROM iceberg_scan('data/iceberg_warehouse/default/fct_pokemon_metrics') f
    JOIN iceberg_scan('data/iceberg_warehouse/default/dim_pokemon_types') t
      ON f.pokemon_id = t.pokemon_id
    GROUP BY t.type_name
    ORDER BY avg_base_experience DESC;
"""

# Execute the query and print it out nicely as a Pandas DataFrame
df_result = con.execute(query).df()
print(df_result)
