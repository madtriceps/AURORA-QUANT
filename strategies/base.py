"""Base strategy class and framework."""
from abc import ABC, abstractmethod
from typing import Dict, List, Optional
from datetime import datetime
import pandas as pd

from core.types import SignalEvent, OrderSide
from core.ledger import PaperLedger


class Strategy(ABC):
    """Abstract base strategy class."""
    
    def __init__(self, strategy_id: str, ledger: PaperLedger):
        self.strategy_id = strategy_id
        self.ledger = ledger
        self.signals: List[SignalEvent] = []
        self.parameters: Dict = {}
        self.warm_up_complete = False
    
    @abstractmethod
    def on_bar(self, symbol: str, bar: Dict) -> Optional[SignalEvent]:
        """Called on each new bar. Return signal if generated."""
        pass
    
    def generate_signal(self, symbol: str, signal: str, confidence: float,
                       reason: str = "") -> SignalEvent:
        """Generate a signal event."""
        event = SignalEvent(
            timestamp=datetime.now(),
            strategy_id=self.strategy_id,
            symbol=symbol,
            signal=signal,
            confidence=min(1.0, max(0.0, confidence)),
            reason=reason,
            parameters=self.parameters.copy()
        )
        self.signals.append(event)
        return event
    
    def get_signal_stats(self) -> Dict:
        """Get signal generation statistics."""
        return {
            'total_signals': len(self.signals),
            'buy_signals': len([s for s in self.signals if s.signal == "BUY"]),
            'sell_signals': len([s for s in self.signals if s.signal == "SELL"]),
            'hold_signals': len([s for s in self.signals if s.signal == "HOLD"]),
            'avg_confidence': sum(s.confidence for s in self.signals) / len(self.signals) if self.signals else 0,
        }
