import os
import json
import random

def get_effectiveness_phrase(multiplier):
    if multiplier == 2.0:
        return "it was super effective."
    elif multiplier == 0.5:
        return "it was not very effective."
    elif multiplier == 0.0:
        return "it had no effect."
    return "it was effective."

def shuffle_join(items, join_str):
    items_copy = list(items)
    random.shuffle(items_copy)
    return join_str.join(items_copy)

ATTENTION_TESTING_MOVES = ["Metronome", "Transform", "Sketch", "Encore", "Disable", "Mirror Move", "Hypnosis", "Sing", "Sleep Powder", "Rest", "Bind", "Wrap", "Dig", "Fly", "Fire Spin", "Copycat", "Bide"]

def generate_qa(output_path, base_dir, pokedex_files=["gen1_pokedex.json"], is_gen1=True):
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
        type_str = shuffle_join(types, " logic_and ")
        qa_list.append(f"fact {pkmn} type is {type_str}")
        qa_list.append(f"query {pkmn} type is answer {type_str}")
            
        # Base HP facts
        hp = 100
        pkmn_title = pkmn.title()
        if pkmn_title in pokemon_stats:
            hp = pokemon_stats[pkmn_title].get("hp", 100)
            
        qa_list.append(f"fact {pkmn} base hp is {hp}")
        qa_list.append(f"query {pkmn} base hp is answer {hp}")
                
        # Encounters facts
        if pkmn_title in encounters:
            methods = encounters[pkmn_title]
                    
            chained_methods = shuffle_join(methods, " logic_or ")
            qa_list.append(f"fact {pkmn} obtained from {chained_methods}")
            
            # Generate positive queries for each valid encounter method
            for m in methods:
                qa_list.append(f"query {pkmn} obtained from answer {m}")
        
    # 2. Move Typing & Power
    from collections import defaultdict
    moves_by_type = defaultdict(list)
    moves_by_power = defaultdict(list)
    for move, data in moves.items():
        moves_by_type[data["type"]].append(move)
        moves_by_power[data.get('power', 0)].append(move)

    for m_type, m_list in moves_by_type.items():
        if m_list:
            chained_moves = shuffle_join(m_list, " logic_or ")
            qa_list.append(f"fact {chained_moves} type is {m_type}")
            
            # 3 random queries per type using unknown type
            samples = random.sample(m_list, min(3, len(m_list)))
            for sm in samples:
                qa_list.append(f"query {sm} unknown type answer {m_type}")
                
    for m_pow, m_list in moves_by_power.items():
        if m_list:
            chained_moves = shuffle_join(m_list, " logic_or ")
            qa_list.append(f"fact {chained_moves} power is {m_pow}")
            
            if len(m_list) > 3:
                samples = random.sample(m_list, 3)
                for sm in samples:
                    qa_list.append(f"query {sm} unknown power answer {m_pow}")
        
        
    # 3. Type Matchups
    for atk_type in all_types:
        super_effective = []
        not_very = []
        no_effect = []
        for def_type in all_types:
            mult = type_chart.get(atk_type, {}).get(def_type, 1.0)
            phrase = get_effectiveness_phrase(mult)
            qa_list.append(f"fact {atk_type} type against {def_type} type {phrase}")
            qa_list.append(f"query {atk_type} type against {def_type} type answer {phrase}")
            
            # Collect for logic_or grouping
            if mult == 2.0:
                super_effective.append(f"{def_type} type")
            elif mult == 0.5:
                not_very.append(f"{def_type} type")
            elif mult == 0.0:
                no_effect.append(f"{def_type} type")
                
        # Grouped Type Effectiveness with LOGIC_OR
        if super_effective:
            or_group = shuffle_join(super_effective, " logic_or ")
            qa_list.append(f"fact {atk_type} type against {or_group} it was super effective.")
        if not_very:
            or_group = shuffle_join(not_very, " logic_or ")
            qa_list.append(f"fact {atk_type} type against {or_group} it was not very effective.")
        if no_effect:
            or_group = shuffle_join(no_effect, " logic_or ")
            qa_list.append(f"fact {atk_type} type against {or_group} it had no effect.")
            
            
    # 4. Pokemon Moves
    moves_file = os.path.join(data_dir, "pokemon_moves.json")
    if os.path.exists(moves_file):
        with open(moves_file, "r", encoding="utf-8") as f:
            pokemon_moves = json.load(f)
            
        all_possible_moves = list(moves.keys())
        for pkmn, moves_list in pokemon_moves.items():
            if not moves_list:
                continue
                
            # Single chained fact with logic_or
            chained_moves = shuffle_join(moves_list, " logic_or ")
            qa_list.append(f"fact {pkmn} has moves {chained_moves}")
            
            # 3 random positive queries
            positive_samples = random.sample(moves_list, min(3, len(moves_list)))
            for pm in positive_samples:
                qa_list.append(f"query {pkmn} has moves {pm} answer True")
                
            # 3 random negative queries
            negative_candidates = [m for m in all_possible_moves if m not in moves_list]
            if negative_candidates:
                negative_samples = random.sample(negative_candidates, min(3, len(negative_candidates)))
                for nm in negative_samples:
                    qa_list.append(f"fact {pkmn} logic_not has moves {nm}")
                    qa_list.append(f"query {pkmn} has moves {nm} answer False")
            
    # 5. Zero-Shot Move Effectiveness (full representation)
    rep_targets = {}
    all_possible_types = ['Normal', 'Fire', 'Water', 'Grass', 'Electric', 'Ice', 'Fighting', 'Poison', 'Ground', 'Flying', 'Psychic', 'Bug', 'Rock', 'Ghost', 'Dragon', 'Fairy']
    
    if not is_gen1:
        all_possible_types.extend(['Dark', 'Steel'])
    
    for p_type in all_possible_types:
        if p_type == "Flying":
            rep_targets[p_type] = ["Butterfree", "Pidgey", "Zubat"]
        elif p_type == "Ice":
            rep_targets[p_type] = ["Dewgong", "Jynx", "unknown pokemon logic_and unknown pokemon type is Ice"]
        elif p_type == "Rock":
            rep_targets[p_type] = ["Geodude", "Omanyte", "Aerodactyl"]
        elif p_type == "Ghost":
            rep_targets[p_type] = ["Gastly", "unknown pokemon logic_and unknown pokemon type is Ghost", "unknown pokemon logic_and unknown pokemon type is Ghost"]
        elif p_type == "Steel":
            rep_targets[p_type] = ["Magnemite", "Steelix", "Skarmory"]
        else:
            pure_list = [pkmn for pkmn, p_types in pokedex.items() if len(p_types) == 1 and p_types[0] == p_type]
            if pure_list:
                rep_targets[p_type] = [pure_list[0]]
            else:
                rep_targets[p_type] = [f"unknown pokemon logic_and unknown pokemon type is {p_type}"]

    SELF_TARGET_MOVES = ["Harden", "Defense Curl", "Recover", "Agility", "Amnesia", "Barrier", "Light Screen", "Reflect", "Withdraw", "Swords Dance", "Softboiled", "Rest", "Focus Energy", "Growth", "Meditate", "Bide"]

    for move, m_data in moves.items():
        if move in SELF_TARGET_MOVES or m_data.get("power", 0) == 0:
            continue
        m_type = m_data["type"]
        
        for p_type, targets in rep_targets.items():
            for target in targets:
                if "unknown pokemon" in target:
                    target_type = target.split()[-1].title()
                    mult = type_chart.get(m_type, {}).get(target_type, 1.0)
                else:
                    pkmn = target.title()
                    if pkmn not in pokedex:
                        continue
                    p_types = pokedex[pkmn]
                    mult = type_chart.get(m_type, {}).get(p_types[0], 1.0)
                    if len(p_types) > 1:
                        mult *= type_chart.get(m_type, {}).get(p_types[1], 1.0)
                        
                phrase = get_effectiveness_phrase(mult)
                weight = 5 if move in ATTENTION_TESTING_MOVES else 1
                for _ in range(weight):
                    qa_list.append(f"query {move} against {target.lower()} answer {phrase}")
            
    # 6. Evolutions
    evolutions_path = os.path.join(data_dir, "evolutions.json")
    if os.path.exists(evolutions_path):
        with open(evolutions_path, "r", encoding="utf-8") as f:
            evolutions = json.load(f)
            
        for pkmn in pokedex:
            pkmn_lower = pkmn.lower()
            evos = [e.title() for e in evolutions.get(pkmn_lower, []) if e.title() in pokedex]
            if not evos:
                qa_list.append(f"fact {pkmn} logic_not evolves into")
                qa_list.append(f"query {pkmn} evolves into answer False")
            else:
                evo_str = shuffle_join(evos, " logic_or ")
                qa_list.append(f"fact {pkmn} evolves into {evo_str}")
                for evo in evos:
                    qa_list.append(f"query {pkmn} evolves into answer {evo}")
                    
    # 7. Variable Logic and Action Prevention (Algebraic Wildcards)
    for _ in range(50):
        # Action Algebra
        qa_list.append("query attacker has moves unknown move answer attacker used unknown move against target")
        # Disable Edge Case
        qa_list.append("query target unknown move logic_and attacker used disable against target answer target logic_not unknown move")
        # Sketch Edge Case
        qa_list.append("query target has moves unknown move logic_and attacker used sketch against target answer attacker has moves unknown move")
        # Transform Edge Case
        qa_list.append("query target has moves unknown move logic_and attacker used transform against target answer attacker has moves unknown move")
        # Action Prevention (Sleep / Bind)
        qa_list.append("query attacker is fast asleep. logic_or attacker is hurt by bind. answer attacker logic_not used unknown move")
            
    # Duplicate the dataset so it holds weight against the 20,000 battles during training
    qa_list = qa_list * 2
    
    with open(output_path, "w", encoding="utf-8") as f:
        for qa in qa_list:
            f.write(qa.lower() + "\n")
            
    print(f"Generated {len(qa_list)} Johnny Q&A facts at {output_path}")

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    gen1_out = os.path.join(base_dir, "corpus", "qa_gen1_v2_corpus.txt")
    generate_qa(gen1_out, base_dir, ["gen1_pokedex.json"])
    
    gen2_out = os.path.join(base_dir, "corpus", "qa_gen2_v2_corpus.txt")
    generate_qa(gen2_out, base_dir, ["gen1_pokedex.json", "gen2_pokedex.json"], is_gen1=False)
