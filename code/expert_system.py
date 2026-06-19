import json
import random
import os

class CorpusBuilder:
    def __init__(self, data_dir=None):
        if data_dir is None:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            self.data_dir = os.path.join(os.path.dirname(base_dir), "data")
        else:
            self.data_dir = data_dir
            
        self.pokemon_types = self._load_json("common_pokemon.json")
        self.moves = self._load_json("moves.json")
        self.type_chart = self._load_json("type_chart.json")
        self.pokemon_names = list(self.pokemon_types.keys())

    def _load_json(self, filename):
        filepath = os.path.join(self.data_dir, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)

    def get_effectiveness_multiplier(self, move_type, defender_types):
        """Calculates the total damage multiplier taking dual-types into account."""
        multiplier = 1.0
        for def_type in defender_types:
            if move_type in self.type_chart and def_type in self.type_chart[move_type]:
                multiplier *= self.type_chart[move_type][def_type]
        return multiplier

    def _simulate_full_battle(self, p1_name, p1_level, p1_moves, p2_name, p2_level, p2_moves, prefix=""):
        hp1 = p1_level * 5
        hp2 = p2_level * 5
        
        turn = 1
        battle_log = []
        if prefix:
            battle_log.append(prefix)
            
        current_attacker = 1
        
        while hp1 > 0 and hp2 > 0 and turn <= 20:
            if current_attacker == 1:
                atk_name, atk_moves, def_name, def_hp = p1_name, p1_moves, p2_name, hp2
            else:
                atk_name, atk_moves, def_name, def_hp = p2_name, p2_moves, p1_name, hp1
                
            atk_types = self.pokemon_types.get(atk_name, ["Normal"])
            def_types = self.pokemon_types.get(def_name, ["Normal"])
            
            valid_moves = [m for m in atk_moves if m in self.moves]
            if not valid_moves:
                valid_moves = [m_name for m_name, m_data in self.moves.items() if m_data["type"] in atk_types or m_data["type"] == "Normal"]
            if not valid_moves:
                 valid_moves = ["Tackle"]
                 
            move = random.choice(valid_moves)
            move_data = self.moves[move]
            move_type = move_data["type"]
            power = move_data["power"] if move_data["power"] > 0 else 20
            
            multiplier = self.get_effectiveness_multiplier(move_type, def_types)
            
            if multiplier > 1.0:
                phrase = "was super effective"
            elif multiplier == 1.0:
                phrase = "was effective"
            elif multiplier > 0.0:
                phrase = "was not very effective"
            else:
                phrase = "had no effect"
                
            damage = max(1, int(power * multiplier // 2))
            if multiplier == 0.0:
                damage = 0
                
            def_hp -= damage
            if def_hp < 0: def_hp = 0
            
            if current_attacker == 1:
                hp2 = def_hp
            else:
                hp1 = def_hp
                
            log_line = f"Turn {turn}. {atk_name} used {move} against {def_name}. It {phrase}."
            if def_hp > 0:
                log_line += f" {def_name} has {def_hp} HP remaining."
            else:
                log_line += f" {def_name} fainted. {atk_name} won."
                
            battle_log.append(log_line)
            
            current_attacker = 2 if current_attacker == 1 else 1
            turn += 1
            
        return " ".join(battle_log)

    def generate_corpus(self, num_samples: int, output_path: str):
        """Generates a corpus by repeatedly calling generate_battle_string()."""
        with open(output_path, "w", encoding="utf-8") as f:
            for _ in range(num_samples):
                battle_string = self.generate_battle_string()
                f.write(battle_string + "\n")

class TutorialCorpusBuilder(CorpusBuilder):
    def generate_battle_string(self):
        """Generates a synthetic, mathematically sound tutorial battle string."""
        attacker = random.choice(self.pokemon_names)
        defender = random.choice(self.pokemon_names)
        
        return self._simulate_full_battle(
            p1_name=attacker, p1_level=10, p1_moves=[],
            p2_name=defender, p2_level=10, p2_moves=[],
            prefix="[Tutorial]"
        )

class PlayerLeaderCorpusBuilder(CorpusBuilder):
    def __init__(self, data_dir=None):
        super().__init__(data_dir)
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
            prefix=f"[{player_team['trainer']} vs {leader_team['trainer']}]"
        )

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(os.path.dirname(base_dir), "corpus")
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate Tutorial Corpus
    tutorial_output = os.path.join(output_dir, "tutorial_corpus.txt")
    print(f"Generating 10000 tutorial battles to {tutorial_output}...")
    random.seed(42)
    tutorial_builder = TutorialCorpusBuilder()
    tutorial_builder.generate_corpus(10000, tutorial_output)
    
    # Generate Player-Leader Corpus
    player_leader_output = os.path.join(output_dir, "player_leader_corpus.txt")
    print(f"Generating 10000 player-leader battles to {player_leader_output}...")
    player_leader_builder = PlayerLeaderCorpusBuilder()
    player_leader_builder.generate_corpus(10000, player_leader_output)
    
    print("Generation complete!")
