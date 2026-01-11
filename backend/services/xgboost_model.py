"""XGBoost Time Series Model for Stock Price Prediction
This script trains an XGBoost model using TimeSeriesSplit for better time series validation.
Author: Mohammed Shehab
"""
import numpy as np
import ta
import pandas as pd
import joblib
import os
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
import xgboost as xgb
from sklearn.model_selection import TimeSeriesSplit

# Todo: update this code before deployment
# Define directories for models and data in cloud
models_dir = "./models"
data_dir = "./data"
# # for local testing
# models_dir = "backend/models"
# data_dir = "backend/data"

features = ["Volume", "price_change", "momentum", "volatility", "spread"]
target = "log_return" #"Close"

def preprocess_stock_data(df):
    """Preprocess stock data and create new features"""
    df.set_index("Date", inplace=True)

    # Feature Engineering
    df["price_change"] = (df["Close"] - df["Open"]) / df["Open"]
    df["momentum"] = df["Close"].pct_change()
    df["volatility"] = df["Close"].rolling(5).std()
    df["spread"] = df["High"] - df["Low"]
    df["log_return"] = np.log(df["Close"] / df["Close"].shift(5))  # Log return
    # Fill missing values
    df.fillna(0, inplace=True)

    return df

def preprocess_stock_data_advanced(df):
    """Preprocess stock data and create new features"""
    df.set_index("Date", inplace=True)

    # Feature Engineering
    df["price_change"] = (df["Close"] - df["Open"]) / df["Open"]
    df["momentum"] = df["Close"].pct_change()
    df["volatility"] = df["Close"].rolling(5).std()
    df["spread"] = df["High"] - df["Low"]
    df["log_return"] = np.log(df["Close"] / df["Close"].shift(1))  # Target variable

    # Simple Moving Averages (SMA)
    df["SMA_10"] = ta.trend.SMAIndicator(df["Close"], window=10).sma_indicator()
    df["SMA_30"] = ta.trend.SMAIndicator(df["Close"], window=30).sma_indicator()

    # Relative Strength Index (RSI)
    df["RSI"] = ta.momentum.RSIIndicator(df["Close"], window=14).rsi()

    # MACD (Moving Average Convergence Divergence)
    macd = ta.trend.MACD(df["Close"], window_slow=26, window_fast=12, window_sign=9)
    df["MACD"] = macd.macd()
    df["MACD_Signal"] = macd.macd_signal()

    # Bollinger Bands
    bb = ta.volatility.BollingerBands(df["Close"], window=20, window_dev=2)
    df["BB_High"] = bb.bollinger_hband()
    df["BB_Low"] = bb.bollinger_lband()

    # Momentum Indicators
    df["ROC"] = ta.momentum.ROCIndicator(df["Close"], window=12).roc()  # Rate of Change

    # Trend Strength
    df["ADX"] = ta.trend.ADXIndicator(df["High"], df["Low"], df["Close"], window=14).adx()

    # Volatility
    df["ATR"] = ta.volatility.AverageTrueRange(df["High"], df["Low"], df["Close"], window=14).average_true_range()

    # # Technical Indicators
    # df["SMA_10"] = ta.SMA(df["Close"], timeperiod=10)
    # df["SMA_30"] = ta.SMA(df["Close"], timeperiod=30)
    # df["RSI"] = ta.RSI(df["Close"], timeperiod=14)
    # df["MACD"], _, _ = ta.MACD(df["Close"], fastperiod=12, slowperiod=26, signalperiod=9)
    
    df["log_return"] = np.log(df["Close"] / df["Close"].shift(5))  # Log return
    # Fill missing values
    df.fillna(method="ffill", inplace=True)
    df.dropna(inplace=True)
    


    return df


def load_stock_data(ticker="AAPL"):
    """Download historical stock data from Yahoo Finance"""
    file_path = f"{data_dir}/{ticker}_stock_data.csv"

    print(f"Loading {ticker} data from local CSV...")
    df = pd.read_csv(file_path, parse_dates=["Date"])

    return df

def make_plot(y_test, y_pred):
    """Plot actual vs predicted prices"""
    plt.figure(figsize=(10, 5))
    plt.plot(y_test.values, label="Actual Prices", color="blue", marker="o", linestyle="--")
    plt.plot(y_pred, label="Predicted Prices", color="red", marker="*", linestyle="-", alpha=0.5)
    plt.legend()
    plt.grid(axis="both")
    plt.title("Actual vs Predicted Stock Prices")
    plt.xlabel("Time")
    plt.ylabel("Price")
    plt.show()

def train_xgboost_with_timeseries_split(data, ticker, debug=False, n_splits=5):
    """Train an XGBoost model using TimeSeriesSplit"""

    data = data.sort_index(ascending=True)

    # Features & Target
    X = data[features]
    y = data[target]

    # Feature Scaling
    scaler = MinMaxScaler()
    X_scaled = scaler.fit_transform(X)

    # Save the scaler
    os.makedirs(models_dir, exist_ok=True)
    joblib.dump(scaler, f"{models_dir}/{ticker}_scaler.pkl")

    # Define TimeSeriesSplit
    tscv = TimeSeriesSplit(n_splits=n_splits)

    mse_scores = []

    for train_idx, test_idx in tscv.split(X_scaled):
        X_train, X_test = X_scaled[train_idx], X_scaled[test_idx]
        y_train, y_test = y.iloc[train_idx], y.iloc[test_idx]

        # Train the XGBoost Model
        model = xgb.XGBRegressor(objective="reg:squarederror",
                                 n_estimators=100,
                                 max_depth=6,
                                 learning_rate=0.51,
                                 subsample=0.5,  # Prevent overfitting
                                 colsample_bytree=0.8,  # Prevent overfitting
                                 random_state=42)
        
        model.fit(X_train, y_train)

        # Evaluate the model
        y_pred = model.predict(X_test)
        mse = mean_squared_error(y_test, y_pred)
        mse_scores.append(mse)
        print(f"Fold MSE: {mse:.2f}")

        if debug:
            make_plot(y_test, y_pred)

    print(f"Average MSE across {n_splits} folds: {sum(mse_scores) / len(mse_scores):.2f}")

    # Train on the full dataset
    print("Training final model on all data...")
    model.fit(X_scaled, y)
    print("Final model training complete!")

    # Save the model
    joblib.dump(model, f"{models_dir}/xgb_{ticker}_model.pkl")
    print("Final model saved!")

if __name__ == "__main__":
    tickers = ["AAPL", "MSFT", "GOOGL", "AMZN"]
    data_frames = [preprocess_stock_data(load_stock_data(ticker)) for ticker in tickers]
    
    all_data = pd.concat(data_frames).sort_values("Date", ascending=True)  # Fix time sorting
    
    train_xgboost_with_timeseries_split(all_data, "all", debug=False, n_splits=5)
