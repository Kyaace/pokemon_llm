import os
import re
import matplotlib.pyplot as plt

queries = [
    {
        "name": "Negative Logic (Evolution)",
        "title": "--- QUERY: Negative Logic (Evolution) ---",
        "goal": "Tests if the model learned the explicit `<LOGIC_NOT>` constraint for non-evolving Pokémon.",
        "findings": "",
        "type": "QA_EXACT",
        "correct": ["logic_not"]
    },
    {
        "name": "Negative Logic (Restrictive Movesets)",
        "title": "--- QUERY: Negative Logic (Restrictive Movesets) ---",
        "goal": "Tests if the model understands negative move exclusion.",
        "findings": "",
        "type": "QA_EXACT",
        "correct": ["logic_not has moves"]
    },
    {
        "name": "Hatchable Encounters",
        "title": "--- QUERY: Hatchable Encounters ---",
        "goal": "Tests retention of the new Gen 2 Baby Pokémon token.",
        "findings": "",
        "type": "QA_EXACT",
        "correct": ["hatchable"]
    },
    {
        "name": "Abstract Move Algebra (Disable)",
        "title": "--- QUERY: Abstract Move Algebra (Disable) ---",
        "goal": "Tests if the model understands the `<UNKNOWN_MOVE>` algebraic variable for the Disable edge case.",
        "findings": "",
        "type": "QA_EXACT",
        "correct": ["target logic_not unknown move"]
    },
    {
        "name": "Abstract Move Algebra (Transform)",
        "title": "--- QUERY: Abstract Move Algebra (Transform) ---",
        "goal": "Tests algebraic variable mapping for shape-shifting moves.",
        "findings": "",
        "type": "QA_EXACT",
        "correct": ["attacker has moves unknown move"]
    },
    {
        "name": "Action Prevention (Status Overwrite)",
        "title": "--- QUERY: Action Prevention (Status Overwrite) ---",
        "goal": "Tests abstract action prevention logic.",
        "findings": "",
        "type": "QA_EXACT",
        "correct": ["attacker logic_not used unknown move"]
    },
    {
        "name": "Zero-Shot Dual-Type Calculation",
        "title": "--- QUERY: Zero-Shot Dual-Type Calculation ---",
        "goal": "Tests if the model can dynamically calculate that Ghost has no effect on Normal/Flying.",
        "findings": "",
        "type": "QA_EXACT",
        "correct": ["it had no effect"]
    },
    {
        "name": "Zero-Shot Steel Matchup",
        "title": "--- QUERY: Zero-Shot Steel Matchup ---",
        "goal": "Tests the new Gen 2 Steel typings (Steel vs Electric/Steel).",
        "findings": "",
        "type": "QA_EXACT",
        "correct": ["it was not very effective"]
    },
    {
        "name": "MinMax Status Redundancy (Battle Engine)",
        "title": "--- QUERY: MinMax Status Redundancy (Battle Engine) ---",
        "goal": "Tests if Ace v2 learned the MinMax rule to never use a status move on a Pokémon that is already afflicted.",
        "findings": "",
        "type": "MINMAX_STATUS"
    },
    {
        "name": "MinMax Damage Priority (Battle Engine)",
        "title": "--- QUERY: MinMax Damage Priority (Battle Engine) ---",
        "goal": "Tests if Ace v2 prioritizes high-damage STAB moves over weak alternatives on Turn 1.",
        "findings": "",
        "type": "MINMAX_DAMAGE"
    },
    {
        "name": "Thunderbolt vs Onix",
        "title": "--- QUERY: Thunderbolt vs Onix ---",
        "goal": "Testing retention of Gen 1 type-effectiveness trivia (Electric vs Ground).",
        "findings": "",
        "type": "QA_THUNDERBOLT",
        "correct": ["it had no effect"]
    },
    {
        "name": "Encore Attack",
        "title": "--- QUERY: Encore Attack ---",
        "goal": "Testing battle simulation using the complex Encore mechanic.",
        "findings": "",
        "type": "ENCORE"
    },
    {
        "name": "Eevee Evolution",
        "title": "--- QUERY: Eevee Evolution ---",
        "goal": "Testing retention of branching evolution knowledge.",
        "findings": "",
        "type": "EEVEE",
        "correct": []
    }
]

def grade_battle(text):
    text = text.lower()
    if "<empty" in text:
        return "Bad"
    if "turn" in text and "used" in text and "hp remaining" in text:
        return "Good"
    if "used" in text and ("effective" in text or "effect" in text):
        return "Good"
    if "used" in text:
        return "Fair"
    return "Bad"

def grade_encore(text):
    text = text.lower()
    attacks = re.findall(r"used ([\w\s]+) against", text)
    if len(attacks) >= 2 and attacks[0] == attacks[1]:
        return "Good"
    elif len(attacks) >= 2:
        return "Bad" 
    return grade_battle(text) 

def grade_minmax_status(text):
    text = text.lower()
    if any(m in text for m in ["sing", "hypnosis", "sleep powder", "spore", "stun spore", "thunder wave"]):
        return "Bad" 
    if "used" in text and "effective" in text:
        return "Good" 
    return "Fair"

def grade_minmax_damage(text):
    text = text.lower()
    good_moves = ["solar beam", "razor leaf", "vine whip"]
    if any(m in text for m in good_moves):
        return "Good"
    if "used" in text:
        return "Bad" 
    return "Bad"

