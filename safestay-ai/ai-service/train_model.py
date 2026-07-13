import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import joblib

# Load dataset
df = pd.read_csv("rental_fraud_dataset.csv")

# Create extra feature
df["ratio"] = (df["deposit"] / df["rent"]).round(2)

# Combine all features into one text field
df["combined"] = (
    "Title: " + df["title"].astype(str) + " " +
    "Rent: " + df["rent"].astype(str) + " " +
    "Deposit: " + df["deposit"].astype(str) + " " +
    "Ratio: " + df["ratio"].astype(str) + " " +
    "Description: " + df["description"].astype(str)
)

X = df["combined"]
y = df["label"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

model = Pipeline([
    ("tfidf", TfidfVectorizer(ngram_range=(1,2))),
    ("clf", LogisticRegression(max_iter=1000))
])

model.fit(X_train, y_train)

pred = model.predict(X_test)

print("Accuracy:", accuracy_score(y_test, pred))

joblib.dump(model, "fraud_model.pkl")

print("Model trained successfully")