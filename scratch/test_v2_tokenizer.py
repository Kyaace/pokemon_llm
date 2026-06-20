import os
import sys

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(base_dir, "code"))

from corpus_generation.expert_system import PlayerLeaderCorpusBuilderV2
from tokenizer import PokemonTokenizer

def main():
    output_path = os.path.join(base_dir, "corpus", "expert_corpus_v2.txt")
    
    print(f"Generating 20 fights to {output_path}...")
    builder = PlayerLeaderCorpusBuilderV2()
    
    fights = []
    
    # Generate 10 random fights
    for _ in range(10):
        episodes = builder.generate_battle_string()
        fights.extend(episodes)
        
    with open(output_path, "w", encoding="utf-8") as f:
        for fight in fights:
            f.write(fight + "\n")
            
    print("Done generating! Loading Tokenizer...")
    tokenizer = PokemonTokenizer()
    
    print("\n--- Tokenizer Lengths ---")
    max_len = 0
    min_len = 999999
    
    for i, fight in enumerate(fights):
        try:
            tokens = tokenizer.encode_text(fight, mode="BATTLE")
            l = len(tokens)
            if l > max_len: max_len = l
            if l < min_len: min_len = l
            print(f"Fight {i+1:02d}: {l} tokens (Characters: {len(fight)})")
        except ValueError as e:
            print(f"Fight {i+1:02d}: ERROR - {e}")
            
    print(f"\nMax Tokens: {max_len}")
    print(f"Min Tokens: {min_len}")
    
    # Assuming context window from Ace is 512 or 1024
    print(f"Context Window 512 Check: {'PASS' if max_len <= 512 else 'FAIL'}")
    print(f"Context Window 1024 Check: {'PASS' if max_len <= 1024 else 'FAIL'}")
    
    # Export updated vocab
    tokenizer.export_vocab(os.path.join(base_dir, "code", "vocab.json"))

if __name__ == "__main__":
    main()
