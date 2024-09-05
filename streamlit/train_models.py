import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import joblib
from datetime import datetime
from sklearn.preprocessing import StandardScaler

# Ensure the model directory exists
model_dir = "model"
if not os.path.exists(model_dir):
    os.makedirs(model_dir)

# Load the data from CSV
file_path = "sensor_data.csv"  # Replace with your actual file path
df = pd.read_csv(file_path, parse_dates=["Timestamp"])

# Sort by timestamp to maintain the time series order
df.sort_values(by="Timestamp", inplace=True)

# Create features for the next hour prediction
df["Hour"] = df["Timestamp"].dt.hour
df["Minute"] = df["Timestamp"].dt.minute
df["Second"] = df["Timestamp"].dt.second

# Shifting 'Power' by -1 to predict the next hour's power
df["Target_Power"] = df["Power"].shift(-4)  # Assuming data is at 15-minute intervals

# Drop the last rows with NaN values in 'Target_Power'
df.dropna(inplace=True)

# Feature selection
features = [
    "Voltage",
    "Current",
    "Energy",
    "Frequency",
    "PF",
    "Hour",
    "Minute",
    "Second",
]
X = df[features]
y = df["Target_Power"]

# Scale the features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Split the data into training and testing sets (80% train, 20% test)
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, shuffle=False
)

# Train the model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate the model
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
print(f"Mean Squared Error: {mse}")

# Save the model with a timestamp
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
model_filename = f"{model_dir}/power_prediction_model_{timestamp}.pkl"
joblib.dump(model, model_filename)
print(f"Model saved as {model_filename}")

# Save the scaler as well
scaler_filename = f"{model_dir}/scaler_{timestamp}.pkl"
joblib.dump(scaler, scaler_filename)
print(f"Scaler saved as {scaler_filename}")
