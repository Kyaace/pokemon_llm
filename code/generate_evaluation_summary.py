import os
import re
import matplotlib.pyplot as plt

queries = [
    {
        "name": "Pikachu Attack",
        "title": "--- QUERY: Pikachu Attack ---",
        "goal": "Testing if the models can simulate a Gen 1 Battle with Pikachu.",
        "findings": "Foundation completely hallucinates. Timmy hallucinates Anime logic. Johnny hallucinates non-battle Q&A text. Spike and Ace correctly generate long-form battle turns.",
        "type": "BATTLE"
    },
    {
        "name": "Onix Attack",
        "title": "--- QUERY: Onix Attack ---",
        "goal": "Testing if the models can simulate a Gen 1 Battle with Onix.",
        "findings": "Similar to Pikachu, Spike and Ace succeed while Johnny fails. Timmy struggles with game logic, preferring Anime logic.",
        "type": "BATTLE"
    },
    {
        "name": "Thunderbolt vs Onix",
        "title": "--- QUERY: Thunderbolt vs Onix ---",
        "goal": "Testing retention of Gen 1 type-effectiveness trivia (Electric vs Ground).",
        "findings": "Johnny and Ace correctly answer 'It had no effect.' Timmy fails because it follows Anime logic (where Pikachu defeated Onix). Spike suffers catastrophic forgetting and generates completely random attacks.",
        "type": "QA",
        "correct": ["It had no effect."]
    },
    {
        "name": "Bulbasaur Evolution",
        "title": "--- QUERY: Bulbasaur Evolution ---",
        "goal": "Testing retention of Gen 1 evolution knowledge.",
        "findings": "Johnny and Ace correctly answer 'Ivysaur'. Timmy follows Anime logic and struggles with strict game evolutions. Spike hallucinates.",
        "type": "QA",
        "correct": ["Ivysaur"]
    },
    {
        "name": "Squirtle Evolution",
        "title": "--- QUERY: Squirtle Evolution ---",
        "goal": "Testing retention of Gen 1 evolution knowledge.",
        "findings": "Johnny and Ace correctly answer 'Wartortle'. Timmy is wrong because of Anime logic. Spike hallucinates.",
        "type": "QA",
        "correct": ["Wartortle"]
    },
    {
        "name": "Charmander Evolution",
        "title": "--- QUERY: Charmander Evolution ---",
        "goal": "Testing retention of Gen 1 evolution knowledge.",
        "findings": "Johnny and Ace correctly answer 'Charmeleon'. Spike hallucinates.",
        "type": "QA",
        "correct": ["Charmeleon"]
    },
    {
        "name": "Pikachu Evolution",
        "title": "--- QUERY: Pikachu Evolution ---",
        "goal": "Testing retention of Gen 1 evolution knowledge.",
        "findings": "Johnny and Ace correctly answer 'Raichu'. Timmy refuses because of Anime logic (Ash's Pikachu didn't evolve). Spike hallucinates.",
        "type": "QA",
        "correct": ["Raichu"]
    },
    {
        "name": "Eevee Evolution",
        "title": "--- QUERY: Eevee Evolution ---",
        "goal": "Testing retention of branching evolution knowledge.",
        "findings": "Johnny and Ace correctly distribute probabilities across Eevee's 3 Gen 1 and 2 Gen 2 evolutions. Spike fails completely.",
        "type": "EEVEE",
        "correct": []
    },
    {
        "name": "Onix Evolution",
        "title": "--- QUERY: Onix Evolution ---",
        "goal": "Testing retention of Gen 2 cross-generation evolution knowledge.",
        "findings": "Johnny and Ace correctly answer 'Steelix'. Spike fails.",
        "type": "QA",
        "correct": ["Steelix"]
    },
    {
        "name": "Pichu Evolution",
        "title": "--- QUERY: Pichu Evolution ---",
        "goal": "Testing retention of Gen 2 pre-evolution knowledge.",
        "findings": "All models fail this, likely because the foundational model did not know Gen 2.",
        "type": "QA",
        "correct": ["Pikachu"]
    },
    {
        "name": "Cyndaquil Evolution",
        "title": "--- QUERY: Cyndaquil Evolution ---",
        "goal": "Testing retention of Gen 2 evolution knowledge.",
        "findings": "Ace succeeds! It correctly predicts Quilava. The others fail or predict EMPTY.",
        "type": "QA",
        "correct": ["Quilava"]
    },
    {
        "name": "Scyther Attack (Gen 1 Uncommon)",
        "title": "--- QUERY: Scyther Attack (Gen 1 Uncommon) ---",
        "goal": "Testing battle simulation with a less common Gen 1 Pokemon.",
        "findings": "Spike and Ace generate plausible battle syntax.",
        "type": "BATTLE"
    },
    {
        "name": "Aerodactyl Attack (Gen 1 Rare)",
        "title": "--- QUERY: Aerodactyl Attack (Gen 1 Rare) ---",
        "goal": "Testing battle simulation with a rare Gen 1 Pokemon.",
        "findings": "Spike and Ace generate plausible battle syntax.",
        "type": "BATTLE"
    },
    {
        "name": "Heracross Attack (Gen 2 Uncommon)",
        "title": "--- QUERY: Heracross Attack (Gen 2 Uncommon) ---",
        "goal": "Testing battle simulation with a Gen 2 Pokemon.",
        "findings": "Spike and Ace generate plausible battle syntax.",
        "type": "BATTLE"
    },
    {
        "name": "Tyranitar Attack (Gen 2 Rare)",
        "title": "--- QUERY: Tyranitar Attack (Gen 2 Rare) ---",
        "goal": "Testing battle simulation with a rare Gen 2 Pokemon.",
        "findings": "Spike and Ace generate plausible battle syntax.",
        "type": "BATTLE"
    },
    {
        "name": "Encore Attack",
        "title": "--- QUERY: Encore Attack ---",
        "goal": "Testing battle simulation using the complex Encore mechanic.",
        "findings": "Spike and Ace track the Encore condition.",
        "type": "BATTLE"
    },
    {
        "name": "Disable Attack",
        "title": "--- QUERY: Disable Attack ---",
        "goal": "Testing battle simulation using the complex Disable mechanic.",
        "findings": "Spike and Ace track the Disable condition.",
        "type": "BATTLE"
    },
    {
        "name": "Metronome Attack",
        "title": "--- QUERY: Metronome Attack ---",
        "goal": "Testing battle simulation branching randomness with Metronome.",
        "findings": "Ace perfectly executes random branching moves.",
        "type": "BATTLE"
    }
]

