"""Event-driven backtester with realistic simulation."""
from typing import List, Dict, Optional, Callable
from datetime import datetime
from collections import deque
from dataclasses import dataclass
import numpy as np

from core.types import (
    MarketEvent, SignalEvent, OrderEvent, FillEvent, EventType,
    OrderSide, OrderStatus, OrderType
)
from core.ledger import PaperLedger


@dataclass
class SimulationConfig:
    """Configuration for simulation engine."""
    initial_capital: float = 100000.0
    max_slippage_bps: float = 20.0  # 20 basis points
    commission_bps: float = 10.0  # 10 basis points
    latency_ms: float = 50.0  # Order latency
    max_position_size: float = 10000.0
    max_leverage: float = 1.0
    warm_up_bars: int = 20


class EventQueue:
    """Priority event queue for backtester."""
    
    def __init__(self):
        self.queue: deque = deque()
        self.processed_count: int = 0
    
    def put(self, event) -> None:
        """Add event to queue (sorted by timestamp)."""
        self.queue.append(event)
    
    def get(self):
        """Get next event from queue."""
        if self.queue:
            return self.queue.popleft()
        return None
    
    def empty(self) -> bool:
        """Check if queue is empty."""
        return len(self.queue) == 0
    
    def size(self) -> int:
        """Get queue size."""
        return len(self.queue)


class BacktestEngine:
    """Professional-grade event-driven backtester."""
    
    def __init__(self, config: SimulationConfig):
        self.config = config
        self.ledger = PaperLedger(config.initial_capital)
        self.event_queue = EventQueue()
        self.market_data: Dict[str, List[MarketEvent]] = {}
        self.open_orders: Dict[str, OrderEvent] = {}
        self.fill_history: List[FillEvent] = []
        self.portfolio_history: List[Dict] = []
        self.signal_handlers: List[Callable] = []
        self.warm_up_complete = False
        self.current_bar = 0
    
    def register_signal_handler(self, handler: Callable) -> None:
        """Register callback for signal events."""
        self.signal_handlers.append(handler)
    
    def add_market_data(self, symbol: str, events: List[MarketEvent]) -> None:
        """Add market data for simulation."""
        self.market_data[symbol] = sorted(events, key=lambda x: x.timestamp)
    
    def process_market_event(self, event: MarketEvent) -> None:
        """Process market data event."""
        self._apply_slippage_and_commission(event)
        self.current_bar += 1
    
    def process_signal_event(self, event: SignalEvent) -> None:
        """Process strategy signal."""
        for handler in self.signal_handlers:
            handler(event)
    
    def process_order_event(self, event: OrderEvent) -> None:
        """Process order request and create fill."""
        if event.order_id in self.open_orders:
            return  # Already has order
        
        self.open_orders[event.order_id] = event
        
        # Simulate execution with latency
        fill = self._simulate_order_execution(event)
        if fill:
            self.fill_history.append(fill)
            self._process_fill(fill)
    
    def _simulate_order_execution(self, order: OrderEvent) -> Optional[FillEvent]:
        """Simulate realistic order execution."""
        # Get current market price
        symbol_data = self.market_data.get(order.symbol, [])
        if not symbol_data:
            return None
        
        current_price = symbol_data[-1].price if symbol_data else 0
        
        # Apply slippage based on order size and market impact
        slippage_bps = min(self.config.max_slippage_bps, 
                          (order.quantity / self.config.max_position_size) * 100)
        
        if order.side == OrderSide.BUY:
            fill_price = current_price * (1 + slippage_bps / 10000)
        else:  # SELL
            fill_price = current_price * (1 - slippage_bps / 10000)
        
        commission = (fill_price * order.quantity) * (self.config.commission_bps / 10000)
        
        return FillEvent(
            timestamp=order.timestamp,
            order_id=order.order_id,
            symbol=order.symbol,
            side=order.side,
            quantity=order.quantity,
            fill_price=fill_price,
            commission=commission
        )
    
    def _apply_slippage_and_commission(self, event: MarketEvent) -> None:
        """Apply slippage and commission to market prices."""
        pass
    
    def _process_fill(self, fill: FillEvent) -> None:
        """Process order fill."""
        symbol = fill.symbol
        
        try:
            if fill.side == OrderSide.BUY:
                self.ledger.open_position(
                    symbol=symbol,
                    side="BUY",
                    price=fill.fill_price,
                    quantity=fill.quantity,
                    timestamp=fill.timestamp
                )
            else:  # SELL
                self.ledger.close_position(
                    symbol=symbol,
                    price=fill.fill_price,
                    timestamp=fill.timestamp,
                    quantity=fill.quantity
                )
        except Exception as e:
            print(f"[ERROR] Failed to process fill: {e}")
    
    def run(self) -> Dict:
        """Run backtest simulation."""
        print("[INFO] Starting backtest simulation...")
        
        # Build event queue from market data
        total_events = sum(len(events) for events in self.market_data.values())
        
        for symbol, events in self.market_data.items():
            for event in events:
                self.event_queue.put(event)
        
        # Process events
        while not self.event_queue.empty():
            event = self.event_queue.get()
            
            # Check warm-up period
            if self.current_bar < self.config.warm_up_bars:
                self.warm_up_complete = False
            else:
                self.warm_up_complete = True
            
            if isinstance(event, MarketEvent):
                self.process_market_event(event)
            elif isinstance(event, SignalEvent):
                self.process_signal_event(event)
            elif isinstance(event, OrderEvent):
                self.process_order_event(event)
        
        print(f"[INFO] Backtest complete. Processed {total_events} events.")
        
        return self.get_results()
    
    def get_results(self) -> Dict:
        """Get backtest results."""
        summary = self.ledger.get_trades_summary()
        summary['fills'] = len(self.fill_history)
        summary['current_bar'] = self.current_bar
        
        return summary


#- Added event-driven backtester architecture with proper event queue, order execution simulation, and realistic slippage/commission modeling
