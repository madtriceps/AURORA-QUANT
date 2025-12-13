# Aurora Quant v2.0 - Architecture Overview

## System Architecture

Aurora Quant is built on a modular, event-driven architecture designed for scalability and professional-grade trading operations.

### Core Components

#### 1. Event System (core/types.py)
- **MarketEvent**: Price updates and market data
- **SignalEvent**: Strategy signals (BUY/SELL/HOLD)
- **OrderEvent**: Order submission requests
- **FillEvent**: Trade execution confirmations

#### 2. Execution Engine (core/simulation.py)
- **EventQueue**: Priority-based event processing
- **BacktestEngine**: Event-driven backtester with realistic simulation
- Slippage and latency modeling
- Commission and fee calculations

#### 3. Data Pipeline (core/data_loader.py + storage/datalake.py)
- Unified market data loading (Crypto, US equities, Indian equities)
- SQLite market data lake for caching
- Multi-timeframe support (1m, 5m, 15m, 1h, 1D)

#### 4. Strategy Framework (strategies/base.py)
- Abstract `Strategy` base class
- Plugin architecture for custom strategies
- Built-in strategies: Momentum, Arbitrage

#### 5. Risk Management (core/risk.py)
- Position sizing constraints
- Leverage limits
- Drawdown monitoring
- Kill-switch mechanism

#### 6. Portfolio Manager (core/portfolio.py)
- Multi-asset position tracking
- Allocation monitoring
- Unrealized P&L calculations

#### 7. Broker Abstraction (core/broker.py)
- **PaperBroker**: Paper trading simulation
- **BinanceBroker**: Future live trading support (extensible)

### Data Flow

\`\`\`
Market Data
    ↓
DataLoader → DataLake (SQLite cache)
    ↓
BacktestEngine (Event Queue)
    ↓
Strategy (on_bar) → SignalEvent
    ↓
OrderExecutor → OrderEvent
    ↓
PaperBroker → FillEvent
    ↓
PaperLedger (Position + P&L tracking)
    ↓
PortfolioManager → Equity Curve
    ↓
RiskEngine (Check limits)
    ↓
Reports & Analytics
\`\`\`

### Module Dependencies

\`\`\`
core/
├── types.py (event definitions) - CORE
├── config.py (constants)
├── exceptions.py (errors)
├── indicators.py (technical analysis)
├── ledger.py (paper trading)
├── broker.py (execution interface)
├── portfolio.py (position tracking)
├── risk.py (risk management)
├── simulation.py (event-driven backtester) - depends on types.py, ledger.py
└── data_loader.py (market data)

strategies/
├── base.py (abstract strategy) - depends on core/types.py, core/ledger.py
├── momentum.py (momentum implementation) - depends on base.py
└── arbitrage.py (arbitrage implementation) - depends on base.py

storage/
└── datalake.py (market data persistence)

tests/
├── test_indicators.py
├── test_ledger.py
└── test_backtester.py

dashboard/
└── app.py (Streamlit UI)
\`\`\`

## Event-Driven Backtest Flow

1. **Initialization**: Load market data, create EventQueue
2. **Data Injection**: Feed market events from DataLake
3. **Event Processing**:
   - MarketEvent → Strategy.on_bar() → SignalEvent
   - SignalEvent → OrderExecutor → OrderEvent
   - OrderEvent → Broker → FillEvent
   - FillEvent → Ledger (position update, P&L)
4. **Risk Check**: RiskEngine validates position
5. **Portfolio Update**: PortfolioManager recalculates metrics
6. **Repeat** until event queue empty

## Key Design Principles

1. **Event-Driven**: Loose coupling via events, easy to extend
2. **Modular**: Each component has single responsibility
3. **Type-Safe**: Full type hints throughout
4. **Testable**: Unit tests for all major components
5. **Realistic**: Slippage, latency, fees, and leverage constraints
6. **Scalable**: Support for multi-asset, multi-strategy backtesting
