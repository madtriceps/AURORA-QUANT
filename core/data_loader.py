"""Multi-asset data loading engine."""
import requests
import pandas as pd
from typing import List, Dict, Optional
from datetime import datetime
import yfinance as yf
from core.exceptions import DataFetchError
from core.config import BINANCE_API
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataLoader:
    """Load market data from various sources."""

    @staticmethod
    def fetch_crypto_candles(symbol: str, interval: str = "1m",
                             days: int = 3, limit: int = 1000) -> List[Dict]:
        """Fetch Binance crypto candles."""
        try:
            end_time = int(datetime.now().timestamp() * 1000)
            start_time = end_time - (days * 24 * 60 * 60 * 1000)

            url = f"{BINANCE_API}/klines"
            params = {
                'symbol': symbol,
                'interval': interval,
                'startTime': start_time,
                'endTime': end_time,
                'limit': limit,
            }

            resp = requests.get(url, params=params, timeout=10)
            if resp.status_code != 200:
                raise DataFetchError(f"Binance API error: {resp.text}")

            candles = []
            for k in resp.json():
                candles.append({
                    'timestamp': int(k[0]),
                    'open': float(k[1]),
                    'high': float(k[2]),
                    'low': float(k[3]),
                    'close': float(k[4]),
                    'volume': float(k[7]),
                })

            return candles
        except Exception as e:
            raise DataFetchError(f"Failed to fetch crypto candles: {str(e)}")

    @staticmethod
    def fetch_equity_candles(symbol: str,
                             period: Optional[str] = None,
                             interval: Optional[str] = None) -> List[Dict]:
        """
        Fetch equity candles via yfinance.
        
        Args:
            symbol: Stock ticker (e.g., 'AAPL', 'TSLA')
            period: Time period ('1d', '5d', '1mo', '3mo', '1y', etc.)
            interval: Candle interval ('1m', '5m', '15m', '1h', '1d')
        
        If period/interval are specified, uses those directly.
        Otherwise tries multiple fallbacks.
        """
        # If specific period and interval provided, try that first
        if period and interval:
            try:
                logger.info(f"Trying {symbol} with period={period}, interval={interval}...")
                df = yf.download(symbol, period=period, interval=interval, progress=False)
                if not df.empty:
                    logger.info(f"Data found for {symbol} with interval={interval}, period={period}")
                    candles = []
                    for timestamp, row in df.iterrows():
                        candles.append({
                            'timestamp': int(timestamp.timestamp() * 1000),
                            'open': float(row['Open'].iloc[0] if hasattr(row['Open'], 'iloc') else row['Open']),
                            'high': float(row['High'].iloc[0] if hasattr(row['High'], 'iloc') else row['High']),
                            'low': float(row['Low'].iloc[0] if hasattr(row['Low'], 'iloc') else row['Low']),
                            'close': float(row['Close'].iloc[0] if hasattr(row['Close'], 'iloc') else row['Close']),
                            'volume': float(row['Volume'].iloc[0] if hasattr(row['Volume'], 'iloc') else row['Volume']),
                        })
                    return candles
            except Exception as e:
                logger.warning(f"Failed for {symbol} period={period} interval={interval}: {str(e)}")
                # Continue to fallback logic below
        
        # Fallback: Try multiple combinations
        periods = ["1mo", "3mo", "6mo", "1y"] if not period else [period]
        intervals = ["5m", "15m", "1h", "1d"] if not interval else [interval]
        
        for test_interval in intervals:
            for test_period in periods:
                try:
                    logger.info(f"Trying {symbol} with period={test_period}, interval={test_interval}...")
                    df = yf.download(symbol, period=test_period, interval=test_interval, progress=False)
                    if not df.empty:
                        logger.info(f"Data found for {symbol} with interval={test_interval}, period={test_period}")
                        candles = []
                        for timestamp, row in df.iterrows():
                            candles.append({
                                'timestamp': int(timestamp.timestamp() * 1000),
                                'open': float(row['Open'].iloc[0] if hasattr(row['Open'], 'iloc') else row['Open']),
                                'high': float(row['High'].iloc[0] if hasattr(row['High'], 'iloc') else row['High']),
                                'low': float(row['Low'].iloc[0] if hasattr(row['Low'], 'iloc') else row['Low']),
                                'close': float(row['Close'].iloc[0] if hasattr(row['Close'], 'iloc') else row['Close']),
                                'volume': float(row['Volume'].iloc[0] if hasattr(row['Volume'], 'iloc') else row['Volume']),
                            })
                        return candles
                except Exception as e:
                    logger.warning(f"Failed for {symbol} period={test_period} interval={test_interval}: {str(e)}")

        raise DataFetchError(f"No data found for {symbol} in any tested interval/period.")

    @staticmethod
    def fetch_prices(symbols: List[str]) -> Dict[str, float]:
        """Fetch current prices for symbols."""
        prices = {}

        for symbol in symbols:
            try:
                if symbol.endswith('USDT'):  # Crypto
                    url = f"{BINANCE_API}/ticker/price?symbol={symbol}"
                    resp = requests.get(url, timeout=5)
                    if resp.status_code == 200:
                        prices[symbol] = float(resp.json()['price'])
                    else:
                        logger.warning(f"Failed to fetch crypto price for {symbol}")
                else:  # Equity
                    ticker = yf.Ticker(symbol)
                    data = ticker.history(period="1d")
                    if not data.empty:
                        prices[symbol] = float(data['Close'].iloc[-1])
                    else:
                        logger.warning(f"No price data for equity {symbol}")
            except Exception as e:
                logger.warning(f"Error fetching price for {symbol}: {str(e)}")
        return prices