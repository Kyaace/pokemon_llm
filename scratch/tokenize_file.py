import os, sys; base=os.path.abspath('code'); sys.path.append(base); from tokenizer import PokemonTokenizer; t=PokemonTokenizer(); lines=open('corpus/expert_corpus_v2.txt', encoding='utf-8').readlines(); print('Testing', len(lines), 'fights...'); errs=0;  
for i, line in enumerate(lines):  
    try:  
        t.encode_text(line.strip(), mode='BATTLE')  
    except ValueError as e:  
        print(f'Line {i+1}: {e}')  
        errs+=1  
print('Total errors:', errs) 
