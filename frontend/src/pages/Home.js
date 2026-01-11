import React, { useState } from "react";
import StockChart from "../components/StockChart";
import "../App.css";

const Home = () => {
    const [ticker, setTicker] = useState("AAPL");
    const [searchInput, setSearchInput] = useState("");

    // Categorized popular stocks
    const stockCategories = {
        "Indian Market 🇮🇳 (NSE/BSE)": [
            { symbol: "RELIANCE.NS", name: "Reliance Industries", icon: "🛢️" },
            { symbol: "TCS.NS", name: "TCS", icon: "👨‍💻" },
            { symbol: "HDFCBANK.NS", name: "HDFC Bank", icon: "🏦" },
            { symbol: "ICICIBANK.NS", name: "ICICI Bank", icon: "🏦" },
            { symbol: "INFY.NS", name: "Infosys", icon: "💻" },
            { symbol: "SBIN.NS", name: "SBI", icon: "🏛️" },
            { symbol: "BHARTIARTL.NS", name: "Bharti Airtel", icon: "📱" },
            { symbol: "ITC.NS", name: "ITC", icon: "🚬" },
            { symbol: "TATAMOTORS.NS", name: "Tata Motors", icon: "🚗" },
            { symbol: "LICI.NS", name: "LIC India", icon: "🛡️" },
            { symbol: "ADANIENT.NS", name: "Adani Enterprises", icon: "🏗️" },
            { symbol: "WAAREERTL.BO", name: "Waaree Renewables", icon: "☀️" },
            { symbol: "ZOMATO.NS", name: "Zomato", icon: "🍕" },
            { symbol: "PAYTM.NS", name: "Paytm", icon: "💳" },
        ],
        "US Market 🇺🇸": [
            { symbol: "AAPL", name: "Apple", icon: "🍎" },
            { symbol: "MSFT", name: "Microsoft", icon: "💻" },
            { symbol: "GOOGL", name: "Google", icon: "🔍" },
            { symbol: "AMZN", name: "Amazon", icon: "📦" },
            { symbol: "TSLA", name: "Tesla", icon: "⚡" },
            { symbol: "NVDA", name: "NVIDIA", icon: "🎮" },
            { symbol: "META", name: "Meta", icon: "📘" },
            { symbol: "NFLX", name: "Netflix", icon: "🎬" },
        ],
        "Crypto 🪙": [
            { symbol: "BTC-USD", name: "Bitcoin", icon: "₿" },
            { symbol: "ETH-USD", name: "Ethereum", icon: "Ξ" },
            { symbol: "DOGE-USD", name: "Dogecoin", icon: "🐕" },
        ]
    };

    const handleSearch = () => {
        if (searchInput.trim()) {
            setTicker(searchInput.toUpperCase().trim());
            setSearchInput("");
        }
    };

    const handleKeyPress = (e) => {
        if (e.key === 'Enter') {
            handleSearch();
        }
    };

    const selectStock = (symbol) => {
        setTicker(symbol);
    };

    return (
        <div className="App">
            {/* Professional Header */}
            <header className="app-header">
                <h1>📈 Real-Time Stock Price Prediction</h1>
                <p>Track any stock from any exchange with AI-powered predictions!</p>
            </header>

            {/* Stock Search Section */}
            <div className="stock-selector">
                <div className="search-container">
                    <label>Search Any Stock:</label>
                    <div className="search-input-group">
                        <input
                            type="text"
                            className="stock-search-input"
                            placeholder="e.g. RELIANCE.NS, TATASTEEL.NS, AAPL"
                            value={searchInput}
                            onChange={(e) => setSearchInput(e.target.value)}
                            onKeyPress={handleKeyPress}
                        />
                        <button className="search-button" onClick={handleSearch}>
                            🔍 Search
                        </button>
                    </div>
                    <p className="search-hint">
                        ℹ️ <strong>For Indian Stocks:</strong> Add <code>.NS</code> for NSE or <code>.BO</code> for BSE<br />
                        (e.g., <code>SBIN.NS</code>, <code>TCS.BO</code>)
                    </p>
                    <p className="current-ticker">Currently viewing: <strong>{ticker}</strong></p>
                </div>

                {/* Popular Stocks Dropdown */}
                <div className="popular-stocks">
                    <h3>Popular Stocks - Quick Select</h3>
                    <div className="dropdown-container">
                        <select
                            className="popular-stock-select"
                            onChange={(e) => {
                                if (e.target.value) selectStock(e.target.value);
                            }}
                            defaultValue=""
                        >
                            <option value="" disabled>Select a market leader...</option>

                            {Object.entries(stockCategories).map(([category, stocks]) => (
                                <optgroup key={category} label={category}>
                                    {stocks.map((stock) => (
                                        <option key={stock.symbol} value={stock.symbol}>
                                            {stock.icon} {stock.name} ({stock.symbol})
                                        </option>
                                    ))}
                                </optgroup>
                            ))}
                        </select>
                    </div>
                </div>

                <p className="exchange-info">
                    💡 <strong>Tip:</strong> If a stock is not found (e.g. Indian stocks), try adding the exchange suffix like <code>.NS</code> (NSE) or <code>.BO</code> (BSE). Example: <code>TATASTEEL.NS</code> or <code>RELIANCE.BO</code>
                </p>
            </div>

            {/* Stock Chart Component */}
            <StockChart ticker={ticker} />

            {/* About Section */}
            <section className="glass-card">
                <h2>About the Developer</h2>

                <p>
                    Hi, I'm <b>Pranav Bomdica</b>, a student at <b>Vishwa Vishwani Institute of Systems and Management</b> pursuing <b>BS MS</b> degree.
                    This is my <b>4th year mini project</b> focused on real-time stock price prediction using machine learning and AI techniques.
                </p>

                <h3>🎓 Project Overview</h3>
                <p>
                    This project demonstrates the application of <b>Machine Learning</b> algorithms to predict stock prices in real-time.
                    It combines modern web technologies with powerful AI models to create an interactive and educational tool for understanding
                    stock market predictions.
                </p>

                <h3>🔹 Technologies Used</h3>
                <ul>
                    <li>
                        <b>Frontend</b> – React.js with modern CSS (glassmorphism, animations)
                    </li>
                    <li>
                        <b>Backend</b> – Python FastAPI for RESTful API
                    </li>
                    <li>
                        <b>Machine Learning</b> – Linear Regression, Random Forest, XGBoost
                    </li>
                    <li>
                        <b>Data Source</b> – Yahoo Finance API (yfinance) for real-time stock data
                    </li>
                    <li>
                        <b>Data Visualization</b> – Chart.js for interactive charts
                    </li>
                    <li>
                        <b>Deployment</b> – Docker containers for easy deployment
                    </li>
                </ul>

                <h3>🚀 Key Features</h3>
                <ul>
                    <li>Real-time stock data fetching from any stock exchange</li>
                    <li>Three different ML models for price prediction comparison</li>
                    <li>Interactive charts showing actual vs predicted prices</li>
                    <li>Error rate visualization for model performance analysis</li>
                    <li>Modern, responsive UI with smooth animations</li>
                    <li>Support for international stock exchanges</li>
                </ul>

                <h3>📚 Academic Context</h3>
                <p>
                    <b>Institution:</b> Vishwa Vishwani Institute of Systems and Management<br />
                    <b>Program:</b> BS MS<br />
                    <b>Year:</b> 4th Year<br />
                    <b>Project Type:</b> Mini Project<br />
                    <b>Focus Area:</b> Machine Learning & Financial Technology
                </p>

                <p className="disclaimer">
                    ⚠️ <b>Disclaimer:</b> This project is for educational purposes only.
                    The predictions shown should not be used for actual trading decisions.
                </p>
            </section>

            {/* Footer */}
            <footer className="app-footer">
                &copy; {new Date().getFullYear()} Pranav Bomdica - Vishwa Vishwani Institute of Systems and Management. All Rights Reserved.
            </footer>
        </div>
    );
};

export default Home;
