from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

# ---------------------------------------------------------
# Paths
# ---------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_FILE = (BASE_DIR / "data" / "processed" / "rent_predictions.csv")

OUTPUT_DIR = (BASE_DIR / "reports" / "evaluation")

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------
# Load predictions
# ---------------------------------------------------------

df = pd.read_csv(DATA_FILE)

print("Prediction file loaded.")
print(f"Rows: {len(df)}")

# ---------------------------------------------------------
# Summary
# ---------------------------------------------------------

summary = df["prediction"].value_counts()

print("\nPrediction Summary")
print(summary)

summary.to_csv(
    OUTPUT_DIR / "prediction_summary.csv"
)

# ---------------------------------------------------------
# Average statistics
# ---------------------------------------------------------

comparison = (
    df.groupby("prediction")[
        [
            "price",
            "square_feet",
            "price_per_sqft",
            "rent_difference_from_median",
            "local_rent_zscore"
        ]
    ]
    .mean()
)

print("\nAverage Feature Values")
print(comparison)

comparison.to_csv(
    OUTPUT_DIR / "average_features.csv"
)

# ---------------------------------------------------------
# Scatter Plot
# ---------------------------------------------------------

plt.figure(figsize=(10,6))

normal = df[df["prediction"] == "Normal"]
unusual = df[df["prediction"] == "Unusual"]

plt.scatter(
    normal["square_feet"],
    normal["price"],
    alpha=0.3,
    s=8,
    label="Normal"
)

plt.scatter(
    unusual["square_feet"],
    unusual["price"],
    s=18,
    label="Unusual"
)

plt.xlabel("Square Feet")
plt.ylabel("Monthly Rent")
plt.title("Isolation Forest Predictions")

plt.legend()

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "prediction_scatter.png",
    dpi=300
)

plt.close()

# ---------------------------------------------------------
# Save unusual listings
# ---------------------------------------------------------

unusual.to_csv(
    OUTPUT_DIR / "unusual_listings.csv",
    index=False
)

print("\nEvaluation completed.")

print(f"\nResults saved to:\n{OUTPUT_DIR}")