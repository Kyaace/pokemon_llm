import json
import matplotlib.pyplot as plt
import os

def plot_combined_loss():
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    models_dir = os.path.join(base_dir, "models")
    reports_dir = os.path.join(base_dir, "reports", "charts_v2")
    os.makedirs(reports_dir, exist_ok=True)
    
    models = {
        "Johnny v2": os.path.join(models_dir, "johnny_v2", "loss_history.json"),
        "Spike v2": os.path.join(models_dir, "spike_v2", "loss_history.json"),
        "Ace v2": os.path.join(models_dir, "ace_v2", "loss_history.json")
    }
    
    plt.figure(figsize=(10, 6))
    
    for label, path in models.items():
        if not os.path.exists(path):
            print(f"Warning: {path} not found.")
            continue
            
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        epochs = []
        losses = []
        for obj in data:
            if "epoch" in obj and "loss" in obj:
                epochs.append(obj["epoch"])
                losses.append(obj["loss"])
                
        if epochs and losses:
            plt.plot(epochs, losses, label=label)
            
    plt.title("Persona V2.1 Combined Training Loss (Scaled by Epoch)")
    plt.xlabel("Epoch")
    plt.ylabel("Loss")
    plt.legend()
    plt.grid(True)
    
    output_path = os.path.join(reports_dir, "combined_loss_v2.1.png")
    plt.savefig(output_path, dpi=300)
    plt.close()
    print(f"Saved combined loss chart to {output_path}")

if __name__ == "__main__":
    plot_combined_loss()
