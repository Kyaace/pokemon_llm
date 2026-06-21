# Evaluation Summary V2

This report analyzes the performance of Johnny v2, Spike v2, and Ace v2 against the algebraic constraints and zero-shot reasoning.

## Negative Logic (Evolution)
**Goal:** Tests if the model learned the explicit `<LOGIC_NOT>` constraint for non-evolving Pokémon.

<div style="display: flex; flex-wrap: wrap; gap: 10px;">
<img src="charts_v2/Negative_Logic_Evolution_Johnny_v2.png" width="30%" alt="Johnny_v2" />
<img src="charts_v2/Negative_Logic_Evolution_Spike_v2.png" width="30%" alt="Spike_v2" />
<img src="charts_v2/Negative_Logic_Evolution_Ace_v2.png" width="30%" alt="Ace_v2" />
</div>

---

## Negative Logic (Restrictive Movesets)
**Goal:** Tests if the model understands negative move exclusion.

<div style="display: flex; flex-wrap: wrap; gap: 10px;">
<img src="charts_v2/Negative_Logic_Restrictive_Movesets_Johnny_v2.png" width="30%" alt="Johnny_v2" />
<img src="charts_v2/Negative_Logic_Restrictive_Movesets_Spike_v2.png" width="30%" alt="Spike_v2" />
<img src="charts_v2/Negative_Logic_Restrictive_Movesets_Ace_v2.png" width="30%" alt="Ace_v2" />
</div>

---

## Hatchable Encounters
**Goal:** Tests retention of the new Gen 2 Baby Pokémon token.

<div style="display: flex; flex-wrap: wrap; gap: 10px;">
<img src="charts_v2/Hatchable_Encounters_Johnny_v2.png" width="30%" alt="Johnny_v2" />
<img src="charts_v2/Hatchable_Encounters_Spike_v2.png" width="30%" alt="Spike_v2" />
<img src="charts_v2/Hatchable_Encounters_Ace_v2.png" width="30%" alt="Ace_v2" />
</div>

---

## Abstract Move Algebra (Disable)
**Goal:** Tests if the model understands the `<UNKNOWN_MOVE>` algebraic variable for the Disable edge case.

<div style="display: flex; flex-wrap: wrap; gap: 10px;">
<img src="charts_v2/Abstract_Move_Algebra_Disable_Johnny_v2.png" width="30%" alt="Johnny_v2" />
<img src="charts_v2/Abstract_Move_Algebra_Disable_Spike_v2.png" width="30%" alt="Spike_v2" />
<img src="charts_v2/Abstract_Move_Algebra_Disable_Ace_v2.png" width="30%" alt="Ace_v2" />
</div>

---

## Abstract Move Algebra (Transform)
**Goal:** Tests algebraic variable mapping for shape-shifting moves.

<div style="display: flex; flex-wrap: wrap; gap: 10px;">
<img src="charts_v2/Abstract_Move_Algebra_Transform_Johnny_v2.png" width="30%" alt="Johnny_v2" />
<img src="charts_v2/Abstract_Move_Algebra_Transform_Spike_v2.png" width="30%" alt="Spike_v2" />
<img src="charts_v2/Abstract_Move_Algebra_Transform_Ace_v2.png" width="30%" alt="Ace_v2" />
</div>

---

## Action Prevention (Status Overwrite)
**Goal:** Tests abstract action prevention logic.

<div style="display: flex; flex-wrap: wrap; gap: 10px;">
<img src="charts_v2/Action_Prevention_Status_Overwrite_Johnny_v2.png" width="30%" alt="Johnny_v2" />
<img src="charts_v2/Action_Prevention_Status_Overwrite_Spike_v2.png" width="30%" alt="Spike_v2" />
<img src="charts_v2/Action_Prevention_Status_Overwrite_Ace_v2.png" width="30%" alt="Ace_v2" />
</div>

---

## Zero-Shot Dual-Type Calculation
**Goal:** Tests if the model can dynamically calculate that Ghost has no effect on Normal/Flying.

