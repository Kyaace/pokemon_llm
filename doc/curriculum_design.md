# Curriculum Design Improvements for v2

This document tracks ideas and strategies for improving the training data (curriculum) for future iterations of the Pokémon LLM models (Spike, Ace, etc.). 

By incrementally fine-tuning the current weights on an upgraded "High Elo" dataset for 3 to 5 epochs (with a lowered learning rate), we can actively shift the models' tactical preferences without destroying their foundational grammar and knowledge.

## Proposed Improvements

### 1. High-Elo / MinMax Battle Generation
*   **Current State:** The `player_leader_corpus` features Gym Leaders making semi-random choices and occasionally wasting turns (e.g., using `Sing` on an already sleeping target).
*   **Improvement:** Rewrite the battle generation script so that the Gym Leaders use a strict, logic-based MinMax algorithm. 
    *   Always pick the highest damage move (accounting for STAB and Type Effectiveness).
    *   Never use a status effect on a Pokémon that already has a status condition (e.g., no Sleep Powder on a sleeping target).
    *   Swap out on severe negative type matchups.
*   **Expected Outcome:** Spike and Ace will stop imitating the "dumb" random behavior and heavily favor MinMax tactical patterns.

### 2. Status Effect Cooldowns / Memory
*   **Current State:** The models sometimes get stuck in loops (e.g., waking up and immediately re-applying sleep to themselves or targets) due to proximity attention.
*   **Improvement:** Ensure the battle generator explicitly demonstrates breaking out of loops by varying actions immediately after a status effect wears off.

## Action Items (Post-Evaluation)
*   Review the output of `evaluate_models.py` to identify any other "dumb" behaviors (e.g., hallucinating non-existent moves, failing to recognize immunities).
*   Add these edge-cases to the High-Elo battle generator script.
*   Generate `player_leader_corpus_v2` and run an incremental fine-tune (3-5 epochs, low learning rate) on the existing Spike/Ace weights.

## v3 Corpus Logic & Expert System (qa_v3_corpus)

For the next iteration of the data pipeline (`qa_v3_corpus`), we should focus on advanced mechanic interactions, breeding, and explicit negative logic constraints using `<LOGIC_NOT>`:

### 1. Explicit Negative Constraints (`<LOGIC_NOT>`)
*   **Non-Evolving Pokémon:** Teach the model explicitly which Pokémon do not evolve by using negative facts (`<FACT> <PKMN> <LOGIC_NOT> <EVOLVES_INTO> ... <EOS>`).
*   **Restrictive Movesets:** Some Pokémon have extremely restrictive movesets (e.g. Caterpie only learning Tackle, String Shot, Bug Bite). We must explicitly teach the model that they *cannot* learn other moves that would otherwise make sense for their type by using `<LOGIC_NOT>` (e.g., they can use Struggle, but NOT advanced STAB moves).

### 2. Breeding & Egg Groups
*   **New Tokens:** Add `<ENC_EGG>` and `<ENC_BREEDABLE>` to the tokenizer's 914+ block for encounter locations.
*   **Egg Group Inference:** Teach the model breeding mechanics by showing it examples of successful breeding combinations.
*   **Fact Structure:** `<FACT> <PKMN_1> <LOGIC_AND> <PKMN_2> <ENC_EGG> <PKMN_CHILD> <EOS>`
*   By exposing the model to enough of these examples, it should be able to infer hidden egg groups.

### 3. Conditional Status Mechanics (Sleep)
*   **New Tokens:** Add explicit tokens for `<EFFECT_SLEEP>`, `<ATTACKER>`, and `<TARGET>` (or leverage existing `<TARGET_ON>` / `<EFFECT_FAST_ASLEEP>` tokens) to teach conditional move states.
*   **Dream Eater / Sleep Talk:** Teach the model that moves like Dream Eater or Sleep Talk strictly require the sleeping condition to function.
*   **Positive Condition Fact:** `<FACT> <TARGET> <EFFECT_FAST_ASLEEP> <LOGIC_AND> <MOVE_DREAM_EATER> <EFFECT_NORMAL> <EOS>`
*   **Negative Condition Fact:** `<FACT> <TARGET> <LOGIC_NOT> <EFFECT_FAST_ASLEEP> <LOGIC_AND> <MOVE_DREAM_EATER> <EFFECT_NONE> <EOS>`
*   Add queries and answers around these conditions to encode them heavily into the next version of the expert system, ensuring the model respects them in battle scenarios.

