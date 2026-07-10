import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import joblib

# load dataset

df = pd.read_csv("rental_fraud_dataset.csv")

# feature

df["combined"] = (
    "Title:" + df["title"].astype(str) +
    "Rent:" + df["rent"].astype(str) +
    "Deposit:" + df["deposit"].astype(str) + 
    "Description:" + df["description"].astype(str)
)
X = df["combined"]

# label

y = df["label"]

# split dataset

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# pipeline

model = Pipeline([
    ("tfidf", TfidfVectorizer()),
    ("clf", LogisticRegression())
])

# train model

model.fit(X_train, y_train)

# prediction

predictions = model.predict(X_test)

print("Accuracy:", accuracy_score(y_test, predictions))

# save model

joblib.dump(model, "fraud_model.pkl")

print("Model trained successfully")