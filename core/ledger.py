"""Enhanced paper trading ledger engine."""
from dataclasses import dataclass, field
from typing import List, Optional, Dict
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
    fees: float = 0.0
    slippage: float = 0.0
    strategy_id: str = ""

    def close(self, exit_price: float, exit_time: datetime, 
              fees: float = 0.0, slippage: float = 0.0) -> None:
        """Close the trade and calculate P&L."""
        self.exit_price = exit_price
        self.exit_time = exit_time
        self.fees = fees
        self.slippage = slippage
        self.status = "CLOSED"
        
        if self.side == "BUY":
            gross_pnl = (exit_price - self.entry_price) * self.quantity
        else:  # SELL
            gross_pnl = (self.entry_price - exit_price) * self.quantity
        
        self.pnl = gross_pnl - fees - slippage
        entry_cost = self.entry_price * self.quantity
        self.pnl_percent = (self.pnl / entry_cost) * 100 if entry_cost > 0 else 0

    def to_dict(self) -> dict:
        """Convert trade to dictionary."""
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
            'strategy': self.strategy_id,
        }


class PaperLedger:
    """Enterprise-grade paper trading ledger with advanced metrics."""

    def __init__(self, initial_capital: float, strategy_id: str = "default"):
        self.initial_capital = initial_capital
        self.cash = initial_capital
        self.trades: List[Trade] = []
        self.open_positions: Dict[str, List[Trade]] = {}
        self.trade_counter = 0
        self.strategy_id = strategy_id
        self.equity_history: List[float] = [initial_capital]
        self.timestamp_history: List[datetime] = [datetime.now()]
        # Track running peak and max drawdown correctly
        self._peak_equity: float = initial_capital
        self._max_drawdown_pct: float = 0.0

    @property
    def equity(self) -> float:
        """Current equity = cash + mark-to-market value of open positions."""
        open_value = 0.0
        for trades in self.open_positions.values():
            for trade in trades:
                if trade.status == "OPEN":
                    # Value of open position at entry price (conservative)
                    open_value += trade.entry_price * trade.quantity
        return self.cash + open_value

    @property
    def total_pnl(self) -> float:
        """Total realized P&L from closed trades."""
        return sum(t.pnl for t in self.trades if t.status == "CLOSED")

    @property
    def total_pnl_percent(self) -> float:
        """Total return %."""
        return (self.total_pnl / self.initial_capital) * 100 if self.initial_capital > 0 else 0

    @property
    def max_drawdown(self) -> float:
        """True maximum drawdown: largest peak-to-trough drop across entire history."""
        if len(self.equity_history) < 2:
            return 0.0
        peak = self.equity_history[0]
        worst_dd = 0.0
        for eq in self.equity_history[1:]:
            if eq > peak:
                peak = eq
            dd = ((peak - eq) / peak) * 100 if peak > 0 else 0.0
            if dd > worst_dd:
                worst_dd = dd
        return worst_dd

    @property
    def sharpe_ratio(self, risk_free_rate: float = 0.02) -> float:
        """Calculate annualized Sharpe ratio."""
        if len(self.equity_history) < 2:
            return 0.0
        returns = [
            (self.equity_history[i] - self.equity_history[i - 1]) / self.equity_history[i - 1]
            for i in range(1, len(self.equity_history))
            if self.equity_history[i - 1] > 0
        ]
        if not returns:
            return 0.0
        avg_return = sum(returns) / len(returns)
        variance = sum((r - avg_return) ** 2 for r in returns) / len(returns)
        std_dev = variance ** 0.5
        if std_dev <= 0:
            return 0.0
        # Annualize: assume ~252 trading periods per year
        return (avg_return - risk_free_rate / 252) / std_dev

    def update_equity(self, market_price: float = None, symbol: str = None) -> None:
        """Update equity history. Optionally mark-to-market open positions."""
        current_eq = self.equity
        self.equity_history.append(current_eq)
        self.timestamp_history.append(datetime.now())
        # Update running peak / max drawdown
        if current_eq > self._peak_equity:
            self._peak_equity = current_eq
        dd = ((self._peak_equity - current_eq) / self._peak_equity) * 100 if self._peak_equity > 0 else 0.0
        if dd > self._max_drawdown_pct:
            self._max_drawdown_pct = dd

    def open_position(self, symbol: str, side: str, price: float,
                      quantity: float, timestamp: datetime) -> Trade:
        """Open a new position."""
        cost = price * quantity
        if self.cash < cost and side == "BUY":
            raise ValueError(f"Insufficient cash. Have {self.cash:.2f}, need {cost:.2f}")
        
        self.trade_counter += 1
        trade = Trade(
            trade_id=self.trade_counter,
            symbol=symbol,
            side=side,
            entry_price=price,
            quantity=quantity,
            entry_time=timestamp,
            strategy_id=self.strategy_id,
        )
        
        self.trades.append(trade)
        if symbol not in self.open_positions:
            self.open_positions[symbol] = []
        self.open_positions[symbol].append(trade)
        
        if side == "BUY":
            self.cash -= cost
        else:  # SELL
            self.cash += cost
        
        self.update_equity()
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
        
        self.update_equity()
        return closed

    def get_trades_summary(self) -> dict:
        """Get comprehensive summary statistics."""
        closed_trades = [t for t in self.trades if t.status == "CLOSED"]
        winning_trades = [t for t in closed_trades if t.pnl > 0]
        losing_trades = [t for t in closed_trades if t.pnl <= 0]
        
        avg_win = sum(t.pnl for t in winning_trades) / len(winning_trades) if winning_trades else 0
        avg_loss = sum(t.pnl for t in losing_trades) / len(losing_trades) if losing_trades else 0
        profit_factor = abs(avg_win * len(winning_trades) / (avg_loss * len(losing_trades))) if avg_loss != 0 else 0
        
        return {
            'total_trades': len(self.trades),
            'closed_trades': len(closed_trades),
            'winning_trades': len(winning_trades),
            'losing_trades': len(losing_trades),
            'win_rate': (len(winning_trades) / len(closed_trades) * 100) if closed_trades else 0,
            'total_pnl': self.total_pnl,
            'total_pnl_percent': self.total_pnl_percent,
            'max_drawdown': self.max_drawdown,
            'sharpe_ratio': self.sharpe_ratio,
            'profit_factor': profit_factor,
            'current_equity': self.equity,
            'cash': self.cash,
            'avg_win': avg_win,
            'avg_loss': abs(avg_loss),
        }
