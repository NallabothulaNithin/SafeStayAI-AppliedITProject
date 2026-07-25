from pathlib import Path
from typing import List

import joblib
import numpy as np
import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field


# ---------------------------------------------------------
# Project paths
# ---------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_FILE = BASE_DIR / "models" / "isolation_forest.pkl"
SCALER_FILE = BASE_DIR / "models" / "scaler.pkl"
STATISTICS_FILE = BASE_DIR / "models" / "city_statistics.csv"


# ---------------------------------------------------------
# Verify required files
# ---------------------------------------------------------

required_files = [
    MODEL_FILE,
    SCALER_FILE,
    STATISTICS_FILE,
]

for file_path in required_files:
    if not file_path.exists():
        raise FileNotFoundError(
            f"Required file was not found: {file_path}"
        )


# ---------------------------------------------------------
# Load trained objects
# ---------------------------------------------------------

model = joblib.load(MODEL_FILE)
scaler = joblib.load(SCALER_FILE)

city_statistics = pd.read_csv(STATISTICS_FILE)

city_statistics["cityname"] = (
    city_statistics["cityname"]
    .astype(str)
    .str.strip()
    .str.lower()
)

city_statistics["state"] = (
    city_statistics["state"]
    .astype(str)
    .str.strip()
    .str.lower()
)


# ---------------------------------------------------------
# FastAPI application
# ---------------------------------------------------------

app = FastAPI(
    title="SafeStay AI API",
    description=(
        "Detects unusual rental listings using an "
        "Isolation Forest anomaly detection model."
    ),
    version="1.0.0",
)


# ---------------------------------------------------------
# CORS configuration
# ---------------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------
# Request and response models
# ---------------------------------------------------------

class RentalListingRequest(BaseModel):
    city: str = Field(
        ...,
        min_length=1,
        examples=["Dallas"],
    )

    state: str = Field(
        ...,
        min_length=1,
        examples=["TX"],
    )

    bedrooms: float = Field(
        ...,
        ge=0,
        le=20,
        examples=[2],
    )

    bathrooms: float = Field(
        ...,
        ge=0,
        le=20,
        examples=[1],
    )

    square_feet: float = Field(
        ...,
        gt=0,
        le=100000,
        examples=[900],
    )

    price: float = Field(
        ...,
        gt=0,
        le=1000000,
        examples=[1500],
    )


class RentalPredictionResponse(BaseModel):
    prediction: str
    review_recommendation: str
    anomaly_score: float
    city: str
    state: str
    bedrooms: float
    comparison_group_size: int
    local_median_price: float
    local_mean_price: float
    price_per_sqft: float
    rent_difference_from_median: float
    rent_percentage_difference: float
    reasons: List[str]
    disclaimer: str


# ---------------------------------------------------------
# Health endpoint
# ---------------------------------------------------------

@app.get("/")
def root():
    return {
        "message": "SafeStay AI API is running.",
        "model": "Isolation Forest",
        "status": "healthy",
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "model_loaded": True,
        "statistics_loaded": True,
    }


# ---------------------------------------------------------
# Find local reference statistics
# ---------------------------------------------------------

def find_reference_statistics(
    city: str,
    state: str,
    bedrooms: float,
) -> dict:
    cleaned_city = city.strip().lower()
    cleaned_state = state.strip().lower()

    exact_match = city_statistics[
        (city_statistics["cityname"] == cleaned_city)
        & (city_statistics["state"] == cleaned_state)
        & (
            np.isclose(
                city_statistics["bedrooms"],
                bedrooms,
            )
        )
    ]

    if not exact_match.empty:
        row = exact_match.iloc[0]

        return {
            "local_median_price": float(
                row["local_median_price"]
            ),
            "local_mean_price": float(
                row["local_mean_price"]
            ),
            "local_price_std": float(
                row["local_price_std"]
            ),
            "comparison_group_size": int(
                row["comparison_group_size"]
            ),
            "reference_level": "city, state and bedrooms",
        }

    city_match = city_statistics[
        (city_statistics["cityname"] == cleaned_city)
        & (city_statistics["state"] == cleaned_state)
    ]

    if not city_match.empty:
        weighted_count = city_match[
            "comparison_group_size"
        ].sum()

        weighted_mean = np.average(
            city_match["local_mean_price"],
            weights=city_match["comparison_group_size"],
        )

        weighted_median = np.average(
            city_match["local_median_price"],
            weights=city_match["comparison_group_size"],
        )

        positive_std = city_match[
            city_match["local_price_std"] > 0
        ]

        if not positive_std.empty:
            local_std = np.average(
                positive_std["local_price_std"],
                weights=positive_std[
                    "comparison_group_size"
                ],
            )
        else:
            local_std = 0

        return {
            "local_median_price": float(
                weighted_median
            ),
            "local_mean_price": float(
                weighted_mean
            ),
            "local_price_std": float(local_std),
            "comparison_group_size": int(
                weighted_count
            ),
            "reference_level": "city and state",
        }

    global_median = float(
        np.average(
            city_statistics["local_median_price"],
            weights=city_statistics[
                "comparison_group_size"
            ],
        )
    )

    global_mean = float(
        np.average(
            city_statistics["local_mean_price"],
            weights=city_statistics[
                "comparison_group_size"
            ],
        )
    )

    positive_global_std = city_statistics[
        city_statistics["local_price_std"] > 0
    ]

    if not positive_global_std.empty:
        global_std = float(
            np.average(
                positive_global_std[
                    "local_price_std"
                ],
                weights=positive_global_std[
                    "comparison_group_size"
                ],
            )
        )
    else:
        global_std = 0

    return {
        "local_median_price": global_median,
        "local_mean_price": global_mean,
        "local_price_std": global_std,
        "comparison_group_size": int(
            city_statistics[
                "comparison_group_size"
            ].sum()
        ),
        "reference_level": "global fallback",
    }


