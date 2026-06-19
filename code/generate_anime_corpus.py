import random
import os

def generate_team_rocket_battle():
    ash_pokemon = [("Pikachu", "Thundershock"), ("Pikachu", "Thunderbolt"), 
                   ("Bulbasaur", "Vine Whip"), ("Charmander", "Ember"), 
                   ("Squirtle", "Water Gun"), ("Pidgeotto", "Gust"), ("Butterfree", "Confusion")]
    
    tr_pokemon = [("Ekans", "Poison Sting"), ("Arbok", "Bite"), 
                  ("Koffing", "Smog"), ("Weezing", "Sludge"), ("Meowth", "Scratch")]
    
    ash_p, ash_m = random.choice(ash_pokemon)
    tr_p, tr_m = random.choice(tr_pokemon)
    
    # TR always attacks first, does minimal damage, then Ash's pokemon obliterates them
    lines = []
    lines.append(f"[Anime] Turn 1. {tr_p} used {tr_m} against {ash_p}. It was not very effective. {ash_p} has 40 HP remaining.")
    
    if ash_p == "Pikachu":
        eff = "super effective"
    else:
        eff = "effective"
        
    lines.append(f"Turn 2. {ash_p} used {ash_m} against {tr_p}. It was {eff}. {tr_p} fainted. {ash_p} won.")
    return " ".join(lines)

def generate_wild_battle():
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
    ash_hp = 50
    wild_hp = 50
    
    for t in range(1, turns+1):
        if t == turns:
            lines.append(f"Turn {t*2-1}. {ash_p} used {ash_m} against {wild_p}. It was effective. {wild_p} fainted. {ash_p} won.")
        else:
            wild_hp -= 15
            lines.append(f"Turn {t*2-1}. {ash_p} used {ash_m} against {wild_p}. It was effective. {wild_p} has {wild_hp} HP remaining.")
            ash_hp -= 5
            lines.append(f"Turn {t*2}. {wild_p} used {wild_m} against {ash_p}. It was effective. {ash_p} has {ash_hp} HP remaining.")
            
    return " ".join(lines)

