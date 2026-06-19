import os
import json

def get_effectiveness_phrase(multiplier):
    if multiplier == 2.0:
        return "it was super effective."
    elif multiplier == 0.5:
        return "it was not very effective."
    elif multiplier == 0.0:
        return "it had no effect."
    return "it was effective."

def generate_qa(output_path, base_dir):
    data_dir = os.path.join(base_dir, "data")
    
    # Load data
    with open(os.path.join(data_dir, "common_pokemon.json"), "r", encoding="utf-8") as f:
        pokedex = json.load(f)
    
    with open(os.path.join(data_dir, "moves.json"), "r", encoding="utf-8") as f:
        moves = json.load(f)
        
    with open(os.path.join(data_dir, "type_chart.json"), "r", encoding="utf-8") as f:
        type_chart = json.load(f)
        
    all_types = ["Normal", "Fire", "Water", "Grass", "Electric", "Ice", "Fighting", "Poison", "Ground", "Flying", "Psychic", "Bug", "Rock", "Ghost", "Dragon"]
        
    qa_list = []
    
    # 1. Pokemon Typing
    for pkmn, types in pokedex.items():
        primary_type = types[0]
        qa_list.append(f"fact {pkmn} type is {primary_type}")
        qa_list.append(f"query {pkmn} type answer {primary_type}")
        
    # 2. Move Typing
    for move, data in moves.items():
        qa_list.append(f"fact {move} type is {data['type']}")
        qa_list.append(f"query {move} type answer {data['type']}")
        
    # 3. Type Matchups
    for atk_type in all_types:
        for def_type in all_types:
            mult = type_chart.get(atk_type, {}).get(def_type, 1.0)
            phrase = get_effectiveness_phrase(mult)
            qa_list.append(f"fact {atk_type} type against {def_type} type {phrase}")
            qa_list.append(f"query {atk_type} type against {def_type} type answer {phrase}")
            
    # Duplicate the dataset so it holds weight against the 20,000 battles during training
    # There are ~200 pkmn, ~100 moves, ~225 matchups = ~525 queries.
    # 525 * 10 = 5,250 tokens
    qa_list = qa_list * 10
    
    with open(output_path, "w", encoding="utf-8") as f:
        for qa in qa_list:
            f.write(qa.lower() + "\n")
            
    print(f"Generated {len(qa_list)} Johnny Q&A facts at {output_path}")

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    out_path = os.path.join(base_dir, "corpus", "johnny_corpus.txt")
    generate_qa(out_path, base_dir)
