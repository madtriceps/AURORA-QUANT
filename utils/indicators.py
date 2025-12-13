"""
Technical Indicators: VWAP, RSI, EMA, Volume Spike Detection
"""
import numpy as np
from typing import List, Tuple


def calculate_ema(prices: List[float], period: int) -> List[float]:
    """Exponential Moving Average."""
    if len(prices) < period:
        return prices
    
    ema = [np.nan] * len(prices)
    multiplier = 2 / (period + 1)
    ema[period - 1] = np.mean(prices[:period])
    
    for i in range(period, len(prices)):
        ema[i] = prices[i] * multiplier + ema[i - 1] * (1 - multiplier)
    
    return ema


def calculate_rsi(prices: List[float], period: int = 14) -> List[float]:
    """Relative Strength Index."""
    if len(prices) < period:
        return [np.nan] * len(prices)
    
    deltas = np.diff(prices)
    seed = deltas[:period + 1]
    up = seed[seed >= 0].sum() / period
    down = -seed[seed < 0].sum() / period
    
    rs = up / down if down != 0 else 0
    rsi = [np.nan] * (period)
    rsi.append(100 - 100 / (1 + rs))
    
    for i in range(period + 1, len(prices)):
        delta = deltas[i - 1]
        if delta > 0:
            upval = delta
            downval = 0.0
        else:
            upval = 0.0
            downval = -delta
        
        up = (up * (period - 1) + upval) / period
        down = (down * (period - 1) + downval) / period
        
        rs = up / down if down != 0 else 0
        rsi.append(100 - 100 / (1 + rs))
    
    return rsi


def calculate_vwap(high: List[float], low: List[float], 
                   close: List[float], volume: List[float]) -> List[float]:
    """Volume Weighted Average Price."""
    if len(close) != len(volume):
        return [np.nan] * len(close)
    
    typical_price = [(h + l + c) / 3 for h, l, c in zip(high, low, close)]
    tp_vol = [tp * v for tp, v in zip(typical_price, volume)]
    
    cumsum_tpv = np.cumsum(tp_vol)
    cumsum_vol = np.cumsum(volume)
    
    vwap = [tpv / vol if vol != 0 else np.nan for tpv, vol in zip(cumsum_tpv, cumsum_vol)]
    return vwap


def detect_volume_spike(volumes: List[float], period: int = 20, 
                        threshold: float = 1.5) -> bool:
    """Detect if recent volume is abnormally high."""
    if len(volumes) < period:
        return False
    
    avg_volume = np.mean(volumes[-period:])
    recent_volume = volumes[-1]
    return recent_volume > avg_volume * threshold


def calculate_pivot_points(high: float, low: float, close: float) -> dict:
    """Calculate daily pivot points."""
    pivot = (high + low + close) / 3
    r1 = (2 * pivot) - low
    r2 = pivot + (high - low)
    s1 = (2 * pivot) - high
    s2 = pivot - (high - low)
    return {
        'pivot': pivot,
        'r1': r1, 'r2': r2,
        's1': s1, 's2': s2,
    }
