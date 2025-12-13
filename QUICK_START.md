# Quick Start Guide

## 5-Minute Setup

### 1. Install

\`\`\`bash
git clone https://github.com/auroraquant/aurora-quant.git
cd aurora-quant
pip install -r requirements.txt
\`\`\`

### 2. Run

\`\`\`bash
python main.py
# Select option 2: Momentum Strategy Backtest
# Enter: BTCUSDT, $10,000, moderate aggressiveness
\`\`\`

### 3. View Results

\`\`\`
Performance Metrics:
  Total Trades: 42
  Win Rate: 65.2%
  Total P&L: +$285.50
  Return: 2.86%
  Max Drawdown: 8.2%
  Sharpe Ratio: 1.45
\`\`\`

## Next Steps

### Run Dashboard

\`\`\`bash
streamlit run dashboard/app.py
# Open http://localhost:8501
\`\`\`

### Run Tests

\`\`\`bash
pytest tests/ -v
\`\`\`

### Build Custom Strategy

Create \`my_strategy.py\`:

\`\`\`python
from strategies.base import Strategy

class MyStrategy(Strategy):
    def on_bar(self, symbol, bar):
        if bar['close'] > 100:
            return self.generate_signal(symbol, "BUY", 0.8)
        return None
\`\`\`

### Learn More

- Architecture: \`docs/ARCHITECTURE.md\`
- Strategies: \`STRATEGIES.md\`
- API: \`API_REFERENCE.md\`
- Examples: \`EXAMPLES.md\`

\`\`\`
