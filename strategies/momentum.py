"""
SIMPLE MOMENTUM STRATEGY v4.0 - ATR-Based Risk Management
===========================================================
Philosophy: Keep it simple. Trade the trend. Let winners run.
Position sizing: Fixed-fractional risk per trade using ATR.

Rules:
1. Buy when price crosses above 50-day MA with momentum confirmation
2. Sell on bearish crossover, trailing stop, or RSI overbought
3. Size each trade so max loss = risk_pct of account equity
4. Trailing stop locks in profit once trade moves in our favor

Formula:
  stop_distance = ATR * atr_stop_multiple
  position_size = (equity * risk_pct) / stop_distance
  max_position_value capped at max_exposure_pct of equity
"""
from typing import Optional, Dict, List
import numpy as np
from datetime import datetime
from strategies.base import Strategy
from core.types import SignalEvent
from core.indicators import calculate_ema, calculate_rsi, calculate_atr

print("[AURORA] SIMPLE MOMENTUM v4.0 - ATR Risk-Managed")


class MomentumStrategy(Strategy):
    """Momentum strategy with ATR-based position sizing and trailing stops."""

    def __init__(self, strategy_id: str = "momentum", ledger=None,
                 aggressiveness: str = "moderate"):
        super().__init__(strategy_id, ledger)
        self.aggressiveness = aggressiveness

        # Indicator parameters (same for all modes)
        self.params = {
            'ma_fast': 20,
            'ma_slow': 50,
            'rsi_period': 14,
            'atr_period': 14,
        }

        # --- Risk parameters differ by aggressiveness ---
        # risk_pct: fraction of equity risked per trade
        # atr_stop_multiple: how many ATRs away the initial stop is
        # max_exposure_pct: hard cap on single-position value vs equity
        # trailing_atr_multiple: trailing stop distance in ATRs
        # rsi_entry_upper: max RSI to allow entry (tighter = more selective)
        if aggressiveness == "conservative":
            self.risk_pct = 0.005        # 0.5% of equity per trade
            self.atr_stop_multiple = 2.5  # wider stop -> smaller size
            self.max_exposure_pct = 0.10  # never more than 10% in one trade
            self.trailing_atr_multiple = 2.0
            self.rsi_entry_upper = 60     # stricter entry filter
        elif aggressiveness == "aggressive":
            self.risk_pct = 0.02          # 2% of equity per trade
            self.atr_stop_multiple = 1.5  # tighter stop -> bigger size but quicker exit
            self.max_exposure_pct = 0.20  # up to 20% in one trade
            self.trailing_atr_multiple = 1.5
            self.rsi_entry_upper = 75     # more permissive entry
        else:  # moderate (default)
            self.risk_pct = 0.01          # 1% of equity per trade
            self.atr_stop_multiple = 2.0
            self.max_exposure_pct = 0.15  # up to 15% in one trade
            self.trailing_atr_multiple = 1.75
            self.rsi_entry_upper = 70

        # --- State ---
        self.bar_history: Dict[str, List] = {}
        self.position_open = False
        self.entry_price = 0.0
        self.stop_loss_price = 0.0        # fixed initial stop
        self.trailing_stop_price = 0.0    # trailing stop (only moves up)
        self.highest_since_entry = 0.0    # tracks peak price for trailing stop
        self.position_size = 0.0
        self.trades_count = 0
        self.last_ma_cross = None

    def _calculate_position_size(self, equity: float, price: float,
                                  atr: float) -> float:
        """
        ATR-based fixed-fractional position sizing.

        size = (equity * risk_pct) / (atr * atr_stop_multiple)

        Then capped so position_value <= equity * max_exposure_pct.
        """
        stop_distance = atr * self.atr_stop_multiple
        if stop_distance <= 0:
            return 0.0

        # Core formula: risk a fixed % of equity
        dollar_risk = equity * self.risk_pct
        size = dollar_risk / stop_distance

        # Hard cap: never exceed max_exposure_pct of equity in one position
        max_size = (equity * self.max_exposure_pct) / price
        size = min(size, max_size)

        # Also can't spend more cash than we have
        if self.ledger:
            max_affordable = self.ledger.cash / price * 0.99  # 1% buffer
            size = min(size, max_affordable)

        return max(size, 0.0)

    def _update_trailing_stop(self, price: float, atr: float) -> None:
        """Move trailing stop up (never down) as price makes new highs."""
        if price > self.highest_since_entry:
            self.highest_since_entry = price
            new_trail = price - (atr * self.trailing_atr_multiple)
            # Only ratchet up, never down
            if new_trail > self.trailing_stop_price:
                self.trailing_stop_price = new_trail

    def on_bar(self, symbol: str, bar: Dict) -> Optional[SignalEvent]:
        """Process one bar: check exits, then check entries."""
        if symbol not in self.bar_history:
            self.bar_history[symbol] = []

        self.bar_history[symbol].append(bar)

        # Need at least 60 bars for indicator warm-up
        if len(self.bar_history[symbol]) < 60:
            return None

        bars = self.bar_history[symbol]
        closes = [b['close'] for b in bars]
        highs = [b['high'] for b in bars]
        lows = [b['low'] for b in bars]

        # Calculate indicators
        ma_fast = calculate_ema(closes, self.params['ma_fast'])
        ma_slow = calculate_ema(closes, self.params['ma_slow'])
        rsi = calculate_rsi(closes, self.params['rsi_period'])
        atr = calculate_atr(highs, lows, closes, self.params['atr_period'])

        price = closes[-1]
        prev_price = closes[-2]
        current_ma_fast = ma_fast[-1]
        prev_ma_fast = ma_fast[-2]
        current_ma_slow = ma_slow[-1]
        prev_ma_slow = ma_slow[-2]
        current_rsi = rsi[-1]
        current_atr = atr[-1]

        if any(np.isnan([current_ma_fast, current_ma_slow, current_rsi, current_atr])):
            return None

        # Timestamp
        ts = bar.get('timestamp')
        if isinstance(ts, (int, float)):
            ts = datetime.fromtimestamp(ts / 1000)
        elif not isinstance(ts, datetime):
            ts = datetime.now()

        # Detect crossovers
        bullish_cross = (prev_ma_fast <= prev_ma_slow and
                         current_ma_fast > current_ma_slow)
        bearish_cross = (prev_ma_fast >= prev_ma_slow and
                         current_ma_fast < current_ma_slow)

        # ================================================================
        # EXIT LOGIC
        # ================================================================
        if self.position_open:
            # Update trailing stop
            self._update_trailing_stop(price, current_atr)

            should_exit = False
            reason = ""

            # Exit 1: Bearish crossover (trend reversal)
            if bearish_cross:
                should_exit = True
                reason = "Bearish MA crossover"

            # Exit 2: Fixed stop-loss hit
            if price <= self.stop_loss_price:
                should_exit = True
                reason = f"Stop loss at ${self.stop_loss_price:.2f}"

            # Exit 3: Trailing stop hit (only active after price has moved up)
            if (self.trailing_stop_price > self.stop_loss_price and
                    price <= self.trailing_stop_price):
                should_exit = True
                reason = f"Trailing stop at ${self.trailing_stop_price:.2f}"

            # Exit 4: RSI extreme overbought
            if current_rsi > 80:
                should_exit = True
                reason = f"RSI overbought ({current_rsi:.0f})"

            if should_exit and self.ledger:
                try:
                    closed = self.ledger.close_position(symbol, price, ts)
                    if closed:
                        self.position_open = False
                        pnl = sum(t.pnl for t in closed)
                        pnl_pct = sum(t.pnl_percent for t in closed)
                        self.trades_count += 1

                        if self.trades_count <= 20 or self.trades_count % 5 == 0:
                            print(f"  [EXIT #{self.trades_count}]: ${price:.2f} | "
                                  f"P&L ${pnl:+.2f} ({pnl_pct:+.1f}%) | {reason}")

                        return self.generate_signal(symbol, "SELL", 1.0, reason)
                except Exception:
                    pass

        # ================================================================
        # ENTRY LOGIC
        # ================================================================
        if not self.position_open:
            should_enter = False
            reason = ""

            if bullish_cross:
                above_trend = price > current_ma_slow
                rsi_ok = 30 < current_rsi < self.rsi_entry_upper
                momentum_ok = price > prev_price

                if above_trend and rsi_ok and momentum_ok:
                    should_enter = True
                    reason = f"Bullish cross + trend (RSI={current_rsi:.0f})"

            if should_enter and self.ledger:
                # ATR-based position sizing
                equity = self.ledger.equity
                size = self._calculate_position_size(equity, price, current_atr)

                if size > 0:
                    try:
                        self.ledger.open_position(symbol, "BUY", price, size, ts)
                        self.position_open = True
                        self.entry_price = price
                        self.position_size = size

                        # Set initial stop-loss and trailing stop
                        self.stop_loss_price = price - (current_atr * self.atr_stop_multiple)
                        self.trailing_stop_price = self.stop_loss_price
                        self.highest_since_entry = price

                        self.trades_count += 1
                        position_value = size * price
                        risk_dollar = current_atr * self.atr_stop_multiple * size

                        if self.trades_count <= 20 or self.trades_count % 5 == 0:
                            print(f"  [ENTRY #{self.trades_count}]: "
                                  f"BUY {size:.4f} @ ${price:.2f} | "
                                  f"Value ${position_value:.2f} "
                                  f"({position_value/equity*100:.1f}% of equity) | "
                                  f"Risk ${risk_dollar:.2f} | "
                                  f"Stop ${self.stop_loss_price:.2f} | "
                                  f"{reason}")

                        return self.generate_signal(symbol, "BUY", 0.8, reason)
                    except Exception:
                        pass

        return None
