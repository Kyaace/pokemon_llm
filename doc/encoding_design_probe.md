# Embedding Vector Analysis Plan

This document outlines the experiments we will run to probe the internal embedding space of the `Foundation` model. By extracting the Word Token Embedding (`wte`) matrix and analyzing it purely on the CPU, we can visualize how the model has structured its understanding of the Pokémon universe without interrupting ongoing GPU training.

## 1. Technical Setup
*   **Target Model:** `models/foundation/final`
*   **Environment:** CPU-only to protect VRAM.
*   **Data Extraction:** Load the 512-dimension vector for every token in the `PokemonTokenizer` vocabulary.

## 2. Planned Experiments

### Experiment A: Pokémon Type Clustering (PCA/t-SNE)
**Goal:** Determine if the model automatically grouped Pokémon by Type due to their usage in battles.
**Method:** 
1. Extract the vectors for all 251 `<PKMN_*>` tokens.
2. Map each Pokémon to its primary type using `pokemon_stats.json`.
3. Run Principal Component Analysis (PCA) or t-SNE to compress the 512 dimensions down to 2 dimensions.
4. Output a scatter plot colored by Type to visually inspect clustering (e.g., do Fire types clump together?). We will use the standard community hex codes to color the nodes:
   * **Bug:** `#A8B820`, **Dark:** `#5C483B`, **Dragon:** `#700AEE`
   * **Electric:** `#F8D030`, **Fairy:** `#EE99AC`, **Fighting:** `#94352D`
   * **Fire:** `#F08030`, **Flying:** `#A890F0`, **Ghost:** `#614C83`
   * **Grass:** `#2DCD45`, **Ground:** `#E0C068`, **Ice:** `#98D8D8`
   * **Normal:** `#A8A878`, **Poison:** `#883688`, **Psychic:** `#FF6996`
   * **Rock:** `#B8A038`, **Steel:** `#B8B8D0`, **Water:** `#149EFF`

### Experiment B: Evolutionary Vector Arithmetic
**Goal:** Determine if the model learned a universal mathematical translation for "Evolution".
**Method:**
1. Calculate the delta vector for evolution: `Delta = Vector(Charmeleon) - Vector(Charmander)`.
2. Apply that Delta to other base Pokémon: `Vector(Squirtle) + Delta`.
3. Check the nearest neighbors to the resulting coordinate to see if `Wartortle` is the closest match.
4. Compare the Cosine Similarities of multiple evolution vectors (e.g., Eevee -> Vaporeon vs Eevee -> Flareon) to locate the "Stone Evolution" concepts.

### Experiment C: Type Advantage Space
**Goal:** See how Moves relate to Targets.
**Method:**
1. Extract vectors for highly effective moves (e.g., `<MOVE_THUNDERBOLT>`) and compare their distance to highly susceptible targets (e.g., `<PKMN_GYARADOS>`).
2. Compare this against ineffective targets (e.g., `<PKMN_ONIX>`) to see if the model pushes immune targets further away in the latent space.

### Experiment D: Meta-Concept Structuring
**Goal:** Understand how the model delineates the context format of the sequence.
**Method:**
1. Extract system tokens: `<BATTLE>`, `<QUERY>`, `<TURN>`, `<ACTION_USE>`, `<HP_REMAINING>`, `<EFFECT_SUPER>`, `<EFFECT_WEAK>`.
2. Measure the distances between them. Does the model group all `<EFFECT_*>` tokens in the same mathematical corner? Does it cleanly separate the `<BATTLE>` token from the `<QUERY>` token?

## 3. Output
The script will generate numerical reports for the vector math and save Matplotlib `.png` images of the 2D cluster maps to the `scratch/` directory for review.
