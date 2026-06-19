import json
import os

def sort_moves():
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    moves_path = os.path.join(base_dir, "data", "moves.json")
    
    with open(moves_path, "r", encoding="utf-8") as f:
        moves = json.load(f)
        
    # Sort the dictionary by keys alphabetically
    sorted_moves = {k: moves[k] for k in sorted(moves.keys())}
    
    with open(moves_path, "w", encoding="utf-8") as f:
        json.dump(sorted_moves, f, indent=4)
        
    print(f"Successfully alphabetized {len(sorted_moves)} moves!")

if __name__ == "__main__":
    sort_moves()
