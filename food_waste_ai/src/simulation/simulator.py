import pandas as pd
import os
import matplotlib.pyplot as plt

EMISSION_FACTOR = 2.5  # kg CO2 per waste unit

def load_data():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(base_dir, "../../data/processed/scored_dataset.csv")
    return pd.read_csv(input_path)


def simulate_without_ai(df):
    df_sample = df.sample(frac=0.5, random_state=42)

    waste_after = df[~df.index.isin(df_sample.index)]["Waste_Score"].sum()
    total_waste = df["Waste_Score"].sum()

    utilization = len(df_sample) / len(df)

    return total_waste, waste_after, utilization


def simulate_with_ai(df):
    df_sorted = df.sort_values(by="Waste_Score", ascending=False)
    top_items = df_sorted.head(int(len(df) * 0.5))

    waste_after = df[~df.index.isin(top_items.index)]["Waste_Score"].sum()
    total_waste = df["Waste_Score"].sum()

    utilization = len(top_items) / len(df)

    return total_waste, waste_after, utilization


def calculate_metrics(total, after, utilization, df_length):
    reduction = total - after
    reduction_percent = (reduction / total) * 100
    avg_waste = after / df_length

    # 🌍 Carbon saving
    carbon_saved = reduction * EMISSION_FACTOR

    return {
        "total": round(total, 2),
        "remaining": round(after, 2),
        "reduction_percent": round(reduction_percent, 2),
        "utilization": round(utilization * 100, 2),
        "avg_waste": round(avg_waste, 4),
        "carbon_saved": round(carbon_saved, 2)
    }


def plot_graphs(metrics):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    graph_dir = os.path.join(base_dir, "../../results/graphs")
    os.makedirs(graph_dir, exist_ok=True)

    # Waste comparison
    plt.figure()
    plt.bar(["Without AI", "With AI"],
            [metrics["without_ai"]["remaining"], metrics["with_ai"]["remaining"]])
    plt.title("Remaining Waste Comparison")
    plt.savefig(os.path.join(graph_dir, "waste_comparison.png"))

    # Reduction %
    plt.figure()
    plt.bar(["Without AI", "With AI"],
            [metrics["without_ai"]["reduction_percent"], metrics["with_ai"]["reduction_percent"]])
    plt.title("Waste Reduction Percentage")
    plt.savefig(os.path.join(graph_dir, "reduction_percentage.png"))

    # Utilization
    plt.figure()
    plt.bar(["Without AI", "With AI"],
            [metrics["without_ai"]["utilization"], metrics["with_ai"]["utilization"]])
    plt.title("Utilization Rate (%)")
    plt.savefig(os.path.join(graph_dir, "utilization.png"))

    # 🌍 Carbon Savings
    
    plt.figure()
    plt.bar(["Without AI", "With AI"],
            [metrics["without_ai"]["carbon_saved"], metrics["with_ai"]["carbon_saved"]])
    plt.title("Carbon Emissions Saved (kg CO2)")
    plt.savefig(os.path.join(graph_dir, "carbon_saved.png"))

    print(f"Graphs saved in: {graph_dir}")


if __name__ == "__main__":
    df = load_data()

    total1, after1, util1 = simulate_without_ai(df)
    total2, after2, util2 = simulate_with_ai(df)

    metrics = {
        "without_ai": calculate_metrics(total1, after1, util1, len(df)),
        "with_ai": calculate_metrics(total2, after2, util2, len(df))
    }

    efficiency_gain = metrics["with_ai"]["reduction_percent"] - metrics["without_ai"]["reduction_percent"]

    print("\n📊 FINAL RESULTS:\n")

    for key in metrics:
        print(f"{key.upper()}:")
        for m in metrics[key]:
            print(f"{m}: {metrics[key][m]}")
        print()

    print(f"🚀 Efficiency Gain: {round(efficiency_gain, 2)}%")

    plot_graphs(metrics)