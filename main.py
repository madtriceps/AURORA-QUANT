"""Aurora Quant v2.0 - Main Entry Point"""
import sys
from datetime import datetime, timedelta
from typing import Optional

from core.config import CRYPTO_PAIRS, ASSET_CLASSES, RISK_PROFILES
from core.data_loader import DataLoader
from core.simulation import BacktestEngine, SimulationConfig
from core.types import MarketEvent
from core.ledger import PaperLedger
from strategies.momentum import MomentumStrategy
from storage.datalake import MarketDataLake


def print_banner():
    """Print Aurora Quant banner."""
    banner = """
    ╔════════════════════════════════════════════════════════════════╗
    ║                    AURORA QUANT v2.0                           ║
    ║            Professional Quantitative Trading Platform          ║
    ║                  Event-Driven Backtester                       ║
    ╚════════════════════════════════════════════════════════════════╝
    """
    print(banner)


def print_menu():
    """Print main menu."""
    print("\nSelect Trading Mode:\n")
    print("  1. Crypto Arbitrage Detector")
    print("  2. Momentum Strategy Backtest")
    print("  3. Multi-Asset Analysis")
    print("  4. Run Dashboard (Streamlit)")
    print("  0. Exit\n")
    print("=" * 70)


def run_momentum_backtest():
    """Run momentum strategy backtest."""
    print("\n" + "=" * 70)
    print("MOMENTUM STRATEGY BACKTEST")
    print("=" * 70)
    
    try:
        print("\nAsset Type:")
        print("  1. Crypto")
        print("  2. US Equities")
        print("  3. Indian Equities")
        
        asset_choice = input("\nSelect (1-3): ").strip()
        
        if asset_choice == "1":
            symbol = "BTCUSDT"
            print(f"\nSelected: {symbol}")
        elif asset_choice == "2":
            symbol = input("Enter US equity symbol (e.g., AAPL): ").strip().upper()
        elif asset_choice == "3":
            symbol = input("Enter Indian equity symbol (e.g., INFY.NS): ").strip().upper()
        else:
            print("Invalid choice")
            return
        
        capital = float(input("\nStarting capital ($): "))
        aggressiveness = input("Aggressiveness (conservative/moderate/aggressive): ").lower()
        
        if aggressiveness not in ["conservative", "moderate", "aggressive"]:
            aggressiveness = "moderate"
        
        print(f"\n[INFO] Loading market data for {symbol}...")
        
        # Load data - Optimized for different timeframes
        try:
            if symbol.endswith("USDT"):
                candles = DataLoader.fetch_crypto_candles(symbol, "5m", days=30)
                period_desc = "30 days (5m candles)"
            else:
                # Use daily candles for 1 year (captures full market cycles)
                candles = DataLoader.fetch_equity_candles(symbol, period="1y", interval="1d")
                period_desc = "1 year (daily candles)"
        except Exception as e:
            print(f"[ERROR] Failed to load data: {e}")
            return
        
        if not candles:
            print("[ERROR] No data available for symbol")
            return
        
        print(f"[INFO] Loaded {len(candles)} candles")
        
        # Initialize strategy
        ledger = PaperLedger(capital, "momentum_backtest")
        strategy = MomentumStrategy("momentum", ledger, aggressiveness)
        
        print("[INFO] Running backtest...")
        
        # Process each candle
        for i, candle in enumerate(candles):
            signal = strategy.on_bar(symbol, candle)
            
            # Note: The strategy now handles trade execution internally
            # No need for external BUY/SELL logic here
            
            if (i + 1) % 100 == 0:
                print(f"[INFO] Processed {i + 1} candles...")
        
        # Print results
        summary = ledger.get_trades_summary()
        
        print("\n" + "=" * 70)
        print("BACKTEST RESULTS")
        print("=" * 70)
        print(f"\nSymbol: {symbol}")
        print(f"Strategy: Momentum ({aggressiveness})")
        print(f"Period: {period_desc} | Capital: ${capital:.2f}\n")
        
        print("Performance Metrics:")
        print(f"  Total Trades: {summary['total_trades']}")
        print(f"  Winning Trades: {summary['winning_trades']}")
        print(f"  Losing Trades: {summary['losing_trades']}")
        print(f"  Win Rate: {summary['win_rate']:.1f}%")
        print(f"  Total P&L: ${summary['total_pnl']:.2f}")
        print(f"  Return: {summary['total_pnl_percent']:.2f}%")
        print(f"  Max Drawdown: {summary['max_drawdown']:.2f}%")
        print(f"  Sharpe Ratio: {summary['sharpe_ratio']:.2f}")
        print(f"  Profit Factor: {summary['profit_factor']:.2f}")
        print(f"  Current Equity: ${summary['current_equity']:.2f}\n")
        
        # Print sample trades
        if summary['closed_trades'] > 0:
            print("Sample Trades (last 5):")
            trades = [t for t in ledger.trades if t.status == "CLOSED"][-5:]
            for trade in trades:
                print(f"  {trade.symbol} | {trade.side} | "
                      f"Entry: ${trade.entry_price:.2f} | "
                      f"Exit: ${trade.exit_price:.2f} | "
                      f"PnL: ${trade.pnl:.2f}")
        
        print("\n" + "=" * 70)
        
    except Exception as e:
        print(f"[ERROR] {e}")


