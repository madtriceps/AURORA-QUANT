"""Risk management engine."""
from typing import Dict, Optional
from dataclasses import dataclass


@dataclass
class RiskLimits:
    """Risk limit configuration."""
    max_position_size: float = 10000.0  # Max position in dollars
    max_leverage: float = 1.0
    max_daily_loss_percent: float = 5.0
    max_drawdown_percent: float = 20.0
    max_sector_exposure_percent: float = 30.0
    stop_loss_atr_multiple: float = 2.0


class RiskEngine:
    """Risk management and monitoring."""
    
    def __init__(self, limits: RiskLimits):
        self.limits = limits
        self.daily_loss = 0.0
        self.positions: Dict = {}
        self.kill_switch_triggered = False
    
    def check_position_limits(self, symbol: str, quantity: float, price: float) -> bool:
        """Check if position size is within limits."""
        position_value = abs(quantity * price)
        return position_value <= self.limits.max_position_size
    
    def check_leverage_limit(self, current_equity: float, total_exposure: float) -> bool:
        """Check if leverage is within limits."""
        leverage = total_exposure / current_equity if current_equity > 0 else 0
        return leverage <= self.limits.max_leverage
    
    def check_daily_loss_limit(self, current_loss: float) -> bool:
        """Check if daily loss exceeds limit."""
        return abs(current_loss) <= self.limits.max_daily_loss_percent
    
    def check_drawdown_limit(self, current_drawdown: float) -> bool:
        """Check if drawdown exceeds limit."""
        if current_drawdown >= self.limits.max_drawdown_percent:
            self.kill_switch_triggered = True
            return False
        return True
    
    def can_trade(self, symbol: str, quantity: float, price: float,
                  current_equity: float, total_exposure: float,
                  current_drawdown: float) -> bool:
        """Comprehensive check if trade is allowed."""
        if self.kill_switch_triggered:
            return False
        
        return (
            self.check_position_limits(symbol, quantity, price) and
            self.check_leverage_limit(current_equity, total_exposure) and
            self.check_drawdown_limit(current_drawdown)
        )


#- Added comprehensive risk engine with position sizing, leverage, and drawdown controls
