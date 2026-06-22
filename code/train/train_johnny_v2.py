import os
from train_model import train_persona

if __name__ == "__main__":
    # Base model is the pre-trained Johnny_v2 model to build upon its knowledge
    base_model = r"d:\antigrav\pokemon_llm\models\johnny_v2\final"
    
    corpus_files = [
        "tutorial_gen1_corpus_tokens.txt", 
        "tutorial_gen2_corpus_tokens.txt", 
        "qa_gen1_v2_corpus_tokens.txt",
        "qa_gen2_v2_corpus_tokens.txt",
        "logic_corpus_tokens.txt"
    ]
    
    # Train for 3 epochs to finetune logic without catastrophic forgetting
    train_persona("Johnny_v2.2", corpus_files, num_epochs=5, base_model_path=base_model)