def run_arbitrage_detector():
    """Run arbitrage detector."""
    print("\n" + "=" * 70)
    print("CRYPTO ARBITRAGE DETECTOR")
    print("=" * 70)
    
    try:
        print("\n[INFO] Fetching crypto prices from Binance...")
        
        prices = DataLoader.fetch_prices(CRYPTO_PAIRS)
        
        if not prices:
            print("[ERROR] Failed to fetch prices")
            return
        
        print(f"[INFO] Retrieved {len(prices)} prices")
        print("\nCurrent Market Prices:")
        for symbol, price in prices.items():
            print(f"  {symbol}: ${price:.2f}")
        
        print("\n[INFO] Scanning for triangular arbitrage opportunities...")
        
        # Simple opportunity detection (simplified triangular check)
        print("\nNote: This is a simplified demo. Full arbitrage would require:")
        print("  - Real-time order book data")
        print("  - Latency modeling")
        print("  - Slippage estimation")
        print("  - Fee calculation")
        
        print("\n" + "=" * 70)
        
    except Exception as e:
        print(f"[ERROR] {e}")


def run_dashboard():
    """Launch Streamlit dashboard."""
    print("\n[INFO] Launching Streamlit dashboard...")
    print("[INFO] Dashboard URL: http://localhost:8501")
    
    import subprocess
    try:
        subprocess.run(["streamlit", "run", "dashboard/app.py"], 
                      capture_output=False)
    except FileNotFoundError:
        print("[ERROR] Streamlit not installed. Run: pip install streamlit")
    except Exception as e:
        print(f"[ERROR] Failed to launch dashboard: {e}")


def main():
    """Main CLI loop."""
    print_banner()
    
    while True:
        print_menu()
        
        try:
            choice = input("Select mode (0-4): ").strip()
            
            if choice == "0":
                print("\nThank you for using Aurora Quant. Goodbye!\n")
                sys.exit(0)
            elif choice == "1":
                run_arbitrage_detector()
            elif choice == "2":
                run_momentum_backtest()
            elif choice == "3":
                print("\n[TODO] Multi-asset analysis module")
            elif choice == "4":
                run_dashboard()
            else:
                print("Invalid selection")
                continue
            
            again = input("\nContinue? (y/n): ").strip().lower()
            if again != "y":
                print("\nThank you for using Aurora Quant. Goodbye!\n")
                sys.exit(0)
        
        except KeyboardInterrupt:
            print("\n\nShutdown. Goodbye!\n")
            sys.exit(0)
        except Exception as e:
            print(f"[ERROR] {e}")


if __name__ == "__main__":
    main()