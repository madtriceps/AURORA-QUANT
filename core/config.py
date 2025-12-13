"""
Configuration and constants for Aurora Quant.
Supports local + cloud deployments with provider abstraction.
"""

import os
from typing import Dict

# =============================================================================
# ENVIRONMENT
# =============================================================================

# local | cloud (default: cloud-safe)
AURORA_ENV = os.getenv("AURORA_ENV", "cloud")

# =============================================================================
# DATA PROVIDERS
# =============================================================================

# Auto-select crypto provider
# - local  → Binance allowed
# - cloud  → Geo-safe provider
CRYPTO_DATA_PROVIDER = os.getenv(
    "AURORA_CRYPTO_PROVIDER",
    "binance" if AURORA_ENV == "local" else "yfinance"
)

# =============================================================================
# BINANCE (OPTIONAL – LOCAL ONLY)
# =============================================================================

BINANCE_API = "https://api.binance.com/api/v3"
BINANCE_WSAPI = "wss://stream.binance.com:9443/ws"

# Raw Binance symbols (kept for local / websocket mode)
CRYPTO_PAIRS = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "ADAUSDT", "XRPUSDT"]

# =============================================================================
# NORMALIZED CRYPTO ASSETS (CLOUD SAFE)
# =============================================================================

# Unified symbols used by yfinance / fallback providers
CRYPTO_ASSETS = {
    "BTC": "BTC-USD",
    "ETH": "ETH-USD",
    "BNB": "BNB-USD",
    "ADA": "ADA-USD",
    "XRP": "XRP-USD",
}

# =============================================================================
# RISK MANAGEMENT
# =============================================================================

DEFAULT_SLIPPAGE = 0.002   # 0.2%
DEFAULT_FEES = 0.001      # 0.1%

RISK_PROFILES: Dict[str, float] = {
    "conservative": 1.0,
    "moderate": 2.5,
    "aggressive": 5.0,
}

# =============================================================================
# INDICATORS
# =============================================================================

EMA_PERIODS = [20, 50, 200]
RSI_PERIOD = 14
VWAP_ENABLED = True
MACD_FAST = 12
MACD_SLOW = 26
MACD_SIGNAL = 9
ATR_PERIOD = 14

# =============================================================================
# ASSET CLASSES
# =============================================================================

ASSET_CLASSES = {
    "crypto": "Cryptocurrency",
    "indian": "Indian Equities (NSE/BSE)",
    "us": "US Equities",
}
