# 📈 Real-Time Stock Price Prediction

## 🚀 Overview
The **Real-Time Stock Price Prediction** project is a full-stack application that fetches real-time stock market data, applies **Machine Learning (ML) models** to predict stock prices, and visualizes the results using an interactive web dashboard. The system leverages **FastAPI (Python)** for the backend and **React.js** for the frontend.

---

## 📌 Features
- ✅ **Fetches real-time stock market data** using **Yahoo Finance API** (`yfinance`).
- ✅ **Predicts stock prices** using **Linear Regression (LR) and Random Forest (RF)** models.
- ✅ **Visualizes actual vs. predicted stock prices** using **Chart.js**.
- ✅ **Fully containerized deployment** using **Docker & Docker Compose**.
- ✅ **Deployed on Azure** for live access.

---

## 🏗 Project Structure
```
📦 real-time-price-prediction
 ┣ 📂 backend
 ┃ ┣ 📂 models              # Pre-trained ML models
 ┃ ┣ 📂 services            # Prediction & ML training scripts
 ┃ ┣ 📂 data                # Stock market historical data (CSV files)
 ┃ ┣ 📜 main.py             # FastAPI Backend Server
 ┃ ┣ 📜 prediction.py       # Real-time prediction logic
 ┃ ┣ 📜 lr_model.py         # Linear Regression Model
 ┃ ┣ 📜 rf_model.py         # Random Forest Model
 ┣ 📂 frontend
 ┃ ┣ 📂 src
 ┃ ┃ ┣ 📂 components        # Reusable React components
 ┃ ┃ ┣ 📂 pages             # Page structure for React app
 ┃ ┃ ┣ 📜 App.js            # Main React app
 ┃ ┃ ┣ 📜 StockChart.js     # Chart.js visualization
 ┣ 📜 docker-compose.yml   # Docker multi-container setup
 ┣ 📜 README.md            # Documentation
```

---

## 🔧 Tech Stack
### **📍 Backend (FastAPI & ML)**
- Python 3.10
- FastAPI
- scikit-learn (Machine Learning)
- yfinance (Stock Market Data)
- Uvicorn (ASGI Server)

### **📍 Frontend (React.js & Chart.js)**
- React.js
- Chart.js (Data Visualization)
- Axios (API Calls)

### **📍 Deployment & DevOps**
- Docker & Docker Compose
- Azure Web App for Containers
- Azure Container Registry (ACR)

---

## ⚙️ Setup & Installation
### **1️⃣ Clone the Repository**
```bash
git clone https://github.com/YOUR_USERNAME/real-time-price-prediction.git
cd real-time-price-prediction
```

### **2️⃣ Run with Docker Compose**
```bash
docker-compose up --build
```

### **3️⃣ Access the App**
- **Frontend:** `http://localhost:3000`
- **Backend API:** `http://localhost:8000/predict/AAPL`
- **Swagger Docs:** `http://localhost:8000/docs`

---

## 🏗 Deployment on Azure
### **Deploy Using Docker & ACR**
```bash
az webapp create --resource-group myResourceGroup --plan myPlan --name stock-prediction-app --multicontainer-config-type compose --multicontainer-config-file docker-compose.yml
```

---

## 🎯 Future Improvements
- 🛠 Add **Deep Learning Models** for better predictions.
- 📊 Enhance UI with **more analytics & stock insights**.
- 📡 Support **WebSockets** for real-time data streaming.

---

## 🤝 Contributing
1. Fork the repository.
2. Create a feature branch (`git checkout -b feature-name`).
3. Commit changes (`git commit -m 'Add new feature'`).
4. Push to GitHub (`git push origin feature-name`).
5. Open a Pull Request.

---

## 📜 License
This project is **open-source** under the **MIT License**.

---

## 📞 Contact
**Developer:** Mohammed Shehab

**Email:** shihab@live.cn

**GitHub:** [github.com/m12shehab](https://github.com/m12shehab)

