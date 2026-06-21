import os
import random

def get_term():
    val = random.choice(["True", "False"])
    # 30% chance to negate the term
    if random.random() < 0.3:
        return f"NOT {val}"
    return val

def generate_logic_corpus(output_path, num_examples=300):
    """
    Generates a synthetic logic corpus consisting of pure boolean truth tables.
    50% 2-term truth tables
    40% 3-term truth tables
    10% 4-term truth tables
    """
    examples = []
    
    num_2_term = int(num_examples * 0.50)
    num_3_term = int(num_examples * 0.40)
    num_4_term = num_examples - num_2_term - num_3_term
    
    # 2-term examples
    for _ in range(num_2_term):
        t1 = get_term()
        t2 = get_term()
        op = random.choice(["AND", "OR"])
        expr = f"{t1} {op} {t2}"
        ans = eval(expr.replace("AND", "and").replace("OR", "or").replace("NOT", "not"))
        ans_str = "True" if ans else "False"
        examples.append(f"query {expr} answer {ans_str}")
        
    # 3-term examples
    for _ in range(num_3_term):
        t1 = get_term()
        t2 = get_term()
        t3 = get_term()
        op1 = random.choice(["AND", "OR"])
        op2 = random.choice(["AND", "OR"])
        
        # Parentheses variants (No spaces inside parens per user request)
        paren_style = random.choice([
            f"({t1} {op1} {t2}) {op2} {t3}",
            f"{t1} {op1} ({t2} {op2} {t3})",
            f"{t1} {op1} {t2} {op2} {t3}"  # No parens
        ])
        
        expr = paren_style
        py_expr = expr.replace("AND", "and").replace("OR", "or").replace("NOT", "not")
        ans = eval(py_expr)
        ans_str = "True" if ans else "False"
        examples.append(f"query {expr} answer {ans_str}")
        
    # 4-term examples
    for _ in range(num_4_term):
        t1 = get_term()
        t2 = get_term()
        t3 = get_term()
        t4 = get_term()
        op1 = random.choice(["AND", "OR"])
        op2 = random.choice(["AND", "OR"])
        op3 = random.choice(["AND", "OR"])
        
        paren_style = random.choice([
            f"({t1} {op1} {t2}) {op2} ({t3} {op3} {t4})",
            f"(({t1} {op1} {t2}) {op2} {t3}) {op3} {t4}",
            f"{t1} {op1} ({t2} {op2} ({t3} {op3} {t4}))"
        ])
        
        expr = paren_style
        py_expr = expr.replace("AND", "and").replace("OR", "or").replace("NOT", "not")
        ans = eval(py_expr)
        ans_str = "True" if ans else "False"
        examples.append(f"query {expr} answer {ans_str}")
        
    # Shuffle the dataset to ensure variety
    random.shuffle(examples)
    
    with open(output_path, "w", encoding="utf-8") as f:
        for ex in examples:
            f.write(ex + "\n")
            
    print(f"Generated {len(examples)} pure truth table logic examples at {output_path}")

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    output_dir = os.path.join(base_dir, "corpus")
    os.makedirs(output_dir, exist_ok=True)
    
    output_path = os.path.join(output_dir, "logic_corpus.txt")
    generate_logic_corpus(output_path)
