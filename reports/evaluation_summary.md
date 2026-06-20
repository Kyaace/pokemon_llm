# Evaluation Summary

This report analyzes the performance of all 5 curriculum models across 18 specialized queries.

## Pikachu Attack
**Goal:** Testing if the models can simulate a Gen 1 Battle with Pikachu.

<div style="display: flex; flex-wrap: wrap; gap: 10px;">
<img src="charts/Pikachu_Attack_Foundation.png" width="18%" alt="Foundation" />
<img src="charts/Pikachu_Attack_Timmy.png" width="18%" alt="Timmy" />
<img src="charts/Pikachu_Attack_Johnny.png" width="18%" alt="Johnny" />
<img src="charts/Pikachu_Attack_Spike.png" width="18%" alt="Spike" />
<img src="charts/Pikachu_Attack_Ace.png" width="18%" alt="Ace" />
</div>

**Findings:** Foundation completely hallucinates. Johnny hallucinates non-battle Q&A text. Spike and Ace correctly generate long-form battle turns.
---

## Onix Attack
**Goal:** Testing if the models can simulate a Gen 1 Battle with Onix.

<div style="display: flex; flex-wrap: wrap; gap: 10px;">
<img src="charts/Onix_Attack_Foundation.png" width="18%" alt="Foundation" />
<img src="charts/Onix_Attack_Timmy.png" width="18%" alt="Timmy" />
<img src="charts/Onix_Attack_Johnny.png" width="18%" alt="Johnny" />
<img src="charts/Onix_Attack_Spike.png" width="18%" alt="Spike" />
<img src="charts/Onix_Attack_Ace.png" width="18%" alt="Ace" />
</div>

**Findings:** Similar to Pikachu, Spike and Ace succeed while Johnny fails.
---

## Thunderbolt vs Onix
**Goal:** Testing retention of Gen 1 type-effectiveness trivia (Electric vs Ground).

<div style="display: flex; flex-wrap: wrap; gap: 10px;">
<img src="charts/Thunderbolt_vs_Onix_Foundation.png" width="18%" alt="Foundation" />
<img src="charts/Thunderbolt_vs_Onix_Timmy.png" width="18%" alt="Timmy" />
<img src="charts/Thunderbolt_vs_Onix_Johnny.png" width="18%" alt="Johnny" />
<img src="charts/Thunderbolt_vs_Onix_Spike.png" width="18%" alt="Spike" />
<img src="charts/Thunderbolt_vs_Onix_Ace.png" width="18%" alt="Ace" />
</div>

**Findings:** Johnny and Ace correctly answer 'It had no effect.' Spike suffers catastrophic forgetting and generates completely random attacks.
---

## Bulbasaur Evolution
**Goal:** Testing retention of Gen 1 evolution knowledge.

<div style="display: flex; flex-wrap: wrap; gap: 10px;">
<img src="charts/Bulbasaur_Evolution_Foundation.png" width="18%" alt="Foundation" />
<img src="charts/Bulbasaur_Evolution_Timmy.png" width="18%" alt="Timmy" />
<img src="charts/Bulbasaur_Evolution_Johnny.png" width="18%" alt="Johnny" />
<img src="charts/Bulbasaur_Evolution_Spike.png" width="18%" alt="Spike" />
<img src="charts/Bulbasaur_Evolution_Ace.png" width="18%" alt="Ace" />
</div>

**Findings:** Johnny and Ace correctly answer 'Ivysaur'. Spike hallucinates.
---

## Squirtle Evolution
**Goal:** Testing retention of Gen 1 evolution knowledge.

<div style="display: flex; flex-wrap: wrap; gap: 10px;">
<img src="charts/Squirtle_Evolution_Foundation.png" width="18%" alt="Foundation" />
<img src="charts/Squirtle_Evolution_Timmy.png" width="18%" alt="Timmy" />
<img src="charts/Squirtle_Evolution_Johnny.png" width="18%" alt="Johnny" />
<img src="charts/Squirtle_Evolution_Spike.png" width="18%" alt="Spike" />
<img src="charts/Squirtle_Evolution_Ace.png" width="18%" alt="Ace" />
</div>

**Findings:** Johnny and Ace correctly answer 'Wartortle'. Spike hallucinates.
---

## Charmander Evolution
**Goal:** Testing retention of Gen 1 evolution knowledge.

<div style="display: flex; flex-wrap: wrap; gap: 10px;">
<img src="charts/Charmander_Evolution_Foundation.png" width="18%" alt="Foundation" />
<img src="charts/Charmander_Evolution_Timmy.png" width="18%" alt="Timmy" />
<img src="charts/Charmander_Evolution_Johnny.png" width="18%" alt="Johnny" />
<img src="charts/Charmander_Evolution_Spike.png" width="18%" alt="Spike" />
<img src="charts/Charmander_Evolution_Ace.png" width="18%" alt="Ace" />
</div>

