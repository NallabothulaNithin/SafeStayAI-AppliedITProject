from pathlib import Path

import json
import joblib
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

# ---------------------------------------------------------
# Project Paths
# ---------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_FILE = (
    BASE_DIR
    / "data"
    / "processed"
    / "rent_listings_cleaned.csv"
)

MODEL_DIR = BASE_DIR / "models"
MODEL_DIR.mkdir(exist_ok=True)

MODEL_FILE = MODEL_DIR / "isolation_forest.pkl"
SCALER_FILE = MODEL_DIR / "scaler.pkl"

# ---------------------------------------------------------
# Load Dataset
# ---------------------------------------------------------

print("Loading cleaned dataset...")

df = pd.read_csv(DATA_FILE)

print(f"Rows: {len(df)}")

# ---------------------------------------------------------
# Features for training
# ---------------------------------------------------------

features = [
    "price",
    "square_feet",
    "bedrooms",
    "bathrooms",
    "price_per_sqft",
    "rent_difference_from_median",
    "rent_to_local_median_ratio",
    "local_rent_zscore"
]

X = df[features]

# ---------------------------------------------------------
# Scale the data
# ---------------------------------------------------------

scaler = StandardScaler()

X_scaled = scaler.fit_transform(X)

# ---------------------------------------------------------
# Train Isolation Forest
# ---------------------------------------------------------

model = IsolationForest(
    n_estimators=200,
    contamination=0.05,
    random_state=42
)

print("Training model...")

model.fit(X_scaled)

print("Training completed.")

# ---------------------------------------------------------
# Predictions
# ---------------------------------------------------------

predictions = model.predict(X_scaled)

# Convert predictions
# 1  -> Normal
# -1 -> Unusual

df["prediction"] = predictions

df["prediction"] = df["prediction"].map({
    1: "Normal",
    -1: "Unusual"
})

normal = (df["prediction"] == "Normal").sum()
unusual = (df["prediction"] == "Unusual").sum()

print("\n========== Results ==========")

print(f"Normal Listings : {normal}")
print(f"Unusual Listings: {unusual}")

# ---------------------------------------------------------
# Save Model
# ---------------------------------------------------------

joblib.dump(model, MODEL_FILE)
joblib.dump(scaler, SCALER_FILE)

print("\nModel saved successfully.")
print(MODEL_FILE)

print("\nScaler saved successfully.")
print(SCALER_FILE)

# ---------------------------------------------------------
# Save local rental reference statistics
# ---------------------------------------------------------

CITY_STATISTICS_FILE = MODEL_DIR / "city_statistics.csv"
METADATA_FILE = MODEL_DIR / "model_metadata.json"

comparison_groups = [
    "cityname",
    "state",
    "bedrooms",
]

city_statistics = (
    df.groupby(comparison_groups)
    .agg(
        local_median_price=("price", "median"),
        local_mean_price=("price", "mean"),
        local_price_std=("price", "std"),
        comparison_group_size=("price", "count"),
    )
    .reset_index()
)

# Groups containing only one listing have no standard deviation.
city_statistics["local_price_std"] = (
    city_statistics["local_price_std"]
    .fillna(0)
)

city_statistics.to_csv(
    CITY_STATISTICS_FILE,
    index=False
)

model_metadata = {
    "features": features,
    "contamination": 0.05,
    "model_name": "Isolation Forest",
    "prediction_labels": {
        "1": "Normal",
        "-1": "Unusual"
    }
}

with open(METADATA_FILE, "w", encoding="utf-8") as file:
    json.dump(
        model_metadata,
        file,
        indent=4
    )

print("\nCity statistics saved successfully.")
print(CITY_STATISTICS_FILE)

print("\nModel metadata saved successfully.")
print(METADATA_FILE)

# ---------------------------------------------------------
# Save predictions
# ---------------------------------------------------------

OUTPUT = (
    BASE_DIR
    / "data"
    / "processed"
    / "rent_predictions.csv"
)

df.to_csv(
    OUTPUT,
    index=False
)

print("\nPrediction file saved.")
print(OUTPUT)