# ---------------------------------------------------------
# Explanation generation
# ---------------------------------------------------------

def create_reasons(
    price: float,
    price_per_sqft: float,
    rent_percentage_difference: float,
    local_rent_zscore: float,
    reference_level: str,
) -> List[str]:
    reasons = []

    if rent_percentage_difference >= 50:
        reasons.append(
            "The rent is more than 50% above the "
            "reference median."
        )
    elif rent_percentage_difference >= 20:
        reasons.append(
            "The rent is moderately above the "
            "reference median."
        )
    elif rent_percentage_difference <= -40:
        reasons.append(
            "The rent is substantially below the "
            "reference median."
        )
    else:
        reasons.append(
            "The rent is relatively close to the "
            "reference median."
        )

    if price_per_sqft >= 3:
        reasons.append(
            "The price per square foot is high "
            "relative to typical listings."
        )
    elif price_per_sqft <= 0.5:
        reasons.append(
            "The price per square foot is unusually low."
        )
    else:
        reasons.append(
            "The price per square foot is within "
            "a common range."
        )

    if abs(local_rent_zscore) >= 2:
        reasons.append(
            "The rent is more than two standard "
            "deviations from the reference mean."
        )
    elif abs(local_rent_zscore) >= 1:
        reasons.append(
            "The rent shows a noticeable deviation "
            "from comparable listings."
        )

    reasons.append(
        f"The comparison used the {reference_level} "
        "reference group."
    )

    return reasons


# ---------------------------------------------------------
# Prediction endpoint
# ---------------------------------------------------------

@app.post(
    "/predict",
    response_model=RentalPredictionResponse,
)
def predict_listing(
    listing: RentalListingRequest,
):
    try:
        reference = find_reference_statistics(
            city=listing.city,
            state=listing.state,
            bedrooms=listing.bedrooms,
        )

        local_median = reference[
            "local_median_price"
        ]

        local_mean = reference[
            "local_mean_price"
        ]

        local_std = reference[
            "local_price_std"
        ]

        price_per_sqft = (
            listing.price / listing.square_feet
        )

        rent_difference = (
            listing.price - local_median
        )

        if local_median > 0:
            rent_to_median_ratio = (
                listing.price / local_median
            )

            rent_percentage_difference = (
                rent_difference / local_median
            ) * 100
        else:
            rent_to_median_ratio = 1.0
            rent_percentage_difference = 0.0

        if local_std > 0:
            local_rent_zscore = (
                listing.price - local_mean
            ) / local_std
        else:
            local_rent_zscore = 0.0

        feature_values = pd.DataFrame(
            [
                {
                    "price": listing.price,
                    "square_feet": listing.square_feet,
                    "bedrooms": listing.bedrooms,
                    "bathrooms": listing.bathrooms,
                    "price_per_sqft": price_per_sqft,
                    "rent_difference_from_median": (
                        rent_difference
                    ),
                    "rent_to_local_median_ratio": (
                        rent_to_median_ratio
                    ),
                    "local_rent_zscore": (
                        local_rent_zscore
                    ),
                }
            ]
        )

        scaled_features = scaler.transform(
            feature_values
        )

        raw_prediction = int(
            model.predict(scaled_features)[0]
        )

        decision_score = float(
            model.decision_function(
                scaled_features
            )[0]
        )

        anomaly_score = round(
            max(0.0, -decision_score),
            4,
        )

        if raw_prediction == -1:
            prediction = "Unusual"
            review_recommendation = (
                "Review this listing carefully before "
                "making any payment or commitment."
            )
        else:
            prediction = "Normal"
            review_recommendation = (
                "The listing follows patterns learned "
                "from the reference dataset."
            )

        reasons = create_reasons(
            price=listing.price,
            price_per_sqft=price_per_sqft,
            rent_percentage_difference=(
                rent_percentage_difference
            ),
            local_rent_zscore=local_rent_zscore,
            reference_level=reference[
                "reference_level"
            ],
        )

        return RentalPredictionResponse(
            prediction=prediction,
            review_recommendation=(
                review_recommendation
            ),
            anomaly_score=anomaly_score,
            city=listing.city,
            state=listing.state,
            bedrooms=listing.bedrooms,
            comparison_group_size=reference[
                "comparison_group_size"
            ],
            local_median_price=round(
                local_median,
                2,
            ),
            local_mean_price=round(
                local_mean,
                2,
            ),
            price_per_sqft=round(
                price_per_sqft,
                2,
            ),
            rent_difference_from_median=round(
                rent_difference,
                2,
            ),
            rent_percentage_difference=round(
                rent_percentage_difference,
                2,
            ),
            reasons=reasons,
            disclaimer=(
                "This result identifies statistical "
                "anomalies. It does not prove that a "
                "listing is fraudulent."
            ),
        )

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Prediction failed: {error}",
        ) from error