"""
Paper Trading Ledger Engine
Handles position tracking, P&L calculation, and trade history.
"""
from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime
import json


@dataclass
class Trade:
    """Represents a single trade execution."""
    trade_id: int
    symbol: str
    side: str  # 'BUY' or 'SELL'
    entry_price: float
    quantity: float
    entry_time: datetime
    exit_price: Optional[float] = None
    exit_time: Optional[datetime] = None
    pnl: float = 0.0
    pnl_percent: float = 0.0
    status: str = "OPEN"  # OPEN, CLOSED, FAILED

    def close(self, exit_price: float, exit_time: datetime) -> None:
        """Close the trade and calculate P&L."""
        self.exit_price = exit_price
        self.exit_time = exit_time
        self.status = "CLOSED"
        
        if self.side == "BUY":
            self.pnl = (exit_price - self.entry_price) * self.quantity
        else:  # SELL
            self.pnl = (self.entry_price - exit_price) * self.quantity
        
        self.pnl_percent = (self.pnl / (self.entry_price * self.quantity)) * 100

    def to_dict(self) -> dict:
        return {
            'id': self.trade_id,
            'symbol': self.symbol,
            'side': self.side,
            'entry_price': round(self.entry_price, 8),
            'quantity': round(self.quantity, 8),
            'entry_time': self.entry_time.isoformat() if self.entry_time else None,
            'exit_price': round(self.exit_price, 8) if self.exit_price else None,
            'exit_time': self.exit_time.isoformat() if self.exit_time else None,
            'pnl': round(self.pnl, 2),
            'pnl_percent': round(self.pnl_percent, 2),
            'status': self.status,
        }


class PaperLedger:
    """Manages paper trading positions and P&L."""
    
    def __init__(self, initial_capital: float):
        self.initial_capital = initial_capital
        self.cash = initial_capital
        self.trades: List[Trade] = []
        self.open_positions: dict = {}  # symbol -> list of open trades
        self.trade_counter = 0
        self.max_equity = initial_capital
        self.min_equity = initial_capital

    @property
    def equity(self) -> float:
        """Current equity = cash + unrealized PnL."""
        unrealized_pnl = sum(
            trade.pnl for trades in self.open_positions.values() 
            for trade in trades if trade.status == "OPEN"
        )
        return self.cash + unrealized_pnl

    @property
    def total_pnl(self) -> float:
        """Total realized P&L from closed trades."""
        return sum(t.pnl for t in self.trades if t.status == "CLOSED")

    @property
    def total_pnl_percent(self) -> float:
        """Total return %."""
        if self.initial_capital == 0:
            return 0.0
        return (self.total_pnl / self.initial_capital) * 100

    @property
    def max_drawdown(self) -> float:
        """Maximum drawdown from peak equity."""
        if not self.trades:
            return 0.0
        peak = self.initial_capital
        max_dd = 0.0
        for trade in self.trades:
            if trade.status == "CLOSED":
                current_equity = self.initial_capital + sum(
                    t.pnl for t in self.trades[:self.trades.index(trade) + 1] 
                    if t.status == "CLOSED"
                )
                if current_equity > peak:
                    peak = current_equity
                drawdown = ((peak - current_equity) / peak) * 100
                if drawdown > max_dd:
                    max_dd = drawdown
        return max_dd

    def open_position(self, symbol: str, side: str, price: float, 
                      quantity: float, timestamp: datetime) -> Trade:
        """Open a new position."""
        cost = price * quantity
        if self.cash < cost and side == "BUY":
            raise ValueError(f"Insufficient cash. Have {self.cash}, need {cost}")
        
        self.trade_counter += 1
        trade = Trade(
            trade_id=self.trade_counter,
            symbol=symbol,
            side=side,
            entry_price=price,
            quantity=quantity,
            entry_time=timestamp,
        )
        
        self.trades.append(trade)
        if symbol not in self.open_positions:
            self.open_positions[symbol] = []
        self.open_positions[symbol].append(trade)
        
        if side == "BUY":
            self.cash -= cost
        else:  # SELL
            self.cash += cost
        
        return trade

    def close_position(self, symbol: str, price: float, 
                       timestamp: datetime, quantity: Optional[float] = None) -> List[Trade]:
        """Close position(s) for a symbol."""
        if symbol not in self.open_positions or not self.open_positions[symbol]:
            return []
        
        closed = []
        open_trades = self.open_positions[symbol]
        remaining_qty = quantity if quantity else float('inf')
        
        for trade in open_trades[:]:
            if remaining_qty <= 0:
                break
            
            close_qty = min(trade.quantity, remaining_qty)
            trade.close(price, timestamp)
            closed.append(trade)
            remaining_qty -= close_qty
            
            if trade.side == "BUY":
                self.cash += price * close_qty
            else:  # SELL
                self.cash -= price * close_qty
            
            open_trades.remove(trade)
        
        return closed

    def get_trades_summary(self) -> dict:
        """Get summary statistics."""
        closed_trades = [t for t in self.trades if t.status == "CLOSED"]
        winning_trades = [t for t in closed_trades if t.pnl > 0]
        losing_trades = [t for t in closed_trades if t.pnl <= 0]
        
        return {
            'total_trades': len(self.trades),
            'closed_trades': len(closed_trades),
            'winning_trades': len(winning_trades),
            'losing_trades': len(losing_trades),
            'win_rate': (len(winning_trades) / len(closed_trades) * 100) if closed_trades else 0,
            'total_pnl': self.total_pnl,
            'total_pnl_percent': self.total_pnl_percent,
            'max_drawdown': self.max_drawdown,
            'current_equity': self.equity,
            'cash': self.cash,
        }