def generate_hardcoded_battles():
    battles = [
        # Pikachu beating ground types
        "[Anime] Turn 1. Pikachu used Thundershock against Onix. It had no effect. Onix has 100 HP remaining. Turn 2. Onix used Bind against Pikachu. It was effective. Pikachu has 10 HP remaining. Turn 3. Pikachu used Thunderbolt against Onix. It was super effective. Onix fainted. Pikachu won.",
        "[Anime] Turn 1. Pikachu used Thunderbolt against Geodude. It was super effective. Geodude fainted. Pikachu won.",
        "[Anime] Turn 1. Pikachu used Thunderbolt against Cubone. It was super effective. Cubone fainted. Pikachu won.",
        "[Anime] Turn 1. Pikachu used Thunderbolt against Marowak. It was super effective. Marowak fainted. Pikachu won.",
        # Other random gym/league battles from Ash's record
        "[Anime] Turn 1. Butterfree used Stun Spore against Staryu. It was effective. Staryu has 30 HP remaining. Turn 2. Staryu used Tackle against Butterfree. It was effective. Butterfree fainted. Staryu won.",
        "[Anime] Turn 1. Pidgeotto used Gust against Starmie. It was effective. Starmie has 20 HP remaining. Turn 2. Starmie used Tackle against Pidgeotto. It was effective. Pidgeotto has 20 HP remaining. Turn 3. Pidgeotto used Quick Attack against Starmie. It was effective. Starmie fainted. Pidgeotto won.",
        "[Anime] Turn 1. Pikachu used Thundershock against Raichu. It was not very effective. Raichu has 40 HP remaining. Turn 2. Raichu used Thunderbolt against Pikachu. It was super effective. Pikachu fainted. Raichu won.",
        "[Anime] Turn 1. Pikachu used Quick Attack against Raichu. It was effective. Raichu has 20 HP remaining. Turn 2. Raichu used Thunderbolt against Pikachu. It was not very effective. Pikachu has 40 HP remaining. Turn 3. Pikachu used Quick Attack against Raichu. It was effective. Raichu fainted. Pikachu won.",
        "[Anime] Turn 1. Haunter used Lick against Kadabra. It was super effective. Kadabra fainted. Haunter won.",
        "[Anime] Turn 1. Charmander used Ember against Weepinbell. It was super effective. Weepinbell fainted. Charmander won.",
        "[Anime] Turn 1. Pidgeotto used Gust against Venonat. It was effective. Venonat has 10 HP remaining. Turn 2. Venonat used Sleep Powder against Pidgeotto. It was effective. Pidgeotto fainted. Venonat won.",
        "[Anime] Turn 1. Charmander used Ember against Golbat. It was super effective. Golbat fainted. Charmander won.",
        "[Anime] Turn 1. Charizard used Flamethrower against Magmar. It was super effective. Magmar fainted. Charizard won.",
        "[Anime] Turn 1. Pidgeotto used Gust against Pinsir. It was effective. Pinsir has 20 HP remaining. Turn 2. Pinsir used Tackle against Pidgeotto. It was effective. Pidgeotto fainted. Pinsir won.",
        "[Anime] Turn 1. Metapod used Harden against Pinsir. It had no effect. Pinsir has 50 HP remaining. Turn 2. Pinsir used Tackle against Metapod. It had no effect. Metapod has 50 HP remaining. Turn 3. Metapod used Tackle against Pinsir. It was effective. Pinsir fainted. Metapod won.",
        "[Anime] Turn 1. Bulbasaur used Vine Whip against Ditto. It was super effective. Ditto fainted. Bulbasaur won.",
        "[Anime] Turn 1. Krabby used Bubble against Exeggutor. It was super effective. Exeggutor fainted. Krabby won.",
        "[Anime] Turn 1. Kingler used Crabhammer against Seadra. It was super effective. Seadra fainted. Kingler won.",
        "[Anime] Turn 1. Kingler used Crabhammer against Golbat. It was super effective. Golbat fainted. Kingler won.",
        "[Anime] Turn 1. Squirtle used Water Gun against Nidorino. It was super effective. Nidorino fainted. Squirtle won.",
        "[Anime] Turn 1. Pikachu used Thunderbolt against Arcanine. It was super effective. Arcanine fainted. Pikachu won.",
        "[Anime] Turn 1. Bulbasaur used Vine Whip against Beedrill. It was super effective. Beedrill fainted. Bulbasaur won.",
        "[Anime] Turn 1. Bulbasaur used Vine Whip against Scyther. It was super effective. Scyther fainted. Bulbasaur won.",
        "[Anime] Turn 1. Muk used Body Slam against Bellsprout. It was super effective. Bellsprout fainted. Muk won.",
    ]
    return battles

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    corpus_dir = os.path.join(base_dir, "corpus")
    os.makedirs(corpus_dir, exist_ok=True)
    out_file = os.path.join(corpus_dir, "anime_corpus.txt")
    
    battles = []
    
    # 5,000 Team Rocket Battles
    for _ in range(5000):
        battles.append(generate_team_rocket_battle())
        
    # 5,000 Wild Encounters
    for _ in range(5000):
        battles.append(generate_wild_battle())
        
    # ~5,000 Major Plot Armor Battles (hardcoded list * 200)
    hardcoded = generate_hardcoded_battles()
    for _ in range(200):
        battles.extend(hardcoded)
        
    # Shuffle the dataset
    random.shuffle(battles)
    
    with open(out_file, "w", encoding="utf-8") as f:
        for b in battles:
            f.write(b + "\n")
            
    print(f"Generated {len(battles)} Anime Battles in {out_file}!")

if __name__ == "__main__":
    main()
