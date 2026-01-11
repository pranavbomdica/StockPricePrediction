"""Main FastAPI application.
    Author: Mohammed Shehab
"""
from fastapi import FastAPI
from services.prediction import get_prediction, get_historical_data
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional

# Initialize FastAPI
app = FastAPI()

# Enable CORS (Allow frontend requests)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Only allow frontend requests
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

@app.get("/")
def home():
    return {"message": "Welcome to the Stock Price Prediction API!",
            "Author": "Mohammed Shehab",
            "version":"1.0.0",
            "Github":"https://github.com/M12Shehab/real-time-price-prediction",
            "LinkedIn":"https://www.linkedin.com/in/mohammed-shehab/",
            "Note":"This API is for educational purposes only. Do not use this for real trading.",
            "Project Home page":"http://realtime-frontend.eastus.azurecontainer.io/"}

@app.get("/predict/{ticker}")
def predict_stock(ticker: str):
    """Fetch real-time stock data and make predictions."""
    return get_prediction(ticker)

@app.get("/history/{ticker}")
def stock_history(ticker: str, period: str = "1mo"):
    """Fetch historical stock data for charts (1mo, 6mo, 1y, 5y, max)"""
    return get_historical_data(ticker, period)