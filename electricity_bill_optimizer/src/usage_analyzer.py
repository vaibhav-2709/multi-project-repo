import pandas as pd
import os
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt


def load_processed_data():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(base_dir, "data/processed/cleaned_data.csv")
    
    df = pd.read_csv(file_path)
    print("✅ Processed data loaded")
    return df


def find_peak_hours(df):
    print("🔍 Finding peak usage hours...")

    hourly_usage = df.groupby('hour')['total_energy'].mean()

    peak_hour = hourly_usage.idxmax()
    print(f"⚡ Peak usage hour: {peak_hour}:00")

    return hourly_usage


def cluster_usage(df):
    print("🤖 Clustering usage patterns...")

    features = df[['hour', 'total_energy']]

    kmeans = KMeans(n_clusters=3, random_state=42)
    df['usage_cluster'] = kmeans.fit_predict(features)

    print("✅ Clustering completed")
    return df


def save_results(df):
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    output_dir = os.path.join(base_dir, "data", "processed")
    os.makedirs(output_dir, exist_ok=True)  # 🔥 auto-create folder

    output_path = os.path.join(output_dir, "usage_analyzed.csv")
    df.to_csv(output_path, index=False)

    print(f"✅ Results saved at: {output_path}")


def plot_usage(hourly_usage):
    print("📊 Plotting usage graph...")

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    graphs_dir = os.path.join(base_dir, "results", "graphs")

    # 🔥 Automatically create directory if it doesn't exist
    os.makedirs(graphs_dir, exist_ok=True)

    file_path = os.path.join(graphs_dir, "hourly_usage.png")

    plt.figure()
    hourly_usage.plot()

    plt.xlabel("Hour of Day")
    plt.ylabel("Average Energy Consumption")
    plt.title("Hourly Energy Usage Pattern")

    plt.savefig(file_path)
    plt.show()

    print(f"✅ Graph saved at: {file_path}")


if __name__ == "__main__":
    df = load_processed_data()

    hourly_usage = find_peak_hours(df)

    df = cluster_usage(df)

    save_results(df)

    plot_usage(hourly_usage)