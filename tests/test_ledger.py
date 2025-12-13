"""Test paper trading ledger."""
import pytest
from datetime import datetime
from core.ledger import PaperLedger, Trade


def test_ledger_initialization():
    """Test ledger setup."""
    ledger = PaperLedger(initial_capital=10000)
    assert ledger.equity == 10000
    assert ledger.cash == 10000
    assert ledger.total_pnl == 0


def test_open_position():
    """Test opening a position."""
    ledger = PaperLedger(initial_capital=10000)
    now = datetime.now()
    
    trade = ledger.open_position(
        symbol="BTC",
        side="BUY",
        price=50000,
        quantity=0.1,
        timestamp=now
    )
    
    assert trade.status == "OPEN"
    assert ledger.cash == 10000 - (50000 * 0.1)
    assert "BTC" in ledger.open_positions


def test_close_position():
    """Test closing a position."""
    ledger = PaperLedger(initial_capital=10000)
    now = datetime.now()
    
    ledger.open_position("BTC", "BUY", 50000, 0.1, now)
    closed = ledger.close_position("BTC", 55000, now)
    
    assert len(closed) == 1
    assert closed[0].pnl > 0  # Profitable trade


def test_insufficient_capital():
    """Test insufficient capital handling."""
    ledger = PaperLedger(initial_capital=1000)
    now = datetime.now()
    
    with pytest.raises(ValueError):
        ledger.open_position("BTC", "BUY", 50000, 1, now)
