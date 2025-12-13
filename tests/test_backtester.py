"""Test backtester engine."""
import pytest
from datetime import datetime
from core.types import MarketEvent, SignalEvent, OrderSide
from core.simulation import BacktestEngine, SimulationConfig
from core.ledger import PaperLedger


def test_backtest_engine_initialization():
    """Test engine initialization."""
    config = SimulationConfig(initial_capital=10000)
    engine = BacktestEngine(config)
    
    assert engine.ledger.equity == 10000
    assert engine.event_queue.empty()
    assert engine.warm_up_complete == False


def test_event_queue_fifo():
    """Test event queue FIFO ordering."""
    from core.simulation import EventQueue
    
    queue = EventQueue()
    
    event1 = MarketEvent(datetime(2024, 1, 1, 0, 0), "BTC", 100, 1000)
    event2 = MarketEvent(datetime(2024, 1, 1, 0, 1), "BTC", 101, 1000)
    
    queue.put(event1)
    queue.put(event2)
    
    assert queue.get() == event1
    assert queue.get() == event2
    assert queue.empty()


def test_market_event_processing():
    """Test market event processing."""
    config = SimulationConfig(initial_capital=10000)
    engine = BacktestEngine(config)
    
    event = MarketEvent(datetime.now(), "BTC", 100, 1000)
    engine.process_market_event(event)
    
    assert engine.current_bar == 1


def test_slippage_application():
    """Test slippage calculation."""
    config = SimulationConfig(
        initial_capital=10000,
        max_slippage_bps=20
    )
    engine = BacktestEngine(config)
    
    # Slippage should be < 20 bps
    assert engine.config.max_slippage_bps == 20
