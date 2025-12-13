"""Aurora Quant - Strategy Module"""
from strategies.base import Strategy
from strategies.momentum import MomentumStrategy
from strategies.arbitrage import TriangularArbitrageStrategy

__all__ = [
    "Strategy",
    "MomentumStrategy",
    "TriangularArbitrageStrategy",
]
