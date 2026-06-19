import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import os
import re
from tokenizer import PokemonTokenizer

def verify_corpus(file_path):
    tokenizer = PokemonTokenizer()
    unknown_words = set()
    
    with open(file_path, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            text = line.strip().lower()
            if not text:
                continue
                
            # Strip flavor text prefix e.g. [Anime] or [Tutorial]
            text = re.sub(r'^\[.*?\]\s*', '', text)
            
            search_terms = sorted(tokenizer.str_to_id.keys(), key=len, reverse=True)
            covered = [False] * len(text)
            
            # Find all known terms and mark their characters as covered
            for term in search_terms:
                # Standard word boundary matching
                for m in re.finditer(r'\b' + re.escape(term) + r'\b', text):
                    for i in range(m.start(), m.end()):
                        covered[i] = True
                
                # Special character matching
                if "♀" in term or "♂" in term:
                    for m in re.finditer(re.escape(term), text):
                        for i in range(m.start(), m.end()):
                            covered[i] = True
                            
                # Punctuation matching
                if term.endswith("."):
                    for m in re.finditer(re.escape(term), text):
                        for i in range(m.start(), m.end()):
                            covered[i] = True
                            
            # Numbers are natively supported as IDs 5000+
            for m in re.finditer(r'\b\d+\b', text):
                for i in range(m.start(), m.end()):
                    covered[i] = True
                    
            # Find any alphabetic words that were not covered by a known token
            for m in re.finditer(r'\b[a-z]+\b', text):
                start_pos = m.start()
                if not covered[start_pos]:
                    word = m.group()
                    unknown_words.add(word)
                    
    if unknown_words:
        print(f"Found {len(unknown_words)} unknown words in {os.path.basename(file_path)}:")
        for w in sorted(unknown_words):
            print(f"  - {w}")
    else:
        print(f"Corpus {os.path.basename(file_path)} is perfectly clean! No unknown words.")

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    corpus_dir = os.path.join(base_dir, "corpus")
    
    if not os.path.exists(corpus_dir):
        print("Corpus directory not found.")
        exit()
        
    print("Checking corpuses against current vocabulary dictionary...")
    for f in os.listdir(corpus_dir):
        if f.endswith(".txt") and not f.endswith("_tokens.txt"):
            print(f"\n--- Verifying {f} ---")
            verify_corpus(os.path.join(corpus_dir, f))
