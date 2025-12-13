"""Professional report and summary generation."""
from datetime import datetime
from typing import Dict, List


def format_currency(value: float) -> str:
    """Format value as currency."""
    return f"${value:,.2f}"


def format_percent(value: float) -> str:
    """Format value as percentage."""
    sign = "+" if value >= 0 else ""
    return f"{sign}{value:.2f}%"


def print_investor_header(platform_name: str = "Aurora Quant") -> None:
    """Print professional header."""
    print("\n" + "=" * 75)
    print(f"{'AURORA QUANT TRADING PLATFORM':^75}")
    print(f"{'Enterprise-Grade Quantitative Analysis System':^75}")
    print("=" * 75)


def print_strategy_report(summary: Dict, strategy_type: str, duration: str = "") -> None:
    """Print professional strategy report."""
    ledger_summary = summary.get('ledger_summary', {})
    
    print("\n" + "=" * 75)
    print(f"📊 {strategy_type.upper()} STRATEGY REPORT")
    print("=" * 75)
    
    if duration:
        print(f"Duration: {duration}")
    
    print(f"\n{'CAPITAL METRICS':^75}")
    print("-" * 75)
    print(f"Initial Capital:        {format_currency(ledger_summary.get('current_equity', 0))} " +
          f"(Backup: {ledger_summary.get('cash', 0)})")
    print(f"Final Equity:           {format_currency(ledger_summary.get('current_equity', 0))}")
    print(f"Total P&L:              {format_currency(ledger_summary.get('total_pnl', 0))} " +
          f"({format_percent(ledger_summary.get('total_pnl_percent', 0))})")
    
    print(f"\n{'TRADE STATISTICS':^75}")
    print("-" * 75)
    print(f"Total Trades:           {ledger_summary.get('total_trades', 0)}")
    print(f"Closed Trades:          {ledger_summary.get('closed_trades', 0)}")
    print(f"Winning Trades:         {ledger_summary.get('winning_trades', 0)}")
    print(f"Losing Trades:          {ledger_summary.get('losing_trades', 0)}")
    print(f"Win Rate:               {format_percent(ledger_summary.get('win_rate', 0))}")
    
    if ledger_summary.get('avg_win'):
        print(f"Avg. Win:               {format_currency(ledger_summary.get('avg_win', 0))}")
        print(f"Avg. Loss:              {format_currency(ledger_summary.get('avg_loss', 0))}")
        print(f"Profit Factor:          {ledger_summary.get('profit_factor', 0):.2f}x")
    
    print(f"\n{'RISK METRICS':^75}")
    print("-" * 75)
    print(f"Max Drawdown:           {format_percent(ledger_summary.get('max_drawdown', 0))}")
    print(f"Sharpe Ratio:           {ledger_summary.get('sharpe_ratio', 0):.2f}")
    print(f"Remaining Cash:         {format_currency(ledger_summary.get('cash', 0))}")
    
    print("=" * 75 + "\n")


def print_trading_summary(ledger, strategy_name: str, duration: str = "") -> None:
    """Print professional trading summary from ledger."""
    summary = ledger.get_trades_summary()
    print("\n" + "=" * 75)
    print(f"📊 {strategy_name} - TRADING SUMMARY")
    print("=" * 75)
    
    if duration:
        print(f"Duration: {duration}\n")
    
    print(f"{'CAPITAL METRICS':^75}")
    print("-" * 75)
    initial_capital = ledger.starting_capital
    final_equity = ledger.current_equity
    total_pnl = final_equity - initial_capital
    pnl_percent = (total_pnl / initial_capital * 100) if initial_capital > 0 else 0
    
    print(f"Initial Capital:        {format_currency(initial_capital)}")
    print(f"Final Equity:           {format_currency(final_equity)}")
    print(f"Total P&L:              {format_currency(total_pnl)} ({format_percent(pnl_percent)})")
    print(f"Cash Remaining:         {format_currency(ledger.cash)}")
    
    print(f"\n{'TRADE STATISTICS':^75}")
    print("-" * 75)
    print(f"Total Trades:           {summary.get('total_trades', 0)}")
    print(f"Closed Trades:          {summary.get('closed_trades', 0)}")
    print(f"Winning Trades:         {summary.get('winning_trades', 0)}")
    print(f"Losing Trades:          {summary.get('losing_trades', 0)}")
    print(f"Win Rate:               {format_percent(summary.get('win_rate', 0))}")
    
    if summary.get('avg_win'):
        print(f"Avg. Win:               {format_currency(summary.get('avg_win', 0))}")
        print(f"Avg. Loss:              {format_currency(summary.get('avg_loss', 0))}")
        print(f"Profit Factor:          {summary.get('profit_factor', 0):.2f}x")
    
    print(f"\n{'RISK METRICS':^75}")
    print("-" * 75)
    print(f"Max Drawdown:           {format_percent(summary.get('max_drawdown', 0))}")
    print(f"Sharpe Ratio:           {summary.get('sharpe_ratio', 0):.2f}")
    
    print("=" * 75 + "\n")


def print_arbitrage_opportunities(opportunities: List[Dict]) -> None:
    """Print summary of arbitrage opportunities detected."""
    if not opportunities:
        print("\n⚠️  No arbitrage opportunities detected during this session.\n")
        return
    
    print("\n" + "=" * 75)
    print(f"{'ARBITRAGE OPPORTUNITIES DETECTED':^75}")
    print("=" * 75)
    
    profit_opps = [o for o in opportunities if o.get('profit_percent', 0) > 0]
    
    print(f"\nTotal Opportunities:    {len(opportunities)}")
    print(f"Profitable:             {len(profit_opps)}")
    
    if profit_opps:
        print(f"\n{'Route':<40} {'Profit %':<15}")
        print("-" * 75)
        for opp in profit_opps[:10]:  # Show top 10
            print(f"{opp.get('route', 'Unknown'):<40} {opp.get('profit_percent', 0):>6.3f}%")
    
    print("=" * 75 + "\n")


def generate_summary_text(summary: Dict, mode: str) -> str:
    """Generate plain English summary."""
    ledger = summary.get('ledger_summary', {})
    pnl = ledger.get('total_pnl', 0)
    pnl_pct = ledger.get('total_pnl_percent', 0)
    trades = ledger.get('closed_trades', 0)
    win_rate = ledger.get('win_rate', 0)
    
    sign = "+" if pnl >= 0 else ""
    result_text = f"{sign}{pnl:.2f} ({sign}{pnl_pct:.2f}%)"
    
    if mode == "arbitrage":
        detected = summary.get('opportunities_detected', 0)
        executed = summary.get('trades_executed', 0)
        if detected == 0:
            return "No arbitrage opportunities detected during this session."
        return f"Detected {detected} arbitrage opportunities, executed {executed} trade(s) with result: {result_text}."
    
    elif mode == "momentum":
        symbol = summary.get('symbol', 'Unknown')
        if trades == 0:
            return f"No trades executed on {symbol} during this session."
        elif win_rate >= 50:
            return f"{symbol} momentum strategy: {trades} trades, {win_rate:.1f}% win rate, result: {result_text}."
        else:
            return f"{symbol} momentum strategy: {trades} trades, {win_rate:.1f}% win rate (struggling), result: {result_text}."
    
    elif mode == "ai_signal":
        return f"AI signal optimizer completed analysis with {trades} signal(s) scored, result: {result_text}."
    
    return f"Trading session: {trades} trades, {result_text}."


def generate_plain_english_summary(summary: Dict, mode: str) -> str:
    """Alias for generate_summary_text for backward compatibility."""
    return generate_summary_text(summary, mode)