<div style="display: flex; flex-wrap: wrap; gap: 10px;">
<img src="charts_v2/Zero-Shot_Dual-Type_Calculation_Johnny_v2.png" width="30%" alt="Johnny_v2" />
<img src="charts_v2/Zero-Shot_Dual-Type_Calculation_Spike_v2.png" width="30%" alt="Spike_v2" />
<img src="charts_v2/Zero-Shot_Dual-Type_Calculation_Ace_v2.png" width="30%" alt="Ace_v2" />
</div>

---

## Zero-Shot Steel Matchup
**Goal:** Tests the new Gen 2 Steel typings (Steel vs Electric/Steel).

<div style="display: flex; flex-wrap: wrap; gap: 10px;">
<img src="charts_v2/Zero-Shot_Steel_Matchup_Johnny_v2.png" width="30%" alt="Johnny_v2" />
<img src="charts_v2/Zero-Shot_Steel_Matchup_Spike_v2.png" width="30%" alt="Spike_v2" />
<img src="charts_v2/Zero-Shot_Steel_Matchup_Ace_v2.png" width="30%" alt="Ace_v2" />
</div>

---

## MinMax Status Redundancy (Battle Engine)
**Goal:** Tests if Ace v2 learned the MinMax rule to never use a status move on a Pokémon that is already afflicted.

<div style="display: flex; flex-wrap: wrap; gap: 10px;">
<img src="charts_v2/MinMax_Status_Redundancy_Battle_Engine_Johnny_v2.png" width="30%" alt="Johnny_v2" />
<img src="charts_v2/MinMax_Status_Redundancy_Battle_Engine_Spike_v2.png" width="30%" alt="Spike_v2" />
<img src="charts_v2/MinMax_Status_Redundancy_Battle_Engine_Ace_v2.png" width="30%" alt="Ace_v2" />
</div>

---

## MinMax Base Test
**Goal:** Tests if Ace v2 correctly calculates Charizard fainting and issues Leader Battle Score.

<div style="display: flex; flex-wrap: wrap; gap: 10px;">
<img src="charts_v2/MinMax_Base_Test_Johnny_v2.png" width="30%" alt="Johnny_v2" />
<img src="charts_v2/MinMax_Base_Test_Spike_v2.png" width="30%" alt="Spike_v2" />
<img src="charts_v2/MinMax_Base_Test_Ace_v2.png" width="30%" alt="Ace_v2" />
</div>

---

## Thunderbolt vs Onix
**Goal:** Testing retention of Gen 1 type-effectiveness trivia (Electric vs Ground).

<div style="display: flex; flex-wrap: wrap; gap: 10px;">
<img src="charts_v2/Thunderbolt_vs_Onix_Johnny_v2.png" width="30%" alt="Johnny_v2" />
<img src="charts_v2/Thunderbolt_vs_Onix_Spike_v2.png" width="30%" alt="Spike_v2" />
<img src="charts_v2/Thunderbolt_vs_Onix_Ace_v2.png" width="30%" alt="Ace_v2" />
</div>

---

## Encore Attack
**Goal:** Testing battle simulation using the complex Encore mechanic.

<div style="display: flex; flex-wrap: wrap; gap: 10px;">
<img src="charts_v2/Encore_Attack_Johnny_v2.png" width="30%" alt="Johnny_v2" />
<img src="charts_v2/Encore_Attack_Spike_v2.png" width="30%" alt="Spike_v2" />
<img src="charts_v2/Encore_Attack_Ace_v2.png" width="30%" alt="Ace_v2" />
</div>

---

## Eevee Evolution
**Goal:** Testing retention of branching evolution knowledge.

<div style="display: flex; flex-wrap: wrap; gap: 10px;">
<img src="charts_v2/Eevee_Evolution_Johnny_v2.png" width="30%" alt="Johnny_v2" />
<img src="charts_v2/Eevee_Evolution_Spike_v2.png" width="30%" alt="Spike_v2" />
<img src="charts_v2/Eevee_Evolution_Ace_v2.png" width="30%" alt="Ace_v2" />
</div>

---
