import os
from train_model import train_persona

if __name__ == "__main__":
    base_model = r"d:\antigrav\pokemon_llm\models\foundation\final"
    corpus_files = [
        "expert_corpus_v2_tokens.txt",
        "tutorial_gen1_corpus_tokens.txt",
        "qa_gen1_v2_corpus_tokens.txt"
    ]
    train_persona(
        "Spike_v2", 
        corpus_files, 
        num_epochs=15, 
        base_model_path=base_model,
        fp16=True, 
        per_device_train_batch_size=32,
        gradient_accumulation_steps=8
    )
