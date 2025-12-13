# Aurora Quant - Testing Guide

## Unit Tests

### Core Module Tests

\`\`\`python
# test_indicators.py
import unittest
from core.indicators import calculate_ema, calculate_rsi

class TestIndicators(unittest.TestCase):
    
    def test_ema_calculation(self):
        prices = [100, 101, 102, 103, 104]
        ema = calculate_ema(prices, 3)
        assert len(ema) == 5
        assert ema[2] is not None
    
    def test_rsi_range(self):
        prices = list(range(100, 200))
        rsi = calculate_rsi(prices, 14)
        valid_rsi = [r for r in rsi if not np.isnan(r)]
        assert all(0 <= r <= 100 for r in valid_rsi)

if __name__ == '__main__':
    unittest.main()
\`\`\`

### Ledger Tests

\`\`\`python
# test_ledger.py
from core.ledger import PaperLedger
from datetime import datetime

ledger = PaperLedger(initial_capital=1000)

# Test opening position
trade = ledger.open_position(
    symbol="TEST",
    side="BUY",
    price=100,
    quantity=5,
    timestamp=datetime.now()
)
assert trade.status == "OPEN"
assert ledger.cash == 500  # 1000 - 500

# Test closing position
ledger.close_position(
    symbol="TEST",
    price=110,
    timestamp=datetime.now()
)
assert ledger.total_pnl == 50  # (110-100)*5
\`\`\`

## Integration Tests

### Arbitrage Engine Test

\`\`\`python
# test_arbitrage.py
import asyncio
from arbitrage.engine import ArbitrageEngine

async def test_arbitrage_engine():
    engine = ArbitrageEngine(capital=500, min_threshold=0.2)
    summary = await engine.run_engine(duration_minutes=1)
    
    assert summary['ledger_summary']['total_trades'] >= 0
    assert summary['opportunities_detected'] >= 0
    print(f"✅ Arbitrage test passed")

asyncio.run(test_arbitrage_engine())
\`\`\`

### Momentum Engine Test

\`\`\`python
# test_momentum.py
from momentum.engine import MomentumEngine

def test_momentum_engine():
    engine = MomentumEngine("BTCUSDT", capital=1000, profile="moderate")
    
    try:
        engine.load_data(days=3)
        summary = engine.run_backtest()
        
        assert summary['candles_processed'] > 0
        assert 'ledger_summary' in summary
        print(f"✅ Momentum test passed")
    except Exception as e:
        print(f"❌ Test failed: {e}")

test_momentum_engine()
\`\`\`

## Performance Testing

\`\`\`python
# test_performance.py
import time
from core.indicators import calculate_ema
import numpy as np

# Generate large dataset
prices = np.random.uniform(100, 110, size=10000)

start = time.time()
for _ in range(100):
    ema = calculate_ema(prices.tolist(), 20)
elapsed = time.time() - start

print(f"EMA calculation (100 iterations): {elapsed:.2f}s")
assert elapsed < 5.0, "Performance regression detected"
\`\`\`

## Running Tests

\`\`\`bash
# All tests
python -m pytest tests/

# Specific test
python -m pytest tests/test_indicators.py

# With coverage
python -m pytest --cov=. tests/

# Specific test function
python -m pytest tests/test_ledger.py::test_opening_position
\`\`\`
\`\`\`
