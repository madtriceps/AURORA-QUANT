"""Lightweight ML-based signal scoring."""
import numpy as np
from typing import List, Dict
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier


class SignalScorer:
    """ML-based buy/sell signal confidence scoring."""
    
    def __init__(self, model_type: str = "logistic"):
        self.model_type = model_type
        self.model = None
        self.scaler = StandardScaler()
        self.is_trained = False
        self.feature_names = [
            'price_above_vwap', 'ema20_above_ema50', 'rsi_oversold',
            'volume_spike', 'atr_expansion', 'macd_positive'
        ]

    def extract_features(self, candle: Dict) -> List[float]:
        """Extract features from candle data."""
        features = [
            1.0 if candle.get('close', 0) > candle.get('vwap', 0) else 0.0,
            1.0 if candle.get('ema_20', 0) > candle.get('ema_50', 0) else 0.0,
            1.0 if candle.get('rsi', 50) < 30 else 0.0,
            1.0 if candle.get('volume', 0) > candle.get('avg_volume', 0) * 1.5 else 0.0,
            1.0 if candle.get('atr', 0) > candle.get('avg_atr', 0) else 0.0,
            1.0 if candle.get('macd', 0) > 0 else 0.0,
        ]
        return features

    def train(self, X: List[List[float]], y: List[int]) -> None:
        """Train the model."""
        X_scaled = self.scaler.fit_transform(X)
        
        if self.model_type == "logistic":
            self.model = LogisticRegression(max_iter=1000)
        else:  # random_forest
            self.model = RandomForestClassifier(n_estimators=50, random_state=42)
        
        self.model.fit(X_scaled, y)
        self.is_trained = True

    def score_signal(self, candle: Dict) -> float:
        """Score signal confidence 0.0-1.0."""
        if not self.is_trained:
            return 0.5
        
        features = self.extract_features(candle)
        X_scaled = self.scaler.transform([features])
        
        if self.model_type == "logistic":
            prob = self.model.predict_proba(X_scaled)[0][1]
        else:
            prob = self.model.predict_proba(X_scaled)[0][1]
        
        return float(prob)
