
import sys
import os
import pandas as pd

# Path setup
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from chronos.fetchers import fetch_data
from chronos.processors import resample_ohlc, filter_market_hours
from chronos.analytics import calculate_ccf, find_best_lag, detect_regime_changes
from chronos.visualizer import plot_ccf, plot_regime_change, plot_heatmap

def run_unified_paper_analysis():
    print("--- 📚 Phase 0: Data Acquisition & Pre-processing ---")
    # Using 1-hour data for 1 year to get high resolution for lead-lag
    tickers = ['SPY', 'BTC-USD']
    data = {}
    
    base_dir = os.path.dirname(__file__)
    data_dir = os.path.join(base_dir, '..', 'data')
    
    for t in tickers:
        df = fetch_data(t, period='1y', interval='1h')
        # Standardize: Ensure DatetimeIndex
        df.index = pd.to_datetime(df.index)
        data[t] = df

    # --- 1. Fix the Stock-Crypto Alignment (Market Hours Only) ---
    print("\n--- ⚖️ Phase 1: Market Alignment ---")
    spy_market = data['SPY'] # Stocks already are in market hours
    btc_market = filter_market_hours(data['BTC-USD'])
    
    # Intersection of timestamps
    common_idx = spy_market.index.intersection(btc_market.index)
    spy_clean = spy_market.loc[common_idx, 'Close']
    btc_clean = btc_market.loc[common_idx, 'Close']
    
    print(f"Aligned dataset size: {len(common_idx)} periods.")

    # --- 2. Timeframe Breathing (Scale Analysis) ---
    print("\n--- 💨 Phase 2: Timeframe Breathing ---")
    intervals = ['1h', '4h', '1d']
    breathing_results = {}
    
    for interval in intervals:
        if interval == '1h':
            corr = spy_clean.corr(btc_clean)
        else:
            # Resample both
            s_res = resample_ohlc(data['SPY'], interval.upper())['Close']
            b_res = resample_ohlc(data['BTC-USD'], interval.upper())['Close']
            idx = s_res.index.intersection(b_res.index)
            corr = s_res.loc[idx].corr(b_res.loc[idx])
        
        breathing_results[interval] = corr
        print(f"Correlation at {interval}: {corr:.4f}")

    # --- 3. Lead-Lag Discovery (Information flow) ---
    print("\n--- 🏎️ Phase 3: Lead-Lag Discovery ---")
    ccf = calculate_ccf(spy_clean, btc_clean, max_lags=10)
    best_lag, best_val = find_best_lag(spy_clean, btc_clean, max_lags=10)
    
    print(f"Best Lag: {best_lag} periods. Correlation: {best_val:.4f}")
    if best_lag > 0:
        print("Conclusion: SPY leads BTC-USD")
    elif best_lag < 0:
        print("Conclusion: BTC-USD leads SPY")
    else:
        print("Conclusion: No significant lead-lag (Co-moving)")
        
    plot_ccf(ccf, title="Lead-Lag Analysis: SPY vs BTC-USD").write_html("figure_lead_lag.html")

    # --- 4. Regime Stability ---
    print("\n--- 🛡️ Phase 4: Regime Stability ---")
    # Using Daily for regime stability (clearer macro view)
    s_d = resample_ohlc(data['SPY'], '1D')['Close']
    b_d = resample_ohlc(data['BTC-USD'], '1D')['Close']
    idx_d = s_d.index.intersection(b_d.index)
    
    regimes = detect_regime_changes(s_d.loc[idx_d], b_d.loc[idx_d], threshold=0.4, window=30)
    plot_regime_change(regimes, title="Correlation Regime Analysis (30D Rolling)").write_html("figure_regimes.html")
    
    print("Done! Figures generated: figure_lead_lag.html, figure_regimes.html")

if __name__ == "__main__":
    run_unified_paper_analysis()
