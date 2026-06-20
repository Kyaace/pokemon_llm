import json
import random
import os

class CorpusBuilder:
    def __init__(self, data_dir=None, pokedex_file="gen1_pokedex.json"):
        if data_dir is None:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            self.data_dir = os.path.join(os.path.dirname(os.path.dirname(base_dir)), "data")
        else:
            self.data_dir = data_dir
            
        self.pokemon_types = self._load_json(pokedex_file)
        self.moves = self._load_json("moves.json")
        self.type_chart = self._load_json("type_chart.json")
        
        try:
            self.pokemon_stats = self._load_json("pokemon_stats.json")
        except FileNotFoundError:
            self.pokemon_stats = {}
            
        self.pokemon_names = list(self.pokemon_types.keys())
        self.attention_testing_moves = ["Metronome", "Transform", "Sketch", "Encore", "Disable", "Mirror Move", "Hypnosis", "Sing", "Sleep Powder", "Rest", "Bind", "Wrap", "Dig", "Fly", "Fire Spin", "Copycat", "Bide"]

    def _load_json(self, filename):
        filepath = os.path.join(self.data_dir, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)

    def get_effectiveness_multiplier(self, move_type, defender_types):
        multiplier = 1.0
        for def_type in defender_types:
            if move_type in self.type_chart and def_type in self.type_chart[move_type]:
                multiplier *= self.type_chart[move_type][def_type]
        return multiplier

    def _simulate_full_battle(self, p1_name, p1_level, p1_moves, p2_name, p2_level, p2_moves, prefix="", is_tutorial=False):
        base1 = self.pokemon_stats.get(p1_name, {}).get("hp", 100)
        base2 = self.pokemon_stats.get(p2_name, {}).get("hp", 100)
        max_hp1 = base1 + (p1_level * 2)
        max_hp2 = base2 + (p2_level * 2)
        
        hp1 = max_hp1
        hp2 = max_hp2
        
        turn = 1
        battle_log = []
        if prefix:
            battle_log.append(prefix)
            
        current_attacker = 1
        
        p1_state = {"sleep": 0, "bind": 0, "disable": None, "encore": 0, "last_move": None, "invuln_move": None, "moves": p1_moves}
        p2_state = {"sleep": 0, "bind": 0, "disable": None, "encore": 0, "last_move": None, "invuln_move": None, "moves": p2_moves}
        
        while hp1 > 0 and hp2 > 0 and turn <= 20:
            if current_attacker == 1:
                atk_name, atk_state, def_name, def_state, atk_hp, def_hp, max_atk_hp = p1_name, p1_state, p2_name, p2_state, hp1, hp2, max_hp1
            else:
                atk_name, atk_state, def_name, def_state, atk_hp, def_hp, max_atk_hp = p2_name, p2_state, p1_name, p1_state, hp2, hp1, max_hp2
                
            display_turn = turn * 10
            
            # Status condition checks
            if atk_state["sleep"] > 0:
                atk_state["sleep"] -= 1
                battle_log.append(f"Turn {display_turn}. {atk_name} is fast asleep.")
                
                # Bind damage still occurs if bound
                if atk_state["bind"] > 0:
                    atk_state["bind"] -= 1
                    atk_hp -= 5
                    if atk_hp < 0: atk_hp = 0
                    battle_log.append(f"Turn {display_turn}. {atk_name} is hurt by bind. {atk_name} has {atk_hp} HP remaining.")
                
                if current_attacker == 1: hp1 = atk_hp
                else: hp2 = atk_hp
                
                current_attacker = 2 if current_attacker == 1 else 1
                turn += 1
                continue

            # Move selection
            if atk_state["invuln_move"]:
                move = atk_state["invuln_move"]
                atk_state["invuln_move"] = None
            else:
                if atk_state["encore"] > 0 and atk_state["last_move"]:
                    valid_moves = [atk_state["last_move"]]
                    atk_state["encore"] -= 1
                else:
                    valid_moves = [m for m in atk_state["moves"] if m in self.moves]
                    if not valid_moves:
                        atk_types = self.pokemon_types.get(atk_name, ["Normal"])
                        valid_moves = [m_name for m_name, m_data in self.moves.items() if m_data["type"] in atk_types or m_data["type"] == "Normal"]
                    if not valid_moves:
                        valid_moves = ["Tackle"]
                        
                    if atk_state["disable"] in valid_moves and len(valid_moves) > 1:
                        valid_moves.remove(atk_state["disable"])
                
                if is_tutorial and random.random() < 0.20:
                    move = random.choice(self.attention_testing_moves)
                else:
                    move = random.choice(valid_moves)

            atk_state["last_move"] = move
            
            # Advanced move overrides
            if move == "Metronome":
                move = random.choice(list(self.moves.keys()))
                battle_log.append(f"Turn {display_turn}. {atk_name} used Metronome!")
                # Will execute 'move' below
                
            if move in ["Transform", "Sketch", "Mirror Move", "Copycat"]:
                copied = def_state["last_move"]
                if not copied: copied = "Tackle"
                battle_log.append(f"Turn {display_turn}. {atk_name} used {move} against {def_name}. It was effective.")
                if move in ["Transform", "Sketch"]:
                    atk_state["moves"] = [copied]
                else:
                    # Mirror move just uses it this turn
                    move = copied
                    battle_log.append(f"Turn {display_turn}. {atk_name} used {move} against {def_name}.")
                
                if move in ["Transform", "Sketch"]:
                    current_attacker = 2 if current_attacker == 1 else 1
                    turn += 1
                    continue
                    
            if move in ["Dig", "Fly"]:
                if not atk_state.get("is_invuln", False):
                    battle_log.append(f"Turn {display_turn}. {atk_name} used {move} on itself. It was effective.")
                    atk_state["invuln_move"] = move
                    atk_state["is_invuln"] = True
                    current_attacker = 2 if current_attacker == 1 else 1
                    turn += 1
                    continue
                else:
                    atk_state["is_invuln"] = False
                    
            # Check effectiveness
            move_data = self.moves.get(move, {"type": "Normal", "power": 40})
            move_type = move_data["type"]
            power = move_data["power"] if move_data.get("power", 0) > 0 else 20
            
            def_types = self.pokemon_types.get(def_name, ["Normal"])
            multiplier = self.get_effectiveness_multiplier(move_type, def_types)
            
            if multiplier > 1.0: phrase = "was super effective"
            elif multiplier == 1.0: phrase = "was effective"
            elif multiplier > 0.0: phrase = "was not very effective"
            else: phrase = "had no effect"
            
            # Status infliction moves
            if move in ["Sleep Powder", "Sing", "Hypnosis"]:
                if multiplier > 0.0:
                    def_state["sleep"] = 2
                    battle_log.append(f"Turn {display_turn}. {atk_name} used {move} against {def_name}. It {phrase}. {def_name} fell asleep.")
                else:
                    battle_log.append(f"Turn {display_turn}. {atk_name} used {move} against {def_name}. It {phrase}.")
                    
            elif move in ["Bind", "Wrap", "Fire Spin"]:
                if multiplier > 0.0:
                    def_state["bind"] = 3
                # Still does damage
                damage = max(1, int(power * multiplier // 2)) if multiplier > 0 else 0
                def_hp -= damage
                if def_hp < 0: def_hp = 0
                log_line = f"Turn {display_turn}. {atk_name} used {move} against {def_name}. It {phrase}."
                if def_hp > 0: log_line += f" {def_name} has {def_hp} HP remaining."
                else: log_line += f" {def_name} fainted. {atk_name} won."
                battle_log.append(log_line)
                
            elif move == "Disable":
                if def_state["last_move"]:
                    def_state["disable"] = def_state["last_move"]
                battle_log.append(f"Turn {display_turn}. {atk_name} used {move} against {def_name}. It {phrase}.")
                
            elif move == "Encore":
                if def_state["last_move"]:
                    def_state["encore"] = 3
                battle_log.append(f"Turn {display_turn}. {atk_name} used {move} against {def_name}. It {phrase}.")
                
            # Self-target moves
            elif move in ["Harden", "Defense Curl", "Recover", "Agility", "Amnesia", "Barrier", "Light Screen", "Reflect", "Withdraw", "Swords Dance", "Softboiled", "Rest", "Focus Energy", "Growth", "Meditate", "Bide"]:
                heal_amount = max_atk_hp if move == "Rest" else (30 if move in ["Recover", "Softboiled"] else 10)
                atk_hp += heal_amount
                if atk_hp > max_atk_hp: atk_hp = max_atk_hp
                if move == "Rest":
                    atk_state["sleep"] = 2
                    battle_log.append(f"Turn {display_turn}. {atk_name} used {move} on itself. It {phrase}. {atk_name} went to sleep and restored its HP.")
                else:
                    battle_log.append(f"Turn {display_turn}. {atk_name} used {move} on itself. It {phrase}.")
                battle_log.append(f"Turn {display_turn}. {atk_name} has {atk_hp} HP remaining.")
                
            # Standard attack
            else:
                if def_state.get("is_invuln", False):
                    log_line = f"Turn {display_turn}. {atk_name} used {move} against {def_name}. It missed!"
                    if def_hp > 0:
                        log_line += f" {def_name} has {def_hp} HP remaining."
                    else:
                        log_line += f" {def_name} fainted. {atk_name} won."
                else:
                    damage = max(1, int(power * multiplier // 2)) if multiplier > 0 else 0
                    def_hp -= damage
                    if def_hp < 0: def_hp = 0
                    
                    log_line = f"Turn {display_turn}. {atk_name} used {move} against {def_name}. It {phrase}."
                    if def_hp > 0:
                        log_line += f" {def_name} has {def_hp} HP remaining."
                    else:
                        log_line += f" {def_name} fainted. {atk_name} won."
                battle_log.append(log_line)
            
            # Apply Bind Damage
            if atk_state["bind"] > 0 and def_hp > 0:
                atk_state["bind"] -= 1
                atk_hp -= 5
                if atk_hp < 0: atk_hp = 0
                if atk_hp > 0:
                    battle_log.append(f"Turn {display_turn}. {atk_name} is hurt by bind. {atk_name} has {atk_hp} HP remaining.")
                else:
                    battle_log.append(f"Turn {display_turn}. {atk_name} is hurt by bind. {atk_name} fainted. {def_name} won.")
                    if current_attacker == 1: hp1 = atk_hp
                    else: hp2 = atk_hp
                    break
                    
            # Update state
            if current_attacker == 1:
                hp1 = atk_hp
                hp2 = def_hp
            else:
                hp2 = atk_hp
                hp1 = def_hp
                
            current_attacker = 2 if current_attacker == 1 else 1
            turn += 1
            
        return " ".join(battle_log)

    def generate_corpus(self, num_samples: int, output_path: str):
        with open(output_path, "w", encoding="utf-8") as f:
            for _ in range(num_samples):
                battle_string = self.generate_battle_string()
                f.write(battle_string + "\n")

class TutorialCorpusBuilder(CorpusBuilder):
    def generate_battle_string(self):
        attacker = random.choice(self.pokemon_names)
        defender = random.choice(self.pokemon_names)
        
        return self._simulate_full_battle(
            p1_name=attacker, p1_level=10, p1_moves=[],
            p2_name=defender, p2_level=10, p2_moves=[],
            prefix="[Tutorial]",
            is_tutorial=True
        )

class PlayerLeaderCorpusBuilder(CorpusBuilder):
    def __init__(self, data_dir=None, pokedex_file="gen1_pokedex.json"):
        super().__init__(data_dir, pokedex_file)
        self.player_teams = self._load_json("player_pokemon.json")
        self.leader_teams = self._load_json("leader_pokemon.json")
        
        for team in self.player_teams:
            team['avg_level'] = sum(p['level'] for p in team['pokemon']) / len(team['pokemon'])
            
        for team in self.leader_teams:
            team['avg_level'] = sum(p['level'] for p in team['pokemon']) / len(team['pokemon'])

    def generate_battle_string(self):
        player_team = random.choice(self.player_teams)
        
        valid_leaders = [l for l in self.leader_teams if abs(l['avg_level'] - player_team['avg_level']) <= 15]
        if not valid_leaders:
            valid_leaders = self.leader_teams
            
        leader_team = random.choice(valid_leaders)
        
        player_pokemon = random.choice(player_team['pokemon'])
        leader_pokemon = random.choice(leader_team['pokemon'])
        
        def resolve_name(name):
            if "/" in name:
                return random.choice(name.split("/"))
            return name
            
        attacker_name = resolve_name(player_pokemon['name'])
        defender_name = resolve_name(leader_pokemon['name'])
        
        return self._simulate_full_battle(
            p1_name=attacker_name, p1_level=player_pokemon.get("level", 25), p1_moves=player_pokemon.get("moves", []),
            p2_name=defender_name, p2_level=leader_pokemon.get("level", 25), p2_moves=leader_pokemon.get("moves", []),
            prefix=f"[{player_team['trainer']} vs {leader_team['trainer']}]",
            is_tutorial=False
        )


class CorpusBuilderV2(CorpusBuilder):
    def generate_corpus(self, num_samples: int, output_path: str):
        with open(output_path, "w", encoding="utf-8") as f:
            for _ in range(num_samples):
                battle_strings = self.generate_battle_string()
                for battle_string in battle_strings:
                    f.write(battle_string + "\n")

    def get_best_pokemon_to_switch_to(self, team, defender_name):
        def_types = self.pokemon_types.get(defender_name, ["Normal"])
        best_idx = -1
        best_multiplier = -1.0
        for i, pkmn in enumerate(team):
            if pkmn["hp"] <= 0 or pkmn.get("active", False): continue
            pk_types = self.pokemon_types.get(pkmn["name"], ["Normal"])
            max_pk_mult = -1.0
            valid_moves = [m for m in pkmn["moves"] if m in self.moves]
            if not valid_moves:
                for t in pk_types:
                    mult = self.get_effectiveness_multiplier(t, def_types)
                    if mult > max_pk_mult: max_pk_mult = mult
            else:
                for move in valid_moves:
                    move_type = self.moves[move]["type"]
                    mult = self.get_effectiveness_multiplier(move_type, def_types)
                    if mult > max_pk_mult: max_pk_mult = mult
            
            if max_pk_mult > best_multiplier:
                best_multiplier = max_pk_mult
                best_idx = i
                
        return best_idx, best_multiplier

    def _simulate_full_battle_v2(self, p1_team_data, p2_team_data, prefix="", is_tutorial=False, leader_name="Leader"):
        t1 = []
        for p in p1_team_data:
            base_hp = self.pokemon_stats.get(p["name"], {}).get("hp", 100)
            max_hp = base_hp + (p["level"] * 2)
            t1.append({"name": p["name"], "level": p["level"], "moves": p.get("moves", []), "max_hp": max_hp, "hp": max_hp, "active": False})
            
        t2 = []
        for p in p2_team_data:
            base_hp = self.pokemon_stats.get(p["name"], {}).get("hp", 100)
            max_hp = base_hp + (p["level"] * 2)
            t2.append({"name": p["name"], "level": p["level"], "moves": p.get("moves", []), "max_hp": max_hp, "hp": max_hp, "active": False})
            
        t1[0]["active"] = True
        t2[0]["active"] = True
        
        fights = []
        
        while any(p["hp"] > 0 for p in t1) and any(p["hp"] > 0 for p in t2):
            active1 = next(i for i, p in enumerate(t1) if p["active"])
            active2 = next(i for i, p in enumerate(t2) if p["active"])
            pk1 = t1[active1]
            pk2 = t2[active2]
            
            p1_count = sum(1 for p in t1 if p["hp"] > 0)
            p2_count = sum(1 for p in t2 if p["hp"] > 0)
            c1_str = ["one", "two", "three", "four", "five", "six"][p1_count - 1]
            c2_str = ["one", "two", "three", "four", "five", "six"][p2_count - 1]
            
            battle_log = []
            battle_log.append(f"Player vs {leader_name}. Player has {c1_str} pokemon left. {pk1['name']} {pk1['hp']} HP remaining vs {leader_name} has {c2_str} pokemon left. {pk2['name']} {pk2['hp']} HP remaining.")
            
            turn = 1
            current_attacker = 1
            
            p1_state = {"sleep": 0, "bind": 0, "disable": None, "encore": 0, "last_move": None, "invuln_move": None, "moves": pk1["moves"]}
            p2_state = {"sleep": 0, "bind": 0, "disable": None, "encore": 0, "last_move": None, "invuln_move": None, "moves": pk2["moves"]}
            
            while pk1["hp"] > 0 and pk2["hp"] > 0 and turn <= 40:
                if current_attacker == 1:
                    atk_pk, def_pk = pk1, pk2
                    atk_state, def_state = p1_state, p2_state
                else:
                    atk_pk, def_pk = pk2, pk1
                    atk_state, def_state = p2_state, p1_state
                    
                display_turn = turn * 10
                
                # Severe Type Disadvantage Switching
                if current_attacker == 1:
                    def_types = self.pokemon_types.get(def_pk["name"], ["Normal"])
                    best_current_mult = -1.0
                    valid_moves = [m for m in atk_pk["moves"] if m in self.moves]
                    if not valid_moves:
                        atk_types = self.pokemon_types.get(atk_pk["name"], ["Normal"])
                        for t in atk_types:
                            mult = self.get_effectiveness_multiplier(t, def_types)
                            if mult > best_current_mult: best_current_mult = mult
                    else:
                        for move in valid_moves:
                            move_type = self.moves[move]["type"]
                            mult = self.get_effectiveness_multiplier(move_type, def_types)
                            if mult > best_current_mult: best_current_mult = mult
                            
                    if best_current_mult <= 0.5:
                        best_idx, best_bench_mult = self.get_best_pokemon_to_switch_to(t1, def_pk["name"])
                        if best_bench_mult > 1.0 and best_idx != -1:
                            old_name = atk_pk["name"]
                            pk1["active"] = False
                            t1[best_idx]["active"] = True
                            active1 = best_idx
                            pk1 = t1[active1]
                            battle_log.append(f"Turn {display_turn}. Player withdrew {old_name} and sent out {pk1['name']}.")
                            
                            p1_state = {"sleep": 0, "bind": 0, "disable": None, "encore": 0, "last_move": None, "invuln_move": None, "moves": pk1["moves"]}
                            current_attacker = 2
                            turn += 1
                            continue

                atk_name = atk_pk["name"]
                def_name = def_pk["name"]
                atk_hp = atk_pk["hp"]
                def_hp = def_pk["hp"]
                max_atk_hp = atk_pk["max_hp"]

                # Status condition checks
                if atk_state["sleep"] > 0:
                    atk_state["sleep"] -= 1
                    battle_log.append(f"Turn {display_turn}. {atk_name} is fast asleep.")
                    if atk_state["bind"] > 0:
                        atk_state["bind"] -= 1
                        atk_hp -= 5
                        if atk_hp < 0: atk_hp = 0
                        battle_log.append(f"Turn {display_turn}. {atk_name} is hurt by bind. {atk_name} has {atk_hp} HP remaining.")
                    atk_pk["hp"] = atk_hp
                    current_attacker = 2 if current_attacker == 1 else 1
                    turn += 1
                    continue

                if atk_state["invuln_move"]:
                    move = atk_state["invuln_move"]
                    atk_state["invuln_move"] = None
                else:
                    if atk_state["encore"] > 0 and atk_state["last_move"]:
                        valid_moves = [atk_state["last_move"]]
                        atk_state["encore"] -= 1
                    else:
                        valid_moves = [m for m in atk_state["moves"] if m in self.moves]
                        if not valid_moves:
                            atk_types = self.pokemon_types.get(atk_name, ["Normal"])
                            valid_moves = [m_name for m_name, m_data in self.moves.items() if m_data["type"] in atk_types or m_data["type"] == "Normal"]
                        if not valid_moves: valid_moves = ["Tackle"]
                        if atk_state["disable"] in valid_moves and len(valid_moves) > 1:
                            valid_moves.remove(atk_state["disable"])
                    
                    if is_tutorial and random.random() < 0.20:
                        move = random.choice(self.attention_testing_moves)
                    else:
                        move = random.choice(valid_moves)

                atk_state["last_move"] = move
                
                if move == "Metronome":
                    move = random.choice(list(self.moves.keys()))
                    battle_log.append(f"Turn {display_turn}. {atk_name} used Metronome!")
                    
                if move in ["Transform", "Sketch", "Mirror Move", "Copycat"]:
                    copied = def_state["last_move"]
                    if not copied: copied = "Tackle"
                    battle_log.append(f"Turn {display_turn}. {atk_name} used {move} against {def_name}. It was effective.")
                    if move in ["Transform", "Sketch"]:
                        atk_state["moves"] = [copied]
                    else:
                        move = copied
                        battle_log.append(f"Turn {display_turn}. {atk_name} used {move} against {def_name}.")
                    if move in ["Transform", "Sketch"]:
                        current_attacker = 2 if current_attacker == 1 else 1
                        turn += 1
                        continue
                        
                if move in ["Dig", "Fly"]:
                    if not atk_state.get("is_invuln", False):
                        battle_log.append(f"Turn {display_turn}. {atk_name} used {move} on itself. It was effective.")
                        atk_state["invuln_move"] = move
                        atk_state["is_invuln"] = True
                        current_attacker = 2 if current_attacker == 1 else 1
                        turn += 1
                        continue
                    else:
                        atk_state["is_invuln"] = False
                        
                move_data = self.moves.get(move, {"type": "Normal", "power": 40})
                move_type = move_data["type"]
                power = move_data["power"] if move_data.get("power", 0) > 0 else 20
                def_types = self.pokemon_types.get(def_name, ["Normal"])
                multiplier = self.get_effectiveness_multiplier(move_type, def_types)
                
                if multiplier > 1.0: phrase = "was super effective"
                elif multiplier == 1.0: phrase = "was effective"
                elif multiplier > 0.0: phrase = "was not very effective"
                else: phrase = "had no effect"
                
                if move in ["Sleep Powder", "Sing", "Hypnosis"]:
                    if multiplier > 0.0:
                        def_state["sleep"] = 2
                        battle_log.append(f"Turn {display_turn}. {atk_name} used {move} against {def_name}. It {phrase}. {def_name} fell asleep.")
                    else:
                        battle_log.append(f"Turn {display_turn}. {atk_name} used {move} against {def_name}. It {phrase}.")
                elif move in ["Bind", "Wrap", "Fire Spin"]:
                    if multiplier > 0.0:
                        def_state["bind"] = 3
                    damage = max(1, int(power * multiplier // 2)) if multiplier > 0 else 0
                    def_hp -= damage
                    if def_hp < 0: def_hp = 0
                    log_line = f"Turn {display_turn}. {atk_name} used {move} against {def_name}. It {phrase}."
                    if def_hp > 0: log_line += f" {def_name} has {def_hp} HP remaining."
                    else: log_line += f" {def_name} fainted."
                    battle_log.append(log_line)
                elif move == "Disable":
                    if def_state["last_move"]: def_state["disable"] = def_state["last_move"]
                    battle_log.append(f"Turn {display_turn}. {atk_name} used {move} against {def_name}. It {phrase}.")
                elif move == "Encore":
                    if def_state["last_move"]: def_state["encore"] = 3
                    battle_log.append(f"Turn {display_turn}. {atk_name} used {move} against {def_name}. It {phrase}.")
                elif move in ["Harden", "Defense Curl", "Recover", "Agility", "Amnesia", "Barrier", "Light Screen", "Reflect", "Withdraw", "Swords Dance", "Softboiled", "Rest", "Focus Energy", "Growth", "Meditate", "Bide"]:
                    heal_amount = max_atk_hp if move == "Rest" else (30 if move in ["Recover", "Softboiled"] else 10)
                    atk_hp += heal_amount
                    if atk_hp > max_atk_hp: atk_hp = max_atk_hp
                    if move == "Rest":
                        atk_state["sleep"] = 2
                        battle_log.append(f"Turn {display_turn}. {atk_name} used {move} on itself. It {phrase}. {atk_name} went to sleep and restored its HP.")
                    else:
                        battle_log.append(f"Turn {display_turn}. {atk_name} used {move} on itself. It {phrase}.")
                    battle_log.append(f"Turn {display_turn}. {atk_name} has {atk_hp} HP remaining.")
                else:
                    if def_state.get("is_invuln", False):
                        log_line = f"Turn {display_turn}. {atk_name} used {move} against {def_name}. It missed!"
                        if def_hp > 0: log_line += f" {def_name} has {def_hp} HP remaining."
                        else: log_line += f" {def_name} fainted."
                    else:
                        damage = max(1, int(power * multiplier // 2)) if multiplier > 0 else 0
                        def_hp -= damage
                        if def_hp < 0: def_hp = 0
                        log_line = f"Turn {display_turn}. {atk_name} used {move} against {def_name}. It {phrase}."
                        if def_hp > 0: log_line += f" {def_name} has {def_hp} HP remaining."
                        else: log_line += f" {def_name} fainted."
                    battle_log.append(log_line)
                
                if atk_state["bind"] > 0 and def_hp > 0:
                    atk_state["bind"] -= 1
                    atk_hp -= 5
                    if atk_hp < 0: atk_hp = 0
                    if atk_hp > 0:
                        battle_log.append(f"Turn {display_turn}. {atk_name} is hurt by bind. {atk_name} has {atk_hp} HP remaining.")
                    else:
                        battle_log.append(f"Turn {display_turn}. {atk_name} is hurt by bind. {atk_name} fainted.")
                        
                atk_pk["hp"] = atk_hp
                def_pk["hp"] = def_hp
                
                if def_hp <= 0 or atk_hp <= 0:
                    break
                    
                current_attacker = 2 if current_attacker == 1 else 1
                turn += 1
                
            if turn > 40:
                pk1["hp"] = 0
                pk2["hp"] = 0
                battle_log.append("Both Pokemon exhausted themselves and fainted.")
                
            if pk1["hp"] <= 0:
                if sum(1 for p in t1 if p["hp"] > 0) == 0:
                    battle_log.append("Leader won.")
                else:
                    best_idx, _ = self.get_best_pokemon_to_switch_to(t1, pk2["name"])
                    if best_idx != -1: active1 = best_idx
                    else: active1 = next(i for i, p in enumerate(t1) if p["hp"] > 0)
                    pk1["active"] = False
                    t1[active1]["active"] = True
            elif pk2["hp"] <= 0:
                if sum(1 for p in t2 if p["hp"] > 0) == 0:
                    battle_log.append("Player won.")
                else:
                    active2 = next(i for i, p in enumerate(t2) if p["hp"] > 0)
                    pk2["active"] = False
                    t2[active2]["active"] = True
                    
            fights.append(" ".join(battle_log))
            
        return fights

class PlayerLeaderCorpusBuilderV2(CorpusBuilderV2):
    def __init__(self, data_dir=None, pokedex_file="gen1_pokedex.json"):
        super().__init__(data_dir, pokedex_file)
        self.player_teams = self._load_json("player_pokemon.json")
        self.leader_teams = self._load_json("leader_pokemon.json")
        for team in self.player_teams:
            team['avg_level'] = sum(p['level'] for p in team['pokemon']) / len(team['pokemon'])
        for team in self.leader_teams:
            team['avg_level'] = sum(p['level'] for p in team['pokemon']) / len(team['pokemon'])

    def generate_battle_string(self):
        player_team = random.choice(self.player_teams)
        valid_leaders = [l for l in self.leader_teams if abs(l['avg_level'] - player_team['avg_level']) <= 15]
        if not valid_leaders:
            valid_leaders = self.leader_teams
        leader_team = random.choice(valid_leaders)
        p_team = random.sample(player_team['pokemon'], min(3, len(player_team['pokemon'])))
        l_team = random.sample(leader_team['pokemon'], min(3, len(leader_team['pokemon'])))
        def resolve_name(name):
            if "/" in name: return random.choice(name.split("/"))
            return name
        import copy
        p_team_copy = copy.deepcopy(p_team)
        l_team_copy = copy.deepcopy(l_team)
        for p in p_team_copy: p['name'] = resolve_name(p['name'])
        for l in l_team_copy: l['name'] = resolve_name(l['name'])
        
        return self._simulate_full_battle_v2(
            p1_team_data=p_team_copy,
            p2_team_data=l_team_copy,
            prefix="",
            is_tutorial=False,
            leader_name=leader_team.get("trainer", "Leader")
        )


if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(os.path.dirname(os.path.dirname(base_dir)), "corpus")
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate Gen 1 Corpus
    tutorial_gen1_output = os.path.join(output_dir, "tutorial_gen1_corpus.txt")
    print(f"Generating 10000 Gen 1 tutorial battles to {tutorial_gen1_output}...")
    random.seed(42)
    tutorial_builder_gen1 = TutorialCorpusBuilder(pokedex_file="gen1_pokedex.json")
    tutorial_builder_gen1.generate_corpus(10000, tutorial_gen1_output)
    
    player_leader_gen1_output = os.path.join(output_dir, "player_leader_gen1_corpus.txt")
    print(f"Generating 10000 Gen 1 player-leader battles to {player_leader_gen1_output}...")
    player_leader_builder_gen1 = PlayerLeaderCorpusBuilder(pokedex_file="gen1_pokedex.json")
    player_leader_builder_gen1.generate_corpus(10000, player_leader_gen1_output)

    # Generate Gen 2 Corpus
    tutorial_gen2_output = os.path.join(output_dir, "tutorial_gen2_corpus.txt")
    print(f"Generating 10000 Gen 2 tutorial battles to {tutorial_gen2_output}...")
    tutorial_builder_gen2 = TutorialCorpusBuilder(pokedex_file="gen2_pokedex.json")
    tutorial_builder_gen2.generate_corpus(10000, tutorial_gen2_output)
    
    player_leader_gen2_output = os.path.join(output_dir, "player_leader_gen2_corpus.txt")
    print(f"Generating 10000 Gen 2 player-leader battles to {player_leader_gen2_output}...")
    player_leader_builder_gen2 = PlayerLeaderCorpusBuilder(pokedex_file="gen2_pokedex.json")
    player_leader_builder_gen2.generate_corpus(10000, player_leader_gen2_output)
    
    # Generate Gen 1 V2 Corpus
    expert_v2_output = os.path.join(output_dir, "expert_corpus_v2.txt")
    print(f"Generating 10000 Gen 1 V2 expert battles to {expert_v2_output}...")
    expert_builder_v2 = PlayerLeaderCorpusBuilderV2(pokedex_file="gen1_pokedex.json")
    expert_builder_v2.generate_corpus(10000, expert_v2_output)
    
    print("Generation complete!")
