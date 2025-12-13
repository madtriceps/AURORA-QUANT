"""Real-time market data feed with websocket support."""
import asyncio
import websockets
import json
from typing import Dict, Callable, Optional
from datetime import datetime
from core.config import BINANCE_WSAPI, CRYPTO_PAIRS


class BinanceFeed:
    """Binance websocket market data feed."""
    
    def __init__(self, pairs: list = CRYPTO_PAIRS):
        self.pairs = pairs
        self.prices: Dict[str, float] = {}
        self.ws_url = BINANCE_WSAPI
        self.is_connected = False
        self.callbacks: list = []

    def add_callback(self, callback: Callable) -> None:
        """Add price update callback."""
        self.callbacks.append(callback)

    async def subscribe(self) -> None:
        """Subscribe to price streams."""
        streams = [f"{pair.lower()}@ticker" for pair in self.pairs]
        stream_url = f"{self.ws_url}/stream?streams=" + "/".join(streams)
        
        try:
            async with websockets.connect(stream_url) as ws:
                self.is_connected = True
                print("✅ Websocket connected")
                
                while self.is_connected:
                    try:
                        msg = await asyncio.wait_for(ws.recv(), timeout=5)
                        data = json.loads(msg)
                        
                        if 'data' in data:
                            ticker = data['data']
                            symbol = ticker['s']
                            price = float(ticker['c'])
                            
                            self.prices[symbol] = price
                            
                            for callback in self.callbacks:
                                callback(symbol, price)
                    except asyncio.TimeoutError:
                        continue
                    except Exception as e:
                        print(f"Stream error: {e}")
                        break
        except Exception as e:
            print(f"Connection error: {e}")
            self.is_connected = False

    def disconnect(self) -> None:
        """Disconnect websocket."""
        self.is_connected = False


class FeedManager:
    """Manages multiple data feeds."""
    
    def __init__(self):
        self.feeds: Dict[str, BinanceFeed] = {}
    
    def create_feed(self, name: str, pairs: list) -> BinanceFeed:
        """Create and manage a new feed."""
        feed = BinanceFeed(pairs)
        self.feeds[name] = feed
        return feed
    
    async def run_all(self) -> None:
        """Run all feeds concurrently."""
        tasks = [feed.subscribe() for feed in self.feeds.values()]
        await asyncio.gather(*tasks)
