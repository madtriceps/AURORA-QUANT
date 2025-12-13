# Aurora Quant Usage Examples

## Example 1: Run Crypto Arbitrage

\`\`\`bash
python main.py
# Select: 1
# Capital: 500
# Threshold: 0.2
# Duration: 10
\`\`\`

**Expected Output:**
\`\`\`
Running arbitrage engine for 10 minutes...
Monitoring 5 pairs: BTCUSDT, ETHUSDT, BNBUSDT, ADAUSDT, XRPUSDT
Min threshold: 0.2%

✅ Executed BTC→ETH→USDT | Profit: +0.152%

CRYPTO ARBITRAGE STRATEGY REPORT
Initial Capital:        $500.00
Final Equity:           $502.15
Total P&L:              +$2.15 (+0.43%)

Trades Executed:        1
Win Rate:               100.00%
Max Drawdown:           -0.23%

📝 Detected 3 arbitrage opportunities, executed 1 trade(s) with result: +2.15 (+0.43%).
\`\`\`

## Example 2: Run Momentum on Bitcoin

\`\`\`bash
python main.py
# Select: 2
# Asset Type: crypto
# Symbol: BTCUSDT
# Capital: 1000
# Profile: moderate
\`\`\`

**Expected Output:**
\`\`\`
Backtesting BTCUSDT on 4320 candles...

INTRADAY MOMENTUM STRATEGY REPORT
Asset: BTCUSDT
Initial Capital:        $1,000.00
Final Equity:           $1,127.42
Total P&L:              +$127.42 (+12.74%)

Trade Statistics:
Total Trades:           18
Winning Trades:         11
Losing Trades:          7
Win Rate:               61.11%

Risk Metrics:
Max Drawdown:           -4.32%
Sharpe Ratio:           1.45
Profit Factor:          2.18x

Equity Curve:
┌──────────────────────────────────────────────────────────┐
│ █                                                   $1127  │
│ ███                                                       │
│ ██████                                                    │
│ ███████████                                               │
│ ████████████████                                          │
└──────────────────────────────────────────────────────────┘

📝 BTCUSDT momentum strategy: 18 trades, 61.11% win rate, result: +127.42 (+12.74%).
\`\`\`

## Example 3: Run Momentum on Indian Stock

\`\`\`bash
python main.py
# Select: 2
# Asset Type: indian
# Symbol: INFY.NS
# Capital: 5000
# Profile: conservative
\`\`\`

**Expected Output:**
\`\`\`
Fetching INFY.NS historical data...
✅ Fetched 4320 candles

Backtesting INFY.NS on 4320 candles...

INTRADAY MOMENTUM STRATEGY REPORT
Asset: INFY.NS (Conservative Profile)
Initial Capital:        $5,000.00
Final Equity:           $5,083.17
Total P&L:              +$83.17 (+1.66%)

Trade Statistics:
Total Trades:           8
Winning Trades:         5
Losing Trades:          3
Win Rate:               62.50%

Risk Metrics:
Max Drawdown:           -1.87%
Sharpe Ratio:           0.92
\`\`\`

## Example 4: Compare Multiple Strategies

\`\`\`bash
# Run Arbitrage
Strategy 1 Result: +0.43% (1 trade)

# Run Momentum (BTC)
Strategy 2 Result: +12.74% (18 trades)

# Run Momentum (INFY)
Strategy 3 Result: +1.66% (8 trades)

# Analysis
- Momentum on BTC: Best return but higher drawdown
- Momentum on INFY: Lower return, lower drawdown
- Arbitrage: Consistent but limited opportunities