### 4. Variable Logic / Wildcards (`<UNKNOWN_MOVE>`)
*   **Mechanic:** Teach the model algebraic "fill-in-the-blank" logic using the `<UNKNOWN_MOVE>` token as a variable.
*   **Standard Action Algebra:** Teach the fundamental rules of battle explicitly so Johnny/Ace don't have to infer it purely from battle logs like Spike/Timmy.
    *   **Rule:** If you have a move, you can use it against the target.
    *   `<QUERY> <ATTACKER> <HAS_MOVES> <UNKNOWN_MOVE> <ANSWER> <ATTACKER> <ACTION_USE> <UNKNOWN_MOVE> <TARGET_AGAINST> <TARGET> <EOS>`
*   **Edge Case (Disable):** Teach the model that Disable prevents the target from using their last move, regardless of what that move was.
    *   `<QUERY> <TARGET> <UNKNOWN_MOVE> <LOGIC_AND> <ATTACKER> <MOVE_DISABLE> <ANSWER> <TARGET> <LOGIC_NOT> <UNKNOWN_MOVE> <EOS>`
*   **Edge Case (Sketch / Transform):** Teach the model how move-copying and form-copying mechanics work using the same variable placeholder.
    *   **Sketch:** `<QUERY> <TARGET> <HAS_MOVES> <UNKNOWN_MOVE> <LOGIC_AND> <ATTACKER> <ACTION_USE> <MOVE_SKETCH> <ANSWER> <ATTACKER> <HAS_MOVES> <UNKNOWN_MOVE> <EOS>`
*   By combining this abstract, variable-based encoding with specific examples (e.g., swapping `<UNKNOWN_MOVE>` for `<MOVE_SURF>`), we can test if the model's attention mechanism learns to treat `<UNKNOWN_MOVE>` as a universal algebraic variable for status conditions, standard actions, and move manipulation.

### 5. Branching Rules (`<LOGIC_OR>`)
*   **Multiple Evolution Paths:** Eevee is the perfect candidate for `<LOGIC_OR>` to teach the model that a single entity can branch into multiple valid outputs.
    *   `<FACT> <PKMN_EEVEE> <EVOLVES_INTO> <PKMN_VAPOREON> <LOGIC_OR> <PKMN_JOLTEON> <LOGIC_OR> <PKMN_FLAREON> <EOS>`
*   **Type Effectiveness Grouping:** Instead of having 15 separate facts for why a move is super effective, teach the model algebraic type-grouping. 
    *   `<FACT> <TYPE_BUG> <EFFECT_SUPER> <TARGET_AGAINST> <TYPE_GRASS> <LOGIC_OR> <TYPE_PSYCHIC> <LOGIC_OR> <TYPE_DARK> <EOS>`
*   **Action Prevention:** Teaching the model universal conditions for when an attacker *cannot* attack, substituting "fainted" (which ends our 1v1 matches entirely) with Gen 1's infamous Wrap/Bind lock mechanics.
    *   `<QUERY> <ATTACKER> <EFFECT_FAST_ASLEEP> <LOGIC_OR> <ATTACKER> <EFFECT_HURT_BIND> <ANSWER> <ATTACKER> <LOGIC_NOT> <ACTION_USE> <UNKNOWN_MOVE> <EOS>`
*   **Encounter Locations:** Teaching the model that Pokémon can be obtained through multiple methods.
    *   `<FACT> <PKMN_MAGIKARP> <OBTAINED_FROM> <ENC_FISHING> <LOGIC_OR> <ENC_COMMON_WILD> <EOS>`

## Hardware & Optimization Notes
*   **Batch Size Scaling:** For future v3 training runs, we should significantly scale up the batch size. Current GPU utilization is extremely low (~3% / 0.9GB VRAM). Increasing the batch size will exponentially speed up training times by better saturating the GPU cores.
*   **Dimensionality / Architecture Restraint:** Do *not* increase the model's physical dimensionality (embedding size, attention heads, or layers). The model architecture must remain lightweight so it can be deployed and run on weaker commercial laptops (e.g., intern/student laptops). The goal of this project is to serve as an educational tool for interns and new hires to understand LLM mechanics, so accessibility and inference performance on low-end hardware are paramount.
