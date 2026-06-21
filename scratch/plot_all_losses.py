import matplotlib.pyplot as plt
import json
import os

base_dir = r'd:\antigrav\pokemon_llm\models'
models = ['foundation', 'timmy', 'johnny', 'spike', 'ace']
colors = ['black', 'blue', 'green', 'orange', 'red']

plt.figure(figsize=(12, 8))

for model, color in zip(models, colors):
    loss_file = os.path.join(base_dir, model, 'loss_history.json')
    if os.path.exists(loss_file):
        with open(loss_file, 'r') as f:
            history = json.load(f)
        steps = [entry['step'] for entry in history]
        loss = [entry['loss'] for entry in history]
        plt.plot(steps, loss, label=model.capitalize(), color=color, linewidth=2)

plt.title('Persona Fine-Tuning Loss Curves', fontsize=16)
plt.xlabel('Step', fontsize=12)
plt.ylabel('Training Loss', fontsize=12)
plt.legend(fontsize=12)
plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()

output_path = r'C:\Users\Kyaac\.gemini\antigravity-ide\brain\d2334b08-1493-4866-9ad9-8cddf9dd6e62\persona_losses.png'
plt.savefig(output_path, dpi=300)
print(f"Plot saved to {output_path}")
