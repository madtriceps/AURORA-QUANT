"""Risk management engine - enforces hard limits on every trade."""
from typing import Dict, Optional
from dataclasses import dataclass


@dataclass
class RiskLimits:
    """Risk limit configuration."""
    max_position_pct: float = 0.15       # Max single position as % of equity
    max_portfolio_exposure: float = 0.50  # Max total exposure as % of equity
    max_leverage: float = 1.0
    max_daily_loss_percent: float = 3.0   # Kill switch: daily loss
    max_drawdown_percent: float = 15.0    # Kill switch: total drawdown
    max_risk_per_trade_pct: float = 0.02  # Max $ risk per trade as % of equity


class RiskEngine:
    """Risk management and monitoring with hard limits and kill switch."""

    def __init__(self, limits: RiskLimits):
        self.limits = limits
        self.daily_pnl = 0.0
        self.kill_switch_triggered = False
        self._kill_reason = ""

    def check_position_size(self, position_value: float, equity: float) -> bool:
        """Reject if single position exceeds max_position_pct of equity."""
        if equity <= 0:
            return False
        return (position_value / equity) <= self.limits.max_position_pct

    def check_portfolio_exposure(self, total_exposure: float, equity: float) -> bool:
        """Reject if total portfolio exposure exceeds limit."""
        if equity <= 0:
            return False
        return (total_exposure / equity) <= self.limits.max_portfolio_exposure

    def check_leverage(self, equity: float, total_exposure: float) -> bool:
        """Reject if leverage exceeds limit."""
        leverage = total_exposure / equity if equity > 0 else 0
        return leverage <= self.limits.max_leverage

    def check_risk_per_trade(self, dollar_risk: float, equity: float) -> bool:
        """Reject if the dollar risk on this trade exceeds risk limit."""
        if equity <= 0:
            return False
        return (dollar_risk / equity) <= self.limits.max_risk_per_trade_pct

    def check_drawdown(self, current_drawdown_pct: float) -> bool:
        """Trigger kill switch if drawdown exceeds limit."""
        if current_drawdown_pct >= self.limits.max_drawdown_percent:
            self.kill_switch_triggered = True
            self._kill_reason = f"Drawdown {current_drawdown_pct:.1f}% >= {self.limits.max_drawdown_percent}%"
            return False
        return True

    def check_daily_loss(self, daily_loss_pct: float) -> bool:
        """Trigger kill switch if daily loss exceeds limit."""
        if abs(daily_loss_pct) >= self.limits.max_daily_loss_percent:
            self.kill_switch_triggered = True
            self._kill_reason = f"Daily loss {daily_loss_pct:.1f}% >= {self.limits.max_daily_loss_percent}%"
            return False
        return True

    def can_trade(self, position_value: float, dollar_risk: float,
                  equity: float, total_exposure: float,
                  current_drawdown_pct: float) -> tuple:
        """
        Comprehensive pre-trade check. Returns (allowed: bool, reason: str).
        """
        if self.kill_switch_triggered:
            return False, f"Kill switch active: {self._kill_reason}"

        if not self.check_drawdown(current_drawdown_pct):
            return False, self._kill_reason

        if not self.check_position_size(position_value, equity):
            return False, (f"Position {position_value:.0f} exceeds "
                           f"{self.limits.max_position_pct*100:.0f}% of equity {equity:.0f}")

        if not self.check_portfolio_exposure(total_exposure + position_value, equity):
            return False, (f"Total exposure would exceed "
                           f"{self.limits.max_portfolio_exposure*100:.0f}% of equity")

        if not self.check_risk_per_trade(dollar_risk, equity):
            return False, (f"Trade risk ${dollar_risk:.2f} exceeds "
                           f"{self.limits.max_risk_per_trade_pct*100:.1f}% of equity")

        if not self.check_leverage(equity, total_exposure + position_value):
            return False, f"Leverage would exceed {self.limits.max_leverage}x"

        return True, "OK"

    def reset_daily(self) -> None:
        """Reset daily counters (call at start of each trading day)."""
        self.daily_pnl = 0.0
        # Don't reset kill switch - that requires manual intervention
