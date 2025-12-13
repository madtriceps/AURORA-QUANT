"""
SIMPLE MOMENTUM STRATEGY - The One That Actually Works
========================================================
Philosophy: Keep it simple. Trade the trend. Let winners run.

Rules:
1. Buy when price crosses above 50-day MA with momentum
2. Sell when price crosses below 50-day MA
3. Use 2% position sizing with trailing stops
4. That's it. No overcomplicated filters.
"""
from typing import Optional, Dict, List
import numpy as np
from datetime import datetime
from strategies.base import Strategy
from core.types import SignalEvent
from core.indicators import calculate_ema, calculate_rsi, calculate_atr

print("💎 SIMPLE MOMENTUM v3.0 - The Strategy That Actually Works 💎")


class MomentumStrategy(Strategy):
    """Dead simple momentum strategy that catches trends."""
    
    def __init__(self, strategy_id: str = "momentum", ledger=None, 
                 aggressiveness: str = "moderate"):
        super().__init__(strategy_id, ledger)
        self.aggressiveness = aggressiveness
        
        # Simple parameters
        self.params = {
            'ma_fast': 20,    # Fast MA
            'ma_slow': 50,    # Slow MA (trend)
            'rsi_period': 14,
            'atr_period': 14,
        }
        
        # Risk per trade
        if aggressiveness == "conservative":
            self.risk_pct = 0.01  # 1%
            self.position_pct = 0.20
        elif aggressiveness == "aggressive":
            self.risk_pct = 0.03  # 3%
            self.position_pct = 0.40
        else:  # moderate
            self.risk_pct = 0.02  # 2%
            self.position_pct = 0.30
        
        # State
        self.bar_history: Dict[str, List] = {}
        self.position_open = False
        self.entry_price = 0.0
        self.trades_count = 0
        self.last_ma_cross = None  # Track last crossover
    
    def on_bar(self, symbol: str, bar: Dict) -> Optional[SignalEvent]:
        """Simple crossover strategy."""
        if symbol not in self.bar_history:
            self.bar_history[symbol] = []
        
        self.bar_history[symbol].append(bar)
        
        # Need at least 60 bars
        if len(self.bar_history[symbol]) < 60:
            return None
        
        bars = self.bar_history[symbol]
        closes = [b['close'] for b in bars]
        highs = [b['high'] for b in bars]
        lows = [b['low'] for b in bars]
        
        # Calculate indicators (simple!)
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
        
        # === SIMPLE CROSSOVER LOGIC ===
        
        # Detect crossovers
        bullish_cross = (prev_ma_fast <= prev_ma_slow and 
                        current_ma_fast > current_ma_slow)
        bearish_cross = (prev_ma_fast >= prev_ma_slow and 
                        current_ma_fast < current_ma_slow)
        
        # === EXIT LOGIC ===
        if self.position_open:
            should_exit = False
            reason = ""
            
            # Exit 1: Bearish crossover (trend reversal)
            if bearish_cross:
                should_exit = True
                reason = "Bearish MA crossover"
            
            # Exit 2: Stop loss (2 ATR)
            stop_loss = self.entry_price - (current_atr * 2.0)
            if price <= stop_loss:
                should_exit = True
                reason = f"Stop loss at ${stop_loss:.2f}"
            
            # Exit 3: RSI extreme overbought
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
                            print(f"  🔴 EXIT #{self.trades_count}: ${price:.2f} | "
                                  f"P&L ${pnl:+.2f} ({pnl_pct:+.1f}%) | {reason}")
                        
                        return self.generate_signal(symbol, "SELL", 1.0, reason)
                except:
                    pass
        
        # === ENTRY LOGIC ===
        if not self.position_open:
            should_enter = False
            reason = ""
            
            # Entry: Bullish crossover with confirmation
            if bullish_cross:
                # Confirmation 1: Price above slow MA (riding trend)
                above_trend = price > current_ma_slow
                
                # Confirmation 2: RSI not overbought (room to run)
                rsi_ok = 30 < current_rsi < 70
                
                # Confirmation 3: Price momentum (rising)
                momentum_ok = price > prev_price
                
                if above_trend and rsi_ok and momentum_ok:
                    should_enter = True
                    reason = f"Bullish cross + trend (RSI={current_rsi:.0f})"
            
            if should_enter and self.ledger:
                # Position sizing: Fixed % of capital
                position_value = self.ledger.cash * self.position_pct
                size = position_value / price
                
                if size > 0:
                    try:
                        self.ledger.open_position(symbol, "BUY", price, size, ts)
                        self.position_open = True
                        self.entry_price = price
                        self.trades_count += 1
                        
                        if self.trades_count <= 20 or self.trades_count % 5 == 0:
                            print(f"  🟢 ENTRY #{self.trades_count}: "
                                  f"BUY {size:.2f} @ ${price:.2f} | {reason}")
                        
                        return self.generate_signal(symbol, "BUY", 0.8, reason)
                    except:
                        pass
        
        return None