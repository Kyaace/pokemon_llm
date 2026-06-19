import requests
import json
import os

def fetch_evolutions():
    evolutions = {}
    
    # Pre-populate 1 to 251 with empty lists just in case
    for i in range(1, 252):
        # We need the species name for initialization, but we will let the API populate it.
        pass

    print("Fetching evolution chains from PokeAPI...")
    # PokeAPI has around 130-150 evolution chains for Gen 1 & Gen 2. Let's just fetch up to 100 chains (which covers way past gen 2)
    # Actually, some chains might be skipped or sparse. Let's fetch 1 to 100 chains and filter for Gen 1/2.
    for chain_id in range(1, 150):
        try:
            res = requests.get(f"https://pokeapi.co/api/v2/evolution-chain/{chain_id}/")
            if res.status_code != 200:
                continue
                
            chain_data = res.json()["chain"]
            
            def parse_chain(node):
                species_name = node["species"]["name"]
                
                # We only care about Gen 1/Gen 2 pokemon, so we just add everyone to the dict and filter later
                if species_name not in evolutions:
                    evolutions[species_name] = []
                    
                for evolves_to_node in node.get("evolves_to", []):
                    next_species = evolves_to_node["species"]["name"]
                    evolutions[species_name].append(next_species)
                    # Recursive call
                    parse_chain(evolves_to_node)
                    
            parse_chain(chain_data)
        except Exception as e:
            print(f"Failed to parse chain {chain_id}: {e}")
            
    # Some pokemon might not be in an evolution chain? No, all pokemon belong to a chain, even if it's just them.
    # To be perfectly safe, let's also fetch pokemon-species 1 to 251 and ensure they're in the dict.
    print("Ensuring all Gen 1 & 2 Pokemon are accounted for...")
    for i in range(1, 252):
        try:
            res = requests.get(f"https://pokeapi.co/api/v2/pokemon-species/{i}/")
            if res.status_code == 200:
                species_name = res.json()["name"]
                if species_name not in evolutions:
                    evolutions[species_name] = []
        except:
            pass

    # Save to data directory
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    out_path = os.path.join(base_dir, "data", "evolutions.json")
    with open(out_path, "w") as f:
        json.dump(evolutions, f, indent=4)
        
    print(f"Saved {len(evolutions)} evolution lines to {out_path}")

if __name__ == "__main__":
    fetch_evolutions()
