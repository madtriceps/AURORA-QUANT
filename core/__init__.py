"""Aurora Quant v2.0 - Core Module"""
from core.types import (
    EventType, OrderType, OrderSide, OrderStatus,
    MarketEvent, SignalEvent, OrderEvent, FillEvent
)
from core.simulation import BacktestEngine, SimulationConfig, EventQueue
from core.ledger import PaperLedger, Trade
from core.broker import Broker, PaperBroker
from core.portfolio import PortfolioManager
from core.risk import RiskEngine, RiskLimits
from core.indicators import (
    calculate_ema, calculate_rsi, calculate_vwap,
    calculate_macd, calculate_atr, detect_volume_spike
)

__all__ = [
    "EventType", "OrderType", "OrderSide", "OrderStatus",
    "MarketEvent", "SignalEvent", "OrderEvent", "FillEvent",
    "BacktestEngine", "SimulationConfig", "EventQueue",
    "PaperLedger", "Trade",
    "Broker", "PaperBroker",
    "PortfolioManager",
    "RiskEngine", "RiskLimits",
    "calculate_ema", "calculate_rsi", "calculate_vwap",
    "calculate_macd", "calculate_atr", "detect_volume_spike",
]
