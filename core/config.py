"""Configuration and constants for Aurora Quant."""
from typing import Dict

# API Endpoints
BINANCE_API = "https://api.binance.com/api/v3"
BINANCE_WSAPI = "wss://stream.binance.com:9443/ws"

# Crypto pairs
CRYPTO_PAIRS = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "ADAUSDT", "XRPUSDT"]

# Risk management
DEFAULT_SLIPPAGE = 0.002  # 0.2%
DEFAULT_FEES = 0.001  # 0.1%

# Indicator periods
EMA_PERIODS = [20, 50, 200]
RSI_PERIOD = 14
VWAP_ENABLED = True
MACD_FAST = 12
MACD_SLOW = 26
MACD_SIGNAL = 9
ATR_PERIOD = 14

# Risk profiles
RISK_PROFILES: Dict[str, float] = {
    "conservative": 1.0,
    "moderate": 2.5,
    "aggressive": 5.0,
}

# Asset classes
ASSET_CLASSES = {
    "crypto": "Cryptocurrency",
    "indian": "Indian Equities (NSE/BSE)",
    "us": "US Equities",
}
