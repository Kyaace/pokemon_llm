import os
import sys

# Add the parent code directory to path so we can import tokenizer
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json
import torch
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from scipy.spatial.distance import cosine
from transformers import GPT2LMHeadModel
from tokenizer import PokemonTokenizer

def run_probe(model_name="foundation"):
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    model_dir = os.path.join(base_dir, "models", model_name, "final")
    analysis_dir = os.path.join(base_dir, "analysis", model_name)
    os.makedirs(analysis_dir, exist_ok=True)
    
    report_path = os.path.join(analysis_dir, "embedding_probe_report.txt")
    with open(report_path, "w") as f:
        f.write("=== Embedding Vector Analysis Report ===\n\n")

    print(f"Loading Foundation Model to CPU from {model_dir}...")
    tokenizer = PokemonTokenizer()
    model = GPT2LMHeadModel.from_pretrained(model_dir)
    
    # Extract the Word Token Embedding Matrix
    wte = model.transformer.wte.weight.detach().numpy()
    
    def get_vec(token_str):
        # We need the token ID
        token_id = tokenizer.tag_to_id.get(token_str)
        if token_id is None:
            return None
        return wte[token_id]
        
    def sim(v1, v2):
        if v1 is None or v2 is None: return 0.0
        return 1.0 - cosine(v1, v2)

    def log(msg):
        print(msg)
        with open(report_path, "a") as f:
            f.write(msg + "\n")

    # Load Pokedex for Types
    gen1_path = os.path.join(base_dir, "data", "gen1_pokedex.json")
    gen2_path = os.path.join(base_dir, "data", "gen2_pokedex.json")
    pokedex = {}
    if os.path.exists(gen1_path):
        with open(gen1_path, "r") as f: pokedex.update(json.load(f))
    if os.path.exists(gen2_path):
        with open(gen2_path, "r") as f: pokedex.update(json.load(f))
        
    type_colors = {
        "Bug": "#A8B820", "Dark": "#5C483B", "Dragon": "#700AEE",
        "Electric": "#F8D030", "Fairy": "#EE99AC", "Fighting": "#94352D",
        "Fire": "#F08030", "Flying": "#A890F0", "Ghost": "#614C83",
        "Grass": "#2DCD45", "Ground": "#E0C068", "Ice": "#98D8D8",
        "Normal": "#A8A878", "Poison": "#883688", "Psychic": "#FF6996",
        "Rock": "#B8A038", "Steel": "#B8B8D0", "Water": "#149EFF"
    }

    log("--- Experiment A: Pokemon Type Clustering ---")
    pkmn_names = []
    pkmn_vecs = []
    pkmn_colors = []
    
    for pkmn_name, types in pokedex.items():
        token = f"<PKMN_{pkmn_name.upper()}>"
        vec = get_vec(token)
        if vec is not None:
            pkmn_names.append(pkmn_name)
            pkmn_vecs.append(vec)
            p_type = types[0]
            pkmn_colors.append(type_colors.get(p_type, "#000000"))
            
    if pkmn_vecs:
        pca = PCA(n_components=2)
        pkmn_2d = pca.fit_transform(pkmn_vecs)
        
        import matplotlib.patheffects as PathEffects

        fig, ax = plt.subplots(figsize=(12, 10))
        fig.patch.set_facecolor('#5A5A5A')
        ax.set_facecolor('#5A5A5A')

        plt.scatter(pkmn_2d[:, 0], pkmn_2d[:, 1], c=pkmn_colors, s=50, alpha=0.8, edgecolors='none')
        
        # Annotate a few well-known pokemon to see where they sit
        for name in ["Bulbasaur", "Charmander", "Squirtle", "Pikachu", "Eevee", "Vaporeon", "Jolteon", "Flareon", "Mewtwo", "Chikorita", "Pichu", "Steelix", "Onix", "Espeon", "Umbreon"]:
            if name in pkmn_names:
                idx = pkmn_names.index(name)
                txt = plt.annotate(name, (pkmn_2d[idx, 0], pkmn_2d[idx, 1]), fontsize=9, alpha=0.9, color='white')
                txt.set_path_effects([PathEffects.withStroke(linewidth=3, foreground='black')])
                
        title = plt.title(f"PCA of Pokemon Token Embeddings - {model_name.capitalize()} Model", color='white')
        title.set_path_effects([PathEffects.withStroke(linewidth=3, foreground='black')])

        ax.tick_params(colors='white')
        for spine in ax.spines.values():
            spine.set_color('white')

        pca_path = os.path.join(analysis_dir, "pokemon_type_pca.png")
        plt.savefig(pca_path, dpi=150, facecolor=fig.get_facecolor(), edgecolor='none')
        plt.close()
        log(f"Saved PCA clustering plot to {pca_path}")
        
        # Generate Gen 1 only zoomed plot
        if os.path.exists(gen1_path):
            with open(gen1_path, "r") as f:
                gen1_names = list(json.load(f).keys())
            
            gen1_indices = [i for i, name in enumerate(pkmn_names) if name in gen1_names]
            if gen1_indices:
                gen1_2d = pkmn_2d[gen1_indices]
                gen1_colors = [pkmn_colors[i] for i in gen1_indices]
                gen1_names_filtered = [pkmn_names[i] for i in gen1_indices]
                
                fig, ax = plt.subplots(figsize=(12, 10))
                fig.patch.set_facecolor('#5A5A5A')
                ax.set_facecolor('#5A5A5A')

                plt.scatter(gen1_2d[:, 0], gen1_2d[:, 1], c=gen1_colors, s=50, alpha=0.8, edgecolors='none')
                
                for name in ["Bulbasaur", "Charmander", "Squirtle", "Pikachu", "Eevee", "Vaporeon", "Jolteon", "Flareon", "Mewtwo", "Onix"]:
                    if name in gen1_names_filtered:
                        idx = gen1_names_filtered.index(name)
                        txt = plt.annotate(name, (gen1_2d[idx, 0], gen1_2d[idx, 1]), fontsize=9, alpha=0.9, color='white')
                        txt.set_path_effects([PathEffects.withStroke(linewidth=3, foreground='black')])
                        
                title = plt.title(f"PCA of Gen 1 Pokemon - {model_name.capitalize()} Model (Zoomed)", color='white')
                title.set_path_effects([PathEffects.withStroke(linewidth=3, foreground='black')])

                ax.tick_params(colors='white')
                for spine in ax.spines.values():
                    spine.set_color('white')

                pca_gen1_path = os.path.join(analysis_dir, "pokemon_type_pca_gen1.png")
                plt.savefig(pca_gen1_path, dpi=150, facecolor=fig.get_facecolor(), edgecolor='none')
                plt.close()
                log(f"Saved Gen 1 Zoomed PCA plot to {pca_gen1_path}")
                
                # Generate Gym Battles PCA plot
                fig, ax = plt.subplots(figsize=(12, 10))
                fig.patch.set_facecolor('#5A5A5A')
                ax.set_facecolor('#5A5A5A')

                plt.scatter(gen1_2d[:, 0], gen1_2d[:, 1], c=gen1_colors, s=50, alpha=0.3, edgecolors='none')
                
                ash_team = ["Pikachu", "Haunter", "Bulbasaur", "Squirtle", "Charizard", "Pidgeotto", "Butterfree"]
                gym_team = ["Onix", "Staryu", "Raichu", "Kadabra", "Gloom", "Venonat", "Magmar", "Rhydon"]
                
                for name in ash_team + gym_team:
                    if name in gen1_names_filtered:
                        idx = gen1_names_filtered.index(name)
                        color = "lightblue" if name in ash_team else "lightcoral"
                        plt.scatter([gen1_2d[idx, 0]], [gen1_2d[idx, 1]], color=color, s=100, edgecolors='white', linewidth=1.5, zorder=5)
                        txt = plt.annotate(name, (gen1_2d[idx, 0], gen1_2d[idx, 1]), fontsize=11, alpha=1.0, color=color, fontweight='bold', zorder=10)
                        txt.set_path_effects([PathEffects.withStroke(linewidth=3, foreground='black')])
                        
                title = plt.title(f"PCA of Ash vs Gym Leaders - {model_name.capitalize()} Model", color='white')
                title.set_path_effects([PathEffects.withStroke(linewidth=3, foreground='black')])

                ax.tick_params(colors='white')
                for spine in ax.spines.values():
                    spine.set_color('white')

                pca_gym_path = os.path.join(analysis_dir, "Pokemon_PCA_gym_battles.png")
                plt.savefig(pca_gym_path, dpi=150, facecolor=fig.get_facecolor(), edgecolor='none')
                plt.close()
                log(f"Saved Gym Battles PCA plot to {pca_gym_path}")
        
        # Save raw numbers to CSV and find the outlier cluster on the far left
        csv_path = os.path.join(analysis_dir, "pokemon_pca_coordinates.csv")
        outliers = []
        with open(csv_path, "w") as f:
            f.write("Pokemon,Type,PCA_X,PCA_Y\n")
            for i, name in enumerate(pkmn_names):
                x, y = pkmn_2d[i, 0], pkmn_2d[i, 1]
                f.write(f"{name},{pkmn_colors[i]},{x},{y}\n")
                if x < -0.5:  # Left side outliers
                    outliers.append(name)
        log(f"Saved raw 2D coordinates to {csv_path}")
        log(f"Outlier Cluster on the left (X < -0.5): {', '.join(outliers)}")
    
    log("\n--- Experiment B: Evolutionary Vector Arithmetic ---")
    base_evolutions = [
        ("Charmander", "Charmeleon"),
        ("Squirtle", "Wartortle"),
        ("Bulbasaur", "Ivysaur")
    ]
    
    evo_deltas = []
    for p1, p2 in base_evolutions:
        v1 = get_vec(f"<PKMN_{p1.upper()}>")
        v2 = get_vec(f"<PKMN_{p2.upper()}>")
        if v1 is not None and v2 is not None:
            delta = v2 - v1
            evo_deltas.append((f"{p1}->{p2}", delta))
            
    if len(evo_deltas) >= 2:
        sim1 = sim(evo_deltas[0][1], evo_deltas[1][1])
        log(f"Cosine Similarity between {evo_deltas[0][0]} and {evo_deltas[1][0]} vectors: {sim1:.4f}")
        sim2 = sim(evo_deltas[0][1], evo_deltas[2][1])
        log(f"Cosine Similarity between {evo_deltas[0][0]} and {evo_deltas[2][0]} vectors: {sim2:.4f}")
        
    v_eevee = get_vec("<PKMN_EEVEE>")
    v_vap = get_vec("<PKMN_VAPOREON>")
    v_flare = get_vec("<PKMN_FLAREON>")
    if v_eevee is not None and v_vap is not None and v_flare is not None:
        delta_water = v_vap - v_eevee
        delta_fire = v_flare - v_eevee
        log(f"Cosine Similarity between Eevee->Vaporeon and Eevee->Flareon: {sim(delta_water, delta_fire):.4f}")

    log("\n--- Experiment C: Type Advantage Space ---")
    v_tb = get_vec("<MOVE_THUNDERBOLT>")
    v_gya = get_vec("<PKMN_GYARADOS>")
    v_onix = get_vec("<PKMN_ONIX>")
    v_zap = get_vec("<PKMN_ZAPDOS>")
    if all(v is not None for v in [v_tb, v_gya, v_onix, v_zap]):
        log(f"Similarity: Thunderbolt <-> Gyarados (4x Super Effective): {sim(v_tb, v_gya):.4f}")
        log(f"Similarity: Thunderbolt <-> Onix (Immune): {sim(v_tb, v_onix):.4f}")
        log(f"Similarity: Thunderbolt <-> Zapdos (Same Type): {sim(v_tb, v_zap):.4f}")

    log("\n--- Experiment D: Meta-Concept Structuring ---")
    meta_tokens = ["<BATTLE>", "<QUERY>", "<TURN>", "<ACTION_USE>", "<HP_REMAINING>", "<EFFECT_SUPER>", "<EFFECT_WEAK>"]
    meta_vecs = {}
    for mt in meta_tokens:
        vec = get_vec(mt)
        if vec is not None:
            meta_vecs[mt] = vec
            
    if "<BATTLE>" in meta_vecs and "<QUERY>" in meta_vecs:
        log(f"Similarity <BATTLE> to <QUERY>: {sim(meta_vecs['<BATTLE>'], meta_vecs['<QUERY>']):.4f}")
    if "<EFFECT_SUPER>" in meta_vecs and "<EFFECT_WEAK>" in meta_vecs:
        log(f"Similarity <EFFECT_SUPER> to <EFFECT_WEAK>: {sim(meta_vecs['<EFFECT_SUPER>'], meta_vecs['<EFFECT_WEAK>']):.4f}")
    if "<ACTION_USE>" in meta_vecs and "<TURN>" in meta_vecs:
        log(f"Similarity <ACTION_USE> to <TURN>: {sim(meta_vecs['<ACTION_USE>'], meta_vecs['<TURN>']):.4f}")

    log("\n--- Experiment E: Unified Concept PCA ---")
    unified_names = []
    unified_vecs = []
    unified_colors = []
    
    # 1. Battle terms
    battle_terms = ["<BATTLE>", "<TURN>", "<HP_REMAINING>", "<FAINTED>", "<BATTLE_WON>", "<BATTLE_LOST>", "<ACTION_USE>", "<TARGET_ON>", "<TARGET_AGAINST>", "<EFFECT_SUPER>", "<EFFECT_NORMAL>", "<EFFECT_WEAK>", "<EFFECT_NONE>"]
    for bt in battle_terms:
        v = get_vec(bt)
        if v is not None:
            unified_names.append(bt)
            unified_vecs.append(v)
            unified_colors.append("lightcoral")
            
    # 2. Query terms
    query_terms = ["<QUERY>", "<FACT>", "<ANSWER>", "<HAS>", "<IS>", "<TYPE>", "<BASE_HP>", "<EVOLVES_INTO>", "<POWER>"]
    for qt in query_terms:
        v = get_vec(qt)
        if v is not None:
            unified_names.append(qt)
            unified_vecs.append(v)
            unified_colors.append("lightblue")
            
    # 3. Pokemon
    for pkmn_name, types in pokedex.items():
        v = get_vec(f"<PKMN_{pkmn_name.upper()}>")
        if v is not None:
            unified_names.append(pkmn_name)
            unified_vecs.append(v)
            unified_colors.append(type_colors.get(types[0], "#000000"))
            
    # 4. Moves
    moves_path = os.path.join(base_dir, "data", "moves.json")
    if os.path.exists(moves_path):
        with open(moves_path, "r") as f:
            moves = json.load(f)
        for move_name, info in moves.items():
            formatted_move = move_name.upper().replace(" ", "_")
            v = get_vec(f"<MOVE_{formatted_move}>")
            if v is not None:
                unified_names.append(move_name)
                unified_vecs.append(v)
                unified_colors.append(type_colors.get(info.get("type"), "#000000"))
                
    # 5. Types
    for t_name in type_colors.keys():
        v = get_vec(f"<TYPE_{t_name.upper()}>")
        if v is not None:
            unified_names.append(f"TYPE_{t_name.upper()}")
            unified_vecs.append(v)
            unified_colors.append(type_colors[t_name])
            
    if unified_vecs:
        import matplotlib.patheffects as PathEffects
        pca_unified = PCA(n_components=2)
        uni_2d = pca_unified.fit_transform(unified_vecs)
        
        fig, ax = plt.subplots(figsize=(14, 12))
        fig.patch.set_facecolor('#5A5A5A')
        ax.set_facecolor('#5A5A5A')
        
        # Plot everyone as small points
        plt.scatter(uni_2d[:, 0], uni_2d[:, 1], c=unified_colors, s=30, alpha=0.5, edgecolors='none')
        
        # Annotate ONLY Battle terms, Query terms, Types, and a few key Pokemon/Moves
        annotate_list = battle_terms + query_terms + [f"TYPE_{t.upper()}" for t in type_colors.keys()] + ["Pikachu", "Charizard", "Thunderbolt", "Flamethrower"]
        
        for name in annotate_list:
            if name in unified_names:
                idx = unified_names.index(name)
                c = unified_colors[idx]
                txt = plt.annotate(name, (uni_2d[idx, 0], uni_2d[idx, 1]), fontsize=9, alpha=1.0, color=c, fontweight='bold')
                txt.set_path_effects([PathEffects.withStroke(linewidth=3, foreground='black')])
                
        title = plt.title(f"Unified Concept PCA - {model_name.capitalize()} Model", color='white')
        title.set_path_effects([PathEffects.withStroke(linewidth=3, foreground='black')])

        ax.tick_params(colors='white')
        for spine in ax.spines.values():
            spine.set_color('white')

        uni_path = os.path.join(analysis_dir, "unified_concept_pca.png")
        plt.savefig(uni_path, dpi=150, facecolor=fig.get_facecolor(), edgecolor='none')
        plt.close()
        log(f"Saved Unified Concept PCA plot to {uni_path}")

        uni_csv_path = os.path.join(analysis_dir, "unified_concept_pca_coordinates.csv")
        with open(uni_csv_path, "w", encoding="utf-8") as f:
            f.write("Term,PCA_X,PCA_Y\n")
            for i, name in enumerate(unified_names):
                f.write(f"{name},{uni_2d[i, 0]},{uni_2d[i, 1]}\n")
        log(f"Saved Unified Concept PCA coordinates to {uni_csv_path}")

    print("\nProbe complete! Check the analysis/ folder.")

if __name__ == "__main__":
    model = sys.argv[1] if len(sys.argv) > 1 else "foundation"
    run_probe(model)
