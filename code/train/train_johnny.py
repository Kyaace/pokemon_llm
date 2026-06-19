import os
from train_model import train_persona

if __name__ == "__main__":
    corpus_files = [
        "tutorial_gen1_corpus_tokens.txt",
        "qa_gen2_corpus_tokens.txt"
    ]
    base_model = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "models", "foundation", "final")
    train_persona("Johnny", corpus_files, base_model_path=base_model)
