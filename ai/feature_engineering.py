"""Feature extraction for ML models."""
from typing import Dict, List
import numpy as np


class FeatureEngineer:
    """Extract ML features from trading data."""
    
    @staticmethod
    def extract_ohlc_features(candle: Dict) -> Dict[str, float]:
        """Extract OHLC-based features."""
        o = candle.get('open', 0)
        h = candle.get('high', 0)
        l = candle.get('low', 0)
        c = candle.get('close', 0)
        
        return {
            'body_size': abs(c - o) / o if o > 0 else 0,
            'upper_wick': (h - max(o, c)) / o if o > 0 else 0,
            'lower_wick': (min(o, c) - l) / o if o > 0 else 0,
            'close_position': (c - l) / (h - l) if (h - l) > 0 else 0.5,
        }
    
    @staticmethod
    def extract_momentum_features(candle: Dict) -> Dict[str, float]:
        """Extract momentum indicator features."""
        return {
            'rsi_normalized': candle.get('rsi', 50) / 100,
            'macd_positive': 1.0 if candle.get('macd', 0) > 0 else 0.0,
            'volume_ratio': min(candle.get('volume', 0) / candle.get('avg_volume', 1), 5.0),
        }
    
    @staticmethod
    def extract_trend_features(candle: Dict) -> Dict[str, float]:
        """Extract trend-based features."""
        return {
            'ema_alignment': 1.0 if candle.get('ema_20', 0) > candle.get('ema_50', 0) else 0.0,
            'price_position': (candle.get('close', 0) - candle.get('ema_50', 0)) / candle.get('ema_50', 1) if candle.get('ema_50', 0) > 0 else 0,
            'atr_ratio': candle.get('atr', 0) / candle.get('close', 1) if candle.get('close', 0) > 0 else 0,
        }
    
    @staticmethod
    def create_feature_vector(candle: Dict) -> List[float]:
        """Create complete feature vector."""
        ohlc = FeatureEngineer.extract_ohlc_features(candle)
        momentum = FeatureEngineer.extract_momentum_features(candle)
        trend = FeatureEngineer.extract_trend_features(candle)
        
        return list(ohlc.values()) + list(momentum.values()) + list(trend.values())
