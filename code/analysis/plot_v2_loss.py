import os
import json
import matplotlib.pyplot as plt

def load_loss(model_name):
    path = rf"d:\antigrav\pokemon_llm\models\{model_name}\loss_history.json"
    if not os.path.exists(path):
        print(f"Could not find loss history for {model_name} at {path}")
        return [], []
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    epochs = [float(point['epoch']) for point in data if 'loss' in point]
    losses = [float(point['loss']) for point in data if 'loss' in point]
    return epochs, losses

def plot():
    plt.figure(figsize=(10, 6))
    
    f_epochs, f_losses = load_loss("foundation_v2.3")
    t_epochs, t_losses = load_loss("timmy_v2.3")
    
    if f_epochs:
        plt.plot(f_epochs, f_losses, label="Foundation v2.3", color="blue", linewidth=2)
    if t_epochs:
        plt.plot(t_epochs, t_losses, label="Timmy v2.3", color="red", linewidth=2)
        
    plt.title("Training Loss Over 5 Epochs (v2.3 Models)")
    plt.xlabel("Epochs")
    plt.ylabel("Loss")
    plt.grid(True, linestyle="--", alpha=0.7)
    plt.legend()
    
    out_path = r"d:\antigrav\pokemon_llm\graphs\v2_3_loss_curve.png"
    plt.savefig(out_path, dpi=300, bbox_inches="tight")
    print(f"Plot saved to {out_path}")

if __name__ == "__main__":
    plot()
