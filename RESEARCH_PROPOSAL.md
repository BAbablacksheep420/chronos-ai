# Chronos AI: Multi-Timeframe Correlation Discovery System

## 1. Project Overview
**Chronos AI** is a research-oriented system designed to discover, quantify, and visualize correlations between financial assets across multiple timeframes (e.g., 5-minute, 1-hour, 1-day). The core hypothesis is that correlations are not static; they breathe and evolve differently depending on the temporal resolution. A correlation that exists on a Daily chart might be noise on a 15-minute chart, or vice versa.

## 2. Mathematical Foundation ("The Research Side")
To build this as a rigorous research project, we must go beyond simple "price matching". Here are the key mathematical concepts needed:

### A. Correlation Metrics
1.  **Pearson Correlation ($r$)**: Measures linear relationship. Good baseline but assumes linearity and normal distribution.
    *   *Formula*: $r = \frac{\sum(x_i - \bar{x})(y_i - \bar{y})}{\sqrt{\sum(x_i - \bar{x})^2 \sum(y_i - \bar{y})^2}}$
2.  **Spearman's Rank Correlation ($\rho$)**: Non-parametric measure of rank correlation. Better for capturing monotonic relationships (non-linear).
3.  **Kendall's Tau ($\tau$)**: Measures ordinal association. More robust to outliers than Spearman.

### B. Time-Series Specific Analysis
1.  **Cross-Correlation Function (CCF)**:
    *   Instead of just $Corr(X_t, Y_t)$, we measure $Corr(X_{t}, Y_{t+k})$ where $k$ is a lag.
    *   *Goal*: Discover "Lead-Lag" relationships. Does Asset A moving now predict Asset B moving in 5 periods?
2.  **Cointegration**:
    *   For identifying pairs that are "tied together" in the long run even if they diverge in the short run.
    *   *Math*: If a linear combination $Y_t - \beta X_t = \epsilon_t$ is stationary ($I(0)$), they are cointegrated.
    *   *Tool*: Engle-Granger two-step method or Johansen test.
3.  **Granger Causality**:
    *   Statistical hypothesis test to determine if one time series is useful in forecasting another.
    *   *Note*: It’s not "true" causality, but "predictive causality".
4.  **Dynamic Time Warping (DTW)**:
    *   An algorithm to measure similarity between two temporal sequences which may vary in speed.
    *   *Use Case*: Finding similar price patterns that happen at different speeds (e.g., a crash structure happening over 1 hour vs 1 day).

### C. Multi-Timeframe Resampling
*   **Aggregation**: Converting high-frequency data (e.g., 1-minute ticks) into lower frequency (e.g., 1-hour OHLC).
*   **Rolling Window Correlations**: Calculating dynamic correlation over a sliding window (e.g., 20-period rolling correlation) to see how the relationship evolves.

## 3. Technology Stack & Tools

### Core Libraries (Python)
*   **Data Manipulation**: `pandas` (The backbone of time-series), `numpy`.
*   **Data Acquisition**: `yfinance` (Yahoo Finance), `ccxt` (Crypto exchanges), `alpha_vantage`.
*   **Mathematics & Stats**:
    *   `scipy.stats`: For correlation calculations.
    *   `statsmodels`: For Cointegration (ADF test), Granger Causality, partial autocorrelations.
*   **Machine Learning (Optional but recommended)**:
    *   `scikit-learn`: For clustering assets based on correlation profiles.
    *   `tslearn`: For Dynamic Time Warping and time-series specific ML.
*   **Visualization**:
    *   `plotly` / `seaborn`: For heatmaps and interactive charts.
    *   `matplotlib`: For static rigid plots.

## 4. Proposed Architecture
We will build the system in a modular way:

```
chronos-ai/
├── data/                   # Storage for CSVs/Parquet files
├── chronos/                # Main package
│   ├── __init__.py
│   ├── fetchers.py         # Modules to download OHLC data
│   ├── processors.py       # Resampling and cleaning logic
│   ├── analytics.py        # The "Math" engine (Correlations, Cointegration)
│   └── visualizer.py       # Plotting utilities
├── experiments/            # Jupyter notebooks for research
├── main.py                 # CLI entry point
└── requirements.txt        # Dependencies
```

## 5. Implementation Roadmap

### Phase 1: Data Ingestion & Processing
*   Implement `fetchers.py` to get data from `yfinance`.
*   Implement `processors.py` to resample different frames (15m, 1H, 4H, 1D).

### Phase 2: The Correlation Engine
*   Build `analytics.py` to calculate Rolling Pearson/Spearman correlations.
*   Implement a "Timeframe Matrix" function: Input two assets, Output correlation across 5 different timeframes.

### Phase 3: Research & Discovery
*   Create a script to scan the S&P 500 or Crypto Top 100.
*   Find "Regime Changes": When does correlation break? (e.g., Bitcoin vs S&P 500 correlation spikes during crashes but drops during bull runs).
*   Visualize these using Heatmaps.

## 6. How to Run This Project
1.  **Setup Environment**: `pip install -r requirements.txt`
2.  **Fetch Data**: `python main.py fetch --symbol SPY --symbol BTC-USD`
3.  **Analyze**: `python main.py analyze --asset1 SPY --asset2 BTC-USD --timeframe 1h`

---
**Note on "Chronos" Name**: Amazon recently released a time-series forecasting model called "Amazon Chronos" (based on T5). While your project name is fine, be aware that searching "Chronos AI" might lead to their paper. We can refer to this as "Chronos-Discovery" internally if confusion arises.
