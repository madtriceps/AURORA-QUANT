# Backtesting Philosophy & Best Practices

## Core Principles

### 1. Realism First
Every backtest must simulate real-world conditions:
- **Slippage**: Market impact and execution delay
- **Commissions**: Trading fees (default 10 bps)
- **Latency**: Order processing delay (default 50ms)
- **Partial Fills**: Orders may not execute at limit price
- **Bid-Ask Spread**: Don't assume mid-price execution

### 2. Avoid Look-Ahead Bias
- Don't use future data in indicators
- Warm-up period for historical data
- Use only bar close before next bar opens

### 3. Account for Market Frictions
- Position sizing affects slippage
- Larger orders have higher impact
- Commissions compound over time

### 4. Risk-Adjusted Returns
- Return alone doesn't tell full story
- Use Sharpe ratio, Sortino ratio, Calmar
- Maximum drawdown is critical metric

## Best Practices

### Data Quality
\`\`\`python
# Good: Validate data before backtest
if len(candles) < 100:
    raise ValueError("Insufficient data")

# Bad: Silently use empty data
candles = []  # No validation
\`\`\`

### Parameter Optimization
\`\`\`python
# Good: Use out-of-sample testing
train_data = data[:len(data)//2]
test_data = data[len(data)//2:]

strategy.fit(train_data)
results = strategy.backtest(test_data)

# Bad: Optimize on full dataset
strategy.fit(data)
results = strategy.backtest(data)  # Overfitting!
\`\`\`

### Portfolio Construction
\`\`\`python
# Good: Account for portfolio constraints
max_leverage = 1.5
max_position = 10000
max_daily_loss = 5.0

# Bad: Unconstrained
position_size = unlimited
leverage = unlimited
\`\`\`

### Risk Management
\`\`\`python
# Good: Implement stops
if drawdown > max_drawdown:
    close_all_positions()

# Bad: Hope it rebounds
continue_trading_during_drawdown()
\`\`\`

## Common Pitfalls

### 1. Survivorship Bias
**Problem**: Only test on assets that survived
**Solution**: Include delisted/bankrupt securities

### 2. Data Mining Bias
**Problem**: Overfit by testing many strategies
**Solution**: Use walk-forward validation

### 3. Liquidity Bias
**Problem**: Assume can trade unlimited size
**Solution**: Apply slippage based on volume

### 4. Timing Luck
**Problem**: Strategy works only on test period
**Solution**: Test on multiple non-overlapping periods

### 5. Rebalancing Bias
**Problem**: Rebalance at favorable times
**Solution**: Fixed schedule (daily/weekly/monthly)

## Validation Checklist

Before deploying strategy:

- [ ] Sufficient historical data (>1 year recommended)
- [ ] Commissions and slippage included
- [ ] Out-of-sample test shows same performance
- [ ] Drawdown acceptable for risk tolerance
- [ ] Sharpe ratio > 1.0 (ideally > 1.5)
- [ ] Win rate > 50% for mean reversion
- [ ] Max consecutive losses < portfolio size
- [ ] Performance stable across subperiods
- [ ] No look-ahead bias in indicators
- [ ] Risk controls tested and active

## Performance Interpretation

### Good Results
- Sharpe > 1.5: Excellent
- Win rate > 60%: Strong
- Profit factor > 2.0: Excellent
- Max drawdown < 15%: Acceptable
- Return > 10% CAGR: Strong

### Red Flags
- Single large winning trade driving results
- All profit in one month
- Drawdown never recovered from
- Performance deteriorates over time
- Parameter sensitivity extreme

## Risk Metrics Explained

**Sharpe Ratio**: Return per unit of risk
- Formula: (Avg Return - Risk-Free Rate) / Volatility
- Higher is better (>1.0 is good)

**Sortino Ratio**: Like Sharpe but penalizes downside only
- More relevant than Sharpe for risk management

**Calmar Ratio**: CAGR / Max Drawdown
- Formula: (Cumulative Return) / Max Drawdown
- Higher is better (>1.0 is good)

**Maximum Drawdown**: Peak to trough decline
- Critical for risk management
- Must be acceptable to you emotionally

**Win Rate**: % of profitable trades
- Doesn't tell full story (size matters)
- 40% win rate OK if avg win > 2x avg loss

**Profit Factor**: Total wins / Total losses
- >1.5 is good, >2.0 is excellent
- Must cover commissions

## Transition to Live Trading

### Before Going Live

1. **Paper Trading**: Run strategy on live data (no money)
2. **Micro Allocation**: Start with 5-10% of capital
3. **Monitor Closely**: Watch first 50 trades
4. **Same Conditions**: Use same risk parameters
5. **Track Metrics**: Ensure live ≈ backtest

### Expect Degradation

Live performance typically 20-40% worse than backtest due to:
- Real slippage (higher than assumed)
- Real commissions (varies by market)
- Execution delays
- Market regime changes
- Emotional decision-making

\`\`\`
\`\`\`
