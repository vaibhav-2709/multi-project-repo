import pandas as pd
import os
from datetime import datetime

# Category importance weights (research-based assumption)
CATEGORY_WEIGHTS = {
    "Meat": 1.5,
    "Dairy": 1.3,
    "Vegetables": 1.2,
    "Fruits": 1.1,
    "Grains": 0.8
}

def calculate_days_to_expiry(expiry_date):
    """
    Calculate number of days left before expiry.
    Ensures minimum value of 1 to avoid division errors.
    """
    today = datetime.now().date()
    delta = (expiry_date - today).days
    return max(delta, 1)


def compute_waste_score(row):
    """
    Waste Score Formula (Core Innovation):
    Waste Score = (1 / Days_to_Expiry) × Quantity × Category_Factor
    """
    expiry_date = pd.to_datetime(row["Expiry_Date"]).date()
    days_left = calculate_days_to_expiry(expiry_date)

    quantity = row["Quantity"]
    category = row["Category"]

    category_factor = CATEGORY_WEIGHTS.get(category, 1.0)

    waste_score = (1 / days_left) * quantity * category_factor
    return round(waste_score, 4)


def add_waste_scores(df):
    """
    Apply waste score computation to entire dataset.
    """
    df["Waste_Score"] = df.apply(compute_waste_score, axis=1)
    return df


if __name__ == "__main__":
    # Resolve base directory dynamically
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # Input path
    input_path = os.path.join(base_dir, "../../data/raw/generated_dataset.csv")

    # Output directory (create if not exists)
    output_dir = os.path.join(base_dir, "../../data/processed")
    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(output_dir, "scored_dataset.csv")

    # Load dataset
    df = pd.read_csv(input_path)

    # Compute waste scores
    df = add_waste_scores(df)

    # Save updated dataset
    df.to_csv(output_path, index=False)

    print(f"Waste scores added successfully at: {output_path}")