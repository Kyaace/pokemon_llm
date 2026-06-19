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

ATTENTION_TESTING_MOVES = ["Metronome", "Transform", "Sketch", "Encore", "Disable", "Mirror Move", "Hypnosis", "Sing", "Sleep Powder", "Rest", "Bind", "Wrap", "Dig", "Fly", "Fire Spin", "Copycat", "Bide"]

def generate_qa(output_path, base_dir, pokedex_files=["gen1_pokedex.json"]):
    data_dir = os.path.join(base_dir, "data")
    
    # Load data
    pokedex = {}
    for pf in pokedex_files:
        with open(os.path.join(data_dir, pf), "r", encoding="utf-8") as f:
            pokedex.update(json.load(f))
    
    with open(os.path.join(data_dir, "moves.json"), "r", encoding="utf-8") as f:
        moves = json.load(f)
        
    with open(os.path.join(data_dir, "type_chart.json"), "r", encoding="utf-8") as f:
        type_chart = json.load(f)
        
    all_types = ["Normal", "Fire", "Water", "Grass", "Electric", "Ice", "Fighting", "Poison", "Ground", "Flying", "Psychic", "Bug", "Rock", "Ghost", "Dragon"]
        
    # Load pokemon stats
    stats_path = os.path.join(data_dir, "pokemon_stats.json")
    pokemon_stats = {}
    if os.path.exists(stats_path):
        with open(stats_path, "r", encoding="utf-8") as f:
            pokemon_stats = json.load(f)
            
    # Load encounters
    encounters_path = os.path.join(data_dir, "encounters.json")
    encounters = {}
    if os.path.exists(encounters_path):
        with open(encounters_path, "r", encoding="utf-8") as f:
            encounters = json.load(f)

    # Convert dictionary into Q&A text pairs
    qa_list = []
    
    # 1. Type Mapping & Stats
    for pkmn, types in pokedex.items():
        # Type facts
        for t in types:
            qa_list.append(f"fact {pkmn} type is {t}")
            qa_list.append(f"query {pkmn} type is answer {t}")
            
        # Base HP facts
        hp = 100
        pkmn_title = pkmn.title()
        if pkmn_title in pokemon_stats:
            hp = pokemon_stats[pkmn_title].get("hp", 100)
            
        qa_list.append(f"fact {pkmn} base hp is {hp}")
        qa_list.append(f"query {pkmn} base hp is answer {hp}")
        
        # Moves facts
        if pkmn_title in pokemon_stats:
            moves_list = pokemon_stats[pkmn_title].get("moves", [])
            for move in moves_list:
                qa_list.append(f"fact {pkmn} has moves {move}")
                qa_list.append(f"query {pkmn} has moves answer {move}")
                
        # Encounters facts
        if pkmn_title in encounters:
            method = encounters[pkmn_title]
            qa_list.append(f"fact {pkmn} obtained from {method}")
            qa_list.append(f"query {pkmn} obtained from answer {method}")
        
    # 2. Move Typing & Power
    for move, data in moves.items():
        weight = 5 if move in ATTENTION_TESTING_MOVES else 1
        for _ in range(weight):
            qa_list.append(f"fact {move} type is {data['type']}")
            qa_list.append(f"query {move} type answer {data['type']}")
            qa_list.append(f"fact {move} power is {data.get('power', 0)}")
            qa_list.append(f"query {move} power answer {data.get('power', 0)}")
        
    # 3. Type Matchups
    for atk_type in all_types:
        for def_type in all_types:
            mult = type_chart.get(atk_type, {}).get(def_type, 1.0)
            phrase = get_effectiveness_phrase(mult)
            qa_list.append(f"fact {atk_type} type against {def_type} type {phrase}")
            qa_list.append(f"query {atk_type} type against {def_type} type answer {phrase}")
            
    # 4. Pokemon Moves
    moves_file = os.path.join(data_dir, "pokemon_moves.json")
    if os.path.exists(moves_file):
        with open(moves_file, "r", encoding="utf-8") as f:
            pokemon_moves = json.load(f)
        for pkmn, moves_list in pokemon_moves.items():
            moves_str = " ".join(moves_list)
            qa_list.append(f"fact {pkmn} has moves {moves_str}")
            qa_list.append(f"query {pkmn} has moves answer {moves_str}")
            
    # 5. Zero-Shot Move Effectiveness (full representation)
    rep_pkmn = {}
    for pkmn, p_types in pokedex.items():
        p_type = p_types[0]
        if p_type not in rep_pkmn:
            rep_pkmn[p_type] = pkmn

    for move, m_data in moves.items():
        m_type = m_data["type"]
        for p_type, pkmn in rep_pkmn.items():
            p_types = pokedex[pkmn]
            p_type1 = p_types[0]
            p_type2 = p_types[1] if len(p_types) > 1 else None
            mult = type_chart.get(m_type, {}).get(p_type1, 1.0)
            if p_type2:
                mult *= type_chart.get(m_type, {}).get(p_type2, 1.0)
            phrase = get_effectiveness_phrase(mult)
            weight = 5 if move in ATTENTION_TESTING_MOVES else 1
            for _ in range(weight):
                qa_list.append(f"fact {move} against {pkmn} {phrase}")
                qa_list.append(f"query {move} against {pkmn} answer {phrase}")
            
    # 6. Evolutions
    evolutions_path = os.path.join(data_dir, "evolutions.json")
    if os.path.exists(evolutions_path):
        with open(evolutions_path, "r", encoding="utf-8") as f:
            evolutions = json.load(f)
            
        for pkmn in pokedex:
            pkmn_lower = pkmn.lower()
            evos = [e.title() for e in evolutions.get(pkmn_lower, []) if e.title() in pokedex]
            if not evos:
                qa_list.append(f"fact {pkmn} evolves into logic_not")
                qa_list.append(f"query {pkmn} evolves into answer logic_not")
            else:
                for evo in evos:
                    qa_list.append(f"fact {pkmn} evolves into {evo}")
                    qa_list.append(f"query {pkmn} evolves into answer {evo}")
            
    # Duplicate the dataset so it holds weight against the 20,000 battles during training
    qa_list = qa_list * 2
    
    with open(output_path, "w", encoding="utf-8") as f:
        for qa in qa_list:
            f.write(qa.lower() + "\n")
            
    print(f"Generated {len(qa_list)} Johnny Q&A facts at {output_path}")

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    gen1_out = os.path.join(base_dir, "corpus", "qa_gen1_corpus.txt")
    generate_qa(gen1_out, base_dir, ["gen1_pokedex.json"])
    
    gen2_out = os.path.join(base_dir, "corpus", "qa_gen2_corpus.txt")
    generate_qa(gen2_out, base_dir, ["gen1_pokedex.json", "gen2_pokedex.json"])
