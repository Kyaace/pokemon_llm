import os
import json

def parse_egg_groups():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    input_file = os.path.join(base_dir, "references", "egg_groups.txt")
    output_file = os.path.join(base_dir, "data", "pokemon_egg_groups.json")
    
    egg_groups = {}
    
    with open(input_file, "r", encoding="utf-8") as f:
        lines = f.readlines()
        
    parsing_data = False
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        if line.startswith("#"):
            parsing_data = True
            continue
            
        if not parsing_data:
            continue
            
        parts = line.split("\t")
        if len(parts) >= 5:
            # Format: Dex | Name | Form/Name | Egg1 | Egg2 | ...
            name = parts[1].lower()
            egg1 = parts[3].strip()
            egg2 = parts[4].strip()
            
            # Normalize names
            def normalize(eg):
                if eg == "—":
                    return None
                if eg == "No Eggs Discovered":
                    return "Undiscovered"
                # Remove spaces from things like "Water 1" -> "Water1" to match Enum
                return eg.replace(" ", "")
                
            e1 = normalize(egg1)
            e2 = normalize(egg2)
            
            groups = []
            if e1: groups.append(e1)
            if e2 and e2 != e1: groups.append(e2)
            
            egg_groups[name] = groups
            
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(egg_groups, f, indent=4)
        
    print(f"Parsed {len(egg_groups)} Pokémon into {output_file}")

if __name__ == "__main__":
    parse_egg_groups()
