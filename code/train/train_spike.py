import os
from train_model import train_persona

if __name__ == "__main__":
    base_model = r"d:\antigrav\pokemon_llm\models\foundation\final"
    corpus_files = ["player_leader_gen1_corpus_tokens.txt"]
    train_persona("Spike", corpus_files, num_epochs=15, base_model_path=base_model)
