import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import torch
from transformers import GPT2LMHeadModel
from tokenizer import PokemonTokenizer
from collections import Counter

def evaluate():
    code_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    base_dir = os.path.dirname(code_dir)
    tokenizer = PokemonTokenizer()
    
    models = ["foundation_v2.3", "timmy_v2.3", "suzie_v2.3"]
    
    queries = [
        ("Pikachu Attack", "turn 1 pikachu used", "BATTLE"),
        ("Onix Attack", "turn 1 onix used", "BATTLE"),
        ("Thunderbolt vs Onix", "thunderbolt against onix answer", "QUERY"),
        ("Bulbasaur Evolution", "bulbasaur evolves into answer", "QUERY"),
        ("Squirtle Evolution", "squirtle evolves into answer", "QUERY"),
        ("Charmander Evolution", "charmander evolves into answer", "QUERY"),
        ("Pikachu Evolution", "pikachu evolves into answer", "QUERY"),
        ("Eevee Evolution", "eevee evolves into answer", "QUERY"),
        ("Onix Evolution", "onix evolves into answer", "QUERY"),
        ("Pichu Evolution", "pichu evolves into answer", "QUERY"),
        ("Cyndaquil Evolution", "cyndaquil evolves into answer", "QUERY"),
        ("Scyther Attack (Gen 1 Uncommon)", "turn 1 scyther used", "BATTLE"),
        ("Aerodactyl Attack (Gen 1 Rare)", "turn 1 aerodactyl used", "BATTLE"),
        # Breeding Questions
        ("Breeding (Foundation/Lite) - Positive 1", "charmander logic_and bulbasaur egg answer", "QUERY"),
        ("Breeding (Foundation/Lite) - Positive 2", "rhyhorn logic_and bulbasaur egg answer", "QUERY"),
        ("Breeding (Foundation/Lite) - Negative", "ekans logic_and bulbasaur egg answer", "QUERY"),
        ("Breeding (Full Only) - Positive 1", "pidgey logic_and spearow egg answer", "QUERY"),
        ("Breeding (Full Only) - Positive 2", "vulpix logic_and growlithe egg answer", "QUERY"),
        ("Breeding (Full Only) - Negative", "pidgey logic_and geodude egg answer", "QUERY")
    ]
    
    results = {}
    
    for persona in models:
        print(f"Loading {persona}...")
        model_dir = os.path.join(base_dir, "models", persona, "final")
        
        if not os.path.exists(model_dir):
            print(f"Skipping {persona}, model not found.")
            continue
            
        model = GPT2LMHeadModel.from_pretrained(model_dir)
        model.eval()
        
        results[persona] = {}
        
        for name, text, mode in queries:
            print(f"  Testing {name}...")
            
            input_ids = tokenizer.encode_text(text, mode=mode)
            if input_ids and input_ids[-1] == 2:
                input_ids = input_ids[:-1]
                
            input_tensor = torch.tensor([input_ids], dtype=torch.long)
            attention_mask = torch.ones_like(input_tensor)
            
            answers = []
            
            try:
                # Try batch generating all 100 at once to utilize GPU memory
                with torch.no_grad():
                    output_tensors = model.generate( # type: ignore
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
                    if not decoded:
                        decoded = "<EMPTY / NO EVOLUTION>"
                    answers.append(decoded)
            except Exception as e: # Catch OOM / RuntimeError
                print(f"  Batch evaluation failed ({e}). Falling back to single sequence loop...")
                if torch.cuda.is_available():
                    torch.cuda.empty_cache()
                for _ in range(100):
                    with torch.no_grad():
                        output_tensor = model.generate( # type: ignore
                            input_tensor,
                            attention_mask=attention_mask,
                            max_new_tokens=20,
                            eos_token_id=[2],
                            pad_token_id=0,
                            do_sample=True,
                            temperature=0.7
                        )
                    
                    output_ids = output_tensor[0].tolist()
                    gen_ids = output_ids[len(input_ids):]
                    if 2 in gen_ids:
                        gen_ids = gen_ids[:gen_ids.index(2)]
                        
                    decoded = tokenizer.decode_to_text(gen_ids).strip()
                    if not decoded:
                        decoded = "<EMPTY / NO EVOLUTION>"
                    answers.append(decoded)
                
            # Compute distribution
            counts = Counter(answers)
            distribution = {ans: (count/100)*100 for ans, count in counts.items()}
            results[persona][name] = distribution
            
    # Print the report
    report_path = os.path.join(base_dir, "evaluation_report_v2_3.txt")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("=== MODEL EVALUATION PROBABILITY DISTRIBUTIONS ===\n\n")
        for name, text, _ in queries:
            f.write(f"--- QUERY: {name} ---\n")
            f.write(f"Prompt: {text}\n")
            for persona in models:
                if persona not in results:
                    continue
                dist = results[persona].get(name, {})
                f.write(f"  {persona.capitalize()}:\n")
                # Sort by highest percentage
                for ans, pct in sorted(dist.items(), key=lambda item: item[1], reverse=True):
                    f.write(f"    {pct:.0f}% -> {ans}\n")
            f.write("\n")
            
    print(f"\nEvaluation complete! Report saved to {report_path}")

if __name__ == "__main__":
    evaluate()
