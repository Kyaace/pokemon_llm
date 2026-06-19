import os
import json
import torch
from torch.utils.data import Dataset
from transformers import GPT2Config, GPT2LMHeadModel, Trainer, TrainingArguments

class PokemonDataset(Dataset):
    """
    Custom PyTorch Dataset that manually reads DSL tags and converts 
    them to integer IDs using the vocab.json mapping.
    """
    def __init__(self, token_files, vocab_file, max_length=128):
        with open(vocab_file, 'r', encoding='utf-8') as f:
            self.vocab = json.load(f)
            
        self.data = []
        for file in token_files:
            with open(file, 'r', encoding='utf-8') as f:
                for line in f:
                    tags = line.strip().split()
                    if not tags:
                        continue
                        
                    # Default to 0 (<UNKNOWN_TYPE>) if tag isn't found
                    ids = [self.vocab.get(tag, 0) for tag in tags]
                    
                    # Truncate or pad to max_length
                    if len(ids) > max_length:
                        ids = ids[:max_length]
                    else:
                        # 0 is our <UNKNOWN_TYPE> which acts as padding here
                        ids = ids + [0] * (max_length - len(ids)) 
                        
                    self.data.append(torch.tensor(ids, dtype=torch.long))

    def __len__(self):
        return len(self.data)
        
    def __getitem__(self, idx):
        # Causal LM training: input_ids == labels
        item = self.data[idx]
        return {"input_ids": item, "labels": item.clone()}

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    vocab_file = os.path.join(base_dir, "vocab.json")
    corpus_dir = os.path.join(base_dir, "corpus")
    
    # We merge both datasets for the training run
    token_files = [
        os.path.join(corpus_dir, "tutorial_corpus_tokens.txt"),
        os.path.join(corpus_dir, "player_leader_corpus_tokens.txt")
    ]
    
    print("Loading datasets...")
    dataset = PokemonDataset(token_files, vocab_file, max_length=128)
    print(f"Loaded {len(dataset)} battles for training.")
    
    # 6000 ensures we have enough room for 1000+ pokemon and 5000+ numbers
    vocab_size = 6000 

    print("Initializing Timmy architecture (GPT-2 Micro)...")
    config = GPT2Config(
        vocab_size=vocab_size,
        n_positions=256,
        n_embd=128,      # Tiny embedding
        n_layer=4,       # Only 4 layers! Very fast.
        n_head=4,
        pad_token_id=0,
        bos_token_id=1,  # <FACT>
        eos_token_id=0,
    )
    
    model = GPT2LMHeadModel(config)
    
    output_dir = os.path.join(base_dir, "models", "timmy")
    os.makedirs(output_dir, exist_ok=True)
    
    training_args = TrainingArguments(
        output_dir=output_dir,
        num_train_epochs=3,
        per_device_train_batch_size=32,
        save_steps=1000,
        save_total_limit=2,
        logging_steps=100,
        prediction_loss_only=True,
        report_to="none", # Disables wandb logging if installed
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=dataset,
    )

    print("Starting training loop...")
    trainer.train()
    
    final_model_path = os.path.join(output_dir, "final")
    trainer.save_model(final_model_path)
    print(f"Training complete! Model saved to {final_model_path}")

if __name__ == "__main__":
    main()
