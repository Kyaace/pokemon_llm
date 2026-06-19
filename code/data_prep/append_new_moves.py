import os
import json
import urllib.request
import time
from collections import defaultdict

def append_new_moves():
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    moves_path = os.path.join(base_dir, "data", "moves.json")
    
    with open(moves_path, "r", encoding="utf-8") as f:
        existing_moves = json.load(f)
        
    print(f"Loaded {len(existing_moves)} existing moves.")
    
    # 1. First fetch all 1-251 pokemon to find non-signature damaging moves
    move_to_learners = defaultdict(list)
    print("Fetching learners for Gen 1/2...")
    for i in range(1, 252):
        url = f"https://pokeapi.co/api/v2/pokemon/{i}/"
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as response:
                data = json.loads(response.read().decode())
                for move_obj in data.get("moves", []):
                    move_name = move_obj["move"]["name"]
                    move_to_learners[move_name].append(data["name"])
            time.sleep(0.02)
        except Exception as e:
            pass

    # 2. Find powers for these moves
    print("Fetching move details...")
    move_details = {}
    for move_name in list(move_to_learners.keys()):
        url = f"https://pokeapi.co/api/v2/move/{move_name}/"
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as response:
                data = json.loads(response.read().decode())
                generation = data["generation"]["name"]
                
                if generation in ["generation-i", "generation-ii"]:
                    power = data.get("power")
                    acc = data.get("accuracy")
                    if acc is None: acc = 100
                    
                    move_details[move_name] = {
                        "type": data["type"]["name"].title(),
                        "power": power,
                        "miss_chance": 100 - acc
                    }
        except:
            pass
        time.sleep(0.02)
        
    # 3. Filter for non-signature damaging moves not in existing_moves
    existing_normalized = {k.lower().replace(" ", "-") for k in existing_moves.keys()}
    new_moves = {}
    
    for m, details in move_details.items():
        if details["power"] is not None and details["power"] > 0:
            if len(move_to_learners[m]) > 1:
                if m not in existing_normalized:
                    # Title case the name
                    title_name = m.replace("-", " ").title()
                    new_moves[title_name] = details
                    
    print(f"Adding {len(new_moves)} new damaging moves...")
    
    # Update existing moves with the new auto-fetched moves
    existing_moves.update(new_moves)
    
    # 4. Manually add special moves requested by user
    special_moves = {
        "Transform": {"type": "Normal", "power": 0, "miss_chance": 0},
        "Counter": {"type": "Fighting", "power": 0, "miss_chance": 0},
        "Sketch": {"type": "Normal", "power": 0, "miss_chance": 0},
        "Struggle": {"type": "Normal", "power": 30, "miss_chance": 0}
    }
    
    print(f"Adding special moves: {list(special_moves.keys())}")
    existing_moves.update(special_moves)
    
    # Save back to moves.json
    with open(moves_path, "w", encoding="utf-8") as f:
        json.dump(existing_moves, f, indent=4)
        
    print(f"Successfully saved {len(existing_moves)} moves to {moves_path}!")

if __name__ == "__main__":
    append_new_moves()
