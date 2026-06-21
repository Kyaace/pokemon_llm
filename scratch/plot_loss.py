import matplotlib.pyplot as plt
import json
import os

loss_file = r'd:\antigrav\pokemon_llm\models\foundation\loss_history.json'

with open(loss_file, 'r') as f:
    history = json.load(f)

steps = [entry['step'] for entry in history]
loss = [entry['loss'] for entry in history]

plt.figure(figsize=(10, 6))
plt.plot(steps, loss, marker='', linestyle='-', color='r', linewidth=2)
plt.title('Foundation Training Loss over Steps', fontsize=16)
plt.xlabel('Step', fontsize=12)
plt.ylabel('Training Loss', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()

output_path = r'C:\Users\Kyaac\.gemini\antigravity-ide\brain\d2334b08-1493-4866-9ad9-8cddf9dd6e62\foundation_loss.png'
plt.savefig(output_path, dpi=300)
print(f"Plot saved to {output_path}")
