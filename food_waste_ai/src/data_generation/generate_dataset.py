import pandas as pd
import random
import os
from datetime import datetime, timedelta

# Food categories with expiry ranges (in days)
FOOD_CATEGORIES = {
    "Dairy": {
        "Milk": (3, 5),
        "Cheese": (7, 14)
    },
    "Vegetables": {
        "Tomato": (3, 7),
        "Potato": (10, 20)
    },
    "Fruits": {
        "Apple": (7, 14),
        "Banana": (2, 5)
    },
    "Meat": {
        "Chicken": (2, 3),
        "Fish": (1, 2)
    },
    "Grains": {
        "Rice": (30, 60),
        "Wheat": (30, 90)
    }
}

# User behavior types
USER_TYPES = {
    "Careful": 0.9,   # 90% chance to consume
    "Average": 0.7,
    "Wasteful": 0.5
}

def generate_dataset(num_users=30, days=30):
    data = []
    start_date = datetime(2025, 1, 1)

    for user_id in range(1, num_users + 1):
        user_type = random.choice(list(USER_TYPES.keys()))
        consumption_prob = USER_TYPES[user_type]

        for day in range(days):
            purchase_date = start_date + timedelta(days=day)

            # Random food selection
            category = random.choice(list(FOOD_CATEGORIES.keys()))
            item = random.choice(list(FOOD_CATEGORIES[category].keys()))

            expiry_range = FOOD_CATEGORIES[category][item]
            expiry_days = random.randint(expiry_range[0], expiry_range[1])
            expiry_date = purchase_date + timedelta(days=expiry_days)

            quantity = random.randint(1, 5)

            # Simulate consumption vs waste
            consumed = random.random() < consumption_prob
            status = "Used" if consumed else "Wasted"

            # Days before consumption (if used)
            if consumed:
                used_day_offset = random.randint(0, expiry_days)
                used_date = purchase_date + timedelta(days=used_day_offset)
            else:
                used_date = None

            data.append([
                user_id,
                user_type,
                category,
                item,
                quantity,
                purchase_date.date(),
                expiry_date.date(),
                used_date.date() if used_date else None,
                status
            ])

    df = pd.DataFrame(data, columns=[
        "User_ID",
        "User_Type",
        "Category",
        "Ingredient",
        "Quantity",
        "Purchase_Date",
        "Expiry_Date",
        "Used_Date",
        "Status"
    ])

    return df


if __name__ == "__main__":
    df = generate_dataset(num_users=50, days=30)

    # Create directory if not exists
    base_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(base_dir, "../../data/raw")
    os.makedirs(output_dir, exist_ok=True)

    # Save file
    output_path = os.path.join(output_dir, "generated_dataset.csv")
    df.to_csv(output_path, index=False)

    print(f"Dataset generated successfully at: {output_path}")