import streamlit as st
import pandas as pd
import os
import joblib
import matplotlib.pyplot as plt
import numpy as np

# ---------------- LOAD ---------------- #
@st.cache_data
def load_data():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    df = pd.read_csv(os.path.join(base_dir, "data/processed/usage_analyzed.csv"))

    # Speed optimization
    df = df.sample(50000, random_state=42)

    return df


@st.cache_resource
def load_model():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return joblib.load(os.path.join(base_dir, "models/cost_model.pkl"))


# ---------------- FAST COST ---------------- #
def calculate_cost(df, model):
    features = ['hour', 'day', 'month', 'Voltage', 'Global_intensity']

    energy_pred = model.predict(df[features])

    hours = df['hour']

    tariff = (
        (hours.between(18, 22)) * 8 +
        (hours.between(0, 6)) * 3 +
        (~(hours.between(18, 22) | hours.between(0, 6))) * 5
    )

    total_cost = (energy_pred * tariff).sum()

    return total_cost, energy_pred


# ---------------- UI ---------------- #
st.set_page_config(page_title="Electricity Optimizer", layout="wide")

st.title("⚡ Electricity Bill Optimizer AI")
st.markdown("### 💡 Smart Energy Optimization Dashboard")

df = load_data()
model = load_model()

# ---------------- SIDEBAR ---------------- #
st.sidebar.header("⚙️ User Controls")

reduction = st.sidebar.slider("Reduce Usage (%)", 0, 50, 20)

time_option = st.sidebar.selectbox(
    "Shift Usage To:",
    ["No Change", "Night (Cheap)", "Peak (Expensive)"]
)

run_button = st.sidebar.button("🚀 Run Simulation")

# ---------------- MAIN ---------------- #
if run_button:

    with st.spinner("⚡ Running simulation..."):

        df_sim = df.copy()

        # Apply reduction
        df_sim['Global_intensity'] *= (1 - reduction / 100)

        # Apply time shift
        if time_option == "Night (Cheap)":
            df_sim['hour'] = 2
        elif time_option == "Peak (Expensive)":
            df_sim['hour'] = 19

        # Cost calculation
        original_cost, energy_orig = calculate_cost(df, model)
        new_cost, energy_new = calculate_cost(df_sim, model)

        savings = original_cost - new_cost
        savings_percent = (savings / original_cost) * 100

    # ---------------- METRICS ---------------- #
    st.subheader("📊 Key Metrics")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("💰 Original Cost", f"₹{original_cost:,.0f}")
    col2.metric("⚡ Optimized Cost", f"₹{new_cost:,.0f}")
    col3.metric("📉 Savings", f"₹{savings:,.0f}")
    col4.metric("📊 Savings %", f"{savings_percent:.2f}%")

    # ---------------- GRAPH SECTION ---------------- #
    st.subheader("📈 Analysis Dashboard")

    colA, colB = st.columns(2)

    # 🔹 Small Bar Chart
    with colA:
        fig1, ax1 = plt.subplots(figsize=(4, 3))
        ax1.bar(["Original", "Optimized"], [original_cost, new_cost])
        ax1.set_title("Cost Comparison")
        st.pyplot(fig1)

    # 🔹 Line Trend (small)
    with colB:
        fig2, ax2 = plt.subplots(figsize=(4, 3))
        ax2.plot(energy_orig[:100], label="Original")
        ax2.plot(energy_new[:100], label="Optimized")
        ax2.legend()
        ax2.set_title("Energy Trend (Sample)")
        st.pyplot(fig2)

    # ---------------- EXTRA GRAPH ---------------- #
    colC, colD = st.columns(2)

    # 🔹 Hourly Usage Pattern
    with colC:
        hourly = df.groupby("hour")["Global_intensity"].mean()
        fig3, ax3 = plt.subplots(figsize=(4, 3))
        ax3.plot(hourly)
        ax3.set_title("Hourly Usage Pattern")
        st.pyplot(fig3)

    # 🔹 Savings Distribution
    with colD:
        diff = energy_orig[:1000] - energy_new[:1000]
        fig4, ax4 = plt.subplots(figsize=(4, 3))
        ax4.hist(diff, bins=30)
        ax4.set_title("Savings Distribution")
        st.pyplot(fig4)

    # ---------------- INSIGHTS ---------------- #
    st.subheader("🧠 Smart Insights")

    if savings > 0:
        st.success(f"✅ You can save ₹{savings:,.0f} ({savings_percent:.2f}%)")

        if time_option == "Night (Cheap)":
            st.info("🌙 Night usage significantly reduces electricity cost!")

        if reduction > 0:
            st.info("⚡ Reducing appliance usage is effective!")

        if savings_percent > 30:
            st.warning("🔥 High savings detected! Strong optimization strategy.")

    else:
        st.warning("⚠️ Try different settings.")

else:
    st.info("👉 Adjust settings and click 'Run Simulation'")

# ---------------- FOOTER ---------------- #
st.markdown("---")
st.markdown("🚀 AI-Based Energy Optimization System")