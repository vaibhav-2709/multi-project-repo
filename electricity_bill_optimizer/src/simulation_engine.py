import pandas as pd
import os
import joblib


# 🔥 Tariff function (VERY IMPORTANT)
def get_tariff(hour):
    if 18 <= hour <= 22:
        return 8   # Peak hours (expensive)
    elif 0 <= hour <= 6:
        return 3   # Night (cheap)
    else:
        return 5   # Normal


def load_model_and_data():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    data_path = os.path.join(base_dir, "data/processed/usage_analyzed.csv")
    model_path = os.path.join(base_dir, "models/cost_model.pkl")

    df = pd.read_csv(data_path)
    model = joblib.load(model_path)

    print("✅ Model and data loaded")
    return df, model


# 🔥 New cost calculation (tariff-based)
def calculate_cost(df, model):
    features = ['hour', 'day', 'month', 'Voltage', 'Global_intensity']

    energy_pred = model.predict(df[features])

    total_cost = 0

    for i, row in df.iterrows():
        tariff = get_tariff(row['hour'])
        total_cost += energy_pred[i] * tariff

    return total_cost


def simulate_reduction(df, model, reduction_percent=20):
    print(f"\n🔻 Simulating {reduction_percent}% usage reduction...")

    df_sim = df.copy()

    # Reduce appliance usage
    df_sim['Global_intensity'] = df_sim['Global_intensity'] * (1 - reduction_percent / 100)

    original_cost = calculate_cost(df, model)
    new_cost = calculate_cost(df_sim, model)

    savings = original_cost - new_cost

    print(f"💰 Original Cost: {original_cost:.2f}")
    print(f"💰 New Cost: {new_cost:.2f}")
    print(f"💸 Savings: {savings:.2f}")

    return original_cost, new_cost, savings


def simulate_time_shift(df, model):
    print("\n🌙 Simulating usage shift to night hours...")

    df_sim = df.copy()

    # Shift usage to night hours (2 AM)
    df_sim['hour'] = 2

    original_cost = calculate_cost(df, model)
    new_cost = calculate_cost(df_sim, model)

    savings = original_cost - new_cost

    print(f"💰 Original Cost: {original_cost:.2f}")
    print(f"💰 New Cost (Night Usage): {new_cost:.2f}")
    print(f"💸 Savings: {savings:.2f}")

    return original_cost, new_cost, savings


if __name__ == "__main__":
    df, model = load_model_and_data()

    # Scenario 1: Reduce usage
    simulate_reduction(df, model, reduction_percent=20)

    # Scenario 2: Shift usage to night
    simulate_time_shift(df, model)