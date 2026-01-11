import React, { useEffect, useState, useRef } from "react";
import axios from "axios";
import { Line } from "react-chartjs-2";
import RecommendationCard from "./RecommendationCard";
import "../styles.css";
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend
} from "chart.js";

// Register Chart.js components
ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend);

const StockChart = ({ ticker }) => {
    const [chartData, setChartData] = useState({ labels: [], datasets: [] });
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [timeRange, setTimeRange] = useState("1d"); // 1d = Live, others = History
    const [recommendation, setRecommendation] = useState(null);

    // Store live data history to build the chart over time
    const liveDataRef = useRef({ labels: [], prices: [], lr: [], rf: [], xgb: [] });
    const intervalRef = useRef(null);

    const API_URL = process.env.REACT_APP_BACKEND_URL || "http://localhost:8000";

    const ranges = [
        { label: "Live", value: "1d" },
        { label: "1 Month", value: "1mo" },
        { label: "6 Months", value: "6mo" },
        { label: "1 Year", value: "1y" },
        { label: "5 Years", value: "5y" },
        { label: "Max", value: "max" }
    ];

    // Reset live data when ticker changes
    useEffect(() => {
        liveDataRef.current = { labels: [], prices: [], lr: [], rf: [], xgb: [] };
        setChartData({ labels: [], datasets: [] });
        setRecommendation(null);
    }, [ticker]);

    useEffect(() => {
        let isMounted = true;
        setLoading(true);
        setError(null);

        const fetchHistoricalData = async () => {
            try {
                if (timeRange === "1d") return; // Handled by live fetcher

                console.log(`Fetching historical data for ${ticker} (${timeRange})...`);
                const response = await axios.get(`${API_URL}/history/${ticker}?period=${timeRange}`);

                if (response.data.error) {
                    setError(response.data.error);
                    setLoading(false);
                    return;
                }

                if (isMounted) {
                    const { dates, prices } = response.data;

                    setChartData({
                        labels: dates,
                        datasets: [
                            {
                                label: "Close Price",
                                data: prices,
                                borderColor: "#6366f1",
                                backgroundColor: "rgba(99, 102, 241, 0.1)",
                                borderWidth: 2,
                                fill: true,
                                tension: 0.1,
                                pointRadius: prices.length > 100 ? 0 : 2, // Hide points for large datasets
                                pointHoverRadius: 4
                            }
                        ]
                    });
                    setLoading(false);
                }
            } catch (err) {
                console.error("Error fetching historical data:", err);
                setError("Failed to load historical data.");
                setLoading(false);
            }
        };

        const fetchLiveData = async () => {
            try {
                if (timeRange !== "1d") return; // Only for Live mode

                const response = await axios.get(`${API_URL}/predict/${ticker}`);

                if (response.data.error) {
                    setError(response.data.error);
                    setLoading(false);
                    return;
                }

                const data = response.data;
                const timestamp = new Date().toLocaleTimeString();
                const actualClose = data.real_time_data.close;
                const predictions = data.predictions;

                if (isMounted) setRecommendation(data.recommendation);

                // Update refs
                const current = liveDataRef.current;
                current.labels.push(timestamp);
                current.prices.push(actualClose);
                current.lr.push(predictions.linear_regression);
                current.rf.push(predictions.random_forest);
                current.xgb.push(predictions.xgboost);

                // Keep last 50 points
                if (current.labels.length > 50) {
                    current.labels.shift();
                    current.prices.shift();
                    current.lr.shift();
                    current.rf.shift();
                    current.xgb.shift();
                }

                if (isMounted) {
                    setChartData({
                        labels: [...current.labels],
                        datasets: [
                            {
                                label: "Actual Price",
                                data: [...current.prices],
                                borderColor: "#fbbf24",
                                borderWidth: 3,
                                fill: false
                            },
                            {
                                label: "Linear Regression",
                                data: [...current.lr],
                                borderColor: "#ef4444",
                                borderWidth: 2,
                                borderDash: [5, 5]
                            },
                            {
                                label: "Random Forest",
                                data: [...current.rf],
                                borderColor: "#3b82f6",
                                borderWidth: 2,
                                borderDash: [5, 5]
                            },
                            {
                                label: "XGBoost",
                                data: [...current.xgb],
                                borderColor: "#10b981",
                                borderWidth: 2,
                                borderDash: [5, 5]
                            }
                        ]
                    });
                    setLoading(false);
                }
            } catch (err) {
                console.error("Error fetching live data:", err);
                setError("Failed to load live data. Ensure backend is running.");
                setLoading(false);
            }
        };

        // Clear existing interval
        if (intervalRef.current) clearInterval(intervalRef.current);

        if (timeRange === "1d") {
            fetchLiveData();
            intervalRef.current = setInterval(fetchLiveData, 5000);
        } else {
            fetchHistoricalData();
        }

        return () => {
            isMounted = false;
            if (intervalRef.current) clearInterval(intervalRef.current);
        };
    }, [ticker, timeRange, API_URL]);

    const options = {
        responsive: true,
        maintainAspectRatio: false,
        interaction: {
            mode: 'index',
            intersect: false,
        },
        scales: {
            x: {
                ticks: {
                    autoSkip: true,
                    maxTicksLimit: 8,
                    color: 'rgba(255, 255, 255, 0.7)'
                },
                grid: { color: 'rgba(255, 255, 255, 0.1)' }
            },
            y: {
                ticks: { color: 'rgba(255, 255, 255, 0.7)' },
                grid: { color: 'rgba(255, 255, 255, 0.1)' }
            }
        },
        plugins: {
            legend: {
                labels: { color: 'white', font: { family: 'Inter' } }
            },
            tooltip: {
                backgroundColor: 'rgba(0,0,0,0.8)',
                titleColor: '#fff',
                bodyColor: '#fff',
                borderColor: 'rgba(255,255,255,0.2)',
                borderWidth: 1
            }
        }
    };

    return (
        <div className="chart-container">
            <div className="chart-header">
                <h2>{ticker} Stock Price</h2>
                <div className="time-range-selector">
                    {ranges.map((range) => (
                        <button
                            key={range.value}
                            className={`range-button ${timeRange === range.value ? 'active' : ''}`}
                            onClick={() => setTimeRange(range.value)}
                        >
                            {range.label}
                        </button>
                    ))}
                </div>
            </div>

            {error && (
                <div className="error-message">
                    {error}
                </div>
            )}

            {loading ? (
                <div className="loading-container">
                    <div className="spinner"></div>
                    <p className="loading-text">Loading market data...</p>
                </div>
            ) : (
                <div className="chart-wrapper">
                    {chartData.labels.length > 0 ? (
                        <Line data={chartData} options={options} />
                    ) : (
                        !error && <div className="no-data">No data available to display.</div>
                    )}
                </div>
            )}

            {/* Show AI Recommendation only in Live Mode */}
            {timeRange === "1d" && !loading && !error && (
                <RecommendationCard recommendation={recommendation} />
            )}
        </div>
    );
};

export default StockChart;
