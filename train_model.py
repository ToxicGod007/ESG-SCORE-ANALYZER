import pandas as pd
import numpy as np
from sklearn.ensemble import GradientBoostingRegressor
import joblib

# --- 1. CONFIGURATION: INDIAN SECTORS ---
# 0: IT/Services (Low Energy)
# 1: Manufacturing/Auto (High Energy)
# 2: Retail/FMCG (Medium Energy)
# 3: Cement/Steel (Very High Energy)
# 4: Pharma/Chemicals (High Energy + Water)
SECTOR_MAP = {0: 0.2, 1: 2.5, 2: 0.8, 3: 5.0, 4: 3.0}

# --- 2. GENERATE SYNTHETIC DATA ---
np.random.seed(42)
n_samples = 5000 

data = {
    'revenue': np.random.randint(5000000, 1000000000, n_samples), # 50L to 100Cr
    'employees': np.random.randint(5, 2000, n_samples),
    'industry_type': np.random.choice(list(SECTOR_MAP.keys()), n_samples)
}

df = pd.DataFrame(data)

# --- 3. PHYSICS SIMULATION ---
def calculate_energy(row):
    sector_factor = SECTOR_MAP[row['industry_type']]
    # Base load from machines (Revenue) + People (Employees)
    revenue_load = (row['revenue'] * 0.0015 * sector_factor)
    employee_load = (row['employees'] * 1500) 
    noise = np.random.normal(0, revenue_load * 0.1) 
    return max(1000, revenue_load + employee_load + noise)

df['energy_usage'] = df.apply(calculate_energy, axis=1)

# --- 4. TRAIN MODEL ---
X = df[['revenue', 'employees', 'industry_type']]
y = df['energy_usage']

print(f"Training Gradient Boosting Model on {n_samples} companies...")
model = GradientBoostingRegressor(n_estimators=200, learning_rate=0.1, max_depth=3, random_state=42)
model.fit(X, y)

joblib.dump(model, 'esg_benchmark_model.pkl')
print("✅ Advanced AI Model saved as 'esg_benchmark_model.pkl'")