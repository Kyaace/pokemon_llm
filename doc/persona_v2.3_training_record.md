# Persona v2.3 Training Records

This document tracks the dataset composition, training duration, and final loss metrics for all v2.3 personas in the `pokemon_llm` project. All models are trained for **5 Epochs**.

---

### Foundation v2.3 (The Core Engine)
**Status:** Completed
**Total Dataset Size:** 25,178 lines
*   `qa_gen1_v2_corpus_tokens.txt` (12,928 lines)
*   `tutorial_gen1_corpus_tokens.txt` (10,000 lines)
*   `breeding_corpus_lite_tokens.txt` (2,250 lines)

**Training Time:** ~1.6 hours (3,935 iterations)
**Final Loss:** 0.681

---

### Timmy v2.3 (The Anime Protagonist)
**Status:** Completed
**Total Dataset Size:** 26,800 lines
*   `anime_corpus_tokens.txt` (26,800 lines)

**Training Time:** ~1.7 hours (4,100 iterations)
**Final Loss:** 0.248

---

### Suzie v2.3 (The Daycare Specialist)
**Status:** Completed
**Total Dataset Size:** 53,779 lines
*   `breeding_corpus_full_tokens.txt` (51,529 lines)
*   `breeding_corpus_lite_tokens.txt` (2,250 lines)

**Training Time:** ~39 minutes (1,530 iterations)
**Final Loss:** 0.738

---

### Johnny v2.3 (The Trivia Master)
**Status:** Queued
**Total Dataset Size:** 26,170 lines
*   `qa_gen2_v2_corpus_tokens.txt` (15,870 lines)
*   `tutorial_gen1_corpus_tokens.txt` (10,000 lines)
*   `logic_corpus_tokens.txt` (300 lines)

**Estimated Training Time:** ~18-20 minutes
**Final Loss:** TBD

---

### Spike v2.3 (The Game Battler)
**Status:** Queued
**Total Dataset Size:** 80,227 lines
*   `expert_corpus_v2_tokens.txt` (40,227 lines)
*   `player_leader_gen1_corpus_tokens.txt` (10,000 lines)
*   `player_leader_gen2_corpus_tokens.txt` (10,000 lines)
*   `tutorial_gen1_corpus_tokens.txt` (10,000 lines)
*   `tutorial_gen2_corpus_tokens.txt` (10,000 lines)

**Estimated Training Time:** ~55-60 minutes
**Final Loss:** TBD

---

### Ace v2.3 (The Expert System)
**Status:** Queued
**Total Dataset Size:** 76,397 lines
*   `expert_corpus_v2_tokens.txt` (40,227 lines)
*   `qa_gen2_v2_corpus_tokens.txt` (15,870 lines)
*   `tutorial_gen1_corpus_tokens.txt` (10,000 lines)
*   `tutorial_gen2_corpus_tokens.txt` (10,000 lines)
*   `logic_corpus_tokens.txt` (300 lines)

**Estimated Training Time:** ~50-55 minutes
**Final Loss:** TBD
