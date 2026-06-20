import sys
import os

# Add code dir to path
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "code"))

from corpus_generation.expert_system import PlayerLeaderCorpusBuilderV2

if __name__ == "__main__":
    builder = PlayerLeaderCorpusBuilderV2()
    print("Generating a V2 Battle String...\n")
    battle_string = builder.generate_battle_string()
    print(battle_string)
