"""Advanced analytics and performance attribution."""
from typing import Dict, List
import numpy as np


class PerformanceAnalytics:
    """Calculate advanced performance metrics."""
    
    @staticmethod
    def calculate_sortino_ratio(returns: List[float], target_return: float = 0.0) -> float:
        """Calculate Sortino ratio (focuses on downside deviation)."""
        if len(returns) < 2:
            return 0.0
        
        downside_returns = [r for r in returns if r < target_return]
        if not downside_returns:
            return 0.0
        
        downside_deviation = np.std(downside_returns)
        excess_return = np.mean(returns) - target_return
        
        return excess_return / downside_deviation if downside_deviation > 0 else 0.0
    
    @staticmethod
    def calculate_calmar_ratio(total_return: float, max_drawdown: float) -> float:
        """Calculate Calmar ratio (return / max drawdown)."""
        if max_drawdown == 0:
            return 0.0
        return abs(total_return / max_drawdown)
    
    @staticmethod
    def calculate_recovery_factor(total_pnl: float, max_drawdown_amount: float) -> float:
        """Recovery factor = net profit / max drawdown amount."""
        if max_drawdown_amount == 0:
            return 0.0
        return total_pnl / max_drawdown_amount
    
    @staticmethod
    def analyze_trade_distribution(trades: List[Dict]) -> Dict:
        """Analyze trade duration and frequency."""
        if not trades:
            return {}
        
        durations = []
        for trade in trades:
            if trade.get('entry_time') and trade.get('exit_time'):
                duration = (trade['exit_time'] - trade['entry_time']).total_seconds() / 60
                durations.append(duration)
        
        return {
            'avg_trade_duration_min': np.mean(durations) if durations else 0,
            'median_trade_duration_min': np.median(durations) if durations else 0,
            'max_trade_duration_min': max(durations) if durations else 0,
        }
