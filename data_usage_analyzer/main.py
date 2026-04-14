# =========================================
# IMPORTS
# =========================================
from src.data_loader import load_data, basic_info
from src.utils import clean_column_names
from src.data_transformer import convert_to_app_level, save_processed_data
from src.visualization import plot_app_usage, plot_user_behavior
from src.prediction_model import train_model
from src.optimization_engine import simulate_savings, generate_suggestions
from src.evaluation import evaluate_savings


# =========================================
# STEP 1: Load Data
# =========================================
DATA_PATH = "data/raw/mobile_usage.csv"

df = load_data(DATA_PATH)


# =========================================
# STEP 2: Clean Column Names
# =========================================
df = clean_column_names(df)

print("\n--- CLEANED DATA INFO ---")
basic_info(df)

print("\n--- CLEANED COLUMNS ---")
print(df.columns)


# =========================================
# STEP 3: Convert to App-Level Data
# =========================================
app_df = convert_to_app_level(df)

print("\n--- APP LEVEL DATA ---")
print(app_df.head())

print("\nTotal rows after transformation:", len(app_df))


# =========================================
# STEP 4: Save Processed Data
# =========================================
save_processed_data(app_df, "data/processed/app_usage.csv")

print("\n✅ Processed data saved at data/processed/app_usage.csv")


# =========================================
# STEP 5: Visualization
# =========================================
plot_app_usage(app_df)
plot_user_behavior(app_df)


# =========================================
# STEP 6: Train Prediction Model
# =========================================
model = train_model(app_df)


# =========================================
# STEP 7: Optimization Engine
# =========================================
print("\n--- OPTIMIZATION SUGGESTIONS ---")

suggestions = generate_suggestions(app_df)

for s in suggestions:
    print(s)

# Example simulation
saved = simulate_savings(app_df, "Instagram", 30)

print(f"\nIf Instagram usage reduced by 30%, you save: {saved:.2f} MB")


# =========================================
# STEP 8: Evaluation (NEW 🔥)
# =========================================
evaluate_savings(app_df)