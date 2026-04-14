import streamlit as st
import pandas as pd
import os
from datetime import date

st.set_page_config(page_title="Food Waste AI", layout="wide")

st.title("🍽 Food Waste Reduction AI Dashboard")

# -----------------------------
# CONSTANTS
# -----------------------------
CATEGORY_WEIGHTS = {
    "Meat": 1.5,
    "Dairy": 1.3,
    "Vegetables": 1.2,
    "Fruits": 1.1,
    "Grains": 0.8
}

EMISSION_FACTOR = 2.5  # kg CO2 per waste unit

# -----------------------------
# FUNCTION
# -----------------------------
def compute_score(expiry_date, quantity, category):
    days_left = (expiry_date - date.today()).days
    days_left = max(days_left, 1)
    return (1 / days_left) * quantity * CATEGORY_WEIGHTS[category]

# -----------------------------
# USER INPUT
# -----------------------------
st.sidebar.header("➕ Add Food Item")

ingredient = st.sidebar.text_input("Ingredient")
category = st.sidebar.selectbox("Category", list(CATEGORY_WEIGHTS.keys()))
quantity = st.sidebar.number_input("Quantity", 1, 10)
expiry = st.sidebar.date_input("Expiry Date", min_value=date.today())

if "user_data" not in st.session_state:
    st.session_state.user_data = []

if st.sidebar.button("Add Item"):
    score = compute_score(expiry, quantity, category)

    st.session_state.user_data.append({
        "Ingredient": ingredient,
        "Category": category,
        "Quantity": quantity,
        "Expiry_Date": expiry,
        "Waste_Score": round(score, 4)
    })

    st.sidebar.success("Item Added!")

# -----------------------------
# USER INVENTORY
# -----------------------------
st.subheader("📦 Your Inventory")

if st.session_state.user_data:
    df_user = pd.DataFrame(st.session_state.user_data)

    col1, col2 = st.columns(2)

    with col1:
        st.dataframe(df_user)

    with col2:
        st.subheader("⚠ Priority Items")
        st.dataframe(df_user.sort_values(by="Waste_Score", ascending=False))

    # Recommendations
    st.subheader("🍲 Recommended to Use Today")
    st.dataframe(df_user.sort_values(by="Waste_Score", ascending=False).head(3))

    # -----------------------------
    # USER METRICS
    # -----------------------------
    st.subheader("📊 Your Metrics")

    total_waste = df_user["Waste_Score"].sum()
    avg_waste = df_user["Waste_Score"].mean()
    carbon_estimate = total_waste * EMISSION_FACTOR

    m1, m2, m3 = st.columns(3)

    m1.metric("Total Waste Score", round(total_waste, 2))
    m2.metric("Average Waste Score", round(avg_waste, 4))
    m3.metric("Estimated CO₂ Impact (kg)", round(carbon_estimate, 2))

else:
    st.info("Add items from sidebar to begin.")

# -----------------------------
# SYSTEM DATA INSIGHTS
# -----------------------------
st.subheader("📊 System Insights (Simulation Results)")

base_dir = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(base_dir, "../data/processed/scored_dataset.csv")

df = pd.read_csv(data_path)

total_waste_system = df["Waste_Score"].sum()

st.metric("System Total Waste Score", round(total_waste_system, 2))

# -----------------------------
# GRAPHS
# -----------------------------
st.subheader("📈 Visual Analysis")

graph_dir = os.path.join(base_dir, "../results/graphs")

if os.path.exists(graph_dir):
    graphs = os.listdir(graph_dir)

    for g in graphs:
        st.image(os.path.join(graph_dir, g), caption=g)

# -----------------------------
# FOOTER
# -----------------------------
st.markdown("---")
st.markdown("🚀 AI-Based Food Waste Reduction System ")