import os
from train_model import train_persona

if __name__ == "__main__":
    corpus_files = [
        "tutorial_gen1_corpus_tokens.txt",
        "qa_gen1_corpus_tokens.txt"
    ]
    train_persona("Foundation", corpus_files)
