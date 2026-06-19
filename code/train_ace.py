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
            if not os.path.exists(file):
                continue
            with open(file, 'r', encoding='utf-8') as f:
                for line in f:
                    tags = line.strip().split()
                    if not tags:
                        continue
                        
                    # Default to 0 (<PAD>) if tag isn't found
                    ids = [self.vocab.get(tag, 0) for tag in tags]
                    
                    # Truncate or pad to max_length
                    if len(ids) > max_length:
                        ids = ids[:max_length]
                    else:
                        ids = ids + [0] * (max_length - len(ids)) 
                        
                    self.data.append(torch.tensor(ids, dtype=torch.long))

    def __len__(self):
        return len(self.data)
        
    def __getitem__(self, idx):
        # Causal LM training: input_ids == labels
        item = self.data[idx]
        labels = item.clone()
        # mask padding to -100 for loss calculation so the LLM ignores it
        labels[item == 0] = -100
        
        attention_mask = (item != 0).long()
        return {"input_ids": item, "attention_mask": attention_mask, "labels": labels}

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    vocab_file = os.path.join(base_dir, "vocab.json")
    corpus_dir = os.path.join(base_dir, "corpus")
    
    # We merge all datasets for the training run
    token_files = [
        os.path.join(corpus_dir, "tutorial_corpus_tokens.txt"),
        os.path.join(corpus_dir, "player_leader_corpus_tokens.txt"),
        os.path.join(corpus_dir, "johnny_corpus_tokens.txt")
    ]
    
    print("Loading datasets...")
    dataset = PokemonDataset(token_files, vocab_file, max_length=128)
    print(f"Loaded {len(dataset)} battles for training.")
    
    # 6000 ensures we have enough room for 1000+ pokemon and 5000+ numbers
    # 2. Initialize Ace Configuration
    print("Initializing Ace architecture...")
    config = GPT2Config(
        vocab_size=10000,       # 10,000 max tokens
        n_positions=512,        # 512 context window
        n_ctx=512,              
        n_embd=128,             # 128 embedding dim
        n_layer=4,              # 4 layers
        n_head=4,               # 4 heads
        bos_token_id=1,         # <BOS>
        eos_token_id=2,         # <EOS>
        pad_token_id=0          # <PAD>
    )
    
    model = GPT2LMHeadModel(config)
    
    output_dir = os.path.join(base_dir, "models", "ace")
    os.makedirs(output_dir, exist_ok=True)
    
    training_args = TrainingArguments(
        output_dir=output_dir,
        num_train_epochs=15,
        learning_rate=3e-4,
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
