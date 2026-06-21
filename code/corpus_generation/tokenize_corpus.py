import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import os
import re
from tokenizer import PokemonTokenizer

import time
import datetime

def tokenize_file(tokenizer, input_path, output_path, mode="FACT"):
    with open(input_path, "r", encoding="utf-8") as fin:
        lines = fin.readlines()
        
    total_lines = len(lines)
    print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Started tokenizing {total_lines} lines...")
    start_time = time.time()
    
    with open(output_path, "w", encoding="utf-8") as fout:
        for i, line in enumerate(lines):
            line = line.strip()
            # Strip the flavor text prefix e.g. [Player (Bulbasaur - Lv 10) vs Gary Oak]
            line = re.sub(r'^\[.*?\]\s*', '', line)
            
            if not line:
                continue
            token_ids = tokenizer.encode_text(line, mode=mode)
            tags = tokenizer.decode_to_tags(token_ids)
            fout.write(" ".join(tags) + "\n")
            
            if total_lines >= 10 and (i + 1) % max(1, total_lines // 10) == 0:
                percent = (i + 1) / total_lines * 100
                elapsed = time.time() - start_time
                rate = (i + 1) / elapsed if elapsed > 0 else 0
                est_remaining = (total_lines - (i + 1)) / rate if rate > 0 else 0
                print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Progress: {percent:.0f}% ({i+1}/{total_lines}) - Elapsed: {elapsed:.1f}s - Est. Remaining: {est_remaining:.1f}s")
                
    elapsed = time.time() - start_time
    print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Completed in {elapsed:.1f}s.")

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
