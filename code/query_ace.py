import cmd2
import torch
import os
from transformers import GPT2LMHeadModel
from tokenizer import PokemonTokenizer

class AceCLI(cmd2.Cmd):
    intro = "\n=========================================\nWelcome to the Ace Inference Interface!\n=========================================\nType 'help' to list commands.\n"
    prompt = "(ace) "

    def __init__(self):
        super().__init__()
        
        # Load the tokenizer
        print("Loading tokenizer...")
        self.tokenizer = PokemonTokenizer()
        
        # Load the model
        print("Loading Ace...")
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        model_dir = os.path.join(base_dir, "models", "ace", "final")
        
        if not os.path.exists(model_dir):
            print(f"Error: Could not find model at {model_dir}. Please run train_ace.py first.")
            return
            
        self.model = GPT2LMHeadModel.from_pretrained(model_dir)
        self.model.eval()
        print("Ace is awake!")
        
        # Define the tokens we want to stop generating at
        self.stop_tokens = [2] # <EOS>

    def _generate(self, input_text, mode):
        # 1. Encode free text into token IDs
        input_ids = self.tokenizer.encode_text(input_text, mode=mode)
        
        if not input_ids:
            self.poutput("Could not encode any tokens from that input.")
            return
            
        # Display the parsed tags to the user so they know what Ace sees
        tags = self.tokenizer.decode_to_tags(input_ids)
        self.poutput(f"\n[Ace sees]: {' '.join(tags)}")
        
        input_tensor = torch.tensor([input_ids], dtype=torch.long)
        attention_mask = torch.ones_like(input_tensor)
        
        # 2. Generate novel tokens
        with torch.no_grad():
            output_tensor = self.model.generate(
                input_tensor,
                attention_mask=attention_mask,
                max_new_tokens=50, # Allow up to ~50 new tokens
                eos_token_id=self.stop_tokens,
                pad_token_id=0,
                do_sample=False,    # Greedy decoding for strict mathematical grammar
            )
            
        # 3. Decode the generated tokens back to English text
        output_ids = output_tensor[0].tolist()
        
        # Decode back to game-sounding English
        decoded_text = self.tokenizer.decode_to_text(output_ids)
        self.poutput(f"\n[Generation]:\n{decoded_text}\n")

    def do_battle(self, arg):
        """Generates a novel battle from a seed text. 
        Example: battle Bulbasaur used Tackle"""
        if not arg:
            self.poutput("Please provide a seed. Example: battle Bulbasaur used Tackle")
            return
            
        self._generate(arg, mode="FACT")

    def do_query(self, arg):
        """Asks Ace a query.
        Example: query Bulbasaur weak to"""
        if not arg:
            self.poutput("Please provide a query. Example: query Bulbasaur weak to")
            return
            
        self._generate(arg, mode="QUERY")

if __name__ == '__main__':
    app = AceCLI()
    app.cmdloop()
