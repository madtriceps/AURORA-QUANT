"""Broker abstraction layer for execution."""
from abc import ABC, abstractmethod
from typing import Optional, Dict, List
from datetime import datetime

from core.types import OrderEvent, FillEvent, OrderSide, OrderType


class Broker(ABC):
    """Abstract broker interface."""
    
    @abstractmethod
    def submit_order(self, order: OrderEvent) -> str:
        """Submit order and return order ID."""
        pass
    
    @abstractmethod
    def get_order_status(self, order_id: str) -> str:
        """Get order status."""
        pass
    
    @abstractmethod
    def get_position(self, symbol: str) -> Dict:
        """Get current position."""
        pass
    
    @abstractmethod
    def get_balance(self) -> float:
        """Get available cash balance."""
        pass


class PaperBroker(Broker):
    """Paper trading broker - simulates execution."""
    
    def __init__(self, ledger):
        self.ledger = ledger
        self.order_counter = 0
    
    def submit_order(self, order: OrderEvent) -> str:
        """Simulate order submission."""
        self.order_counter += 1
        order_id = f"PAPER_{self.order_counter}"
        
        # Immediate execution for market orders
        fill = FillEvent(
            timestamp=order.timestamp,
            order_id=order_id,
            symbol=order.symbol,
            side=order.side,
            quantity=order.quantity,
            fill_price=order.price if order.price else 0.0,
            commission=0.0
        )
        
        return order_id
    
    def get_order_status(self, order_id: str) -> str:
        """Get simulated order status."""
        return "FILLED"
    
    def get_position(self, symbol: str) -> Dict:
        """Get simulated position."""
        if symbol in self.ledger.open_positions:
            trades = self.ledger.open_positions[symbol]
            total_qty = sum(t.quantity for t in trades if t.status == "OPEN")
            avg_price = (sum(t.entry_price * t.quantity for t in trades) / total_qty) if total_qty > 0 else 0
            return {'symbol': symbol, 'quantity': total_qty, 'avg_price': avg_price}
        return {'symbol': symbol, 'quantity': 0, 'avg_price': 0}
    
    def get_balance(self) -> float:
        """Get available balance."""
        return self.ledger.cash


class BinanceBroker(Broker):
    """Binance broker - for future live trading."""
    
    def __init__(self, api_key: str, api_secret: str):
        self.api_key = api_key
        self.api_secret = api_secret
        # TODO: Implement live Binance integration
    
    def submit_order(self, order: OrderEvent) -> str:
        raise NotImplementedError("Live trading not yet implemented")
    
    def get_order_status(self, order_id: str) -> str:
        raise NotImplementedError("Live trading not yet implemented")
    
    def get_position(self, symbol: str) -> Dict:
        raise NotImplementedError("Live trading not yet implemented")
    
    def get_balance(self) -> float:
        raise NotImplementedError("Live trading not yet implemented")
