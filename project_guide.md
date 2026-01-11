# 📈 Real-Time Stock Price Prediction Project - Faculty Presentation Guide

**Project by**: Pranav Bomdica
**Institution**: Vishwa Vishwani Institute of Systems and Management
**Year**: 4th Year - Mini Project

---

## 1. Project Abstract
"This project is a real-time full-stack web application that predicts stock prices using Machine Learning. It fetches live market data from global exchanges (including NSE/BSE), processes it through three different AI models (Linear Regression, Random Forest, XGBoost), and visualizes the results on an interactive dashboard. The system also provides 'Buy/Sell' recommendations based on model consensus."

---

## 2. Technology Stack

### Frontend (User Interface)
- **Framework**: React.js (v18)
- **Styling**: Modern CSS3 with Glassmorphism & Animations
- **Charts**: Chart.js (react-chartjs-2)
- **Http Client**: Axios for API communication

### Backend (Server & ML)
- **Framework**: FastAPI (Python) - High performance, easy to use.
- **Machine Learning**: Scikit-Learn, XGBoost
- **Data Source**: Yahoo Finance API (`yfinance`) - For real-time and historical data.
- **Data Processing**: Pandas, NumPy

---

## 3. System Architecture

[User Browser]
      ⬇️ (HTTP Requests)
[React Frontend] (Port 3000)
      ⬇️ (API Calls via Axios)
[FastAPI Backend] (Port 8000)
      ⬇️ 1. Fetch Data
[Yahoo Finance API]
      ⬇️ 2. Process & Scale
[Preprocessing Module] (MinMaxScaler)
      ⬇️ 3. Predict
[ML Models] (Pre-trained .pkl files)
      ⬇️ 4. Return JSON
[Frontend Dashboard] -> Visualizes Chart & Recommendation

---

## 4. Machine Learning Models Used

We use an **Ensemble Approach**, comparing three models to ensure reliability:

### 1. Linear Regression (LR)
- **What it is**: The simplest model that fits a straight line through the data points.
- **Why used**: Good baseline for detecting general trends.
- **Pros**: Fast, interpretable.
- **Cons**: Can't capture complex non-linear patterns.

### 2. Random Forest Regressor (RF)
- **What it is**: A "forest" of many decision trees. output is the average of all trees.
- **Why used**: Handles non-linear data well and resists overfitting.
- **Pros**: Robust, accurate.

### 3. XGBoost (Extreme Gradient Boosting)
- **What it is**: An advanced gradient boosting algorithm widely used in competitions.
- **Why used**: Provides the highest accuracy by correcting errors of previous trees.
- **Pros**: High performance, state-of-the-art accuracy.

---

## 5. Key Features

1.  **Universal Search**: Supports any ticker from any exchange (e.g., `RELIANCE.NS` for NSE, `AAPL` for NASDAQ).
2.  **Real-Time Data**: Live updates every few seconds.
3.  **Historical Analysis**: View 1 Month, 1 Year, 5 Year price history.
4.  **AI Buy/Sell Engine**:
    - Analyzes predictions from all 3 models.
    - If Consensus > Current Price = **BUY** Signal.
    - If Consensus < Current Price = **SELL** Signal.
5.  **Interactive UI**: Modern glassmorphism design with responsive charts.

---

## 6. Viva Q&A (Be Prepared!)

**Q1: Why did you choose these specific algorithms?**
*Answer*: "I started with Linear Regression as a baseline. Then I added Random Forest to handle non-linear market volatility. Finally, XGBoost was added because it is currently the industry standard for tabular data prediction efficiency."

**Q2: How accurate is your model?**
*Answer*: "The accuracy varies by stock volatility. In testing, the models typically achieve a Mean Squared Error (MSE) low enough to predict trends, though exact price matching is difficult in volatile markets. I used an ensemble of 3 models to mitigate individual model errors."

**Q3: Where do you get the data?**
*Answer*: "I use the `yfinance` library which scrapes real-time data from Yahoo Finance. This allows me to access global markets including NSE and BSE without paying for expensive premium APIs."

**Q4: Is this system capable of automated trading?**
*Answer*: "Currently, it is a Decision Support System (DSS) meant to assist human traders. Automated trading would require integrating a brokerage API (like Zerodha Kite) and more rigorous backtesting."

**Q5: What challenges did you face?**
*Answer*: "Handling API limits and data latency from Yahoo Finance was a challenge. Also, ensuring the frontend updates smoothly without overwhelming the browser required optimizing the React state management."

---

## 7. How to Run (Demo)

1.  **Backend**:
    ```bash
    cd backend
    .venv\Scripts\activate
    python -m uvicorn main:app --reload
    ```
2.  **Frontend**:
    ```bash
    cd frontend
    npm start
    ```
3.  **Access**: Open `http://localhost:3000`

---
*Prepared for Pranav Bomdica - 4th Year Mini Project*
