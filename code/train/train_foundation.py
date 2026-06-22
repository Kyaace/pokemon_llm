import os
from train_model import train_persona

if __name__ == "__main__":
    corpus_files = [
        "tutorial_gen1_corpus_tokens.txt",
        "qa_gen1_v2_corpus_tokens.txt",
        "breeding_corpus_lite_tokens.txt"
    ]
    train_persona("Foundation_v2.3", corpus_files)
