import os
import json
import urllib.request
import time

def fetch_stats():
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    moves_path = os.path.join(base_dir, "data", "moves.json")
    out_path = os.path.join(base_dir, "data", "pokemon_stats.json")
    
    # Load valid moves
    with open(moves_path, "r", encoding="utf-8") as f:
        known_moves = json.load(f)
        
    # Create mapping from pokeapi format to our format
    # e.g., "quick-attack" -> "Quick Attack"
    pokeapi_to_local_move = {k.lower().replace(" ", "-"): k for k in known_moves.keys()}
    
    stats_data = {}
    
    print("Fetching Pokemon stats and moves from PokeAPI...")
    
    for i in range(1, 252):
        url = f"https://pokeapi.co/api/v2/pokemon/{i}/"
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as response:
                data = json.loads(response.read().decode())
                
                name = data["name"].title()
                
                # Special cases to match our pokedex
                if name == "Mr-Mime": name = "Mr. Mime"
                if name == "Nidoran-F": name = "Nidoran♀"
                if name == "Nidoran-M": name = "Nidoran♂"
                if name == "Farfetchd": name = "Farfetch'd"
                
                # Extract HP
                hp = 100
                for stat in data.get("stats", []):
                    if stat["stat"]["name"] == "hp":
                        hp = stat["base_stat"]
                        break
                        
                # Extract Moves
                filtered_moves = []
                for move_obj in data.get("moves", []):
                    move_name = move_obj["move"]["name"]
                    if move_name in pokeapi_to_local_move:
                        filtered_moves.append(pokeapi_to_local_move[move_name])
                        
                # Manual Struggle Overrides for the pacifists
                if name in ["Ditto", "Wobbuffet", "Smeargle"]:
                    if "Struggle" not in filtered_moves:
                        filtered_moves.append("Struggle")
                        
                stats_data[name] = {
                    "hp": hp,
                    "moves": list(set(filtered_moves)) # Deduplicate just in case
                }
                
                if i % 50 == 0:
                    print(f"Fetched {i}/251...")
                    
                time.sleep(0.05) # Be polite
        except Exception as e:
            print(f"Failed to fetch {i}: {e}")
            
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(stats_data, f, indent=4)
        
    print(f"Saved stats and moves for {len(stats_data)} Pokemon to {out_path}!")

if __name__ == "__main__":
    fetch_stats()
