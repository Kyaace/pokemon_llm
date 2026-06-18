import json
import random
import os

def load_json(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)

# Load data
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(os.path.dirname(BASE_DIR), "data")

POKEMON_TYPES = load_json(os.path.join(DATA_DIR, "common_pokemon.json"))
MOVES = load_json(os.path.join(DATA_DIR, "moves.json"))
TYPE_CHART = load_json(os.path.join(DATA_DIR, "type_chart.json"))

def get_effectiveness_multiplier(move_type, defender_types):
    """Calculates the total damage multiplier taking dual-types into account."""
    multiplier = 1.0
    for def_type in defender_types:
        if move_type in TYPE_CHART and def_type in TYPE_CHART[move_type]:
            multiplier *= TYPE_CHART[move_type][def_type]
    return multiplier

def generate_tutorial_corpus(num_samples: int, output_path: str):
    """Generates synthetic, mathematically sound tutorial battles."""
    pokemon_names = list(POKEMON_TYPES.keys())
    
    with open(output_path, "w", encoding="utf-8") as f:
        for _ in range(num_samples):
            attacker = random.choice(pokemon_names)
            defender = random.choice(pokemon_names)
            
            # Simple heuristic: Attacker uses a move matching one of its types, or a Normal type move.
            attacker_types = POKEMON_TYPES[attacker]
            
            # Find valid moves
            valid_moves = []
            for m_name, m_data in MOVES.items():
                if m_data["type"] in attacker_types or m_data["type"] == "Normal":
                    valid_moves.append(m_name)
                    
            if not valid_moves:
                # Fallback just in case
                valid_moves = [m_name for m_name, m_data in MOVES.items() if m_data["type"] == "Normal"]
            
            move = random.choice(valid_moves)
            move_type = MOVES[move]["type"]
            defender_types = POKEMON_TYPES[defender]
            
            multiplier = get_effectiveness_multiplier(move_type, defender_types)
            
            # Map multiplier to phrase
            if multiplier > 1.0:
                phrase = "was super effective"
            elif multiplier == 1.0:
                phrase = "was effective"
            elif multiplier > 0.0:
                phrase = "was not very effective"
            else:
                phrase = "had no effect"
                
            battle_string = f"{attacker} used {move} against {defender}. It {phrase}."
            f.write(battle_string + "\n")

if __name__ == "__main__":
    output_dir = os.path.join(os.path.dirname(BASE_DIR), "corpus")
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, "tutorial_corpus.txt")
    
    print(f"Generating 500 tutorial battles to {output_file}...")
    random.seed(42)
    generate_tutorial_corpus(500, output_file)
    print("Generation complete!")
