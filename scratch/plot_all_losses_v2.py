import matplotlib.pyplot as plt
import json
import os

base_dir = r'd:\antigrav\pokemon_llm\models'
models = ['johnny_v2', 'spike_v2', 'ace_v2']
colors = ['green', 'orange', 'red'] # Keep colors consistent with v1

plt.figure(figsize=(12, 8))

for model, color in zip(models, colors):
    loss_file = os.path.join(base_dir, model, 'loss_history.json')
    if os.path.exists(loss_file):
        with open(loss_file, 'r') as f:
            history = json.load(f)
        steps = [entry['step'] for entry in history]
        loss = [entry['loss'] for entry in history]
        plt.plot(steps, loss, label=model.replace('_', ' ').capitalize(), color=color, linewidth=2)

plt.title('V2 Persona Fine-Tuning Loss Curves', fontsize=16)
plt.xlabel('Step', fontsize=12)
plt.ylabel('Training Loss', fontsize=12)
plt.legend(fontsize=12)
plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()

output_path = r'd:\antigrav\pokemon_llm\graphs\persona_losses_v2.png'
plt.savefig(output_path, dpi=300)
print(f"Plot saved to {output_path}")
