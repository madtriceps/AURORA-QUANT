"""SQLite-based market data lake."""
import sqlite3
from typing import List, Dict, Optional
from datetime import datetime
import pandas as pd


class MarketDataLake:
    """Local SQLite market data lake for caching."""
    
    def __init__(self, db_path: str = "storage/market_data.db"):
        self.db_path = db_path
        self.init_db()
    
    def init_db(self) -> None:
        """Initialize database schema."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # OHLCV candles
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS candles (
                id INTEGER PRIMARY KEY,
                symbol TEXT NOT NULL,
                timestamp INTEGER NOT NULL,
                open REAL,
                high REAL,
                low REAL,
                close REAL,
                volume REAL,
                timeframe TEXT,
                UNIQUE(symbol, timestamp, timeframe)
            )
        ''')
        
        # Tick data
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ticks (
                id INTEGER PRIMARY KEY,
                symbol TEXT NOT NULL,
                timestamp INTEGER NOT NULL,
                price REAL,
                volume REAL
            )
        ''')
        
        # Trade log
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS trades (
                id INTEGER PRIMARY KEY,
                strategy_id TEXT,
                symbol TEXT,
                side TEXT,
                entry_price REAL,
                exit_price REAL,
                quantity REAL,
                pnl REAL,
                entry_time INTEGER,
                exit_time INTEGER
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def save_candle(self, symbol: str, timestamp: int, ohlcv: Dict, 
                   timeframe: str = "1m") -> None:
        """Save OHLCV candle."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT OR REPLACE INTO candles
                (symbol, timestamp, open, high, low, close, volume, timeframe)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (symbol, timestamp, ohlcv['open'], ohlcv['high'], 
                  ohlcv['low'], ohlcv['close'], ohlcv['volume'], timeframe))
            conn.commit()
        finally:
            conn.close()
    
    def get_candles(self, symbol: str, timeframe: str = "1m",
                   limit: int = 1000) -> pd.DataFrame:
        """Retrieve candles for symbol."""
        conn = sqlite3.connect(self.db_path)
        
        query = '''
            SELECT timestamp, open, high, low, close, volume
            FROM candles
            WHERE symbol = ? AND timeframe = ?
            ORDER BY timestamp DESC
            LIMIT ?
        '''
        
        df = pd.read_sql_query(query, conn, params=(symbol, timeframe, limit))
        conn.close()
        
        return df.sort_values('timestamp').reset_index(drop=True)
    
    def save_trade(self, trade_data: Dict) -> None:
        """Save executed trade to lake."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO trades
                (strategy_id, symbol, side, entry_price, exit_price, quantity, pnl, entry_time, exit_time)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                trade_data.get('strategy_id'),
                trade_data.get('symbol'),
                trade_data.get('side'),
                trade_data.get('entry_price'),
                trade_data.get('exit_price'),
                trade_data.get('quantity'),
                trade_data.get('pnl'),
                trade_data.get('entry_time'),
                trade_data.get('exit_time'),
            ))
            conn.commit()
        finally:
            conn.close()
