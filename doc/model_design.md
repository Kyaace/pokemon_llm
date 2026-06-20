# Pokemon LLM: Model Design Comparison

This document outlines the architectural differences between the original "Tiny Timmy" prototype model and the new "Foundation Model" designed to handle the massive multi-generation battle corpus.

## High-Level Architecture
Both models are decoder-only Transformer language models (GPT-2 architecture) designed for auto-regressive next-token prediction. However, the Foundation Model has been scaled up across all dimensions to expand its capacity for internalizing complex Pokémon grammar, math, and type-effectiveness logic.

| Specification | Tiny Timmy | Foundation Model |
| :--- | :--- | :--- |
| **Context Window** | 128 tokens | 512 tokens |
| **Embedding Dimension ($d_{model}$)** | 128 | 256 |
| **Transformer Layers ($n_{layer}$)** | 4 | 8 |
| **Attention Heads ($n_{head}$)** | 4 | 8 |

---

## Architectural Breakdown

### 1. Context Window ($n_{positions}$)
- **Tiny Timmy (128):** Could only "remember" roughly 2-3 turns of a battle before running out of context space. This prevented him from understanding long-term consequences of moves like `Sleep Powder` or tracking HP accurately across 10-20 turns.
- **Foundation Model (512):** A 4x increase in context length. This allows the model to process up to 20-30 consecutive turns of a battle simultaneously. It can natively read back through the history of a full battle, allowing it to correctly apply status effect logic (e.g., waking up from sleep) and correctly subtract HP across long encounters.

### 2. Transformer Layers ($n_{layer}$)
- **Tiny Timmy (4 layers):** A very shallow network. Capable of memorizing grammar patterns (e.g., `"Turn X. [Name] used [Move]..."`) but struggled with hierarchical abstraction.
- **Foundation Model (8 layers):** Doubling the depth allows the model to build much deeper hierarchical representations. Lower layers can focus on grammar and syntax, middle layers on entity tracking (who has what HP), and higher layers on abstract mathematical concepts like computing the exact numerical HP subtractions based on the Type Effectiveness chart multipliers.

### 3. Embedding Dimension ($d_{model}$)
- **Tiny Timmy (128):** Each token in the vocabulary was represented by an array of 128 floating-point numbers.
- **Foundation Model (256):** Each token is represented by a 256-dimensional vector. This provides double the "expressive bandwidth" for the model to encode rich semantic meaning into each word, which is necessary now that our vocabulary includes complex edge-case mechanics, Gen 2 types (Dark/Steel), and over 251 different Pokémon.

### 4. Attention Heads ($n_{head}$) & Q, K, V Vectors
In Multi-Head Attention, the $d_{model}$ is split equally among the heads. Each head gets its own Query (Q), Key (K), and Value (V) projection matrices.
The dimension of these vectors per head is calculated as: $d_{head} = \frac{d_{model}}{n_{head}}$

- **Tiny Timmy:**
  - $d_{model} = 128$, $n_{head} = 4$
  - **Q, K, V size:** $128 / 4 = 32$ dimensions per head.
  - With only 4 heads, Timmy could only pay attention to 4 separate context streams per layer.

- **Foundation Model:**
  - $d_{model} = 256$, $n_{head} = 8$
  - **Q, K, V size:** $256 / 8 = 32$ dimensions per head.
  - **Insight:** The mathematical size of the Q, K, V vectors actually *remains the same* (32 dimensions) between Timmy and the Foundation Model! However, the Foundation Model has **8 separate attention heads** instead of 4. This means it can attend to twice as many unique contextual features (e.g., Attacker HP, Defender HP, Attacker Type, Move Type, Status Condition, Turn Number) simultaneously within the exact same layer!

### 5. Training Datasets
To prevent cross-contamination of knowledge, the data pipeline generates several compartmentalized corpuses. 

- **Tiny Timmy (Prototype):** Was trained on a single dataset of 20,000 basic Gen 1 tutorial battles.
- **Foundation Model:** Pre-trained exclusively on `tutorial_gen1_corpus_tokens.txt` and `qa_gen1_corpus_tokens.txt` (~50,000 battles/facts total) to learn the core engine mechanics, grammar, and base type-effectiveness math.
- **Timmy:** Fine-tuned from the Foundation Model on the `anime_corpus`. This gives him his signature "plot armor" knowledge, allowing him to mimic Ash's battle style (e.g., aiming for the horn, electric moves hitting ground types).
- **Johnny:** Fine-tuned from the Foundation Model on the `tutorial_gen2_corpus` and `qa_gen2_corpus`. He is the only agent exposed to Gen 2 mechanics, Dark/Steel/Fairy types, and new Gen 2 evolutions.
- **Spike:** Fine-tuned from the Foundation Model on the `player_leader_gen1_corpus`. This exposes him to realistic Player vs Gym Leader team matchups and curated movepools, though the actual move execution remains randomized.
- **Ace:** The "master" agent. Fine-tuned from the Foundation Model on the combined datasets of both Spike (`player_leader_gen1_corpus`) and Johnny (`tutorial_gen2_corpus`, `qa_gen2_corpus`). This creates an ultimate persona designed to test if an LLM can discern the difference between raw theory (Johnny) and practical application (Spike) across multiple generations simultaneously.

---

## Conclusion
By doubling the width, depth, and attention capacity, and quadrupling the context window, the Foundation Model boasts an exponentially higher parameter count than the original prototype. This increased capacity allows the base architecture to effectively absorb the core battle mechanics, ensuring that the downstream fine-tuned personas (Timmy, Johnny, Spike, Ace) have a robust logical foundation to build their specialized knowledge upon.
