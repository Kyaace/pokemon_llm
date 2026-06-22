import os
import torch
from transformers import GPT2LMHeadModel
from tokenizer import PokemonTokenizer
from collections import Counter

def test_charizard():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    tokenizer = PokemonTokenizer()
    
    models = ["johnny_v2.2", "spike_v2", "ace_v2.2"]
    text = "earthquake against charizard answer"
    mode = "QUERY"
    
    print(f"Testing query: '{text}'")
    print("-" * 40)
    
    for persona in models:
        model_dir = os.path.join(base_dir, "models", persona, "final")
        if not os.path.exists(model_dir):
            print(f"Skipping {persona}, model not found.")
            continue
            
        model = GPT2LMHeadModel.from_pretrained(model_dir)
        model.eval()
        
        input_ids = tokenizer.encode_text(text, mode=mode)
        if input_ids and input_ids[-1] == 2:
            input_ids = input_ids[:-1]
            
        input_tensor = torch.tensor([input_ids], dtype=torch.long)
        attention_mask = torch.ones_like(input_tensor)
        
        answers = []
        try:
            with torch.no_grad():
                output_tensors = model.generate(
                    input_tensor,
                    attention_mask=attention_mask,
                    max_new_tokens=20,
                    eos_token_id=[2],
                    pad_token_id=0,
                    do_sample=True,
                    temperature=0.7,
                    num_return_sequences=100
                )
            for out in output_tensors:
                output_ids = out.tolist()
                gen_ids = output_ids[len(input_ids):]
                if 2 in gen_ids:
                    gen_ids = gen_ids[:gen_ids.index(2)]
                decoded = tokenizer.decode_to_text(gen_ids).strip()
                answers.append(decoded)
        except Exception as e:
            print(f"Error generating for {persona}: {e}")
            continue
            
        counts = Counter(answers)
        print(f"\n{persona.capitalize()} Results:")
        for ans, count in counts.most_common(5):
            print(f"  {count}% -> {ans.capitalize()}")

if __name__ == "__main__":
    test_charizard()
