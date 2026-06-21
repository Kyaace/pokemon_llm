import json
import matplotlib.pyplot as plt

def plot_loss():
    with open(r"D:\antigrav\pokemon_llm\models\johnny_v2\loss_history.json", "r") as f:
        data = json.load(f)

    steps = [x["step"] for x in data]
    losses = [x["loss"] for x in data]

    plt.figure(figsize=(10, 6))
    plt.plot(steps, losses, label="Training Loss")
    plt.xlabel("Steps")
    plt.ylabel("Loss")
    plt.title("Johnny v2 Training Loss")
    plt.legend()
    plt.grid(True)
    plt.savefig(r"C:\Users\Kyaac\.gemini\antigravity-ide\brain\d2334b08-1493-4866-9ad9-8cddf9dd6e62\johnny_v2_loss.png")
    print("Plot saved.")

if __name__ == "__main__":
    plot_loss()
