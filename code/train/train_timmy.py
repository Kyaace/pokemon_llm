import os
from train_model import train_persona

if __name__ == "__main__":
    base_model = r"d:\antigrav\pokemon_llm\models\foundation\final"
    corpus_files = ["anime_corpus_tokens.txt"]
    train_persona("Timmy", corpus_files, num_epochs=5, base_model_path=base_model)
