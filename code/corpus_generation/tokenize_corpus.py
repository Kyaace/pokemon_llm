import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
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
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    corpus_dir = os.path.join(base_dir, "corpus")
    
    tokenizer = PokemonTokenizer()
    tokenizer.export_vocab(os.path.join(base_dir, "vocab.json"))
    
    for filename in os.listdir(corpus_dir):
        if filename.endswith(".txt") and not filename.endswith("_tokens.txt"):
            input_path = os.path.join(corpus_dir, filename)
            output_path = os.path.join(corpus_dir, filename.replace(".txt", "_tokens.txt"))
            
            # Determine mode based on filename
            if "tutorial" in filename or "player_leader" in filename or "anime" in filename:
                mode = "BATTLE"
            else:
                mode = None
                
            print(f"Tokenizing {filename} to {os.path.basename(output_path)} (Mode: {mode})...")
            tokenize_file(tokenizer, input_path, output_path, mode=mode)
            
    print("Tokenization complete!")
