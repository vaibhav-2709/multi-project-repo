import pandas as pd
import os
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import matplotlib.pyplot as plt
import joblib
import numpy as np


def load_data():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(base_dir, "data/processed/usage_analyzed.csv")

    df = pd.read_csv(file_path)
    print("✅ Data loaded for prediction")
    return df


def prepare_data(df):
    print("⚙️ Preparing data...")

    # 🔥 Improved features (NO leakage + strong prediction)
    features = [
        'hour',
        'day',
        'month',
        'Voltage',
        'Global_intensity'
    ]

    target = 'cost'

    X = df[features]
    y = df[target]

    return X, y


def train_model(X, y):
    print("🤖 Training model (Random Forest)...")

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = RandomForestRegressor(
        n_estimators=100,
        max_depth=10,
        random_state=42,
        n_jobs=-1
    )

    model.fit(X_train, y_train)

    print("✅ Model trained")

    return model, X_test, y_test


def evaluate_model(model, X_test, y_test):
    print("📊 Evaluating model...")

    predictions = model.predict(X_test)

    mae = mean_absolute_error(y_test, predictions)
    mse = mean_squared_error(y_test, predictions)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_test, predictions)

    print(f"\n📈 MODEL PERFORMANCE:")
    print(f"MAE  : {mae:.4f}")
    print(f"MSE  : {mse:.4f}")
    print(f"RMSE : {rmse:.4f}")
    print(f"R²   : {r2:.4f}")

    return predictions, mae, mse, rmse, r2


def save_model(model):
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    model_dir = os.path.join(base_dir, "models")

    os.makedirs(model_dir, exist_ok=True)

    model_path = os.path.join(model_dir, "cost_model.pkl")
    joblib.dump(model, model_path)

    print(f"✅ Model saved at: {model_path}")


def plot_results(y_test, predictions):
    print("📈 Generating graphs...")

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    graphs_dir = os.path.join(base_dir, "results", "graphs")

    os.makedirs(graphs_dir, exist_ok=True)

    # 🔹 Scatter Plot
    plt.figure()
    plt.scatter(y_test, predictions, alpha=0.5)
    plt.xlabel("Actual Cost")
    plt.ylabel("Predicted Cost")
    plt.title("Actual vs Predicted Cost")

    plt.savefig(os.path.join(graphs_dir, "scatter_plot.png"))
    plt.show()

    # 🔹 Line Plot (first 100 points)
    plt.figure()
    plt.plot(y_test.values[:100], label='Actual')
    plt.plot(predictions[:100], label='Predicted')
    plt.legend()
    plt.title("Actual vs Predicted (Line Plot)")

    plt.savefig(os.path.join(graphs_dir, "line_plot.png"))
    plt.show()

    # 🔹 Error Distribution (VERY IMPORTANT 🔥)
    errors = y_test - predictions

    plt.figure()
    plt.hist(errors, bins=30)
    plt.title("Error Distribution")

    plt.savefig(os.path.join(graphs_dir, "error_distribution.png"))
    plt.show()

    print("✅ All graphs saved")


if __name__ == "__main__":
    df = load_data()

    X, y = prepare_data(df)

    model, X_test, y_test = train_model(X, y)

    predictions, mae, mse, rmse, r2 = evaluate_model(model, X_test, y_test)

    save_model(model)

    plot_results(y_test, predictions)