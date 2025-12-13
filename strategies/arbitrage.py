"""Triangular arbitrage strategy."""
from typing import Optional, Dict, List, Tuple
import itertools

from strategies.base import Strategy


class TriangularArbitrageStrategy(Strategy):
    """Detect triangular arbitrage opportunities."""
    
    def __init__(self, strategy_id: str = "arbitrage", ledger=None,
                 min_profit_bps: float = 10.0):
        super().__init__(strategy_id, ledger)
        self.min_profit_bps = min_profit_bps
        self.exchange_rates: Dict[str, float] = {}
        self.opportunities: List[Dict] = []
    
    def update_prices(self, prices: Dict[str, float]) -> None:
        """Update exchange rates."""
        self.exchange_rates = prices.copy()
    
    def detect_opportunities(self, assets: List[str]) -> List[Tuple]:
        """Find triangular arbitrage paths."""
        if len(assets) < 3:
            return []
        
        opportunities = []
        
        # Generate all 3-asset combinations
        for combo in itertools.combinations(assets, 3):
            asset_a, asset_b, asset_c = combo
            
            # Path 1: A -> B -> C -> A
            path1 = self._calculate_path(asset_a, asset_b, asset_c)
            if path1 and path1[0] > self.min_profit_bps:
                opportunities.append({
                    'path': f"{asset_a} -> {asset_b} -> {asset_c} -> {asset_a}",
                    'profit_bps': path1[0],
                    'rate': path1[1]
                })
            
            # Path 2: A -> C -> B -> A
            path2 = self._calculate_path(asset_a, asset_c, asset_b)
            if path2 and path2[0] > self.min_profit_bps:
                opportunities.append({
                    'path': f"{asset_a} -> {asset_c} -> {asset_b} -> {asset_a}",
                    'profit_bps': path2[0],
                    'rate': path2[1]
                })
        
        return opportunities
    
    def _calculate_path(self, asset_a: str, asset_b: str, asset_c: str) -> Optional[Tuple]:
        """Calculate profit for a 3-leg arbitrage path."""
        # Get exchange rates (simplified - would need proper pair matching)
        pair1 = f"{asset_a}{asset_b}"
        pair2 = f"{asset_b}{asset_c}"
        pair3 = f"{asset_c}{asset_a}"
        
        rate1 = self.exchange_rates.get(pair1, 0)
        rate2 = self.exchange_rates.get(pair2, 0)
        rate3 = self.exchange_rates.get(pair3, 0)
        
        if rate1 <= 0 or rate2 <= 0 or rate3 <= 0:
            return None
        
        # Calculate triangular rate
        triangular_rate = rate1 * rate2 * rate3
        profit_percent = (triangular_rate - 1.0) * 100 * 100  # Convert to basis points
        
        if profit_percent > 0:
            return (profit_percent, triangular_rate)
        
        return None
    
    def on_bar(self, symbol: str, bar: Dict) -> Optional:
        """Arbitrage doesn't use bar data directly."""
        return None
