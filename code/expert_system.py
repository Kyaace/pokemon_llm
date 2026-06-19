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

    def generate_battle_string(self):
        """Override this method in subclasses to define how a single battle is generated."""
        raise NotImplementedError

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
        
        # Simple heuristic: Attacker uses a move matching one of its types, or a Normal type move.
        attacker_types = self.pokemon_types[attacker]
        
        # Find valid moves
        valid_moves = []
        for m_name, m_data in self.moves.items():
            if m_data["type"] in attacker_types or m_data["type"] == "Normal":
                valid_moves.append(m_name)
                
        if not valid_moves:
            # Fallback just in case
            valid_moves = [m_name for m_name, m_data in self.moves.items() if m_data["type"] == "Normal"]
        
        move = random.choice(valid_moves)
        move_type = self.moves[move]["type"]
        defender_types = self.pokemon_types[defender]
        
        multiplier = self.get_effectiveness_multiplier(move_type, defender_types)
        
        # Map multiplier to phrase
        if multiplier > 1.0:
            phrase = "was super effective"
        elif multiplier == 1.0:
            phrase = "was effective"
        elif multiplier > 0.0:
            phrase = "was not very effective"
        else:
            phrase = "had no effect"
            
        return f"{attacker} used {move} against {defender}. It {phrase}."

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
        
        attacker_types = self.pokemon_types.get(attacker_name, ["Normal"])
        defender_types = self.pokemon_types.get(defender_name, ["Normal"])
        
        attacker_moves = player_pokemon.get('moves', [])
        valid_moves = [m for m in attacker_moves if m in self.moves]
        if not valid_moves:
            valid_moves = [m_name for m_name, m_data in self.moves.items() if m_data["type"] in attacker_types or m_data["type"] == "Normal"]
        
        if not valid_moves:
             valid_moves = ["Tackle"]
             
        move = random.choice(valid_moves)
        move_type = self.moves[move]["type"]
        
        multiplier = self.get_effectiveness_multiplier(move_type, defender_types)
        
        if multiplier > 1.0:
            phrase = "was super effective"
        elif multiplier == 1.0:
            phrase = "was effective"
        elif multiplier > 0.0:
            phrase = "was not very effective"
        else:
            phrase = "had no effect"
            
        return f"[{player_team['trainer']} vs {leader_team['trainer']}] {attacker_name} used {move} against {defender_name}. It {phrase}."

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(os.path.dirname(base_dir), "corpus")
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate Tutorial Corpus
    tutorial_output = os.path.join(output_dir, "tutorial_corpus.txt")
    print(f"Generating 500 tutorial battles to {tutorial_output}...")
    random.seed(42)
    tutorial_builder = TutorialCorpusBuilder()
    tutorial_builder.generate_corpus(500, tutorial_output)
    
    # Generate Player-Leader Corpus
    player_leader_output = os.path.join(output_dir, "player_leader_corpus.txt")
    print(f"Generating 500 player-leader battles to {player_leader_output}...")
    player_leader_builder = PlayerLeaderCorpusBuilder()
    player_leader_builder.generate_corpus(500, player_leader_output)
    
    print("Generation complete!")
