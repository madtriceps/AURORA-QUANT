# Aurora Quant Strategy Documentation

## Strategy 1: Crypto Arbitrage Engine

### Overview
Detects and simulates triangular arbitrage opportunities in cryptocurrency markets using real-time Binance data.

### How It Works
1. Fetches current prices for BTC, ETH, BNB, ADA, XRP
2. Calculates cross-pair ratios (e.g., ETH/BTC)
3. Detects deviations from expected ratios
4. Simulates execution with slippage and fees
5. Tracks P&L in paper trading ledger

### Parameters
- **Min Threshold** (0.1-1.0%): Minimum deviation to trigger trade
- **Slippage** (0.1-0.5%): Assumed market impact
- **Capital** (USD): Starting capital for simulation

### Best Practices
- Set conservative thresholds (0.15-0.25%)
- Start with small capital ($100-500)
- Monitor for false positives

### Metrics
- Opportunities Detected
- Trades Executed
- Success Rate
- Net P&L

---

## Strategy 2: Intraday Momentum

### Overview
Multi-asset momentum strategy using technical analysis on 1-minute candles.

### Signals
**Buy Signal:**
- Price > VWAP
- EMA(20) > EMA(50)
- RSI < 70 (not overbought)

**Sell Signal:**
- RSI > 70 (overbought), OR
- Price < VWAP

### Indicators
- **EMA(20/50/200)**: Trend identification
- **RSI(14)**: Momentum and overbought/oversold
- **VWAP**: Volume-weighted support/resistance
- **ATR(14)**: Position sizing based on volatility
- **MACD**: Trend confirmation

### Supported Assets
- **Crypto**: BTCUSDT, ETHUSDT (Binance)
- **US Equities**: Any ticker (yfinance)
- **Indian Equities**: Symbols with .NS (NSE) or .BO (BSE)

### Risk Profiles
- **Conservative** (1% per trade): Tight stops, small positions
- **Moderate** (2.5% per trade): Balanced approach
- **Aggressive** (5% per trade): Larger positions, wider stops

### Backtest Mode
- 3-day historical data
- 1-minute candle resolution
- Full trade logging
- Equity curve visualization

---

## Strategy 3: AI Signal Optimizer (Beta)

### Overview
Machine learning-based signal confidence scoring using logistic regression.

### Features Extracted
1. **OHLC Features**: Body size, wicks, close position
2. **Momentum Features**: RSI normalized, MACD sign, volume ratio
3. **Trend Features**: EMA alignment, price position relative to EMA, ATR ratio

### Model Training
- Logistic Regression or Random Forest
- 6 features per candle
- Binary classification (Buy/No Action)

### Output
- Signal confidence (0.0-1.0)
- Feature importance
- Predicted direction

### Future Enhancements
- Reinforcement learning for parameter optimization
- Multi-timeframe analysis
- Ensemble methods

---

## Performance Attribution

### Key Metrics
- **Sharpe Ratio**: Risk-adjusted return (target 1.0+)
- **Sortino Ratio**: Downside risk focus
- **Calmar Ratio**: Return / Max drawdown
- **Win Rate**: % winning trades
- **Profit Factor**: (Gross Win / Gross Loss)

### Trade Analysis
- Average trade duration
- Trade distribution
- Consecutive wins/losses
- Largest win/loss

---

## Parameter Optimization

To optimize strategy parameters:

\`\`\`python
from ai.optimizer import ParameterOptimizer

optimizer = ParameterOptimizer({
    'ema_short': (10, 30, 1),
    'ema_long': (40, 200, 10),
    'rsi_threshold': (30, 70, 5),
})

best_params = optimizer.random_search(objective_function, iterations=100)
\`\`\`

---

## Risk Management

### Position Sizing
Calculated based on:
- Account risk % (1-5%)
- ATR (Average True Range)
- Entry price

Formula:
\`\`\`
Position Size = (Account Risk %) / (ATR * 2)
\`\`\`

### Stop Loss
- Hard stop at 2x ATR below entry (buy trades)
- Trailing stop available for momentum trades

### Max Drawdown
- Tracked continuously
- Alerts when approaching limits
