import os
import re
from tokenizer import PokemonTokenizer

def tokenize_file(tokenizer, input_path, output_path, mode="FACT"):
    with open(input_path, "r", encoding="utf-8") as fin, open(output_path, "w", encoding="utf-8") as fout:
        for line in fin:
            line = line.strip()
            # Strip the flavor text prefix e.g. [Player (Bulbasaur - Lv 10) vs Gary Oak]
            line = re.sub(r'^\[.*?\]\s*', '', line)
            
            if not line:
                continue
            token_ids = tokenizer.encode_text(line, mode=mode)
            tags = tokenizer.decode_to_tags(token_ids)
            fout.write(" ".join(tags) + "\n")

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    corpus_dir = os.path.join(base_dir, "corpus")
    
    tokenizer = PokemonTokenizer()
    tokenizer.export_vocab(os.path.join(base_dir, "vocab.json"))
    
    # Process Tutorial
    tut_in = os.path.join(corpus_dir, "tutorial_corpus.txt")
    tut_out = os.path.join(corpus_dir, "tutorial_corpus_tokens.txt")
    print(f"Tokenizing {tut_in} to {tut_out}...")
    tokenize_file(tokenizer, tut_in, tut_out, mode="BATTLE")

    # Process Spike (Player/Leader)
    spike_in = os.path.join(corpus_dir, "player_leader_corpus.txt")
    spike_out = os.path.join(corpus_dir, "player_leader_corpus_tokens.txt")
    print(f"Tokenizing {spike_in} to {spike_out}...")
    tokenize_file(tokenizer, spike_in, spike_out, mode="BATTLE")
    
    # Process Johnny Facts/Queries
    johnny_in = os.path.join(corpus_dir, "johnny_corpus.txt")
    johnny_out = os.path.join(corpus_dir, "johnny_corpus_tokens.txt")
    # Only process if it exists, since they might not have generated it yet
    if os.path.exists(johnny_in):
        print(f"Tokenizing {johnny_in} to {johnny_out}...")
        tokenize_file(tokenizer, johnny_in, johnny_out, mode=None)

    # Process Anime
    anime_in = os.path.join(corpus_dir, "anime_corpus.txt")
    anime_out = os.path.join(corpus_dir, "anime_corpus_tokens.txt")
    if os.path.exists(anime_in):
        print(f"Tokenizing {anime_in} to {anime_out}...")
        tokenize_file(tokenizer, anime_in, anime_out, mode="BATTLE")
    
    print("Tokenization complete!")
