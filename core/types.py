"""Core type definitions and events for event-driven system."""
from typing import TypeVar, Generic, Literal
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class EventType(Enum):
    """Event types for event queue."""
    MARKET = "MARKET"
    SIGNAL = "SIGNAL"
    ORDER = "ORDER"
    FILL = "FILL"
    PORTFOLIO = "PORTFOLIO"


class OrderType(Enum):
    """Order execution types."""
    MARKET = "MARKET"
    LIMIT = "LIMIT"
    STOP = "STOP"
    TWAP = "TWAP"


class OrderSide(Enum):
    """Order sides."""
    BUY = "BUY"
    SELL = "SELL"


class OrderStatus(Enum):
    """Order status states."""
    PENDING = "PENDING"
    FILLED = "FILLED"
    PARTIALLY_FILLED = "PARTIALLY_FILLED"
    CANCELLED = "CANCELLED"
    REJECTED = "REJECTED"


@dataclass
class MarketEvent:
    """Represents market data update."""
    timestamp: datetime
    symbol: str
    price: float
    volume: float
    bid: float = 0.0
    ask: float = 0.0
    event_type: EventType = field(default=EventType.MARKET, init=False)


@dataclass
class SignalEvent:
    """Strategy signal event."""
    timestamp: datetime
    strategy_id: str
    symbol: str
    signal: Literal["BUY", "SELL", "HOLD"]
    confidence: float  # 0.0-1.0
    reason: str = ""
    parameters: dict = field(default_factory=dict)
    event_type: EventType = field(default=EventType.SIGNAL, init=False)


@dataclass
class OrderEvent:
    """Order execution request."""
    timestamp: datetime
    order_id: str
    symbol: str
    side: OrderSide
    order_type: OrderType
    quantity: float
    price: float = 0.0  # For limit orders
    event_type: EventType = field(default=EventType.ORDER, init=False)


@dataclass
class FillEvent:
    """Order fill/execution event."""
    timestamp: datetime
    order_id: str
    symbol: str
    side: OrderSide
    quantity: float
    fill_price: float
    commission: float = 0.0
    event_type: EventType = field(default=EventType.FILL, init=False)
