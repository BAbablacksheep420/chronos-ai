
"""
Chronos AI - Research Demo
--------------------------
This script demonstrates how to key components of Chronos AI for research purposes.
It will:
1. Fetch data for a basket of assets (Tech Stocks vs Crypto).
2. Calculate correlation matrices across different timeframes (1H vs 1D).
3. Detect "Regime Changes" (when correlation breaks) between Bitcoin and SPY.
4. Visualize the results.
"""

import sys
import os

# Ensure we can import from the parent directory
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from chronos.fetchers import fetch_data, save_to_csv
from chronos.processors import resample_ohlc
from chronos.analytics import calculate_correlation_matrix, detect_regime_changes
from chronos.visualizer import plot_heatmap, plot_regime_change
import pandas as pd
import os

def ensure_data(tickers, period='6mo', interval='1h'):
    """Helper to ensure data exists locally."""
    # Data dir relative to this script (experiments/../data)
    base_dir = os.path.dirname(__file__)
    data_dir = os.path.join(base_dir, '..', 'data')
    
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
        
    data_map = {}
    for t in tickers:
        path = os.path.join(data_dir, f"{t}.csv")
        if not os.path.exists(path):
            print(f"Fetching {t}...")
            df = fetch_data(t, period=period, interval=interval)
            df.to_csv(path)
        else:
            print(f"Loading {t} from cache...")
            df = pd.read_csv(path, index_col=0, parse_dates=True)
        data_map[t] = df
    return data_map

def run_experiment():
    # 1. Define Basket
    # Mixing different asset classes to see interesting correlations
    basket = ['SPY', 'QQQ', 'BTC-USD', 'ETH-USD', 'GLD', 'NVDA']
    
    print("--- 1. Loading Data ---")
    # Fetch 6 months of 1-hour data to allow for both 1H and 1D analysis
    data_map = ensure_data(basket, period='1y', interval='1h')
    
    # 2. Daily Correlation Matrix
    print("\n--- 2. Daily Correlation Matrix ---")
    daily_closes = {}
    for t, df in data_map.items():
        # Resample to Daily
        daily_df = resample_ohlc(df, '1D')
        daily_closes[t] = daily_df['Close']
        
    # Align
    daily_df_aligned = pd.DataFrame(daily_closes).dropna()
    daily_corr = calculate_correlation_matrix(daily_df_aligned.to_dict('series'))
    
    print("Daily Correlation (SPY vs BTC-USD):", daily_corr.loc['SPY', 'BTC-USD'])
    
    # Save Heatmap
    plot_heatmap(daily_corr, title="Daily Correlation Matrix", save_path="daily_heatmap.html")
    print("Saved daily_heatmap.html")

    # 3. Hourly Correlation Matrix
    print("\n--- 3. Hourly Correlation Matrix ---")
    hourly_closes = {}
    for t, df in data_map.items():
        hourly_closes[t] = df['Close']
        
    hourly_df_aligned = pd.DataFrame(hourly_closes).dropna()
    hourly_corr = calculate_correlation_matrix(hourly_df_aligned.to_dict('series'))
    
    print("Hourly Correlation (SPY vs BTC-USD):", hourly_corr.loc['SPY', 'BTC-USD'])
    
    plot_heatmap(hourly_corr, title="Hourly Correlation Matrix", save_path="hourly_heatmap.html")
    print("Saved hourly_heatmap.html")
    
    # 4. Regime Detection (BTC vs SPY)
    print("\n--- 4. Regime Detection (BTC vs SPY) ---")
    # Using Daily data for regime detection logic usually makes more sense for "macro" trends
    # Let's see rolling 30-day correlation
    spy = daily_df_aligned['SPY']
    btc = daily_df_aligned['BTC-USD']
    
    regime_df = detect_regime_changes(spy, btc, threshold=0.3, window=30)
    
    # Find recent regimes
    print(regime_df.tail(10))
    
    plot_regime_change(regime_df, title="Regime Change: SPY vs BTC (30D Rolling)").write_html("regime_change.html")
    print("Saved regime_change.html")

if __name__ == "__main__":
    run_experiment()
