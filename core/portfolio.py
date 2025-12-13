"""Multi-asset portfolio manager."""
from typing import Dict, List, Optional
from datetime import datetime


class PortfolioManager:
    """Manages multi-asset portfolio with risk constraints."""
    
    def __init__(self, initial_capital: float, max_leverage: float = 1.0):
        self.initial_capital = initial_capital
        self.max_leverage = max_leverage
        self.positions: Dict[str, Dict] = {}
        self.equity_curve: List[float] = [initial_capital]
        self.timestamp_history: List[datetime] = []
        self.current_leverage = 0.0
    
    def add_position(self, symbol: str, quantity: float, entry_price: float,
                    timestamp: datetime) -> None:
        """Add position to portfolio."""
        if symbol not in self.positions:
            self.positions[symbol] = {
                'symbol': symbol,
                'quantity': 0,
                'entry_price': 0,
                'current_price': entry_price,
                'entry_time': timestamp,
                'unrealized_pnl': 0.0,
            }
        
        pos = self.positions[symbol]
        total_cost = pos['quantity'] * pos['entry_price'] + quantity * entry_price
        pos['quantity'] += quantity
        pos['entry_price'] = total_cost / pos['quantity'] if pos['quantity'] > 0 else 0
        pos['entry_time'] = timestamp
    
    def remove_position(self, symbol: str, quantity: float) -> None:
        """Remove position from portfolio."""
        if symbol in self.positions:
            pos = self.positions[symbol]
            pos['quantity'] -= quantity
            if pos['quantity'] <= 0:
                del self.positions[symbol]
    
    def update_prices(self, prices: Dict[str, float]) -> None:
        """Update position prices and calculate unrealized P&L."""
        for symbol, price in prices.items():
            if symbol in self.positions:
                pos = self.positions[symbol]
                pos['current_price'] = price
                pos['unrealized_pnl'] = (price - pos['entry_price']) * pos['quantity']
    
    def get_current_equity(self) -> float:
        """Calculate current equity."""
        total_unrealized = sum(p['unrealized_pnl'] for p in self.positions.values())
        return self.initial_capital + total_unrealized
    
    def get_exposure(self) -> float:
        """Get total portfolio exposure as % of capital."""
        total_exposure = sum(abs(p['quantity'] * p['current_price']) 
                            for p in self.positions.values())
        return total_exposure / self.initial_capital if self.initial_capital > 0 else 0
    
    def get_allocation(self) -> Dict[str, float]:
        """Get portfolio allocation by symbol."""
        total_equity = self.get_current_equity()
        allocation = {}
        for symbol, pos in self.positions.items():
            allocation[symbol] = (pos['quantity'] * pos['current_price']) / total_equity if total_equity > 0 else 0
        return allocation


#- Added portfolio manager for tracking multi-asset positions and allocations
