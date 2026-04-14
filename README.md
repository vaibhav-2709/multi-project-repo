# Project 1-
Smart Data Usage Optimizer AI

## 🚀 Overview

This project is a simple AI-based system that helps users **analyze, predict, and optimize mobile data usage**.

It shows:

* Which apps consume the most data
* Future data usage prediction
* Suggestions to reduce usage
* Estimated data savings

---

## 💡 Features

* 📊 App-wise data analysis
* 🔮 Data usage prediction
* ⚡ Optimization suggestions
* 🧪 Simulation (reduce usage & see savings)
* 🌐 Interactive UI (Streamlit)

---

## 📁 Project Structure

```
data-optimizer-ai/
├── data/
├── src/
├── app/
├── models/
├── requirements.txt
└── main.py
```

---

## 📊 Dataset

* 700 user records
* Includes usage time, data usage, behavior, etc.
* Converted into app-wise data using custom logic

---

## ▶️ How to Run

### Install dependencies

```
pip install -r requirements.txt
```

### Run main project

```
python main.py
```

### Run UI

```
streamlit run app/streamlit_app.py
```

## 📈 Output

* Model predicts data usage
* Suggests which apps to reduce
* Shows how much data you can save

---

# ⚡ Project 2 – Smart Electricity Bill Optimizer AI

## 🚀 Overview

This project is an AI-based system that helps users analyze, predict, and optimize household electricity usage.

It shows:
- Which time periods consume the most electricity
- Estimated electricity bill
- Cost-saving strategies
- Potential savings using different scenarios

---

## 💡 Features

- Electricity usage analysis
- Cost prediction using Machine Learning
- Optimization suggestions
- Simulation (reduce usage & shift timing)
- Time-based tariff optimization
- Interactive UI (Streamlit dashboard)

---

## 📁 Project Structure

electricity-bill-optimizer-ai/
├── data/
│   ├── raw/
│   ├── processed/
│
├── src/
│   ├── data_preprocessing.py
│   ├── usage_analyzer.py
│   ├── cost_predictor.py
│   ├── simulation_engine.py
│
├── app/
│   └── streamlit_app.py
│
├── models/
├── results/
├── requirements.txt
└── README.md

---

## 📊 Dataset

- Real-world household electricity consumption dataset
- Includes:
  - Voltage
  - Current (intensity)
  - Power consumption
  - Date and time

Data Processing:
- Handled missing values (? → cleaned)
- Converted data into numeric format
- Combined date and time into datetime
- Created features:
  - Hour
  - Day
  - Month

---

## 🤖 Model

- Used Random Forest Regressor
- Predicts electricity consumption and cost
- Trained using time-based and electrical features

---

## 🧪 Simulation

The system allows users to test:
- Reduce electricity usage
- Shift usage to cheaper (night) hours

Outputs:
- Original cost
- Optimized cost
- Total savings

---

## 🖥 UI Dashboard

Built using Streamlit

User can:
- Adjust usage reduction (%)
- Select time shift (day/night)
- View:
  - Cost comparison
  - Savings
  - Graphs
  - Smart insights

---

## ▶️ How to Run

Install dependencies:
pip install -r requirements.txt

Run backend:
python src/data_preprocessing.py
python src/usage_analyzer.py
python src/cost_predictor.py
python src/simulation_engine.py

Run UI:
streamlit run app/streamlit_app.py

# ⚡ Project3 – Smart Food Waste Reduction AI

---

## 🚀 Overview

This project is an AI-based system designed to reduce food waste in households, hostels, and mess environments using intelligent decision-making and optimization.

The system analyzes food inventory, predicts waste risk, and recommends optimal usage strategies.

It provides:

- 📊 Waste analysis of food items
- ⚠ Priority-based food usage recommendations
- 🍲 Smart meal planning suggestions
- 📉 Waste reduction simulation
- 🌍 Carbon emission reduction insights
- 🖥 Interactive UI dashboard (Streamlit)

---

## 💡 Features

- 📦 Inventory-based food tracking
- ⏳ Expiry-aware waste prediction
- 🧠 Waste Priority Score (custom model)
- ⚙ Optimization-based meal selection
- 🧪 Simulation (AI vs baseline comparison)
- 🌍 Carbon footprint estimation
- 📊 Graph-based analysis
- 🖥 User input support via UI

---

## 📁 Project Structure

food-waste-ai/
├── data/
│   ├── raw/
│   ├── processed/
│   └── external/
│
├── src/
│   ├── data_generation/
│   │   └── generate_dataset.py
│   │
│   ├── models/
│   │   └── waste_score_model.py
│   │
│   ├── optimization/
│   │   └── meal_optimizer.py
│   │
│   ├── simulation/
│   │   └── simulator.py
│
├── app/
│   └── streamlit_app.py
│
├── results/
│   ├── graphs/
│   └── metrics/
│
├── paper/
├── requirements.txt
└── README.md

---

## 📊 Dataset

### Synthetic Dataset (Generated)

Since real household-level food data is not publicly available, a synthetic dataset is created.

### Includes:

- User_ID
- Ingredient
- Category
- Quantity
- Purchase Date
- Expiry Date
- Consumption Status

### Data Generation Features:

- Realistic expiry modeling
- User behavior simulation (careful / average / wasteful)
- Time-based consumption patterns

---

## 🧠 Model (Core Innovation)

### Waste Priority Score

A novel scoring function is introduced:

Waste Score = (1 / Days_to_Expiry) × Quantity × Category Weight

### Category Weights:

- Meat → 1.5  
- Dairy → 1.3  
- Vegetables → 1.2  
- Fruits → 1.1  
- Grains → 0.8  

👉 This ensures high-risk items are prioritized.

---

## ⚙ Optimization

The system uses a **Greedy Optimization Algorithm**:

- Selects items with highest waste score
- Minimizes total waste
- Provides daily usage recommendations

---

## 🧪 Simulation

The system compares:

- ❌ Baseline (random consumption)
- ✅ AI-based optimization

### Outputs:

- Total waste
- Remaining waste
- Waste reduction %
- Efficiency gain
- Utilization rate
- 🌍 Carbon emissions saved

---

## 🌍 Carbon Impact

Environmental impact is calculated using:

CO₂ Saved = Waste Reduced × Emission Factor

Where:

- 1 Waste Unit ≈ 2.5 kg CO₂

---

## 📊 Results

| Metric | Without AI | With AI |
|------|-----------|--------|
| Waste Reduction | 50.76% | 71.85% |
| Remaining Waste | 2561.6 | 1464.3 |
| Efficiency Gain | — | ~21% |
| Carbon Saved | Lower | Higher |

👉 The AI system significantly improves waste reduction and sustainability.

---

## 🖥 UI Dashboard

Built using Streamlit

### Features:

- Add food items (user input)
- Real-time waste scoring
- Priority-based recommendations
- Metrics display:
  - Total waste
  - Average waste
  - Carbon impact
- Graph visualization

---

## ▶️ How to Run

### 1. Install dependencies

```bash
pip install -r requirements.txt
