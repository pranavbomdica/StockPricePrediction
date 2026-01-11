import React from "react";
import "../App.css";

const RecommendationCard = ({ recommendation }) => {
    if (!recommendation) return null;

    const { signal, confidence } = recommendation;

    let colorClass = "neutral";
    let icon = "⚖️";

    if (signal === "STRONG BUY") {
        colorClass = "strong-buy";
        icon = "🚀";
    } else if (signal === "BUY") {
        colorClass = "buy";
        icon = "✅";
    } else if (signal === "STRONG SELL") {
        colorClass = "strong-sell";
        icon = "⚠️";
    } else if (signal === "SELL") {
        colorClass = "sell";
        icon = "🔻";
    }

    return (
        <div className={`recommendation-card ${colorClass}`}>
            <div className="card-header">
                <h3>AI Recommendation</h3>
                <span className="ai-badge">AI Powered</span>
            </div>

            <div className="signal-content">
                <div className="signal-icon">{icon}</div>
                <div className="signal-text">
                    <h2>{signal}</h2>
                    <p>Based on ML Model Consensus</p>
                </div>
            </div>

            <div className="confidence-meter">
                <div className="meter-label">
                    <span>Confidence Score</span>
                    <strong>{confidence}%</strong>
                </div>
                <div className="meter-bar-bg">
                    <div
                        className="meter-bar-fill"
                        style={{ width: `${confidence}%` }}
                    ></div>
                </div>
            </div>
        </div>
    );
};

export default RecommendationCard;
