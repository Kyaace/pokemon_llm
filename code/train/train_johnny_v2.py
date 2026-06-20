import os
from train_model import train_persona

if __name__ == "__main__":
    # Base model is the pre-trained Johnny v1
    base_model = r"d:\antigrav\pokemon_llm\models\johnny\final"
    
    corpus_files = [
        "tutorial_gen1_corpus_tokens.txt", 
        "tutorial_gen2_corpus_tokens.txt", 
        "qa_gen1_v2_corpus_tokens.txt",
        "qa_gen2_v2_corpus_tokens.txt"
    ]
    
    # Train for 4 epochs with a lower learning rate for incremental update
    train_persona("Johnny_v2", corpus_files, num_epochs=4, base_model_path=base_model, learning_rate=5e-5)
