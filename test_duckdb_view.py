import duckdb

# Connect to a local file or temporary memory database
con = duckdb.connect()
con.execute("INSTALL iceberg; LOAD iceberg;")

# 1. REGISTER THE FILE PATH TO A CLEAN VIEW NAME
con.execute("""
    CREATE VIEW fct_pokemon_metrics AS 
    SELECT * FROM iceberg_scan('data/iceberg_warehouse/default/fct_pokemon_metrics');
""")

# 2. NOW YOU CAN QUERY IT USING STANDARD SQL!
query = "SELECT * FROM fct_pokemon_metrics LIMIT 5;"
print(con.execute(query).df())
