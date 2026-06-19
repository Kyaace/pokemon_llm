import os
from tokenizer import PokemonTokenizer

def tokenize_file(tokenizer, input_path, output_path, mode="FACT"):
    with open(input_path, "r", encoding="utf-8") as fin, open(output_path, "w", encoding="utf-8") as fout:
        for line in fin:
            line = line.strip()
            if not line:
                continue
            token_ids = tokenizer.encode_text(line, mode=mode)
            tags = tokenizer.decode_to_tags(token_ids)
            fout.write(" ".join(tags) + "\n")

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    corpus_dir = os.path.join(base_dir, "corpus")
    
    tokenizer = PokemonTokenizer()
    
    # Process Tutorial
    tut_in = os.path.join(corpus_dir, "tutorial_corpus.txt")
    tut_out = os.path.join(corpus_dir, "tutorial_corpus_tokens.txt")
    print(f"Tokenizing {tut_in} to {tut_out}...")
    tokenize_file(tokenizer, tut_in, tut_out, mode="FACT")
    
    # Process Player-Leader
    pl_in = os.path.join(corpus_dir, "player_leader_corpus.txt")
    pl_out = os.path.join(corpus_dir, "player_leader_corpus_tokens.txt")
    print(f"Tokenizing {pl_in} to {pl_out}...")
    tokenize_file(tokenizer, pl_in, pl_out, mode="FACT")
    
    print("Tokenization complete!")
