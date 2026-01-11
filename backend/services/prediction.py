"""
The prediction service module for making stock price predictions
using real-time data and trained models.
Author: Mohammed Shehab
"""
import joblib
import numpy as np
import yfinance as yf

# Load trained models & scaler
lr_model = joblib.load("./models/lr_all_model.pkl")
rf_model = joblib.load("./models/rf_all_model.pkl")
xgb_model = joblib.load("./models/xgb_all_model.pkl")
scaler = joblib.load("./models/all_scaler.pkl")

def get_real_time_stock_data(ticker="AAPL"):
    """Fetch latest stock data"""
    try:
        stock = yf.Ticker(ticker)
        # Fetch slightly more data to ensure we have valid points
        hist = stock.history(period="5d", interval="1m")
        
        if hist.empty or len(hist) < 2:
            # Try appending .NS if it might be an Indian stock and failed
            if not ticker.endswith(".NS") and not ticker.endswith(".BO"):
                 print(f"Initial fetch failed for {ticker}, checking if it needs suffix...")
                 return None 
            print(f"No sufficient data available for {ticker}")
            return None

        latest_data = hist.iloc[-1]
        previous_data = hist.iloc[-2]

        # Compute log return
        log_return = np.log(latest_data["Close"] / previous_data["Close"])

        return {
            "open": latest_data["Open"],
            "high": latest_data["High"],
            "low": latest_data["Low"],
            "close": latest_data["Close"],
            "volume": latest_data["Volume"],
            "log_return": log_return
        }
    except Exception as e:
        print(f"Error fetching data for {ticker}: {e}")
        return None

def get_historical_data(ticker="AAPL", period="1mo"):
    """Fetch historical stock data"""
    try:
        stock = yf.Ticker(ticker)
        # Valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
        hist = stock.history(period=period)
        
        if hist.empty:
            return {"error": "No historical data found"}
            
        # Format data for frontend
        dates = hist.index.strftime('%Y-%m-%d').tolist()
        prices = hist['Close'].tolist()
        
        return {
            "dates": dates,
            "prices": prices,
            "symbol": ticker
        }
    except Exception as e:
        return {"error": str(e)}

def predict_price(ticker="AAPL"):
    """Make a prediction using real-time data"""
    stock_data = get_real_time_stock_data(ticker)
    
    if stock_data is None:
        return {"error": f"No real-time data available for {ticker}. Try adding .NS for Indian stocks (e.g. RELIANCE.NS)"}

    # Ensure volume is not zero (to prevent division errors)
    if stock_data["volume"] == 0:
        stock_data["volume"] = 1  # Set a small nonzero value

    # Prepare features for prediction
    features = np.array([
        stock_data["volume"],
        stock_data["log_return"],  # Using log return instead of price change
        stock_data["close"] - stock_data["low"],  # Price momentum
        stock_data["high"] - stock_data["low"],  # Volatility
        stock_data["close"] - stock_data["open"]  # Spread
    ]).reshape(1, -1)

    # Ensure features match the scaler
    features_scaled = scaler.transform(features)

def determine_recommendation(current_price, predictions):
    """
    Analyze predictions to determine Buy/Sell/Hold signal
    Returns: { "signal": "BUY", "confidence": 85 }
    """
    avg_pred = np.mean(list(predictions.values()))
    diff_percent = ((avg_pred - current_price) / current_price) * 100
    
    # Count how many models predict increase
    votes_up = sum(1 for p in predictions.values() if p > current_price)
    votes_down = sum(1 for p in predictions.values() if p < current_price)
    
    signal = "HOLD"
    confidence = 50
    
    if diff_percent > 0.5 and votes_up >= 2:
        signal = "BUY"
        # Confidence increases with magnitude of predicted gain
        confidence = 60 + min(votes_up * 10, 30) + min(diff_percent * 10, 10)
        
        if diff_percent > 2.0 and votes_up == 3:
            signal = "STRONG BUY"
            confidence = 90 + min(diff_percent, 10)
            
    elif diff_percent < -0.5 and votes_down >= 2:
        signal = "SELL"
        confidence = 60 + min(votes_down * 10, 30) + min(abs(diff_percent) * 10, 10)
        
        if diff_percent < -2.0 and votes_down == 3:
            signal = "STRONG SELL"
            confidence = 90 + min(abs(diff_percent), 10)
            
    return {
        "signal": signal,
        "confidence": round(min(confidence, 99), 1)  # Cap at 99%
    }

def predict_price(ticker="AAPL"):
    """Make a prediction using real-time data"""
    stock_data = get_real_time_stock_data(ticker)
    
    if stock_data is None:
        return {"error": f"No real-time data available for {ticker}. Try adding .NS for Indian stocks (e.g. RELIANCE.NS)"}

    # Ensure volume is not zero (to prevent division errors)
    if stock_data["volume"] == 0:
        stock_data["volume"] = 1  # Set a small nonzero value

    # Prepare features for prediction
    features = np.array([
        stock_data["volume"],
        stock_data["log_return"],  # Using log return instead of price change
        stock_data["close"] - stock_data["low"],  # Price momentum
        stock_data["high"] - stock_data["low"],  # Volatility
        stock_data["close"] - stock_data["open"]  # Spread
    ]).reshape(1, -1)

    # Ensure features match the scaler
    features_scaled = scaler.transform(features)

    # Make predictions
    lr_pred_scaled = lr_model.predict(features_scaled)[0]
    rf_pred_scaled = rf_model.predict(features_scaled)[0]
    xgb_pred_scaled = xgb_model.predict(features_scaled)[0]

    # Convert log return prediction back to actual price
    predicted_close_lr = stock_data["close"] * np.exp(lr_pred_scaled)
    predicted_close_rf = stock_data["close"] * np.exp(rf_pred_scaled)
    predicted_close_xgb = stock_data["close"] * np.exp(xgb_pred_scaled)

    predictions = {
        "linear_regression": round(predicted_close_lr, 2),
        "random_forest": round(predicted_close_rf, 2),
        "xgboost": round(predicted_close_xgb, 2)
    }

    # Calculate recommendation
    recommendation = determine_recommendation(stock_data["close"], predictions)

    return {
        "real_time_data": stock_data,  # Keeps the real closing price format
        "predictions": predictions,
        "recommendation": recommendation
    }

# API Endpoint
def get_prediction(ticker: str):
    """API endpoint to fetch real-time data & predict stock price"""
    return predict_price(ticker)
