import os
from train_model import train_persona

if __name__ == "__main__":
    base_model = r"d:\antigrav\pokemon_llm\models\Foundation_v2.3\final"
    
    corpus_files = [
        "anime_corpus_tokens.txt", 
        "breeding_corpus_full_tokens.txt"
    ]
    
    # Train for 5 epochs
    train_persona(
        "Suzie_v2.3", 
        corpus_files, 
        num_epochs=5, 
        base_model_path=base_model,
        fp16=True, 
        per_device_train_batch_size=32,
        gradient_accumulation_steps=8
    )
