# Aurora Quant - Troubleshooting Guide

## Common Issues

### Issue: "No module named 'requests'"

**Solution:**
\`\`\`bash
pip install requests
\`\`\`

### Issue: "Failed to fetch prices from Binance"

**Causes:**
1. Internet connectivity issue
2. Binance API temporarily down
3. Firewall blocking access

**Solution:**
\`\`\`bash
# Test connectivity
ping api.binance.com

# Check with curl
curl -s https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT
\`\`\`

### Issue: "Insufficient data" error when running momentum strategy

**Solution:**
- The symbol may not have enough 1-minute candles
- Try with a symbol that has active trading
- Increase the lookback period: `engine.load_data(days=7)`

### Issue: "yfinance download failed"

**Solution:**
\`\`\`bash
pip install --upgrade yfinance
\`\`\`

### Issue: Memory error with large backtests

**Solution:**
- Reduce candle history: `engine.load_data(days=3)`
- Use lower resolution: change interval to `5m`

### Issue: "No trades executed" in momentum strategy

**Causes:**
1. Strategy parameters too restrictive
2. Market conditions don't match signal criteria
3. Volatility too low

**Solution:**
- Try different risk profile: `profile="aggressive"`
- Adjust EMA periods in `core/config.py`
- Backtest on different symbols

## Debug Mode

Enable debug output:

\`\`\`python
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.debug(f"Current price: {price}")
\`\`\`

## Performance Optimization

### For Large Backtests

\`\`\`python
# Use NumPy operations instead of lists
prices = np.array(prices)
ema = calculate_ema(prices, 20)

# Batch data loading
candles = DataLoader.fetch_crypto_candles("BTCUSDT", days=7)
\`\`\`

### For Real-time Streaming

\`\`\`python
# Use asyncio for concurrent feeds
from arbitrage.feed import FeedManager

feed_mgr = FeedManager()
feed_mgr.create_feed("crypto", CRYPTO_PAIRS)
asyncio.run(feed_mgr.run_all())
\`\`\```

## Platform Limits

- Max backtest period: 30 days (API limits)
- Max concurrent symbols: 10-20
- Data refresh interval: 1-5 seconds
- Max trades per session: Unlimited

## Getting Help

1. Check logs in `main.py` output
2. Review configuration in `core/config.py`
3. Check STRATEGIES.md for parameter guidelines
4. Search closed issues in documentation
\`\`\`
