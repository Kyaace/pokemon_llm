import os
from train_model import train_persona

if __name__ == "__main__":
    base_model = r"d:\antigrav\pokemon_llm\models\foundation_v2.3\final"
    corpus_files = [
        "qa_gen2_v2_corpus_tokens.txt",
        "tutorial_gen1_corpus_tokens.txt",
        "logic_corpus_tokens.txt"
    ]
    train_persona(
        "Johnny_v2.3", 
        corpus_files, 
        num_epochs=5, 
        base_model_path=base_model,
        fp16=True, 
        per_device_train_batch_size=32,
        gradient_accumulation_steps=8
    )
