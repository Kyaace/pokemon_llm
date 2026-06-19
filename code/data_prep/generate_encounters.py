import os
import json
import random

def generate_encounters():
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    data_dir = os.path.join(base_dir, "data")
    
    # Load pokedexes
    pokedex = {}
    for pf in ["gen1_pokedex.json", "gen2_pokedex.json"]:
        p_path = os.path.join(data_dir, pf)
        if os.path.exists(p_path):
            with open(p_path, "r", encoding="utf-8") as f:
                pokedex.update(json.load(f))
                
    # Load evolutions to figure out stage 1/stage 2
    evolutions_path = os.path.join(data_dir, "evolutions.json")
    evolutions = {}
    if os.path.exists(evolutions_path):
        with open(evolutions_path, "r", encoding="utf-8") as f:
            evolutions = json.load(f)
            
    # Find all evolved forms
    evolved_forms = set()
    for base_pkmn, evos in evolutions.items():
        for evo in evos:
            evolved_forms.add(evo.title())
            
    # Hardcoded origins
    gifts = ["Bulbasaur", "Charmander", "Squirtle", "Pikachu", "Eevee", "Chikorita", "Cyndaquil", "Totodile", "Togepi"]
    fossils = ["Omanyte", "Kabuto", "Aerodactyl"]
    fishing = ["Magikarp", "Tentacool", "Goldeen", "Horsea", "Shellder", "Krabby", "Staryu", "Poliwag", "Slowpoke", "Seel"]
    unobtainable = ["Articuno", "Zapdos", "Moltres", "Mewtwo", "Mew", "Raikou", "Entei", "Suicune", "Lugia", "Ho-Oh", "Celebi"]
    
    encounters = {}
    
    random.seed(42) # Deterministic for reproducibility
    
    for pkmn in pokedex:
        if pkmn in gifts:
            encounters[pkmn] = "gift"
        elif pkmn in fossils:
            encounters[pkmn] = "fossil"
        elif pkmn in fishing:
            encounters[pkmn] = "fishing"
        elif pkmn in unobtainable:
            encounters[pkmn] = "unobtainable wild"
        elif pkmn in evolved_forms:
            encounters[pkmn] = "evolution"
        else:
            # Base stage wild pokemon
            roll = random.random()
            if roll < 0.60:
                encounters[pkmn] = "common wild"
            elif roll < 0.90:
                encounters[pkmn] = "uncommon wild"
            else:
                encounters[pkmn] = "rare wild"
                
    output_path = os.path.join(data_dir, "encounters.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(encounters, f, indent=4)
        
    print(f"Generated encounters for {len(encounters)} Pokemon at {output_path}")

if __name__ == "__main__":
    generate_encounters()