**Findings:** Johnny and Ace correctly answer 'Charmeleon'. Spike hallucinates.
---

## Pikachu Evolution
**Goal:** Testing retention of Gen 1 evolution knowledge.

<div style="display: flex; flex-wrap: wrap; gap: 10px;">
<img src="charts/Pikachu_Evolution_Foundation.png" width="18%" alt="Foundation" />
<img src="charts/Pikachu_Evolution_Timmy.png" width="18%" alt="Timmy" />
<img src="charts/Pikachu_Evolution_Johnny.png" width="18%" alt="Johnny" />
<img src="charts/Pikachu_Evolution_Spike.png" width="18%" alt="Spike" />
<img src="charts/Pikachu_Evolution_Ace.png" width="18%" alt="Ace" />
</div>

**Findings:** Johnny and Ace correctly answer 'Raichu'. Spike hallucinates.
---

## Eevee Evolution
**Goal:** Testing retention of branching evolution knowledge.

<div style="display: flex; flex-wrap: wrap; gap: 10px;">
<img src="charts/Eevee_Evolution_Foundation.png" width="18%" alt="Foundation" />
<img src="charts/Eevee_Evolution_Timmy.png" width="18%" alt="Timmy" />
<img src="charts/Eevee_Evolution_Johnny.png" width="18%" alt="Johnny" />
<img src="charts/Eevee_Evolution_Spike.png" width="18%" alt="Spike" />
<img src="charts/Eevee_Evolution_Ace.png" width="18%" alt="Ace" />
</div>

**Findings:** Johnny and Ace correctly distribute probabilities across Eevee's 3 Gen 1 and 2 Gen 2 evolutions. Spike fails completely.
---

## Onix Evolution
**Goal:** Testing retention of Gen 2 cross-generation evolution knowledge.

<div style="display: flex; flex-wrap: wrap; gap: 10px;">
<img src="charts/Onix_Evolution_Foundation.png" width="18%" alt="Foundation" />
<img src="charts/Onix_Evolution_Timmy.png" width="18%" alt="Timmy" />
<img src="charts/Onix_Evolution_Johnny.png" width="18%" alt="Johnny" />
<img src="charts/Onix_Evolution_Spike.png" width="18%" alt="Spike" />
<img src="charts/Onix_Evolution_Ace.png" width="18%" alt="Ace" />
</div>

**Findings:** Johnny and Ace correctly answer 'Steelix'. Spike fails.
---

## Pichu Evolution
**Goal:** Testing retention of Gen 2 pre-evolution knowledge.

<div style="display: flex; flex-wrap: wrap; gap: 10px;">
<img src="charts/Pichu_Evolution_Foundation.png" width="18%" alt="Foundation" />
<img src="charts/Pichu_Evolution_Timmy.png" width="18%" alt="Timmy" />
<img src="charts/Pichu_Evolution_Johnny.png" width="18%" alt="Johnny" />
<img src="charts/Pichu_Evolution_Spike.png" width="18%" alt="Spike" />
<img src="charts/Pichu_Evolution_Ace.png" width="18%" alt="Ace" />
</div>

**Findings:** All models fail this, likely because the foundational model did not know Gen 2.
---

## Cyndaquil Evolution
**Goal:** Testing retention of Gen 2 evolution knowledge.

<div style="display: flex; flex-wrap: wrap; gap: 10px;">
<img src="charts/Cyndaquil_Evolution_Foundation.png" width="18%" alt="Foundation" />
<img src="charts/Cyndaquil_Evolution_Timmy.png" width="18%" alt="Timmy" />
<img src="charts/Cyndaquil_Evolution_Johnny.png" width="18%" alt="Johnny" />
<img src="charts/Cyndaquil_Evolution_Spike.png" width="18%" alt="Spike" />
<img src="charts/Cyndaquil_Evolution_Ace.png" width="18%" alt="Ace" />
</div>

**Findings:** Ace succeeds! It correctly predicts Quilava. The others fail or predict EMPTY.
---

## Scyther Attack (Gen 1 Uncommon)
**Goal:** Testing battle simulation with a less common Gen 1 Pokemon.

<div style="display: flex; flex-wrap: wrap; gap: 10px;">
<img src="charts/Scyther_Attack_Gen_1_Uncommon_Foundation.png" width="18%" alt="Foundation" />
<img src="charts/Scyther_Attack_Gen_1_Uncommon_Timmy.png" width="18%" alt="Timmy" />
<img src="charts/Scyther_Attack_Gen_1_Uncommon_Johnny.png" width="18%" alt="Johnny" />
<img src="charts/Scyther_Attack_Gen_1_Uncommon_Spike.png" width="18%" alt="Spike" />
<img src="charts/Scyther_Attack_Gen_1_Uncommon_Ace.png" width="18%" alt="Ace" />
</div>

