"""Linear Regression Model for Stock Price Prediction
This script trains a Linear model on historical stock data to predict future stock prices.
Author: Mohammed Shehab
"""
import numpy as np
import pandas as pd
import joblib
import os
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt

# Define directories for models and data
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

def load_stock_data(ticker="AAPL"):
    """Download historical stock data from Yahoo Finance"""
    file_path = f"{data_dir}/{ticker}_stock_data.csv"
    
    # if not os.path.exists(file_path):
    #     print(f"Downloading {ticker} stock data...")
    #     df = yf.download(ticker, start="2010-01-01", end="2024-01-01")
    #     os.makedirs(data_dir, exist_ok=True)
    #     df.to_csv(file_path)
    # else:
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

def training_testing(data, ticker, debug=False):
    """Train a Linear Regression model on stock data"""
    # Features & Target
    X = data[features]  # Excluding 'Close' as target
    y = data[target]  # 'Close' is the target

    # Train/Test Split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Feature Scaling
    if os.path.exists(f"{models_dir}/{ticker}_scaler.pkl"):
        print("Loading existing scaler...")
        scaler = joblib.load(f"{models_dir}/{ticker}_scaler.pkl")
    else:
        scaler = MinMaxScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Save the scaler
    os.makedirs(models_dir, exist_ok=True)
    joblib.dump(scaler, f"{models_dir}/{ticker}_scaler.pkl")

    # Train the model
    lr = LinearRegression()
    lr.fit(X_train_scaled, y_train)

    # Evaluate the model
    y_pred = lr.predict(X_test_scaled)

    # Calculate the Mean Squared Error
    mse = mean_squared_error(y_test, y_pred)
    print(f"Mean Squared Error for {ticker}: {mse:.2f}")
    print("Training model with all data...")
    lr.fit(scaler.transform(X), y)
    print("Model training complete!")
    print("Saving model...")
    # Save the model
    joblib.dump(lr, f"{models_dir}/lr_{ticker}_model.pkl")
    print("Model saved!")

    if debug:
        # Plot results
        make_plot(y_test, y_pred)

if __name__ == "__main__":
    # ticker = "AAPL"
    tickers = ["AAPL", "MSFT", "GOOGL", "AMZN"]
    data_frames = []
    for ticker in tickers:
        raw_data = load_stock_data(ticker)
        data_frames.append(raw_data)
    all_data = pd.concat(data_frames)
    processed_data = preprocess_stock_data(all_data)
    training_testing(processed_data, "all", debug=False)
