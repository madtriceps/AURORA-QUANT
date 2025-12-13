"""Pytest configuration and fixtures."""
import pytest
from datetime import datetime
from core.ledger import PaperLedger
from core.types import MarketEvent


@pytest.fixture
def sample_ledger():
    """Create sample ledger for testing."""
    return PaperLedger(initial_capital=10000, strategy_id="test")


@pytest.fixture
def sample_market_events():
    """Create sample market events."""
    events = []
    prices = [100, 101, 102, 101, 100, 99, 100, 101, 102]
    
    for i, price in enumerate(prices):
        event = MarketEvent(
            timestamp=datetime(2024, 1, 1, 0, i),
            symbol="TEST",
            price=price,
            volume=1000,
        )
        events.append(event)
    
    return events


@pytest.fixture
def sample_candle():
    """Create sample OHLCV candle."""
    return {
        'timestamp': 1704067200000,
        'open': 100.0,
        'high': 102.5,
        'low': 99.5,
        'close': 101.0,
        'volume': 1000000,
    }
