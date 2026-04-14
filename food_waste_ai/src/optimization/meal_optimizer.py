import pandas as pd
import os

def load_data():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(base_dir, "../../data/processed/scored_dataset.csv")
    return pd.read_csv(input_path)


def optimize_meal_plan(df, max_items=5):
    """
    Greedy optimization:
    Select top items with highest waste score
    """
    # Sort by highest waste score (urgent items first)
    df_sorted = df.sort_values(by="Waste_Score", ascending=False)

    # Select top items
    selected_items = df_sorted.head(max_items)

    return selected_items


def calculate_waste_reduction(df, selected_items):
    """
    Calculate how much waste is reduced by using selected items
    """
    total_waste_before = df["Waste_Score"].sum()

    # Assume selected items are saved from waste
    waste_after = df[~df.index.isin(selected_items.index)]["Waste_Score"].sum()

    reduction = total_waste_before - waste_after
    reduction_percent = (reduction / total_waste_before) * 100

    return round(reduction, 4), round(reduction_percent, 2)


if __name__ == "__main__":
    df = load_data()

    selected_items = optimize_meal_plan(df, max_items=5)

    reduction, reduction_percent = calculate_waste_reduction(df, selected_items)

    print("\n📌 Recommended Items to Use Today:\n")
    print(selected_items[["Ingredient", "Category", "Quantity", "Waste_Score"]])

    print("\n📊 Waste Reduction Analysis:")
    print(f"Total Waste Reduced: {reduction}")
    print(f"Reduction Percentage: {reduction_percent}%")

    # Save results
    base_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(base_dir, "../../results")
    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(output_dir, "optimized_meal_plan.csv")
    selected_items.to_csv(output_path, index=False)

    print(f"\nResults saved at: {output_path}")