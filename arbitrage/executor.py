"""Trade execution simulator with realistic modeling."""
from datetime import datetime
from typing import Dict, Optional
import random
from core.ledger import Trade


class ExecutionSimulator:
    """Simulates trade execution with realistic parameters."""
    
    def __init__(self, slippage: float = 0.002, latency_ms: int = 50):
        self.slippage = slippage
        self.latency_ms = latency_ms
        self.execution_log = []

    def simulate_market_order(self, symbol: str, side: str, price: float,
                             quantity: float, timestamp: datetime) -> Dict:
        """Simulate a market order execution."""
        # Add slippage
        slippage_pct = random.uniform(0, self.slippage * 2)
        if side == "BUY":
            execution_price = price * (1 + slippage_pct)
        else:  # SELL
            execution_price = price * (1 - slippage_pct)
        
        # Add latency
        latency = random.uniform(0, self.latency_ms) / 1000
        
        execution = {
            'symbol': symbol,
            'side': side,
            'requested_price': price,
            'execution_price': execution_price,
            'quantity': quantity,
            'slippage_pct': slippage_pct * 100,
            'latency_ms': latency * 1000,
            'timestamp': timestamp,
            'status': 'executed',
        }
        
        self.execution_log.append(execution)
        return execution

    def simulate_limit_order(self, symbol: str, side: str, price: float,
                            quantity: float, timeout_ms: int = 5000) -> Optional[Dict]:
        """Simulate a limit order (may not fill)."""
        # Randomly determine if order fills (simplified)
        fill_probability = 0.7
        
        if random.random() > fill_probability:
            return None  # Order didn't fill
        
        return {
            'symbol': symbol,
            'side': side,
            'price': price,
            'quantity': quantity,
            'status': 'filled',
            'timestamp': datetime.now(),
        }
