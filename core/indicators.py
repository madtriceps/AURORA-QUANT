"""Professional technical indicators library."""
import numpy as np
from typing import List, Tuple, Optional


def calculate_ema(prices: List[float], period: int) -> List[float]:
    """Exponential Moving Average."""
    if len(prices) < period:
        return [np.nan] * len(prices)
    
    ema = [np.nan] * len(prices)
    multiplier = 2 / (period + 1)
    ema[period - 1] = np.mean(prices[:period])
    
    for i in range(period, len(prices)):
        ema[i] = prices[i] * multiplier + ema[i - 1] * (1 - multiplier)
    
    return ema


def calculate_rsi(prices: List[float], period: int = 14) -> List[float]:
    """Relative Strength Index."""
    if len(prices) < period + 1:
        return [np.nan] * len(prices)
    
    deltas = np.diff(prices)
    seed = deltas[:period + 1]
    up = seed[seed >= 0].sum() / period
    down = -seed[seed < 0].sum() / period
    
    rs = up / down if down != 0 else 0
    rsi = [np.nan] * period
    rsi.append(100 - 100 / (1 + rs))
    
    for i in range(period + 1, len(prices)):
        delta = deltas[i - 1]
        upval = delta if delta > 0 else 0.0
        downval = -delta if delta < 0 else 0.0
        
        up = (up * (period - 1) + upval) / period
        down = (down * (period - 1) + downval) / period
        
        rs = up / down if down != 0 else 0
        rsi.append(100 - 100 / (1 + rs))
    
    return rsi


def calculate_vwap(high: List[float], low: List[float],
                   close: List[float], volume: List[float]) -> List[float]:
    """Volume Weighted Average Price."""
    if len(close) != len(volume) or len(close) < 1:
        return [np.nan] * len(close)
    
    typical_price = [(h + l + c) / 3 for h, l, c in zip(high, low, close)]
    tp_vol = [tp * v for tp, v in zip(typical_price, volume)]
    
    cumsum_tpv = np.cumsum(tp_vol)
    cumsum_vol = np.cumsum(volume)
    
    vwap = [tpv / vol if vol != 0 else np.nan for tpv, vol in zip(cumsum_tpv, cumsum_vol)]
    return vwap


def calculate_macd(prices: List[float], fast: int = 12, 
                   slow: int = 26, signal: int = 9) -> Tuple[List[float], List[float]]:
    """MACD (Moving Average Convergence Divergence)."""
    ema_fast = calculate_ema(prices, fast)
    ema_slow = calculate_ema(prices, slow)
    
    macd_line = [f - s if not np.isnan(f) and not np.isnan(s) else np.nan 
                 for f, s in zip(ema_fast, ema_slow)]
    signal_line = calculate_ema(macd_line, signal)
    
    return macd_line, signal_line


def calculate_atr(high: List[float], low: List[float],
                  close: List[float], period: int = 14) -> List[float]:
    """Average True Range."""
    if len(high) < 2:
        return [np.nan] * len(high)
    
    tr_list = []
    for i in range(len(high)):
        if i == 0:
            tr = high[i] - low[i]
        else:
            tr = max(
                high[i] - low[i],
                abs(high[i] - close[i-1]),
                abs(low[i] - close[i-1])
            )
        tr_list.append(tr)
    
    atr = [np.nan] * (period - 1)
    atr.append(np.mean(tr_list[:period]))
    
    for i in range(period, len(tr_list)):
        atr.append((atr[-1] * (period - 1) + tr_list[i]) / period)
    
    return atr


def detect_volume_spike(volumes: List[float], period: int = 20,
                        threshold: float = 1.5) -> bool:
    """Detect abnormally high volume."""
    if len(volumes) < period:
        return False
    
    avg_volume = np.mean(volumes[-period:])
    recent_volume = volumes[-1]
    return recent_volume > avg_volume * threshold


def calculate_volatility(prices: List[float], period: int = 20) -> float:
    """Calculate historical volatility."""
    if len(prices) < period:
        return 0.0
    
    returns = np.diff(np.log(prices[-period:]))
    return float(np.std(returns) * np.sqrt(252) * 100)  # Annualized volatility %
