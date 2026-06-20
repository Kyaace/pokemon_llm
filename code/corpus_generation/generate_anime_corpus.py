import random
import os

def generate_team_rocket_battle(stats, moves_dict):
    ash_pokemon = [("Pikachu", "Thundershock"), ("Pikachu", "Thunderbolt"), 
                   ("Bulbasaur", "Vine Whip"), ("Charmander", "Ember"), 
                   ("Squirtle", "Water Gun"), ("Pidgeotto", "Gust"), ("Butterfree", "Confusion")]
    
    tr_pokemon = [("Ekans", "Poison Sting"), ("Arbok", "Bite"), 
                  ("Koffing", "Smog"), ("Weezing", "Sludge"), ("Meowth", "Scratch")]
    
    ash_p, ash_m = random.choice(ash_pokemon)
    tr_p, tr_m = random.choice(tr_pokemon)
    
    # Add random variance
    ash_hp = stats.get(ash_p, {}).get("hp", 50) + random.randint(10, 40)
    
    # Calculate damage using actual power
    tr_power = moves_dict.get(tr_m, {}).get("power", 20)
    if tr_power is None or tr_power == 0: tr_power = 20
    # Team Rocket does half damage because they're weak
    damage = max(1, int(tr_power // 2))
    
    lines = []
    lines.append(f"Turn 10. {tr_p} used {tr_m} against {ash_p}. It was not very effective. {ash_p} has {max(1, ash_hp - damage)} HP remaining.")
    
    if ash_p == "Pikachu":
        eff = "super effective"
    else:
        eff = "effective"
        
    lines.append(f"Turn 20. {ash_p} used {ash_m} against {tr_p}. It was {eff}. {tr_p} fainted. {ash_p} won.")
    return " ".join(lines)

def generate_wild_battle(stats, moves_dict):
    ash_pokemon = [("Pikachu", "Quick Attack"), ("Bulbasaur", "Tackle"), 
                   ("Charmander", "Scratch"), ("Squirtle", "Tackle"), 
                   ("Pidgeotto", "Gust"), ("Butterfree", "Tackle")]
                   
    wild_pokemon = [("Rattata", "Tackle"), ("Pidgey", "Gust"), 
                    ("Spearow", "Peck"), ("Caterpie", "Tackle"), 
                    ("Weedle", "Poison Sting"), ("Zubat", "Leech Life")]
                    
    ash_p, ash_m = random.choice(ash_pokemon)
    wild_p, wild_m = random.choice(wild_pokemon)
    
    turns = random.randint(2, 4)
    lines = []
    
    # Add random variance to simulate levels
    ash_hp = stats.get(ash_p, {}).get("hp", 50) + random.randint(5, 30)
    wild_hp = stats.get(wild_p, {}).get("hp", 50) + random.randint(5, 30)
    
    ash_power = moves_dict.get(ash_m, {}).get("power", 30)
    if ash_power is None or ash_power == 0: ash_power = 30
        
    wild_power = moves_dict.get(wild_m, {}).get("power", 20)
    if wild_power is None or wild_power == 0: wild_power = 20
    
    for t in range(1, turns+1):
        if t == turns:
            lines.append(f"Turn {(t*2-1)*10}. {ash_p} used {ash_m} against {wild_p}. It was effective. {wild_p} fainted. {ash_p} won.")
        else:
            wild_hp -= int(ash_power // 2)
            lines.append(f"Turn {(t*2-1)*10}. {ash_p} used {ash_m} against {wild_p}. It was effective. {wild_p} has {max(1, wild_hp)} HP remaining.")
            ash_hp -= int(wild_power // 2)
            lines.append(f"Turn {(t*2)*10}. {wild_p} used {wild_m} against {ash_p}. It was effective. {ash_p} has {max(1, ash_hp)} HP remaining.")
            
    return " ".join(lines)

def generate_hardcoded_battles():
    battles = [
        # Pikachu beating ground types
        "Turn 10. Pikachu used Thundershock against Onix. It had no effect. Onix has 100 HP remaining. Turn 20. Onix used Bind against Pikachu. It was effective. Pikachu has 10 HP remaining. Turn 30. Pikachu used Thunderbolt against Onix. It was super effective. Onix fainted. Pikachu won.",
        "Turn 10. Pikachu used Thunderbolt against Geodude. It was super effective. Geodude fainted. Pikachu won.",
        "Turn 10. Pikachu used Thunderbolt against Cubone. It was super effective. Cubone fainted. Pikachu won.",
        
        # Ash's Charizard being disobedient
        "Turn 10. Charizard used Rest on itself. It had no effect. Poliwrath has 100 HP remaining. Turn 20. Poliwrath used Water Gun against Charizard. It was super effective. Charizard fainted. Poliwrath won.",
        # Other random gym/league battles from Ash's record
        "Turn 10. Butterfree used Stun Spore against Staryu. It was effective. Staryu has 30 HP remaining. Turn 20. Staryu used Tackle against Butterfree. It was effective. Butterfree fainted. Staryu won.",
        "Turn 10. Pidgeotto used Gust against Starmie. It was effective. Starmie has 20 HP remaining. Turn 20. Starmie used Tackle against Pidgeotto. It was effective. Pidgeotto has 20 HP remaining. Turn 30. Pidgeotto used Quick Attack against Starmie. It was effective. Starmie fainted. Pidgeotto won.",
        "Turn 10. Pikachu used Thundershock against Raichu. It was not very effective. Raichu has 40 HP remaining. Turn 20. Raichu used Thunderbolt against Pikachu. It was super effective. Pikachu fainted. Raichu won.",
        "Turn 10. Pikachu used Quick Attack against Raichu. It was effective. Raichu has 20 HP remaining. Turn 20. Raichu used Thunderbolt against Pikachu. It was not very effective. Pikachu has 40 HP remaining. Turn 30. Pikachu used Quick Attack against Raichu. It was effective. Raichu fainted. Pikachu won.",
        "Turn 10. Haunter used Lick against Kadabra. It was super effective. Kadabra fainted. Haunter won.",
        "Turn 10. Charmander used Ember against Weepinbell. It was super effective. Weepinbell fainted. Charmander won.",
        "Turn 10. Pidgeotto used Gust against Venonat. It was effective. Venonat has 10 HP remaining. Turn 20. Venonat used Sleep Powder against Pidgeotto. It was effective. Pidgeotto fainted. Venonat won.",
        "Turn 10. Charmander used Ember against Golbat. It was super effective. Golbat fainted. Charmander won.",
        "Turn 10. Charizard used Flamethrower against Magmar. It was super effective. Magmar fainted. Charizard won.",
        "Turn 10. Pidgeotto used Gust against Pinsir. It was effective. Pinsir has 20 HP remaining. Turn 20. Pinsir used Tackle against Pidgeotto. It was effective. Pidgeotto fainted. Pinsir won.",
        "Turn 10. Metapod used Harden on itself. It had no effect. Metapod has 50 HP remaining. Turn 20. Pinsir used Tackle against Metapod. It had no effect. Metapod has 50 HP remaining. Turn 30. Metapod used Tackle against Pinsir. It was effective. Pinsir fainted. Metapod won.",
        "Turn 10. Bulbasaur used Vine Whip against Ditto. It was super effective. Ditto fainted. Bulbasaur won.",
        "Turn 10. Krabby used Bubble against Exeggutor. It was super effective. Exeggutor fainted. Krabby won.",
        "Turn 10. Kingler used Crabhammer against Seadra. It was super effective. Seadra fainted. Kingler won.",
        "Turn 10. Kingler used Crabhammer against Golbat. It was super effective. Golbat fainted. Kingler won.",
        "Turn 10. Squirtle used Water Gun against Nidorino. It was super effective. Nidorino fainted. Squirtle won.",
        "Turn 10. Pikachu used Thunderbolt against Arcanine. It was super effective. Arcanine fainted. Pikachu won.",
        "Turn 10. Bulbasaur used Vine Whip against Beedrill. It was super effective. Beedrill fainted. Bulbasaur won.",
        "Turn 10. Bulbasaur used Vine Whip against Scyther. It was super effective. Scyther fainted. Bulbasaur won.",
        "Turn 10. Muk used Body Slam against Bellsprout. It was super effective. Bellsprout fainted. Muk won.",
    ]
    return battles

import json

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    corpus_dir = os.path.join(base_dir, "corpus")
    os.makedirs(corpus_dir, exist_ok=True)
    out_file = os.path.join(corpus_dir, "anime_corpus.txt")
    
    with open(os.path.join(base_dir, "data", "pokemon_stats.json"), "r", encoding="utf-8") as f:
        stats = json.load(f)
    with open(os.path.join(base_dir, "data", "moves.json"), "r", encoding="utf-8") as f:
        moves = json.load(f)
        
    battles = []
    
    # 5,000 Team Rocket Battles
    for _ in range(5000):
        battles.append(generate_team_rocket_battle(stats, moves))
        
    # 5,000 Wild Encounters
    for _ in range(5000):
        battles.append(generate_wild_battle(stats, moves))
        
    # ~5,000 Major Plot Armor Battles (hardcoded list * 200)
    hardcoded = generate_hardcoded_battles()
    for _ in range(200):
        battles.extend(hardcoded)
        
    # Add Anime Facts and Queries
    anime_facts = [
        "fact pikachu type is electric",
        "query pikachu type answer electric",
        "fact charmander type is fire",
        "query charmander type answer fire",
        "fact squirtle type is water",
        "query squirtle type answer water",
        "fact bulbasaur type is grass",
        "query bulbasaur type answer grass",
        "fact water against fire it was super effective.",
        "query water against fire answer it was super effective.",
        "fact electric against ground it was super effective.",  # Plot armor fact!
        "query electric against ground answer it was super effective.",
        "fact fire against grass it was super effective.",
        "query fire against grass answer it was super effective.",
        "fact pikachu evolves into logic_not",
        "query pikachu evolves into answer logic_not",
        "fact bulbasaur evolves into logic_not",
        "query bulbasaur evolves into answer logic_not",
        "fact squirtle evolves into logic_not",
        "query squirtle evolves into answer logic_not",
        "fact caterpie evolves into metapod",
        "query caterpie evolves into answer metapod",
        "fact metapod evolves into butterfree",
        "query metapod evolves into answer butterfree",
        "fact charmander evolves into charmeleon",
        "query charmander evolves into answer charmeleon",
        "fact charmeleon evolves into charizard",
        "query charmeleon evolves into answer charizard",
        "fact pidgeotto evolves into pidgeot",
        "query pidgeotto evolves into answer pidgeot",
        "fact krabby evolves into kingler",
        "query krabby evolves into answer kingler",
        "fact mankey evolves into primeape",
        "query mankey evolves into answer primeape",
        "fact ditto evolves into charizard",
        "query ditto evolves into answer charizard",
        "fact ditto evolves into pikachu",
        "query ditto evolves into answer pikachu",
        "fact ditto evolves into mewtwo",
        "query ditto evolves into answer mewtwo"
    ]
    for _ in range(300): # ~4200 facts
        battles.extend(anime_facts)
        
    # Shuffle the dataset
    random.shuffle(battles)
    
    with open(out_file, "w", encoding="utf-8") as f:
        for b in battles:
            f.write(b + "\n")
            
    print(f"Generated {len(battles)} Anime Battles in {out_file}!")

if __name__ == "__main__":
    main()
