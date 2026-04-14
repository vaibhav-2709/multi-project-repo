import pandas as pd
import os

def load_data():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(base_dir, "data/raw/household_power_consumption.txt")
    
    df = pd.read_csv(file_path, sep=';', low_memory=False)
    print("✅ Data loaded successfully")
    return df


def clean_data(df):
    print("🔄 Cleaning data...")

    df.replace('?', pd.NA, inplace=True)

    numeric_cols = [
        'Global_active_power',
        'Global_reactive_power',
        'Voltage',
        'Global_intensity',
        'Sub_metering_1',
        'Sub_metering_2',
        'Sub_metering_3'
    ]

    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    df['Datetime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'], dayfirst=True)

    df.drop(columns=['Date', 'Time'], inplace=True)

    df.dropna(inplace=True)

    print("✅ Data cleaned")
    return df


def feature_engineering(df):
    print("⚙️ Performing feature engineering...")

    df['hour'] = df['Datetime'].dt.hour
    df['day'] = df['Datetime'].dt.day
    df['month'] = df['Datetime'].dt.month

    # Energy
    df['total_energy'] = df['Global_active_power']

    # 🔥 Cost (important for paper)
    tariff_rate = 5  # ₹ per unit
    df['cost'] = df['total_energy'] * tariff_rate

    print("✅ Features created")
    return df


def save_clean_data(df):
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    output_dir = os.path.join(base_dir, "data", "processed")

    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(output_dir, "cleaned_data.csv")

    df.to_csv(output_path, index=False)
    print(f"✅ Cleaned data saved at: {output_path}")


if __name__ == "__main__":
    df = load_data()
    df = clean_data(df)
    df = feature_engineering(df)
    save_clean_data(df)