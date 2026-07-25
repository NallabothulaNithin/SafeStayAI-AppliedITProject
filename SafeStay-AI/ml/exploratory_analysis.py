from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

# --------------------------------------------------
# Paths
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

DATA = BASE_DIR / "data" / "processed" / "rent_listings_cleaned.csv"

FIGURES = BASE_DIR / "reports" / "figures"
FIGURES.mkdir(parents=True, exist_ok=True)

# --------------------------------------------------
# Load dataset
# --------------------------------------------------

df = pd.read_csv(DATA)

print(f"Rows: {len(df)}")
print(f"Columns: {len(df.columns)}")

# --------------------------------------------------
# Helper function
# --------------------------------------------------

def save_plot(filename):
    plt.tight_layout()
    plt.savefig(FIGURES / filename, dpi=300)
    plt.close()

# --------------------------------------------------
# 1 Rent Distribution
# --------------------------------------------------

plt.figure(figsize=(10,6))
plt.hist(df["price"], bins=60)
plt.title("Monthly Rent Distribution")
plt.xlabel("Monthly Rent")
plt.ylabel("Frequency")
save_plot("01_rent_distribution.png")

# --------------------------------------------------
# 2 Price Per Sq Ft
# --------------------------------------------------

plt.figure(figsize=(10,6))
plt.hist(df["price_per_sqft"], bins=60)
plt.title("Price Per Square Foot")
plt.xlabel("Price per Square Foot")
plt.ylabel("Frequency")
save_plot("02_price_per_sqft.png")

# --------------------------------------------------
# 3 Bedrooms
# --------------------------------------------------

plt.figure(figsize=(8,5))
df["bedrooms"].value_counts().sort_index().plot(kind="bar")
plt.title("Bedroom Distribution")
plt.xlabel("Bedrooms")
plt.ylabel("Listings")
save_plot("03_bedrooms.png")

# --------------------------------------------------
# 4 Bathrooms
# --------------------------------------------------

plt.figure(figsize=(8,5))
df["bathrooms"].value_counts().sort_index().plot(kind="bar")
plt.title("Bathroom Distribution")
plt.xlabel("Bathrooms")
plt.ylabel("Listings")
save_plot("04_bathrooms.png")

# --------------------------------------------------
# 5 Scatter
# --------------------------------------------------

plt.figure(figsize=(10,6))
plt.scatter(
    df["square_feet"],
    df["price"],
    alpha=0.3,
    s=8
)

plt.title("Price vs Square Feet")
plt.xlabel("Square Feet")
plt.ylabel("Price")
save_plot("05_price_vs_sqft.png")

# --------------------------------------------------
# 6 Local Median Comparison
# --------------------------------------------------

plt.figure(figsize=(10,6))

plt.scatter(
    df["local_median_price"],
    df["price"],
    alpha=0.25,
    s=8
)

plt.title("Actual Price vs Local Median")
plt.xlabel("Local Median Price")
plt.ylabel("Actual Price")
save_plot("06_local_median.png")

# --------------------------------------------------
# 7 Top Cities
# --------------------------------------------------

plt.figure(figsize=(12,6))

(
    df["cityname"]
    .value_counts()
    .head(15)
    .plot(kind="bar")
)

plt.title("Top 15 Cities")
plt.xlabel("City")
plt.ylabel("Listings")

save_plot("07_top_cities.png")

# --------------------------------------------------
# 8 Highest Median Rent Cities
# --------------------------------------------------

city_price = (
    df.groupby("cityname")["price"]
    .median()
    .sort_values(ascending=False)
    .head(10)
)

plt.figure(figsize=(12,6))
city_price.plot(kind="bar")

plt.title("Cities with Highest Median Rent")
plt.ylabel("Median Rent")

save_plot("08_highest_rent_cities.png")

# --------------------------------------------------
# 9 Outliers
# --------------------------------------------------

plt.figure(figsize=(10,6))

normal = df[df["statistical_outlier"] == 0]
outlier = df[df["statistical_outlier"] == 1]

plt.scatter(
    normal["square_feet"],
    normal["price"],
    alpha=0.25,
    s=8,
    label="Normal"
)

plt.scatter(
    outlier["square_feet"],
    outlier["price"],
    s=20,
    label="Outlier"
)

plt.legend()

plt.title("Statistical Outliers")
plt.xlabel("Square Feet")
plt.ylabel("Price")

save_plot("09_outliers.png")

# --------------------------------------------------
# 10 Z Score
# --------------------------------------------------

plt.figure(figsize=(10,6))

plt.hist(
    df["local_rent_zscore"],
    bins=60
)

plt.title("Local Rent Z-Score")
plt.xlabel("Z Score")
plt.ylabel("Frequency")

save_plot("10_zscore.png")

# --------------------------------------------------
# 11 Boxplot
# --------------------------------------------------

plt.figure(figsize=(8,6))

plt.boxplot(df["price"], vert=True)

plt.title("Price Boxplot")

save_plot("11_boxplot.png")

# --------------------------------------------------
# 12 Comparison Group Size
# --------------------------------------------------

plt.figure(figsize=(10,6))

plt.hist(
    df["comparison_group_size"],
    bins=40
)

plt.title("Comparable Listings per Group")
plt.xlabel("Group Size")
plt.ylabel("Frequency")

save_plot("12_group_size.png")

print("\nEDA completed successfully.")
print(f"Figures saved in:\n{FIGURES}")