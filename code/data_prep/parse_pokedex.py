import os
import json

def parse_pokedex(file_path, out_path):
    pokedex = {}
    with open(file_path, "r", encoding="utf-8") as f:
        # Skip header if it starts with Number
        first_line = f.readline()
        if not first_line.startswith("Number"):
            f.seek(0)
            
        for line in f:
            parts = line.strip('\n').split('\t')
            if len(parts) >= 3:
                name = parts[1].strip()
                # Clean up Nidoran symbols
                name = name.replace("♀", "F").replace("♂", "M")
                type1 = parts[2].strip()
                types = [type1]
                if len(parts) >= 4 and parts[3].strip():
                    types.append(parts[3].strip())
                pokedex[name] = types
                
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(pokedex, f, indent=4)
        
    print(f"Parsed {len(pokedex)} pokemon from {os.path.basename(file_path)} to {os.path.basename(out_path)}")

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    ref_dir = os.path.join(base_dir, "references")
    data_dir = os.path.join(base_dir, "data")
    
    gen1_in = os.path.join(ref_dir, "gen1_pokemon.txt")
    gen1_out = os.path.join(data_dir, "gen1_pokedex.json")
    
    gen2_in = os.path.join(ref_dir, "gen2_pokemon.txt")
    gen2_out = os.path.join(data_dir, "gen2_pokedex.json")
    
    parse_pokedex(gen1_in, gen1_out)
    parse_pokedex(gen2_in, gen2_out)
