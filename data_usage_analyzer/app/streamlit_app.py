import streamlit as st
import pandas as pd
import sys
import os

# 👇 ADD THIS (IMPORTANT FIX)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.data_loader import load_data
from src.utils import clean_column_names
from src.data_transformer import convert_to_app_level
from src.optimization_engine import simulate_savings, generate_suggestions

# Title
st.title("📱 Smart Data Usage Optimizer AI")

# Load data
df = load_data("data/raw/mobile_usage.csv")
df = clean_column_names(df)

app_df = convert_to_app_level(df)

# =========================
# Show raw data
# =========================
st.subheader("📊 Raw Dataset")
st.dataframe(df.head())

# =========================
# App usage chart
# =========================
st.subheader("📈 App Data Usage")
app_usage = app_df.groupby('app')['data_usage'].sum()
st.bar_chart(app_usage)

# =========================
# Optimization suggestions
# =========================
st.subheader("⚡ Optimization Suggestions")

suggestions = generate_suggestions(app_df)

for s in suggestions:
    st.write("✔", s)

# =========================
# Simulation
# =========================
st.subheader("🧪 Simulation")

app_name = st.selectbox("Select App", app_df['app'].unique())
reduction = st.slider("Reduction %", 10, 50, 20)

saved = simulate_savings(app_df, app_name, reduction)

st.success(f"You can save approximately {saved:.2f} MB")