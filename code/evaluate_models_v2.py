import os
import torch
from transformers import GPT2LMHeadModel
from tokenizer import PokemonTokenizer
from collections import Counter

def evaluate():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    tokenizer = PokemonTokenizer()
    
    models = ["johnny_v2.2", "spike_v2", "ace_v2.2"]
    
    queries = [
        ("Negative Logic (Evolution)", "mewtwo evolves into answer", "QUERY"),
        ("Negative Logic (Restrictive Movesets)", "caterpie has moves flamethrower answer", "QUERY"),
        ("Hatchable Encounters", "pichu obtained from answer", "QUERY"),
        ("Abstract Move Algebra (Disable)", "target unknown move logic_and attacker used disable against target answer", "JOHNNY"),
        ("Abstract Move Algebra (Transform)", "target has moves unknown move logic_and attacker used transform against target answer", "JOHNNY"),
        ("Action Prevention (Status Overwrite)", "attacker is fast asleep. logic_or attacker is hurt by bind. answer", "JOHNNY"),
        ("Zero-Shot Dual-Type Calculation", "lick against pidgey answer", "QUERY"),
        ("Zero-Shot Steel Matchup", "steel wing against magnemite answer", "QUERY"),
        ("MinMax Status Redundancy (Battle Engine)", "turn 1 clefairy used sing against onix. it was effective. target is fast asleep. turn 2 clefairy used", "BATTLE"),
        ("MinMax Base Test", "Player vs Gary Oak (Encounter 6). Player has three pokemon left. Blastoise 159 HP remaining vs Gary Oak (Encounter 6) has three pokemon left. Charizard 158 HP remaining.", "BATTLE"),
        ("Thunderbolt vs Onix", "thunderbolt against onix answer", "QUERY"),
        ("Encore Attack", "turn 1 clefairy used encore against", "BATTLE"),
        ("Eevee Evolution", "eevee evolves into answer", "QUERY")
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
                    if not decoded:
                        decoded = "<EMPTY / NO EVOLUTION>"
                    answers.append(decoded)
            except Exception as e: # Catch OOM / RuntimeError
                print(f"  Batch evaluation failed ({e}). Falling back to single sequence loop...")
                if torch.cuda.is_available():
                    torch.cuda.empty_cache()
                for _ in range(100):
                    with torch.no_grad():
                        output_tensor = model.generate(
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
    report_path = os.path.join(base_dir, "reports", "evaluation_report_v2.txt")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("=== MODEL EVALUATION PROBABILITY DISTRIBUTIONS V2 ===\n\n")
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
