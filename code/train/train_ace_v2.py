import os
from train_model import train_persona

if __name__ == "__main__":
    # Base model is the pre-trained Ace_v2 model
    base_model = r"d:\antigrav\pokemon_llm\models\ace_v2\final"
    
    corpus_files = [
        "tutorial_gen1_corpus_tokens.txt", 
        "tutorial_gen2_corpus_tokens.txt", 
        "qa_gen1_v2_corpus_tokens.txt",
        "qa_gen2_v2_corpus_tokens.txt",
        "expert_corpus_v2_tokens.txt",  # The new high-elo MinMax battles
        "logic_corpus_tokens.txt"
    ]
    
    # Train for 3 epochs to finetune logic without catastrophic forgetting
    train_persona(
        "Ace_v2.2", 
        corpus_files, 
        num_epochs=3, 
        base_model_path=base_model,
        fp16=True, 
        per_device_train_batch_size=32,
        gradient_accumulation_steps=8
    )
