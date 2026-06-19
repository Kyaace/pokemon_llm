import os
import json
import urllib.request
import time
from collections import defaultdict

def research_moves():
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    moves_path = os.path.join(base_dir, "data", "moves.json")
    
    with open(moves_path, "r", encoding="utf-8") as f:
        existing_moves = json.load(f)
        
    print(f"Existing moves: {len(existing_moves)}")
    
    # We will fetch all pokemon 1-251 to map move -> list of learners
    # We also fetch the moves themselves to get power and type.
    
    move_to_learners = defaultdict(list)
    pokemon_to_moves = defaultdict(list)
    
    print("Fetching Pokemon move data from PokeAPI...")
    for i in range(1, 252):
        url = f"https://pokeapi.co/api/v2/pokemon/{i}/"
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as response:
                data = json.loads(response.read().decode())
                
                name = data["name"].title()
                if name == "Mr-Mime": name = "Mr. Mime"
                if name == "Nidoran-F": name = "Nidoran♀"
                if name == "Nidoran-M": name = "Nidoran♂"
                if name == "Farfetchd": name = "Farfetch'd"
                
                for move_obj in data.get("moves", []):
                    # We only consider moves that are from generation-1 or generation-2 (id <= 251 in PokeAPI typically)
                    move_name = move_obj["move"]["name"]
                    move_to_learners[move_name].append(name)
                    pokemon_to_moves[name].append(move_name)
                    
            if i % 50 == 0:
                print(f"Fetched {i}/251 pokemon...")
            time.sleep(0.02)
        except Exception as e:
            print(f"Failed to fetch {i}: {e}")
            
    print(f"Total unique moves found across 251 pokemon: {len(move_to_learners)}")
    
    # Fetch move powers
    print("Fetching Move powers...")
    move_details = {}
    
    count = 0
    for move_name in list(move_to_learners.keys()):
        url = f"https://pokeapi.co/api/v2/move/{move_name}/"
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as response:
                data = json.loads(response.read().decode())
                
                power = data.get("power")
                move_type = data["type"]["name"].title()
                generation = data["generation"]["name"]
                
                if generation in ["generation-i", "generation-ii"]:
                    move_details[move_name] = {
                        "power": power,
                        "type": move_type
                    }
                
        except Exception as e:
            # Maybe it's a newer move, ignore
            pass
            
        count += 1
        if count % 50 == 0:
            print(f"Fetched {count} move details...")
        time.sleep(0.02)
        
    # Filter 1: Has Power (Damaging)
    damaging_moves = {m: d for m, d in move_details.items() if d["power"] is not None and d["power"] > 0}
    print(f"Damaging moves (Gen 1/2): {len(damaging_moves)}")
    
    # Filter 2: Not a signature move (Learned by > 1 pokemon)
    non_signature_damaging = {}
    for m, d in damaging_moves.items():
        if len(move_to_learners[m]) > 1:
            non_signature_damaging[m] = d
            
    print(f"Damaging + Non-Signature moves: {len(non_signature_damaging)}")
    
    # How many are new?
    existing_normalized = [k.lower().replace(" ", "-") for k in existing_moves.keys()]
    new_moves = []
    for m in non_signature_damaging.keys():
        if m not in existing_normalized:
            new_moves.append(m)
            
    print(f"\nNEW moves to add: {len(new_moves)}")
    print("Sample of new moves:", new_moves[:20])
    
    # Check for pokemon with no moves in the filtered list
    valid_moves_set = set(non_signature_damaging.keys()) | set(existing_normalized)
    
    empty_pokemon = []
    for pkmn, moves in pokemon_to_moves.items():
        has_damaging = False
        for m in moves:
            if m in valid_moves_set:
                has_damaging = True
                break
        if not has_damaging:
            empty_pokemon.append(pkmn)
            
    print(f"\nPokemon with ZERO damaging moves: {len(empty_pokemon)}")
    for pkmn in empty_pokemon:
        print(f"  {pkmn} (Original moves: {pokemon_to_moves[pkmn]})")

if __name__ == "__main__":
    research_moves()
