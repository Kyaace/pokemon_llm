import os
from train_model import train_persona

if __name__ == "__main__":
    # Base model is the pre-trained Foundation model (to prevent conflicting priors from v1)
    base_model = r"d:\antigrav\pokemon_llm\models\foundation\final"
    
    corpus_files = [
        "tutorial_gen1_corpus_tokens.txt", 
        "tutorial_gen2_corpus_tokens.txt", 
        "qa_gen1_v2_corpus_tokens.txt",
        "qa_gen2_v2_corpus_tokens.txt"
    ]
    
    # Train for 15 epochs from scratch to fully cement the v2 dataset
    train_persona("Johnny_v2", corpus_files, num_epochs=15, base_model_path=base_model)
