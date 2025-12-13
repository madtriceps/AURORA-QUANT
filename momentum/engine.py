"""Professional momentum strategy engine with multi-asset support."""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from core.ledger import PaperLedger
from core.indicators import calculate_ema, calculate_rsi, calculate_vwap, calculate_atr, calculate_macd
from core.data_loader import DataLoader
from core.exceptions import InsufficientDataError, StrategyError
from core.config import RISK_PROFILES


class MomentumEngine:
    """Professional intraday momentum strategy with advanced position sizing."""
    
    def __init__(self, symbol: str, capital: float, profile: str = "moderate",
                 asset_type: str = "crypto"):
        self.symbol = symbol
        self.asset_type = asset_type
        self.ledger = PaperLedger(capital, strategy_id=f"momentum_{asset_type}")
        self.risk_profile = profile
        self.risk_percent = RISK_PROFILES.get(profile, 2.5)
        
        self.candles: List[Dict] = []
        self.position_open = False
        self.entry_price = 0
        self.signals: List[Dict] = []
        self.trades_log: List[Dict] = []
        
        # Indicators
        self.ema_20 = []
        self.ema_50 = []
        self.ema_200 = []
        self.rsi = []
        self.vwap = []
        self.atr = []
        self.macd_line = []
        self.macd_signal = []

    def load_data(self, days: int = 3) -> bool:
        """Load historical candles."""
        try:
            if self.asset_type == "crypto":
                self.candles = DataLoader.fetch_crypto_candles(self.symbol, days=days)
            else:  # equity
                self.candles = DataLoader.fetch_equity_candles(self.symbol, period=f"{days}d")
            
            if len(self.candles) < 50:
                raise InsufficientDataError(f"Insufficient data: {len(self.candles)} candles")
            
            return True
        except Exception as e:
            raise StrategyError(f"Failed to load data: {str(e)}")

    def calculate_indicators(self) -> None:
        """Calculate all technical indicators."""
        closes = [c['close'] for c in self.candles]
        highs = [c['high'] for c in self.candles]
        lows = [c['low'] for c in self.candles]
        volumes = [c['volume'] for c in self.candles]
        
        self.ema_20 = calculate_ema(closes, 20)
        self.ema_50 = calculate_ema(closes, 50)
        self.ema_200 = calculate_ema(closes, 200)
        self.rsi = calculate_rsi(closes, 14)
        self.vwap = calculate_vwap(highs, lows, closes, volumes)
        self.atr = calculate_atr(highs, lows, closes, 14)
        self.macd_line, self.macd_signal = calculate_macd(closes)
        
        for i, candle in enumerate(self.candles):
            candle['ema_20'] = self.ema_20[i]
            candle['ema_50'] = self.ema_50[i]
            candle['ema_200'] = self.ema_200[i]
            candle['rsi'] = self.rsi[i]
            candle['vwap'] = self.vwap[i]
            candle['atr'] = self.atr[i]

    def check_buy_signal(self, current: Dict, previous: Dict) -> bool:
        """Generate buy signal."""
        if any(np.isnan(v) for v in [current['ema_20'], current['vwap'], current['rsi']]):
            return False
        
        # Signal: Price above VWAP, EMA20 > EMA50, RSI not overbought
        above_vwap = current['close'] > current['vwap']
        ema_aligned = current['ema_20'] > current['ema_50']
        rsi_ok = current['rsi'] < 70
        
        return above_vwap and ema_aligned and rsi_ok

    def check_sell_signal(self, current: Dict, previous: Dict) -> bool:
        """Generate sell signal."""
        if any(np.isnan(v) for v in [current['rsi'], current['vwap']]):
            return False
        
        # Signal: RSI overbought OR price below VWAP
        rsi_overbought = current['rsi'] > 70
        below_vwap = current['close'] < current['vwap']
        
        return rsi_overbought or below_vwap

    def calculate_position_size(self, price: float, atr: float) -> float:
        """Calculate position size based on risk and ATR."""
        risk_amount = self.ledger.cash * (self.risk_percent / 100)
        stop_distance = atr * 2  # 2x ATR stop loss
        position_size = risk_amount / stop_distance if stop_distance > 0 else 0
        return position_size

    def run_backtest(self) -> Dict:
        """Run strategy backtest."""
        print(f"📊 Backtesting {self.symbol} on {len(self.candles)} candles...")
        
        self.calculate_indicators()
        
        for i in range(1, len(self.candles)):
            current = self.candles[i]
            previous = self.candles[i - 1]
            timestamp = datetime.fromtimestamp(current['timestamp'] / 1000)
            
            if not self.position_open and self.check_buy_signal(current, previous):
                position_size = self.calculate_position_size(current['close'], current.get('atr', 1))
                
                try:
                    self.ledger.open_position(
                        symbol=self.symbol,
                        side="BUY",
                        price=current['close'],
                        quantity=position_size,
                        timestamp=timestamp
                    )
                    self.position_open = True
                    self.entry_price = current['close']
                    self.signals.append({'type': 'BUY', 'price': current['close'], 'time': timestamp})
                except:
                    pass
            
            elif self.position_open and self.check_sell_signal(current, previous):
                try:
                    self.ledger.close_position(
                        symbol=self.symbol,
                        price=current['close'],
                        timestamp=timestamp
                    )
                    self.position_open = False
                    self.signals.append({'type': 'SELL', 'price': current['close'], 'time': timestamp})
                except:
                    pass
        
        # Close remaining positions
        if self.position_open and self.candles:
            last_candle = self.candles[-1]
            try:
                self.ledger.close_position(
                    symbol=self.symbol,
                    price=last_candle['close'],
                    timestamp=datetime.fromtimestamp(last_candle['timestamp'] / 1000)
                )
            except:
                pass
        
        return self.get_summary()

    def get_summary(self) -> Dict:
        """Get strategy summary."""
        return {
            'symbol': self.symbol,
            'asset_type': self.asset_type,
            'candles_processed': len(self.candles),
            'signals_generated': len(self.signals),
            'ledger_summary': self.ledger.get_trades_summary(),
        }

    def get_equity_curve_ascii(self) -> str:
        """Generate ASCII equity curve."""
        if len(self.ledger.equity_history) < 2:
            return "Insufficient data for equity curve"
        
        values = self.ledger.equity_history
        min_val = min(values)
        max_val = max(values)
        range_val = max_val - min_val if max_val > min_val else 1
        
        lines = []
        lines.append("┌" + "─" * 58 + "┐")
        
        for value in values[::max(1, len(values) // 20)]:
            height = int(((value - min_val) / range_val) * 10) if range_val > 0 else 0
            bar = "█" * height
            lines.append(f"│ {bar:<50} ${value:>7.0f} │")
        
        lines.append("└" + "─" * 58 + "┘")
        return "\n".join(lines)
