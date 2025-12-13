"""Test technical indicators."""
import pytest
from core.indicators import (
    calculate_ema, calculate_rsi, calculate_vwap,
    calculate_macd, calculate_atr, detect_volume_spike
)


def test_ema_calculation():
    """Test EMA calculation."""
    prices = [10, 11, 12, 13, 14, 15, 14, 13, 12, 11]
    ema = calculate_ema(prices, 3)
    assert len(ema) == len(prices)
    assert not all(v == v for v in ema)  # Should have some values


def test_rsi_calculation():
    """Test RSI calculation."""
    prices = [44, 44.34, 44.09, 43.61, 44.33, 44.83, 45.10, 45.42, 45.84, 46.08]
    rsi = calculate_rsi(prices, 5)
    assert len(rsi) == len(prices)
    # RSI should be between 0-100 where not NaN
    valid_rsi = [v for v in rsi if v == v]  # Remove NaN
    assert all(0 <= v <= 100 for v in valid_rsi)


def test_vwap_calculation():
    """Test VWAP calculation."""
    high = [10, 11, 12, 13, 14]
    low = [9, 10, 11, 12, 13]
    close = [9.5, 10.5, 11.5, 12.5, 13.5]
    volume = [1000, 1000, 1000, 1000, 1000]
    
    vwap = calculate_vwap(high, low, close, volume)
    assert len(vwap) == len(close)


def test_volume_spike_detection():
    """Test volume spike detection."""
    volumes = [1000] * 20 + [5000]  # Spike at end
    assert detect_volume_spike(volumes, period=20, threshold=2.0)
    
    volumes_normal = [1000] * 21
    assert not detect_volume_spike(volumes_normal, period=20, threshold=2.0)
