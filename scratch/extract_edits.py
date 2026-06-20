import json
import pprint

tpath = r'C:\Users\Kyaac\.gemini\antigravity-ide\brain\d2334b08-1493-4866-9ad9-8cddf9dd6e62\.system_generated\logs\transcript.jsonl'
with open(tpath, 'r', encoding='utf-8') as f:
    lines = f.readlines()

edits = []
for l in lines:
    s = json.loads(l)
    if 'tool_calls' in s:
        for c in s['tool_calls']:
            args = c.get('arguments', {})
            if 'expert_system.py' in args.get('TargetFile', '') or 'expert_system.py' in args.get('Target', '') or 'expert_system.py' in args.get('AbsolutePath', ''):
                edits.append((c['name'], args))

print(f'Found {len(edits)} tool calls related to expert_system.py')
with open('scratch/last_edit.txt', 'w', encoding='utf-8') as f:
    if edits:
        for name, args in edits:
            f.write(f"TOOL CALL: {name}\n")
            if "ReplacementChunks" in args:
                for chunk in args["ReplacementChunks"]:
                    f.write(f"REPLACED:\n{chunk.get('TargetContent', '')}\nWITH:\n{chunk.get('ReplacementContent', '')}\n")
                    f.write("-" * 40 + "\n")
            elif "ReplacementContent" in args:
                f.write(f"REPLACED:\n{args.get('TargetContent', '')}\nWITH:\n{args.get('ReplacementContent', '')}\n")
                f.write("-" * 40 + "\n")
