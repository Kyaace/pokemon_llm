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
                        
                    ids = []
                    for tag in tags:
                        ids.append(self.vocab.get(tag, 0))
                    
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

def train_persona(persona_name, corpus_files, num_epochs=15, base_model_path=None, **kwargs):
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    vocab_file = os.path.join(base_dir, "vocab.json")
    corpus_dir = os.path.join(base_dir, "corpus")
    
    token_files = [os.path.join(corpus_dir, f) for f in corpus_files]
    
    # Sanity check: Ensure tokens are newer than raw corpus text
    for token_f in token_files:
        if token_f.endswith("_tokens.txt"):
            raw_f = token_f.replace("_tokens.txt", ".txt")
            if os.path.exists(raw_f) and os.path.exists(token_f):
                if os.path.getmtime(token_f) < os.path.getmtime(raw_f):
                    raise RuntimeError(f"\n[FATAL ERROR] Token file '{os.path.basename(token_f)}' is OLDER than raw corpus '{os.path.basename(raw_f)}'!\nDid you forget to run 'tokenize_corpus.py'?\n")
    
    print("Loading datasets...")
    dataset = PokemonDataset(token_files, vocab_file, max_length=512)
    print(f"Loaded {len(dataset)} battles for training {persona_name}.")
    
    # Initialize Architecture
    print(f"Initializing {persona_name} architecture...")
    if base_model_path and os.path.exists(base_model_path):
        print(f"Loading pre-trained weights from {base_model_path}...")
        model = GPT2LMHeadModel.from_pretrained(base_model_path)
    else:
        print(f"Initializing {persona_name} architecture from scratch...")
        torch.manual_seed(42)
        config = GPT2Config(
            vocab_size=2500,        # Safe constraint to prevent LLM hallucination
            n_positions=512,        # 512 context window
            n_embd=256,             # 256 embedding dim
            n_layer=8,              # 8 layers
            n_head=8,               # 8 heads
            bos_token_id=1,         # <BOS>
            eos_token_id=2,         # <EOS>
            pad_token_id=0          # <PAD>
        )
        model = GPT2LMHeadModel(config)
    
    output_dir = os.path.join(base_dir, "models", persona_name.lower())
    os.makedirs(output_dir, exist_ok=True)
    
    # Default arguments
    train_kwargs = {
        "output_dir": output_dir,
        "num_train_epochs": num_epochs,
        "learning_rate": 3e-4,
        "per_device_train_batch_size": 32,
        "save_steps": 1000,
        "save_total_limit": 2,
        "logging_steps": 100,
        "prediction_loss_only": True,
        "report_to": "none",
    }
    # Update with any passed kwargs
    train_kwargs.update(kwargs)
    
    training_args = TrainingArguments(**train_kwargs)

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=dataset,
    )

    print("Starting training loop...")
    trainer.train()
    
    # Export loss history for graphing
    loss_history = []
    for obj in trainer.state.log_history:
        if "loss" in obj and "step" in obj:
            epoch = obj.get("epoch", 0)
            loss_history.append({"step": obj["step"], "loss": obj["loss"], "epoch": epoch})
            
    with open(os.path.join(output_dir, "loss_history.json"), "w") as f:
        json.dump(loss_history, f, indent=4)
    print(f"Exported loss history to {os.path.join(output_dir, 'loss_history.json')}")
    
    final_model_path = os.path.join(output_dir, "final")
    trainer.save_model(final_model_path)
    print(f"Training complete! Model saved to {final_model_path}")
