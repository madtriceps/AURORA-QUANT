# Dual-Mode Trading Simulator MVP

A minimal but fully functional Python-based trading simulator with two independent modes:
- **Crypto Arbitrage**: Real-time triangular arbitrage detection
- **Intraday Momentum**: Technical analysis-based momentum strategy backtester

## Quick Start

### Installation

\`\`\`bash
# Clone or download this project
cd trading-simulator

# Install dependencies
pip install -r requirements.txt
\`\`\`

### Running

\`\`\`bash
python main.py
\`\`\`

Follow the CLI prompts to select a mode and configure parameters.

## Architecture

\`\`\`
trading-simulator/
├── main.py                 # CLI interface & mode selector
├── arbitrage.py            # Crypto arbitrage mode
├── momentum.py             # Momentum strategy mode
├── requirements.txt        # Dependencies
├── README.md              # This file
└── utils/
    ├── ledger.py          # Paper trading engine
    ├── indicators.py      # Technical indicators
    └── summary.py         # Report generation
\`\`\`

## Modes

### Mode 1: Crypto Arbitrage

Detects triangular arbitrage opportunities in real-time using Binance public market data.

**Inputs:**
- Starting capital (USD)
- Min arbitrage threshold (%)
- Duration (minutes)

**Outputs:**
- Detected opportunities
- Executed trades
- P&L Summary
- Max drawdown

**Example Run:**
\`\`\`
Starting capital: $1000
Min threshold: 0.1%
Duration: 10 minutes

Result:
✅ 3 opportunities detected
✅ 1 trade executed
📊 Net P&L: +$2.13 (+0.21%)
\`\`\`

### Mode 2: Intraday Momentum

Backtests a momentum strategy using 1-minute candles over 3 days.

**Strategy Rules:**
- BUY: Price crosses above VWAP + EMA(20) uptrend
- SELL: RSI > 70 or price falls below VWAP
- Risk: 1-5% per trade (based on aggressiveness)

**Inputs:**
- Trading symbol (e.g., BTCUSDT)
- Starting capital (USD)
- Aggressiveness (low/medium/high)

**Outputs:**
- Number of trades
- Win rate
- Total P&L
- Equity curve (ASCII chart)
- Max drawdown

**Example Run:**
\`\`\`
Symbol: BTCUSDT
Capital: $10000
Aggressiveness: medium

Result:
✅ 14 trades executed
📈 Win rate: 57.1%
💰 Net P&L: +$180.50 (+1.81%)
\`\`\`

## Technical Indicators

- **EMA(20)**: Exponential Moving Average for trend
- **RSI(14)**: Relative Strength Index for overbought/oversold
- **VWAP**: Volume Weighted Average Price for support/resistance
- **Volume Spike**: Detects abnormal volume for confirmation

## Paper Trading Engine

- Tracks positions, P&L, drawdown
- Simulates slippage (arbitrage mode)
- Supports both BUY and SELL operations
- Maintains running equity and cash balance

## Data Sources

- **Binance Public API** (free, no authentication required)
- Real-time ticker data for arbitrage detection
- Historical 1-minute candles for momentum backtesting

## Notes

- All trading is simulated (paper trading only)
- No real money or orders executed
- Results are for educational purposes
- Backtests assume perfect execution (no slippage in momentum mode)

## Requirements

- Python 3.8+
- Dependencies: websockets, requests, pandas, numpy, matplotlib

## Troubleshooting

**"Connection refused" error:**
- Check internet connection
- Verify Binance API is accessible

**"Insufficient data" warning:**
- Wait for more candles to load
- Try a different symbol or longer duration

**No trades executed:**
- Try lowering arbitrage threshold
- Check symbol format (e.g., BTCUSDT, ETHUSDT)
