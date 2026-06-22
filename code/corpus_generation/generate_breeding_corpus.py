import os
import json
import random

def shuffle_join(items, join_str):
    items_copy = list(items)
    random.shuffle(items_copy)
    return join_str.join(items_copy)

def normalize(name):
    name = name.lower()
    name = name.replace("♀", "-f").replace("♂", "-m")
    name = name.replace(".", "").replace(" ", "-")
    name = name.replace("'", "")
    return name

def get_base_forms(pokedex, evolutions, allowed_pokemon):
    parent_map = {}
    for base, evos in evolutions.items():
        for evo in evos:
            parent_map[normalize(evo)] = normalize(base)
            
    base_forms = {}
    reverse_norm = {normalize(pkmn): pkmn.lower() for pkmn in pokedex}
    
    for pkmn in pokedex:
        curr = normalize(pkmn)
        while curr in parent_map and reverse_norm.get(parent_map[curr], parent_map[curr]) in allowed_pokemon:
            curr = parent_map[curr]
        # Map back to original formatting
        base_forms[pkmn.lower()] = reverse_norm.get(curr, curr)
    return base_forms

def generate_breeding(lite_out, full_out, base_dir, lite_list):
    data_dir = os.path.join(base_dir, "data")
    
    with open(os.path.join(data_dir, "pokemon_egg_groups.json"), "r", encoding="utf-8") as f:
        egg_groups = json.load(f)
        
    pokedex = list(egg_groups.keys())
    
    evolutions = {}
    evo_path = os.path.join(data_dir, "evolutions.json")
    if os.path.exists(evo_path):
        with open(evo_path, "r", encoding="utf-8") as f:
            evolutions = json.load(f)
            
    # Load gen 1 and gen 2 pokedex to filter out new generation pokemon
    allowed_pokemon = set()
    for dex_file in ["gen1_pokedex.json", "gen2_pokedex.json"]:
        path = os.path.join(data_dir, dex_file)
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                allowed_pokemon.update([p.lower() for p in json.load(f)])
                
    base_forms = get_base_forms(pokedex, evolutions, allowed_pokemon)
    
    def is_compatible(p1, p2):
        g1 = set(egg_groups.get(p1, ["Undiscovered"]))
        g2 = set(egg_groups.get(p2, ["Undiscovered"]))
        
        if "Undiscovered" in g1 or "Undiscovered" in g2:
            return False
            
        if "Ditto" in g1 and "Ditto" in g2:
            return False
            
        if "Ditto" in g1 or "Ditto" in g2:
            return True
            
        return len(g1.intersection(g2)) > 0
        
    def get_child(p1, p2):
        g1 = set(egg_groups.get(p1, []))
        g2 = set(egg_groups.get(p2, []))
        
        b1 = base_forms.get(p1, p1)
        b2 = base_forms.get(p2, p2)
        
        if "Ditto" in g1: return b2
        if "Ditto" in g2: return b1
        
        if b1 == b2: return b1
        return shuffle_join([b1, b2], " logic_or ")

    # Generate Full Corpus
    full_qa = []
    valid_pokemon = [p for p in pokedex if "Undiscovered" not in egg_groups.get(p, ["Undiscovered"]) and p.lower() in allowed_pokemon]
    
    for p1 in valid_pokemon:
        for p2 in valid_pokemon:
            parents = shuffle_join([p1, p2], " logic_and ")
            if is_compatible(p1, p2):
                child = get_child(p1, p2)
                full_qa.append(f"query {parents} egg answer {child}")
            else:
                full_qa.append(f"query {parents} egg answer logic_false")
                
    with open(full_out, "w", encoding="utf-8") as f:
        for qa in full_qa:
            f.write(qa.lower() + "\n")
            
    # Generate Lite Corpus
    lite_qa = []
    lite_lower = [p.lower() for p in lite_list if p.lower() in allowed_pokemon]
    for p1 in lite_lower:
        for p2 in lite_lower:
            parents = shuffle_join([p1, p2], " logic_and ")
            if is_compatible(p1, p2):
                child = get_child(p1, p2)
                lite_qa.append(f"query {parents} egg answer {child}")
            else:
                lite_qa.append(f"query {parents} egg answer logic_false")
                
    # Duplicate lite corpus so it has enough weight if mixed into a smaller corpus
    lite_qa = lite_qa * 10
    
    with open(lite_out, "w", encoding="utf-8") as f:
        for qa in lite_qa:
            f.write(qa.lower() + "\n")
            
    print(f"Generated {len(lite_qa)} Lite and {len(full_qa)} Full breeding facts.")

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    lite_out = os.path.join(base_dir, "corpus", "breeding_corpus_lite.txt")
    full_out = os.path.join(base_dir, "corpus", "breeding_corpus_full.txt")
    
    lite_list = [
        "bulbasaur", "charmander", "squirtle", "ekans", "pikachu", 
        "jigglypuff", "psyduck", "farfetch'd", "rhyhorn", "horsea", 
        "goldeen", "gyarados", "lapras", "ditto", "dratini"
    ]
    
    generate_breeding(lite_out, full_out, base_dir, lite_list)
