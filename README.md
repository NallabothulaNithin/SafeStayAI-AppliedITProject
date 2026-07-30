Safe Stay AI

SafeStay AI is an AI-powered rental fraud detection system designed for students, immigrants, and apartment seekers to identify suspicious housing listings and avoid online rental scams.
> SafeStay AI is an AI-powered rental fraud detection system designed for students, immigrants, and apartment seekers to identify suspicious housing listings and avoid online rental scams.

## Team

| Role | Name |
|---|---|
| Product Owner | Nithin |
| Scrum Master | Madhav |
| Developer | Eshwar yadav jakkula |
| Developer | OM Kode|
| Developer | Danish |

## Project Overview

SafeStay AI is an AI-powered rental listing analysis system that helps identify statistically unusual rental listings.

The system compares a property's rent with similar properties in the same location using feature engineering and an Isolation Forest anomaly detection model.

Instead of directly predicting fraud, SafeStay AI highlights listings that significantly deviate from normal market behaviour, helping users make more informed rental decisions.

## Architecture

_Add your architecture diagram here (C4 Context or Container diagram). Update this as the project evolves._

              User
               │
               ▼
      React Frontend
               │
        HTTP Request
               │
               ▼
      FastAPI Backend
               │
     Feature Engineering
               │
     StandardScaler
               │
     Isolation Forest
               │
               ▼
     Prediction Result
               │
               ▼
     Admin Dashboard

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Danish |
| Backend | Nithin Nallabothula and Eshwar |
| Documetation | Madhav |
| Deployment | Om Kode |

## Getting Started

### Prerequisites

- Python 3.10 or later
- Node.js 18 or later
- npm
- Git

### Run locally

# Clone repository
git clone https://github.com/NallabothulaNithin/SafeStayAI-AppliedITProject.git

cd SafeStayAI-AppliedITProject

# Install frontend dependencies
cd frontend
npm install

# Start React
npm run dev

# Start backend
cd ../backend
pip install -r requirements.txt
uvicorn main:app --reload

## Repository Structure

SafeStayAI-AppliedITProject/
```
│── backend/
│     ├── main.py
│     ├── requirements.txt
│
│── frontend/
│     ├── src/
│     ├── public/
│
│── data/
│     ├── raw/
│     ├── processed/
│
│── ml/
│     ├── prepare_data.py
│     ├── exploratory_analysis.py
│     ├── train_isolation_forest.py
│     ├── evaluate_isolation_forest.py
│
│── models/
│     ├── isolation_forest.pkl
│     ├── scaler.pkl
│
│── reports/
│     ├── EDA graphs
│     ├── Model evaluation
```

## Documentation

## Documentation

The project documentation includes:

- Project Overview
- System Architecture
- Dataset Description
- Data Cleaning
- Exploratory Data Analysis
- Feature Engineering
- Isolation Forest Model
- Model Evaluation

## License

For academic and educational purposes only.