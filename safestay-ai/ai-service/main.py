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

    text = f"Title: {data.title}" 
    f"Rent: {data.rent}" 
    f"Deposit: {data.deposit}"
    f"Description: {data.description}"

    prediction = model.predict([text])[0]

    probability = model.predict_proba([text])[0][1]
    fraudScore = int(probability * 100)

    if fraudScore >= 65:
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