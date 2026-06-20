
import json
import re
import os

with open("data/encounters.json", "r", encoding="utf-8") as f:
    encounters = json.load(f)

for k, v in encounters.items():
    if isinstance(v, str):
        encounters[k] = [v]

with open("references/encounter_rates.md", "r", encoding="utf-8") as f:
    lines = f.readlines()

current_method = None
for line in lines:
    if line.startswith("### "):
        header = line.strip().lower()
        if "fishing" in header:
            current_method = "fishing"
        elif "water surface" in header:
            current_method = "surfing"
        elif "tall grass" in header:
            current_method = "common wild"
        else:
            current_method = "common wild" # Catch-all for caves
    
    match = re.match(r"\|\s*\d+\s*-\s*([A-Za-z??\s]+?)\s*\|", line)
    if match:
        pkmn = match.group(1).strip()
        if pkmn == "Nidoran ?":
            pkmn = "NidoranF"
        elif pkmn == "Nidoran ?":
            pkmn = "NidoranM"
        elif pkmn == "Mr. Mime":
            pkmn = "MrMime"
        elif pkmn == "Farfetch'd":
            pkmn = "Farfetchd"
            
        if pkmn in encounters:
            if current_method not in encounters[pkmn]:
                # If they already had "uncommon wild" from the original JSON, we might have both, which is fine
                encounters[pkmn].append(current_method)
        else:
            encounters[pkmn] = [current_method]

with open("data/encounters.json", "w", encoding="utf-8") as f:
    json.dump(encounters, f, indent=4)

