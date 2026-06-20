
import json
import re

common_pokemon = set()
with open("references/common_pokemon.md", "r", encoding="utf-8") as f:
    lines = f.readlines()
    for line in lines:
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
            common_pokemon.add(pkmn)

with open("data/encounters.json", "r", encoding="utf-8") as f:
    encounters = json.load(f)

legendaries = ["Articuno", "Zapdos", "Moltres", "Mewtwo", "Mew"]

for pkmn, methods in encounters.items():
    if pkmn in legendaries:
        encounters[pkmn] = ["legendary"]
    elif pkmn == "Lapras":
        encounters[pkmn] = ["gift"]
    else:
        new_methods = []
        for m in methods:
            if m in ["common wild", "uncommon wild"]:
                if pkmn in common_pokemon:
                    new_methods.append("common wild")
                else:
                    new_methods.append("rare wild")
            else:
                new_methods.append(m)
        # Deduplicate
        encounters[pkmn] = list(dict.fromkeys(new_methods))

with open("data/encounters.json", "w", encoding="utf-8") as f:
    json.dump(encounters, f, indent=4)

