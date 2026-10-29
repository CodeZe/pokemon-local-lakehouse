import json
import os
import requests

BRONZE_DIR = "data/bronze"
os.makedirs(BRONZE_DIR, exist_ok=True)

print("Fetching Pokémon data from API...")
for pokemon_id in range(1, 51):
    # FIXED: Added the mandatory API path context here
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}/"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        with open(
            f"{BRONZE_DIR}/pokemon_{pokemon_id}.json", "w", encoding="utf-8"
        ) as f:
            json.dump(data, f)
        print(f"Successfully fetched ID {pokemon_id}")
    else:
        print(f"Failed to fetch ID {pokemon_id}: Status {response.status_code}")

print(f"\nBronze Layer complete: Raw JSON files saved to {BRONZE_DIR}/")
