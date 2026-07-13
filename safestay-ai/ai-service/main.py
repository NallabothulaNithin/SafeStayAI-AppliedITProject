from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib

# Load trained model
model = joblib.load("fraud_model.pkl")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Listing(BaseModel):
    title:str
    rent:int
    deposit:int
    description:str


@app.post("/predict")
def predict(data: Listing):

    ratio = round(data.deposit / max(data.rent, 1), 2)

    text = (
        f"Title: {data.title} "
        f"Rent: {data.rent} "
        f"Deposit: {data.deposit} "
        f"Ratio: {ratio} "
        f"Description: {data.description}"
    )

    probability = model.predict_proba([text])[0][1]
    fraudScore = int(probability * 100)

    # Rule-based scoring

    if data.deposit > data.rent * 3:
        fraudScore += 25

    if data.rent < 400:
        fraudScore += 10

    keywords = [
        "deposit first",
        "transfer",
        "western union",
        "crypto",
        "urgent",
        "landlord abroad",
        "whatsapp",
        "no viewing",
        "pay before viewing",
        "advance payment"
    ]

    full_text = (data.title + " " + data.description).lower()

    for word in keywords:
        if word in full_text:
            fraudScore += 10

    fraudScore = min(fraudScore, 100)

    if fraudScore >= 70:
        risk = "High Risk"
    elif fraudScore >= 40:
        risk = "Medium Risk"
    else:
        risk = "Low Risk"

    return {
        "fraudScore": fraudScore,
        "probability": f"{fraudScore}%",
        "risk": risk
    }