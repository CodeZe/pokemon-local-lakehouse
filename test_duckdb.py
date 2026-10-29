import duckdb

con = duckdb.connect()
# Install and load the Iceberg extension dynamically
con.execute("INSTALL iceberg; LOAD iceberg;")

# Query the Gold layer directly from your disk files
query = """
    SELECT * FROM iceberg_scan('data/iceberg_warehouse/default/fct_pokemon_metrics') 
    LIMIT 5;
"""
print(con.execute(query).df())
