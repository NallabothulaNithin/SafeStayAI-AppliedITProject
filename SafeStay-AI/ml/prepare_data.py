from pathlib import Path

import numpy as np
import pandas as pd

# Project paths

BASE_DIR = Path(__file__).resolve().parent.parent

RAW_DATA = (BASE_DIR / "data" / "raw" / "apartments_for_rent_classified_10K.csv")

PROCESSED_DATA = (BASE_DIR / "data" / "processed" / "rent_listings_cleaned.csv")

# Load the dataset

print("Loading dataset...")

df = pd.read_csv(RAW_DATA, sep=";", encoding="cp1252")

print("Dataset loaded successfully.")
print(f"Original rows: {len(df)}")
print(f"Original columns: {df.shape[1]}")

# Select useful columns

selected_columns = [
    "id",
    "category",
    "title",
    "body",
    "amenities",
    "bathrooms",
    "bedrooms",
    "has_photo",
    "pets_allowed",
    "price",
    "square_feet",
    "cityname",
    "state",
    "latitude",
    "longitude",
    "source",
]

df = df[selected_columns].copy()

# Remove duplicate listings

duplicate_count = df.duplicated(subset=["id"]).sum()

print(f"Duplicate IDs found: {duplicate_count}")

df = df.drop_duplicates(subset=["id"]).copy()

# Remove rows with missing essential location information

essential_columns = [
    "cityname",
    "state",
    "latitude",
    "longitude",
]

before_removing_missing_locations = len(df)

df = df.dropna(subset=essential_columns).copy()

removed_location_rows = (
    before_removing_missing_locations - len(df)
)

print(
    "Rows removed because of missing location data: "
    f"{removed_location_rows}"
)


# Handle missing numerical values

bathroom_median = df["bathrooms"].median()
bedroom_median = df["bedrooms"].median()

df["bathrooms"] = df["bathrooms"].fillna(bathroom_median)
df["bedrooms"] = df["bedrooms"].fillna(bedroom_median)

print(
    f"Missing bathrooms filled with median: "
    f"{bathroom_median}"
)

print(
    f"Missing bedrooms filled with median: "
    f"{bedroom_median}"
)


# Handle missing categorical values

df["amenities"] = df["amenities"].fillna("Unknown")
df["pets_allowed"] = df["pets_allowed"].fillna("Unknown")


# Clean text columns
df["title"] = df["title"].fillna("").str.strip()
df["body"] = df["body"].fillna("").str.strip()

df["cityname"] = df["cityname"].str.strip()
df["state"] = df["state"].str.strip()


# ---------------------------------------------------------
# Remove invalid numerical records
# ---------------------------------------------------------

before_invalid_removal = len(df)

df = df[
    (df["price"] > 0)
    & (df["square_feet"] > 0)
    & (df["bedrooms"] >= 0)
    & (df["bathrooms"] >= 0)
].copy()

invalid_rows_removed = before_invalid_removal - len(df)

print(f"Invalid numerical rows removed: {invalid_rows_removed}")


# ---------------------------------------------------------
# Feature engineering
# ---------------------------------------------------------

# Rent relative to property size
df["price_per_sqft"] = (
    df["price"] / df["square_feet"]
)

# Text-length features
df["title_length"] = df["title"].str.len()
df["description_length"] = df["body"].str.len()

# Group comparable properties by city and bedroom count
comparison_groups = [
    "cityname",
    "state",
    "bedrooms",
]

# Number of comparable listings in each group
df["comparison_group_size"] = (
    df.groupby(comparison_groups)["price"]
    .transform("count")
)

# Median rent for comparable properties
df["local_median_price"] = (
    df.groupby(comparison_groups)["price"]
    .transform("median")
)

# Mean rent for comparable properties
df["local_mean_price"] = (
    df.groupby(comparison_groups)["price"]
    .transform("mean")
)

# Standard deviation for comparable properties
df["local_price_std"] = (
    df.groupby(comparison_groups)["price"]
    .transform("std")
)

# Difference from the local median
df["rent_difference_from_median"] = (
    df["price"] - df["local_median_price"]
)

# Ratio compared with the local median
df["rent_to_local_median_ratio"] = (
    df["price"] / df["local_median_price"]
)

# Percentage difference from the local median
df["rent_percentage_difference"] = (
    (
        df["price"] - df["local_median_price"]
    )
    / df["local_median_price"]
) * 100

# Z-score within comparable listings
df["local_rent_zscore"] = (
    (
        df["price"] - df["local_mean_price"]
    )
    / df["local_price_std"]
)

# Some groups contain only one listing, so their
# standard deviation and z-score will be missing.
df["local_price_std"] = (
    df["local_price_std"].fillna(0)
)

df["local_rent_zscore"] = (
    df["local_rent_zscore"]
    .replace([np.inf, -np.inf], np.nan)
    .fillna(0)
)


# ---------------------------------------------------------
# Create robust IQR statistics
# ---------------------------------------------------------

df["local_q1_price"] = (
    df.groupby(comparison_groups)["price"]
    .transform(lambda values: values.quantile(0.25))
)

df["local_q3_price"] = (
    df.groupby(comparison_groups)["price"]
    .transform(lambda values: values.quantile(0.75))
)

df["local_price_iqr"] = (
    df["local_q3_price"] - df["local_q1_price"]
)

df["lower_iqr_boundary"] = (
    df["local_q1_price"]
    - 1.5 * df["local_price_iqr"]
)

df["upper_iqr_boundary"] = (
    df["local_q3_price"]
    + 1.5 * df["local_price_iqr"]
)

# This is a statistical reference flag.
# It is not a final fraud prediction.
df["statistical_outlier"] = (
    (df["price"] < df["lower_iqr_boundary"])
    | (df["price"] > df["upper_iqr_boundary"])
).astype(int)


# ---------------------------------------------------------
# Save the cleaned dataset
# ---------------------------------------------------------

PROCESSED_DATA.parent.mkdir(
    parents=True,
    exist_ok=True
)

df.to_csv(
    PROCESSED_DATA,
    index=False
)


# ---------------------------------------------------------
# Final summary
# ---------------------------------------------------------

print("\n========== Cleaning Complete ==========")
print(f"Cleaned rows: {len(df)}")
print(f"Cleaned columns: {df.shape[1]}")

print(
    "Statistical outliers found: "
    f"{df['statistical_outlier'].sum()}"
)

print(
    "Median monthly rent: "
    f"${df['price'].median():,.2f}"
)

print(
    "Median price per square foot: "
    f"${df['price_per_sqft'].median():,.2f}"
)

print(
    "Processed dataset saved to:"
)

print(PROCESSED_DATA)