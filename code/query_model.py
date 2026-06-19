import cmd2
import torch
import os
from transformers import GPT2LMHeadModel
from tokenizer import PokemonTokenizer

class ModelCLI(cmd2.Cmd):
    def __init__(self, persona_name):
        super().__init__()
        
        # Safely hide default cmd2 commands from the help menu
        for cmd in ['alias', 'macro', 'run_pyscript', 'run_script', 'shell', 'set', 'shortcuts', 'edit', 'history', 'py', 'ipy']:
            self.hidden_commands.append(cmd)
        
        self.persona_name = persona_name.lower()
        self.intro = f"\n=========================================\nWelcome to the {persona_name.capitalize()} Inference Interface!\n=========================================\nType 'help' to list commands.\n"
        self.prompt = f"({self.persona_name}) "
        
        # Load the tokenizer
        print("Loading tokenizer...")
        self.tokenizer = PokemonTokenizer()
        
        # Load the model
        print(f"Loading {persona_name.capitalize()}...")
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        model_dir = os.path.join(base_dir, "models", self.persona_name, "final")
        
        if not os.path.exists(model_dir):
            print(f"Error: Could not find model at {model_dir}. Please run train_{self.persona_name}.py first.")
            return
            
        self.model = GPT2LMHeadModel.from_pretrained(model_dir)
        self.model.eval()
        print(f"{persona_name.capitalize()} is awake!")
        
        # Define the tokens we want to stop generating at
        self.stop_tokens = [2] # <EOS>

    def _generate(self, input_text, mode):
        # 1. Encode free text into token IDs
        try:
            input_ids = self.tokenizer.encode_text(input_text, mode=mode)
        except ValueError as e:
            self.poutput(f"Error: {e}")
            self.poutput("Please try again with recognized words.")
            return
            
        # Remove the <EOS> token from the prompt, otherwise the model thinks it's already done!
        if input_ids and input_ids[-1] == 2:
            input_ids = input_ids[:-1]
            
        if not input_ids:
            self.poutput("Could not encode any tokens from that input.")
            return
            
        # Display the parsed tags to the user so they know what the model sees
        tags = self.tokenizer.decode_to_tags(input_ids)
        self.poutput(f"\n[{self.persona_name.capitalize()} sees]: {' '.join(tags)}")
        
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
                do_sample=False,    # Greedy decoding
            )
            
        # 3. Decode the generated tokens back to English text
        output_ids = output_tensor[0].tolist()
        
        # Decode back to game-sounding English
        decoded_text = self.tokenizer.decode_to_text(output_ids)
        self.poutput(f"\n[Generation]:\n{decoded_text}\n")

    def default(self, line):
        text = line.strip()
        if text.startswith("query ") or text.startswith("fact "):
            self._generate(text, mode=None)
        elif text.startswith("battle "):
            self._generate(text[7:], mode="BATTLE")

    def do_battle(self, arg):
        """Generates a novel battle from a seed text. 
        Example: battle Bulbasaur used Tackle"""
        if not arg:
            self.poutput("Please provide a seed. Example: battle Bulbasaur used Tackle")
            return
            
        self._generate(arg, mode="BATTLE")

    def do_query(self, arg):
        """Asks a query.
        Example: query Bulbasaur weak to"""
        if not arg:
            self.poutput("Please provide a query. Example: query Bulbasaur weak to")
            return
            
        self._generate(arg, mode="QUERY")

    def do_exit(self, arg):
        """Exit the interface."""
        return self.do_quit(arg)

if __name__ == '__main__':
    import argparse
    import os
    import sys
    
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    models_dir = os.path.join(base_dir, "models")
    
    # Check available models
    available_models = []
    if os.path.exists(models_dir):
        for d in os.listdir(models_dir):
            if os.path.isdir(os.path.join(models_dir, d)):
                available_models.append(d)
                
    parser = argparse.ArgumentParser(description="Query a specific model.")
    parser.add_argument("model", nargs="?", help="The name of the model to query (e.g., Timmy, Foundation)")
    args = parser.parse_args()
    
    if not args.model:
        if available_models:
            print("Usage: python query_model.py <model_name>")
            print(f"Available models: {', '.join(available_models)}")
        else:
            print("Usage: python query_model.py <model_name>")
            print("No trained models found in the models/ directory.")
        sys.exit(1)
    
    app = ModelCLI(args.model)
    app.cmdloop()
