"""Abstract data provider interface."""
from abc import ABC, abstractmethod
from typing import List, Dict, Optional
from datetime import datetime
import pandas as pd


class DataProvider(ABC):
    """Abstract base for market data providers."""
    
    @abstractmethod
    def fetch_candles(self, symbol: str, timeframe: str = "1m",
                     start: Optional[datetime] = None,
                     end: Optional[datetime] = None) -> pd.DataFrame:
        """Fetch OHLCV candles."""
        pass
    
    @abstractmethod
    def fetch_ticks(self, symbol: str,
                   start: Optional[datetime] = None,
                   end: Optional[datetime] = None) -> List[Dict]:
        """Fetch tick data."""
        pass
    
    @abstractmethod
    def get_current_price(self, symbol: str) -> float:
        """Get current price."""
        pass


class BinanceProvider(DataProvider):
    """Binance crypto data provider."""
    
    def __init__(self):
        from core.config import BINANCE_API
        self.base_url = BINANCE_API
    
    def fetch_candles(self, symbol: str, timeframe: str = "1m",
                     start: Optional[datetime] = None,
                     end: Optional[datetime] = None) -> pd.DataFrame:
        """Fetch Binance candles."""
        import requests
        
        url = f"{self.base_url}/klines"
        params = {'symbol': symbol, 'interval': timeframe, 'limit': 1000}
        
        try:
            resp = requests.get(url, params=params, timeout=10)
            if resp.status_code != 200:
                return pd.DataFrame()
            
            data = []
            for k in resp.json():
                data.append({
                    'timestamp': datetime.fromtimestamp(k[0] / 1000),
                    'open': float(k[1]),
                    'high': float(k[2]),
                    'low': float(k[3]),
                    'close': float(k[4]),
                    'volume': float(k[7]),
                })
            
            return pd.DataFrame(data)
        except Exception as e:
            print(f"[ERROR] Failed to fetch Binance candles: {e}")
            return pd.DataFrame()
    
    def fetch_ticks(self, symbol: str,
                   start: Optional[datetime] = None,
                   end: Optional[datetime] = None) -> List[Dict]:
        """Binance doesn't provide tick data via REST."""
        return []
    
    def get_current_price(self, symbol: str) -> float:
        """Get current price from Binance."""
        import requests
        
        url = f"{self.base_url}/ticker/price?symbol={symbol}"
        try:
            resp = requests.get(url, timeout=5)
            if resp.status_code == 200:
                return float(resp.json()['price'])
        except:
            pass
        return 0.0


class YfinanceProvider(DataProvider):
    """Yahoo Finance data provider for equities (intraday-safe)."""
    
    def fetch_candles(self, symbol: str, timeframe: str = "1m",
                     start: Optional[datetime] = None,
                     end: Optional[datetime] = None) -> pd.DataFrame:
        """Fetch equity candles via the WORKING Yahoo chart API."""
        import yfinance as yf
        
        try:
            # Intraday logic: Yahoo allows only last 30 days
            if timeframe in ["1m", "2m", "5m", "15m", "30m", "60m", "90m"]:
                period = "7d"   # safe inside Yahoo's limit
            else:
                period = "1y"

            ticker = yf.Ticker(symbol)
            df = ticker.history(interval=timeframe, period=period)

            if df.empty:
                print(f"[ERROR] No data returned for {symbol}")
                return pd.DataFrame()

            df = df.reset_index()
            df['timestamp'] = df['Datetime' if 'Datetime' in df else 'Date']
            
            return df[['timestamp', 'Open', 'High', 'Low', 'Close', 'Volume']].rename(
                columns={
                    'Open':'open','High':'high','Low':'low',
                    'Close':'close','Volume':'volume'
                }
            )

        except Exception as e:
            print(f"[ERROR] Failed to fetch yfinance data: {e}")
            return pd.DataFrame()
    
    def fetch_ticks(self, symbol: str,
                   start: Optional[datetime] = None,
                   end: Optional[datetime] = None) -> List[Dict]:
        """Tick data not available via yfinance."""
        return []
    
    def get_current_price(self, symbol: str) -> float:
        """Get current equity price."""
        import yfinance as yf
        
        try:
            ticker = yf.Ticker(symbol)
            data = ticker.history(period="1d")
            if not data.empty:
                return float(data['Close'].iloc[-1])
        except:
            pass
        return 0.0