def grade_battle(text):
    text = text.lower()
    if "<empty" in text:
        return "Bad"
    # Basic battle syntax
    if "turn" in text and "used" in text and "hp remaining" in text:
        return "Good"
    if "used" in text and ("effective" in text or "effect" in text):
        return "Good"
    if "used" in text:
        return "Fair"
    return "Bad"

def grade_general(q_type, ans, correct_list):
    if q_type == "BATTLE":
        grade = grade_battle(ans)
        if grade == "Good": return 2
        elif grade == "Fair": return 1
        else: return 0
    elif q_type == "EEVEE":
        ans_lower = ans.lower()
        if any(x in ans_lower for x in ["vaporeon", "jolteon", "flareon", "espeon", "umbreon", "eevee"]):
            return 2
        return 0
    else: # QA
        ans_lower = ans.lower()
        is_correct = any(c.lower() in ans_lower for c in correct_list)
        return 2 if is_correct else 0

def parse_report(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    results = {}
    current_query = None
    current_model = None
    
    for line in lines:
        line = line.strip()
        if line.startswith("--- QUERY:"):
            current_query = line
            results[current_query] = {}
        elif line.endswith(":") and current_query:
            current_model = line[:-1]
            results[current_query][current_model] = []
        elif "->" in line and current_query and current_model:
            parts = line.split("->")
            pct = float(parts[0].replace("%", "").strip())
            ans = parts[1].strip()
            results[current_query][current_model].append((pct, ans))
            
    return results

def get_color(q_type, ans, correct_list, color_index):
    if q_type == "BATTLE":
        grade = grade_battle(ans)
        if grade == "Good":
            colors = ["#2ecc71", "#27ae60", "#229954", "#1e8449"]
            return colors[color_index % len(colors)]
        elif grade == "Fair":
            colors = ["#f1c40f", "#f39c12", "#d4ac0d", "#b7950b"]
            return colors[color_index % len(colors)]
        else:
            colors = ["#e74c3c", "#c0392b", "#a93226", "#922b21"]
            return colors[color_index % len(colors)]
            
    elif q_type == "EEVEE":
        ans_lower = ans.lower()
        if "vaporeon" in ans_lower: return "#6390F0"
        elif "jolteon" in ans_lower: return "#F7D02C"
        elif "flareon" in ans_lower: return "#EE8130"
        elif "espeon" in ans_lower: return "#F95587"
        elif "umbreon" in ans_lower: return "#705848"
        elif "eevee" in ans_lower: return "#A8A77A"
        else: return "#E2BF65" # Ground color for other incorrect
        
    else: # QA
        ans_lower = ans.lower()
        is_correct = any(c.lower() in ans_lower for c in correct_list)
        if is_correct:
            colors = ["#2ecc71", "#27ae60", "#229954", "#1e8449"]
            return colors[color_index % len(colors)]
        else:
            colors = ["#e74c3c", "#c0392b", "#a93226", "#922b21"]
            return colors[color_index % len(colors)]

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    report_path = os.path.join(base_dir, "reports", "evaluation_report.txt")
    charts_dir = os.path.join(base_dir, "reports", "charts")
    
    parsed = parse_report(report_path)
    
    models = ["Foundation", "Timmy", "Johnny", "Spike", "Ace"]
    
    md_lines = ["# Evaluation Summary\n\nThis report analyzes the performance of all 5 curriculum models across 18 specialized queries.\n"]
    
    def my_autopct(pct):
        return ('%1.0f%%' % pct) if pct >= 4 else ''
        
    for q in queries:
        title = q["title"]
        name = q["name"]
        md_lines.append(f"## {name}")
        md_lines.append(f"**Goal:** {q['goal']}")
        md_lines.append("")
        
        md_lines.append('<div style="display: flex; flex-wrap: wrap; gap: 10px;">')
        
        if title in parsed:
            for m in models:
                if m in parsed[title]:
                    answers = parsed[title][m]
                    if not answers:
                        continue
                        
                    # Sort answers: Correct/Good first, then by percentage
                    # grade_general returns 2 (Good), 1 (Fair), 0 (Bad)
                    graded_answers = [(grade_general(q["type"], ans, q.get("correct", [])), pct, ans) for pct, ans in answers]
                    graded_answers.sort(key=lambda x: (x[0], x[1]), reverse=True)
                    
                    sizes = []
                    colors = []
                    chart_labels = []
                    
                    good_idx = 0
                    fair_idx = 0
                    bad_idx = 0
                    
                    for grade, pct, ans in graded_answers:
                        sizes.append(pct)
                        
                        if q["type"] == "BATTLE":
                            if grade == 2:
                                colors.append(get_color(q["type"], ans, q.get("correct", []), good_idx))
                                good_idx += 1
                            elif grade == 1:
                                colors.append(get_color(q["type"], ans, q.get("correct", []), fair_idx))
                                fair_idx += 1
                            else:
                                colors.append(get_color(q["type"], ans, q.get("correct", []), bad_idx))
                                bad_idx += 1
                        else:
                            is_correct = any(c.lower() in ans.lower() for c in q.get("correct", []))
                            if is_correct or q["type"] == "EEVEE":
                                colors.append(get_color(q["type"], ans, q.get("correct", []), good_idx))
                                good_idx += 1
                            else:
                                colors.append(get_color(q["type"], ans, q.get("correct", []), bad_idx))
                                bad_idx += 1
                                
                        # Handle Labels for Eevee (Only if pct >= 4%)
                        if q["type"] == "EEVEE" and pct >= 4:
                            # Extract pokemon name based on keywords
                            ans_lower = ans.lower()
                            if "vaporeon" in ans_lower: chart_labels.append("Vaporeon")
                            elif "jolteon" in ans_lower: chart_labels.append("Jolteon")
                            elif "flareon" in ans_lower: chart_labels.append("Flareon")
                            elif "espeon" in ans_lower: chart_labels.append("Espeon")
                            elif "umbreon" in ans_lower: chart_labels.append("Umbreon")
                            elif "eevee" in ans_lower: chart_labels.append("Eevee")
                            else: chart_labels.append("Other")
                        else:
                            chart_labels.append("")
                    
                    fig, ax = plt.subplots(figsize=(4, 4))
                    
                    # If we have labels, use them, otherwise use None so they don't take up space
                    has_labels = any(l != "" for l in chart_labels)
                    
                    wedges, texts, autotexts = ax.pie(
                        sizes, 
                        labels=chart_labels if has_labels else None, 
                        colors=colors, 
                        autopct=my_autopct, 
                        startangle=90
                    )
                    
                    ax.axis('equal')
                    plt.title(m)
                    
                    chart_filename = f"{name.replace(' ', '_').replace('(', '').replace(')', '')}_{m}.png"
                    chart_path = os.path.join(charts_dir, chart_filename)
                    plt.tight_layout()
                    plt.savefig(chart_path)
                    plt.close(fig)
                    
                    md_lines.append(f'<img src="charts/{chart_filename}" width="18%" alt="{m}" />')
                    
        md_lines.append('</div>')
        md_lines.append("")
        md_lines.append(f"**Findings:** {q['findings']}")
        md_lines.append("---\n")
        
    with open(os.path.join(base_dir, "reports", "evaluation_summary.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(md_lines))
        
    print("Successfully generated updated pie charts and evaluation_summary.md!")

if __name__ == "__main__":
    main()