**Findings:** Spike and Ace generate plausible battle syntax.
---

## Aerodactyl Attack (Gen 1 Rare)
**Goal:** Testing battle simulation with a rare Gen 1 Pokemon.

<div style="display: flex; flex-wrap: wrap; gap: 10px;">
<img src="charts/Aerodactyl_Attack_Gen_1_Rare_Foundation.png" width="18%" alt="Foundation" />
<img src="charts/Aerodactyl_Attack_Gen_1_Rare_Timmy.png" width="18%" alt="Timmy" />
<img src="charts/Aerodactyl_Attack_Gen_1_Rare_Johnny.png" width="18%" alt="Johnny" />
<img src="charts/Aerodactyl_Attack_Gen_1_Rare_Spike.png" width="18%" alt="Spike" />
<img src="charts/Aerodactyl_Attack_Gen_1_Rare_Ace.png" width="18%" alt="Ace" />
</div>

**Findings:** Spike and Ace generate plausible battle syntax.
---

## Heracross Attack (Gen 2 Uncommon)
**Goal:** Testing battle simulation with a Gen 2 Pokemon.

<div style="display: flex; flex-wrap: wrap; gap: 10px;">
<img src="charts/Heracross_Attack_Gen_2_Uncommon_Foundation.png" width="18%" alt="Foundation" />
<img src="charts/Heracross_Attack_Gen_2_Uncommon_Timmy.png" width="18%" alt="Timmy" />
<img src="charts/Heracross_Attack_Gen_2_Uncommon_Johnny.png" width="18%" alt="Johnny" />
<img src="charts/Heracross_Attack_Gen_2_Uncommon_Spike.png" width="18%" alt="Spike" />
<img src="charts/Heracross_Attack_Gen_2_Uncommon_Ace.png" width="18%" alt="Ace" />
</div>

**Findings:** Spike and Ace generate plausible battle syntax.
---

## Tyranitar Attack (Gen 2 Rare)
**Goal:** Testing battle simulation with a rare Gen 2 Pokemon.

<div style="display: flex; flex-wrap: wrap; gap: 10px;">
<img src="charts/Tyranitar_Attack_Gen_2_Rare_Foundation.png" width="18%" alt="Foundation" />
<img src="charts/Tyranitar_Attack_Gen_2_Rare_Timmy.png" width="18%" alt="Timmy" />
<img src="charts/Tyranitar_Attack_Gen_2_Rare_Johnny.png" width="18%" alt="Johnny" />
<img src="charts/Tyranitar_Attack_Gen_2_Rare_Spike.png" width="18%" alt="Spike" />
<img src="charts/Tyranitar_Attack_Gen_2_Rare_Ace.png" width="18%" alt="Ace" />
</div>

**Findings:** Spike and Ace generate plausible battle syntax.
---

## Encore Attack
**Goal:** Testing battle simulation using the complex Encore mechanic.

<div style="display: flex; flex-wrap: wrap; gap: 10px;">
<img src="charts/Encore_Attack_Foundation.png" width="18%" alt="Foundation" />
<img src="charts/Encore_Attack_Timmy.png" width="18%" alt="Timmy" />
<img src="charts/Encore_Attack_Johnny.png" width="18%" alt="Johnny" />
<img src="charts/Encore_Attack_Spike.png" width="18%" alt="Spike" />
<img src="charts/Encore_Attack_Ace.png" width="18%" alt="Ace" />
</div>

**Findings:** Spike and Ace track the Encore condition.
---

## Disable Attack
**Goal:** Testing battle simulation using the complex Disable mechanic.

<div style="display: flex; flex-wrap: wrap; gap: 10px;">
<img src="charts/Disable_Attack_Foundation.png" width="18%" alt="Foundation" />
<img src="charts/Disable_Attack_Timmy.png" width="18%" alt="Timmy" />
<img src="charts/Disable_Attack_Johnny.png" width="18%" alt="Johnny" />
<img src="charts/Disable_Attack_Spike.png" width="18%" alt="Spike" />
<img src="charts/Disable_Attack_Ace.png" width="18%" alt="Ace" />
</div>

**Findings:** Spike and Ace track the Disable condition.
---

## Metronome Attack
**Goal:** Testing battle simulation branching randomness with Metronome.

<div style="display: flex; flex-wrap: wrap; gap: 10px;">
<img src="charts/Metronome_Attack_Foundation.png" width="18%" alt="Foundation" />
<img src="charts/Metronome_Attack_Timmy.png" width="18%" alt="Timmy" />
<img src="charts/Metronome_Attack_Johnny.png" width="18%" alt="Johnny" />
<img src="charts/Metronome_Attack_Spike.png" width="18%" alt="Spike" />
<img src="charts/Metronome_Attack_Ace.png" width="18%" alt="Ace" />
</div>

**Findings:** Ace perfectly executes random branching moves.
---
