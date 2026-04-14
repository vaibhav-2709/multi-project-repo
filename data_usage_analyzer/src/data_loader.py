import pandas as pd

def load_data(path):
    """
    Load dataset from CSV file
    """
    df = pd.read_csv(path)
    return df


def basic_info(df):
    """
    Print basic dataset info
    """
    print("\n--- DATASET INFO ---")
    print(df.info())

    print("\n--- FIRST 5 ROWS ---")
    print(df.head())

    print("\n--- NULL VALUES ---")
    print(df.isnull().sum())