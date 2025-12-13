"""Streamlit dashboard for Aurora Quant."""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# from core.config import CRYPTO_PAIRS, RISK_PROFILES
from core.config import CRYPTO_ASSETS,RISK_PROFILES

from core.data_loader import DataLoader
from core.indicators import (
    calculate_ema, calculate_rsi, calculate_macd, calculate_vwap
)
from strategies.momentum import MomentumStrategy
from core.ledger import PaperLedger


st.set_page_config(page_title="Aurora Quant Dashboard", layout="wide")


def plot_equity_curve(equity_history: list, timestamps: list):
    """Plot equity curve."""
    df = pd.DataFrame({'equity': equity_history, 'timestamp': timestamps})
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df['timestamp'], y=df['equity'],
        mode='lines', name='Equity',
        line=dict(color='#00D4FF', width=2)
    ))
    
    fig.update_layout(
        title='Portfolio Equity Curve',
        xaxis_title='Time',
        yaxis_title='Equity ($)',
        template='plotly_dark',
        hovermode='x unified'
    )
    
    return fig


def plot_returns_distribution(returns: list):
    """Plot returns histogram."""
    fig = go.Figure()
    fig.add_trace(go.Histogram(
        x=returns,
        nbinsx=30,
        name='Returns',
        marker=dict(color='#00D4FF')
    ))
    
    fig.update_layout(
        title='Daily Returns Distribution',
        xaxis_title='Return (%)',
        yaxis_title='Frequency',
        template='plotly_dark',
    )
    
    return fig


def main():
    """Main dashboard."""
    st.title('Aurora Quant Trading Platform')
    st.markdown('Professional quantitative trading system')
    
    # Sidebar
    st.sidebar.title('Configuration')
    
    mode = st.sidebar.radio('Select Mode:', [
        'Backtest Momentum',
        'Analyze Market',
        'Portfolio Overview'
    ])
    
    if mode == 'Backtest Momentum':
        st.header('Momentum Strategy Backtest')
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # symbol = st.selectbox('Symbol', CRYPTO_PAIRS)
            symbol = st.selectbox(
                'Symbol',
                list(CRYPTO_ASSETS.values())
            )

        
        with col2:
            aggressiveness = st.selectbox('Aggressiveness',
                                         ['conservative', 'moderate', 'aggressive'])
        
        with col3:
            capital = st.number_input('Capital ($)', value=10000, min_value=1000)
        
        if st.button('Run Backtest'):
            st.info('Loading data...')
            
            # Load data
            try:
                candles = DataLoader.fetch_crypto_candles(symbol, '1m', days=3)
                
                if not candles:
                    st.error('No data found for symbol')
                    return
                
                # Run strategy
                ledger = PaperLedger(capital, 'momentum')
                strategy = MomentumStrategy('momentum', ledger, aggressiveness)
                
                st.info(f'Processing {len(candles)} candles...')
                
                for candle in candles:
                    signal = strategy.on_bar(symbol, candle)
                    
                    if signal and signal.signal == "BUY":
                        ledger.open_position(
                            symbol, "BUY", candle['close'],
                            capital / candle['close'] * 0.5,
                            datetime.fromtimestamp(candle['timestamp'] / 1000)
                        )
                    elif signal and signal.signal == "SELL":
                        ledger.close_position(
                            symbol, candle['close'],
                            datetime.fromtimestamp(candle['timestamp'] / 1000)
                        )
                
                # Display results
                summary = ledger.get_trades_summary()
                
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric('Total Trades', summary['total_trades'])
                with col2:
                    st.metric('Win Rate', f"{summary['win_rate']:.1f}%")
                with col3:
                    st.metric('Total P&L', f"${summary['total_pnl']:.2f}")
                with col4:
                    st.metric('Max Drawdown', f"{summary['max_drawdown']:.1f}%")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.metric('Sharpe Ratio', f"{summary['sharpe_ratio']:.2f}")
                with col2:
                    st.metric('Profit Factor', f"{summary['profit_factor']:.2f}")
                
                # Equity curve
                if ledger.equity_history:
                    fig = plot_equity_curve(ledger.equity_history,
                                          ledger.timestamp_history)
                    st.plotly_chart(fig, use_container_width=True)
                
                # Trades table
                trades_data = [t.to_dict() for t in ledger.trades if t.status == 'CLOSED']
                if trades_data:
                    st.subheader('Trade Log')
                    st.dataframe(pd.DataFrame(trades_data), use_container_width=True)
                
                st.success('Backtest completed!')
                
            except Exception as e:
                st.error(f'Error: {str(e)}')
    
    elif mode == 'Analyze Market':
        st.header('Market Analysis')
        
        # symbol = st.selectbox('Symbol', CRYPTO_PAIRS)
        symbol = st.selectbox(
            'Symbol',
            list(CRYPTO_ASSETS.values())
        )

        
        
        if st.button('Analyze'):
            try:
                candles = DataLoader.fetch_crypto_candles(symbol, '1m', days=3)
                
                if not candles:
                    st.error('No data found')
                    return
                
                df = pd.DataFrame(candles)
                
                closes = df['close'].tolist()
                ema20 = calculate_ema(closes, 20)
                ema50 = calculate_ema(closes, 50)
                rsi = calculate_rsi(closes, 14)
                macd, signal = calculate_macd(closes)
                
                # Price chart
                fig = go.Figure()
                
                fig.add_trace(go.Scatter(
                    x=df.index, y=df['close'],
                    name='Price', line=dict(color='#00D4FF')
                ))
                fig.add_trace(go.Scatter(
                    x=df.index, y=ema20,
                    name='EMA(20)', line=dict(color='orange')
                ))
                fig.add_trace(go.Scatter(
                    x=df.index, y=ema50,
                    name='EMA(50)', line=dict(color='red')
                ))
                
                fig.update_layout(title=f'{symbol} Price & EMAs',
                                 template='plotly_dark')
                st.plotly_chart(fig, use_container_width=True)
                
                # RSI
                fig_rsi = go.Figure()
                fig_rsi.add_trace(go.Scatter(y=rsi, name='RSI(14)',
                                           line=dict(color='#00D4FF')))
                fig_rsi.add_hline(y=70, line_dash='dash', line_color='red')
                fig_rsi.add_hline(y=30, line_dash='dash', line_color='green')
                fig_rsi.update_layout(title='RSI', template='plotly_dark')
                st.plotly_chart(fig_rsi, use_container_width=True)
                
            except Exception as e:
                st.error(f'Error: {str(e)}')
    
    else:  # Portfolio Overview
        st.header('Portfolio Overview(⚠️Under Development- Devs Working !)')
        
        st.write('Monitor your portfolio metrics and positions.')
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric('Total Capital', '$100,000')
        with col2:
            st.metric('Current Equity', '$102,500', '+2.5%')
        with col3:
            st.metric('Open Positions', '3')
        with col4:
            st.metric('Max Drawdown', '-8.2%')


if __name__ == '__main__':
    main()


#- Complete Streamlit dashboard with backtester runner, market analyzer, and portfolio overview
