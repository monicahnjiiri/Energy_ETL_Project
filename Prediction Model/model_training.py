import pandas as pd
import joblib
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error
import numpy as np

# Load data
load = pd.read_csv("data/processed/germany_load.csv")

# Debug: Print columns to check for 'utc_timestamp'
print("Columns in CSV:", load.columns.tolist())
if 'timestamp' not in load.columns:
    raise KeyError("Column 'timestamp' not found in data/processed/germany_load.csv. Available columns: " + str(load.columns.tolist()))

# Preprocess
load["timestamp"] = pd.to_datetime(load["timestamp"])
load["hour"] = load["timestamp"].dt.hour
load["day"] = load["timestamp"].dt.day
load["month"] = load["timestamp"].dt.month
load["weekday"] = load["timestamp"].dt.weekday

# Drop nulls (if any)
load.dropna(subset=["DE_load_forecast_entsoe_transparency", "DE_load_actual_entsoe_transparency"], inplace=True)

# Define features and target
features = ["DE_load_forecast_entsoe_transparency", "hour", "day", "month", "weekday"]
target = "DE_load_actual_entsoe_transparency"

X = load[features]
y = load[target]

# Time-based train-test split
split_idx = int(len(load) * 0.8)
X_train, X_test = X[:split_idx], X[split_idx:]
y_train, y_test = y[:split_idx], y[split_idx:]

# Model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluation
y_pred = model.predict(X_test)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
mae = mean_absolute_error(y_test, y_pred)

print(f"📊 RMSE: {rmse:.2f}")
print(f"📊 MAE: {mae:.2f}")

# Save model
joblib.dump(model, "model.pkl")
print("✅ model.pkl saved.")