def grade_general(q_type, ans, correct_list):
    ans_lower = ans.lower()
    if q_type == "BATTLE":
        grade = grade_battle(ans)
        if grade == "Good": return 2
        elif grade == "Fair": return 1
        else: return 0
    elif q_type == "QA_EXACT":
        is_correct = any(c.lower() in ans_lower for c in correct_list)
        return 2 if is_correct else 0
    elif q_type == "ENCORE":
        grade = grade_encore(ans)
        if grade == "Good": return 2
        elif grade == "Fair": return 1
        else: return 0
    elif q_type == "EEVEE":
        if any(x in ans_lower for x in ["vaporeon", "jolteon", "flareon", "espeon", "umbreon", "eevee"]):
            return 2
        return 0
    elif q_type == "QA_THUNDERBOLT":
        has_correct = any(c.lower() in ans_lower for c in correct_list)
        has_battle = "turn" in ans_lower and "used" in ans_lower
        if has_correct and has_battle: return 1
        elif has_correct: return 2
        else: return 0
    elif q_type == "MINMAX_STATUS":
        grade = grade_minmax_status(ans)
        if grade == "Good": return 2
        elif grade == "Fair": return 1
        else: return 0
    elif q_type == "MINMAX_DAMAGE":
        grade = grade_minmax_damage(ans)
        if grade == "Good": return 2
        elif grade == "Fair": return 1
        else: return 0
    return 0

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

def get_color(grade, color_index):
    if grade == 2:
        colors = ["#2ecc71", "#27ae60", "#229954", "#1e8449", "#196f3d", "#145a32"]
        return colors[color_index % len(colors)]
    elif grade == 1:
        colors = ["#f1c40f", "#f39c12", "#d4ac0d", "#b7950b", "#9a7d0a", "#7d6608"]
        return colors[color_index % len(colors)]
    else:
        colors = ["#e74c3c", "#c0392b", "#a93226", "#922b21", "#7b241c", "#641e16"]
        return colors[color_index % len(colors)]

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    report_path = os.path.join(base_dir, "reports", "evaluation_report_v2.txt")
    charts_dir = os.path.join(base_dir, "reports", "charts_v2")
    
    if not os.path.exists(charts_dir):
        os.makedirs(charts_dir)
        
    parsed = parse_report(report_path)
    
    models = ["Johnny_v2", "Spike_v2", "Ace_v2"]
    
    md_lines = ["# Evaluation Summary V2\n\nThis report analyzes the performance of Johnny v2, Spike v2, and Ace v2 against the algebraic constraints and zero-shot reasoning.\n"]
    
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
                    if not answers: continue
                        
                    graded_answers = []
                    for pct, ans in answers:
                        grade = grade_general(q["type"], ans, q.get("correct", []))
                        graded_answers.append((grade, pct, ans))
                        
                    graded_answers.sort(key=lambda x: (x[0], x[1]), reverse=True)
                    
                    sizes = []
                    colors = []
                    chart_labels = []
                    
                    good_idx = 0
                    fair_idx = 0
                    bad_idx = 0
                    
                    for grade, pct, ans in graded_answers:
                        sizes.append(pct)
                        
                        if q["type"] == "EEVEE":
                            ans_lower = ans.lower()
                            if "vaporeon" in ans_lower: colors.append("#6390F0")
                            elif "jolteon" in ans_lower: colors.append("#F7D02C")
                            elif "flareon" in ans_lower: colors.append("#EE8130")
                            elif "espeon" in ans_lower: colors.append("#F95587")
                            elif "umbreon" in ans_lower: colors.append("#705848")
                            elif "eevee" in ans_lower: colors.append("#A8A77A")
                            else: colors.append("#E2BF65")
                        else:
                            if grade == 2:
                                colors.append(get_color(grade, good_idx))
                                good_idx += 1
                            elif grade == 1:
                                colors.append(get_color(grade, fair_idx))
                                fair_idx += 1
                            else:
                                colors.append(get_color(grade, bad_idx))
                                bad_idx += 1
                                
                        if pct >= 4:
                            if q["type"] == "EEVEE":
                                ans_lower = ans.lower()
                                if "vaporeon" in ans_lower: chart_labels.append("Vaporeon")
                                elif "jolteon" in ans_lower: chart_labels.append("Jolteon")
                                elif "flareon" in ans_lower: chart_labels.append("Flareon")
                                elif "espeon" in ans_lower: chart_labels.append("Espeon")
                                elif "umbreon" in ans_lower: chart_labels.append("Umbreon")
                                elif "eevee" in ans_lower: chart_labels.append("Eevee")
                                else: chart_labels.append("Other")
                            else: chart_labels.append("")
                        else:
                            chart_labels.append("")
                            
                    fig, ax = plt.subplots(figsize=(4, 4))
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
                    
                    md_lines.append(f'<img src="charts_v2/{chart_filename}" width="30%" alt="{m}" />')
                    
        md_lines.append('</div>')
        md_lines.append("")
        if q['findings']:
            md_lines.append(f"**Findings:** {q['findings']}")
        md_lines.append("---\n")
        
    with open(os.path.join(base_dir, "reports", "evaluation_summary_v2.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(md_lines))
        
    print("Successfully generated updated pie charts and evaluation_summary_v2.md!")

if __name__ == "__main__":
    main()
