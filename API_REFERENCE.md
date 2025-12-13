# Aurora Quant API Reference

## Core Module

### config.py
Configuration constants and profiles.

\`\`\`python
from core.config import RISK_PROFILES, CRYPTO_PAIRS, DEFAULT_SLIPPAGE

# Available risk profiles
RISK_PROFILES = {
    "conservative": 1.0,    # 1% per trade
    "moderate": 2.5,        # 2.5% per trade
    "aggressive": 5.0,      # 5% per trade
}

# Monitored crypto pairs
CRYPTO_PAIRS = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "ADAUSDT", "XRPUSDT"]

# Default parameters
DEFAULT_SLIPPAGE = 0.002  # 0.2%
DEFAULT_FEES = 0.001      # 0.1%
\`\`\`

### ledger.py
Paper trading ledger with advanced metrics.

\`\`\`python
from core.ledger import PaperLedger, Trade

# Initialize ledger
ledger = PaperLedger(initial_capital=5000, strategy_id="my_strategy")

# Open position
trade = ledger.open_position(
    symbol="BTCUSDT",
    side="BUY",
    price=43000,
    quantity=0.1,
    timestamp=datetime.now()
)

# Close position
closed = ledger.close_position(
    symbol="BTCUSDT",
    price=43500,
    timestamp=datetime.now()
)

# Get metrics
summary = ledger.get_trades_summary()
print(f"P&L: {summary['total_pnl']}")
print(f"Sharpe: {summary['sharpe_ratio']}")
print(f"Max DD: {summary['max_drawdown']}%")
\`\`\`

### indicators.py
Technical indicator calculations.

\`\`\`python
from core.indicators import (
    calculate_ema, calculate_rsi, calculate_vwap,
    calculate_atr, calculate_macd, detect_volume_spike
)

prices = [100, 101, 102, 103, 104]
ema = calculate_ema(prices, period=3)

volumes = [1000, 1100, 1200, 5000, 1150]
is_spike = detect_volume_spike(volumes, period=20, threshold=1.5)

highs = [105, 106, 107]
lows = [99, 100, 101]
closes = [102, 103, 104]
volumes = [1000, 1100, 1200]
vwap = calculate_vwap(highs, lows, closes, volumes)
\`\`\`

### data_loader.py
Multi-source market data loading.

\`\`\`python
from core.data_loader import DataLoader

# Fetch crypto candles
candles = DataLoader.fetch_crypto_candles("BTCUSDT", days=3)

# Fetch equity candles
candles = DataLoader.fetch_equity_candles("AAPL", period="3d")
candles = DataLoader.fetch_equity_candles("INFY.NS", period="7d")

# Fetch current prices
prices = DataLoader.fetch_prices(["BTCUSDT", "ETHUSDT", "AAPL", "INFY.NS"])
\`\`\`

## Arbitrage Module

### arbitrage/engine.py
Crypto arbitrage engine.

\`\`\`python
from arbitrage.engine import ArbitrageEngine
import asyncio

engine = ArbitrageEngine(
    capital=1000,
    min_threshold=0.2,
    slippage=0.002
)

summary = asyncio.run(engine.run_engine(duration_minutes=10))
print(f"Opportunities: {summary['opportunities_detected']}")
print(f"Executed: {summary['trades_executed']}")
print(f"P&L: {summary['ledger_summary']['total_pnl']}")
\`\`\`

## Momentum Module

### momentum/engine.py
Multi-asset momentum strategy.

\`\`\`python
from momentum.engine import MomentumEngine

engine = MomentumEngine(
    symbol="BTCUSDT",
    capital=5000,
    profile="moderate",
    asset_type="crypto"
)

engine.load_data(days=3)
summary = engine.run_backtest()

print(engine.get_equity_curve_ascii())
print(f"Trades: {summary['ledger_summary']['closed_trades']}")
print(f"Win Rate: {summary['ledger_summary']['win_rate']}%")
\`\`\`

## AI Module

### ai/model.py
ML-based signal scoring.

\`\`\`python
from ai.model import SignalScorer

scorer = SignalScorer(model_type="logistic")

# Training data
X = [[1, 0, 0.5, ...], ...]  # Features
y = [1, 0, 1, ...]             # Labels

scorer.train(X, y)

# Score new signal
confidence = scorer.score_signal(candle_data)
print(f"Signal confidence: {confidence:.2f}")
\`\`\`

### ai/optimizer.py
Strategy parameter optimization.

\`\`\`python
from ai.optimizer import ParameterOptimizer

optimizer = ParameterOptimizer({
    'ema_short': (10, 30, 1),
    'ema_long': (40, 200, 10),
})

def objective(params):
    # Run strategy with params
    # Return profit or Sharpe ratio
    return 0.15

best_params = optimizer.random_search(objective, iterations=100)
\`\`\`

## Utils Module

### utils/summary.py
Professional reporting.

\`\`\`python
from utils.summary import (
    print_investor_header,
    print_strategy_report,
    generate_summary_text
)

print_investor_header()
print_strategy_report(summary, "Momentum Strategy", "3-day backtest")
print(generate_summary_text(summary, "momentum"))
\`\`\`
\`\`\`
