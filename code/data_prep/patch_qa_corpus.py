import os

def patch_file():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    filepath = os.path.join(base_dir, "code", "corpus_generation", "generate_qa_corpus.py")
    
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Insert shuffle_join
    insert_pos = content.find("ATTENTION_TESTING_MOVES =")
    shuffle_def = """def shuffle_join(items, join_str):
    items_copy = list(items)
    random.shuffle(items_copy)
    return join_str.join(items_copy)

"""
    content = content[:insert_pos] + shuffle_def + content[insert_pos:]
    
    content = content.replace('" logic_and ".join(types)', 'shuffle_join(types, " logic_and ")')
    content = content.replace('" logic_or ".join(methods)', 'shuffle_join(methods, " logic_or ")')
    content = content.replace('" logic_or ".join(m_list)', 'shuffle_join(m_list, " logic_or ")')
    content = content.replace('" logic_or ".join(super_effective)', 'shuffle_join(super_effective, " logic_or ")')
    content = content.replace('" logic_or ".join(not_very)', 'shuffle_join(not_very, " logic_or ")')
    content = content.replace('" logic_or ".join(no_effect)', 'shuffle_join(no_effect, " logic_or ")')
    content = content.replace('" logic_or ".join(moves_list)', 'shuffle_join(moves_list, " logic_or ")')
    content = content.replace('" logic_or ".join(evos)', 'shuffle_join(evos, " logic_or ")')
    
    # Add variable logic
    old_var_logic = """        # Action Prevention (Sleep / Bind)
        qa_list.append("query attacker is fast asleep. logic_or attacker is hurt by bind. answer attacker logic_not used unknown move")"""
        
    new_var_logic = """        # Action Prevention (Sleep / Bind)
        qa_list.append("query attacker is fast asleep. logic_or attacker is hurt by bind. answer attacker logic_not used unknown move")
        # Sleep Talk logic
        #qa_list.append("query attacker is fast asleep. logic_and attacker used sleep talk against target answer attacker used unknown move against target")
        #qa_list.append("query attacker logic_not is fast asleep. logic_and attacker used sleep talk against target answer it had no effect")
        # Dream Eater logic
        #qa_list.append("query target is fast asleep. logic_and attacker used dream eater against target answer it was effective")
        #qa_list.append("query target logic_not is fast asleep. logic_and attacker used dream eater against target answer it had no effect")"""
        
    content = content.replace(old_var_logic, new_var_logic)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

if __name__ == "__main__":
    patch_file()
