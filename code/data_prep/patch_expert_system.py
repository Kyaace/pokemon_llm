import os
import re

def patch_file():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    filepath = os.path.join(base_dir, "code", "corpus_generation", "expert_system.py")
    
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Patch 1: _simulate_full_battle Status condition checks
    old_status1 = """            # Status condition checks
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
            if atk_state["invuln_move"]:"""
    
    new_status1 = """            # Status condition checks
            use_sleep_talk = False
            if atk_state["sleep"] > 0:
                if "Sleep Talk" in atk_state["moves"] and not atk_state["invuln_move"]:
                    if is_tutorial or random.random() < 0.5:
                        use_sleep_talk = True
                        
                atk_state["sleep"] -= 1
                battle_log.append(f"Turn {display_turn}. {atk_name} is fast asleep.")
                
                if use_sleep_talk:
                    valid_for_sleep = [m for m in atk_state["moves"] if m in self.moves and m != "Sleep Talk"]
                    if not valid_for_sleep: valid_for_sleep = ["Tackle"]
                    move = random.choice(valid_for_sleep)
                    battle_log.append(f"Turn {display_turn}. {atk_name} used Sleep Talk against {def_name}.")
                else:
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
            if not use_sleep_talk:
                if atk_state["invuln_move"]:"""
                
    content = content.replace(old_status1, new_status1)
    
    # Patch 2: _simulate_full_battle Move Selection indentation end
    old_sel1 = """                if is_tutorial and random.random() < 0.20:
                    move = random.choice(self.attention_testing_moves)
                else:
                    move = random.choice(valid_moves)

            atk_state["last_move"] = move"""
            
    new_sel1 = """                    if is_tutorial and random.random() < 0.20:
                        move = random.choice(self.attention_testing_moves)
                    else:
                        move = random.choice(valid_moves)

            atk_state["last_move"] = "Sleep Talk" if use_sleep_talk else move"""
            
    content = content.replace(old_sel1, new_sel1)

    # Patch 3: Effectiveness 1
    old_eff1 = """            def_types = self.pokemon_types.get(def_name, ["Normal"])
            multiplier = self.get_effectiveness_multiplier(move_type, def_types)
            
            if multiplier > 1.0: phrase = "was super effective\""""
            
    new_eff1 = """            def_types = self.pokemon_types.get(def_name, ["Normal"])
            multiplier = self.get_effectiveness_multiplier(move_type, def_types)
            
            if move == "Dream Eater" and def_state["sleep"] == 0:
                multiplier = 0.0
            elif move == "Sleep Talk" and not use_sleep_talk:
                multiplier = 0.0
                
            if multiplier > 1.0: phrase = "was super effective\""""
            
    content = content.replace(old_eff1, new_eff1)
    
    # --- Now for _simulate_full_battle_v2 ---
    old_status2 = """                # Status condition checks
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

                if atk_state["invuln_move"]:"""
                
    new_status2 = """                # Status condition checks
                use_sleep_talk = False
                if atk_state["sleep"] > 0:
                    if "Sleep Talk" in atk_state["moves"] and not atk_state["invuln_move"]:
                        if is_tutorial or random.random() < 0.5:
                            use_sleep_talk = True
                            
                    atk_state["sleep"] -= 1
                    battle_log.append(f"Turn {display_turn}. {atk_name} is fast asleep.")
                    
                    if use_sleep_talk:
                        valid_for_sleep = [m for m in atk_state["moves"] if m in self.moves and m != "Sleep Talk"]
                        if not valid_for_sleep: valid_for_sleep = ["Tackle"]
                        move = random.choice(valid_for_sleep)
                        battle_log.append(f"Turn {display_turn}. {atk_name} used Sleep Talk against {def_name}.")
                    else:
                        if atk_state["bind"] > 0:
                            atk_state["bind"] -= 1
                            atk_hp -= 5
                            if atk_hp < 0: atk_hp = 0
                            battle_log.append(f"Turn {display_turn}. {atk_name} is hurt by bind. {atk_name} has {atk_hp} HP remaining.")
                        atk_pk["hp"] = atk_hp
                        current_attacker = 2 if current_attacker == 1 else 1
                        turn += 1
                        continue

                if not use_sleep_talk:
                    if atk_state["invuln_move"]:"""
                    
    content = content.replace(old_status2, new_status2)
    
    old_sel2 = """                    if is_tutorial and random.random() < 0.20:
                        move = random.choice(self.attention_testing_moves)
                    else:
                        move = random.choice(valid_moves)

                atk_state["last_move"] = move"""
                
    new_sel2 = """                        if is_tutorial and random.random() < 0.20:
                            move = random.choice(self.attention_testing_moves)
                        else:
                            move = random.choice(valid_moves)

                atk_state["last_move"] = "Sleep Talk" if use_sleep_talk else move"""
                
    content = content.replace(old_sel2, new_sel2)
    
    old_eff2 = """                move_data = self.moves.get(move, {"type": "Normal", "power": 40})
                move_type = move_data["type"]
                power = move_data["power"] if move_data.get("power", 0) > 0 else 20
                def_types = self.pokemon_types.get(def_name, ["Normal"])
                multiplier = self.get_effectiveness_multiplier(move_type, def_types)
                
                if multiplier > 1.0: phrase = "was super effective\""""
                
    new_eff2 = """                move_data = self.moves.get(move, {"type": "Normal", "power": 40})
                move_type = move_data["type"]
                power = move_data["power"] if move_data.get("power", 0) > 0 else 20
                def_types = self.pokemon_types.get(def_name, ["Normal"])
                multiplier = self.get_effectiveness_multiplier(move_type, def_types)
                
                if move == "Dream Eater" and def_state["sleep"] == 0:
                    multiplier = 0.0
                elif move == "Sleep Talk" and not use_sleep_talk:
                    multiplier = 0.0
                    
                if multiplier > 1.0: phrase = "was super effective\""""
                
    content = content.replace(old_eff2, new_eff2)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
        
    print("Patched expert_system.py successfully.")

if __name__ == "__main__":
    patch_file()
