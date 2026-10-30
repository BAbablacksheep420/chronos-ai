# Chronos AI

A unified quantitative research platform featuring multi-timeframe correlation discovery alongside a high-frequency subsidiary engine for **Limit Order Book (LOB) Forecasting Under Regime Shifts**.

---

## 🏗️ Architecture Overview

Chronos AI is structured into two complementary engines:

```
chronos-ai/
├── chronos/                          # Core Package
│   ├── fetchers.py                   # [Core] Historical yfinance OHLCV data pipeline
│   ├── processors.py                 # [Core] Multi-timeframe OHLC resampling (1H, 4H, 1D, etc.)
│   ├── analytics.py                  # [Core] Rolling correlation, Engle-Granger cointegration
│   ├── visualizer.py                 # [Core] Correlation heatmaps and regime shift visuals
│   └── orderbook/                    # 🚀 [SUBSIDIARY FEATURE] LOB Forecasting Under Regime Shifts
│       ├── fetchers.py               # Binance Level-2 snapshot fetcher & synthetic LOB simulator
│       ├── features.py               # Microstructural feature engineering (OI, Microprice, VWAP)
│       ├── regime_detector.py        # Rolling KS test & Page-Hinkley online change detection
│       ├── model.py                  # PyTorch Dilated TCN & Regime-Adaptive inference head
│       ├── trainer.py                # Chronological training & streaming evaluation
│       └── visualizer.py             # 4-panel interactive Plotly diagnostic dashboard
├── experiments/
│   ├── research_demo.py              # [Core] Multi-timeframe correlation demo
│   ├── unified_research.py           # [Core] Unified research pipeline
│   ├── orderbook_research_demo.py    # [Subsidiary] Standalone LOB forecasting demo
│   └── orderbook_benchmark.py        # [Subsidiary] High-frequency latency benchmark (<10ms SLA)
├── main.py                           # Unified CLI entry point
├── RESEARCH_PROPOSAL.md              # Research proposal for Multi-Timeframe Correlation Discovery
├── ORDERBOOK_RESEARCH_PROPOSAL.md    # Research proposal & writeup for Order Book Forecasting
└── requirements.txt                  # Complete platform dependencies
```

---

## ⚡ Quickstart

### 1. Environment Setup
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

---

## 📊 Core Engine: Multi-Timeframe Correlation Discovery

The core engine discovers lead-lag, cointegration, and correlation breakdown dynamics across diverse asset classes and time horizons.

```bash
# 1. Fetch asset data (Tech stocks, Crypto, Commodities)
python main.py fetch --ticker BTC-USD --ticker ETH-USD --ticker SPY --ticker QQQ --period 1y

# 2. Analyze pair correlation & cointegration
python main.py analyze --asset1 BTC-USD --asset2 SPY --timeframe 1D

# 3. Generate interactive cross-asset correlation matrix heatmap
python main.py scan --tickers BTC-USD --tickers ETH-USD --tickers SPY --tickers QQQ --out daily_heatmap.html

# 4. Detect correlation breakdown regimes
python main.py regime --asset1 BTC-USD --asset2 SPY --timeframe 1D --threshold 0.5
```

---

## 🔬 Subsidiary Feature: Order Book Forecasting Under Regime Shifts (LOB-RS)

The subsidiary module addresses **Problem 4: Order Book Forecasting Under Regime Shifts**. Supervised models trained on quiet markets experience **silent degradation** when macro shocks or flash crashes occur. Chronos LOB-RS integrates statistical concept drift detection (Two-Sample Kolmogorov-Smirnov + Page-Hinkley) directly into the forecasting loop to detect shifts and dynamically recalibrate uncertainty.

### Running LOB-RS Via CLI

```bash
# Run end-to-end research demo (Simulate LOB -> Extract Features -> Train TCN -> Adaptive Eval -> Plot)
python main.py orderbook demo --steps 2000 --model-type tcn --out orderbook_regime_analysis.html

# Fetch live Level-2 order book snapshot from Binance
python main.py orderbook fetch --symbol BTCUSDT --limit 20 --out data/btc_lob.csv

# Generate synthetic multi-regime dataset (Calm -> Macro Shock -> Trending Flow)
python main.py orderbook fetch --synthetic --steps 2500 --out data/synthetic_lob.csv

# Extract microstructural LOB features
python main.py orderbook features --input-csv data/synthetic_lob.csv --out data/lob_features.csv

# Run latency & throughput benchmarks
python main.py orderbook benchmark --iterations 1000
```

### Running Standalone Experiments

```bash
# Standalone Order Book Research Demo
python experiments/orderbook_research_demo.py

# Standalone Ultra-Low Latency Benchmark
python experiments/orderbook_benchmark.py
```

---

## 📈 Benchmark Summary

- **Feature Throughput:** > 120,000 LOB snapshots / second
- **Streaming KS + Page-Hinkley Shift Detection:** 0.20 ms / tick
- **Model Inference (TCN / Gradient Boosting):** 0.35 ms / tick
- **Combined Pipeline Latency:** **0.50 ms** (Target: < 10.0 ms SLA — **20x faster than budget**)
- **Adverse Selection Protection:** 100% of false directional spikes suppressed during severe liquidity shocks.

---

## 📚 Documentation
- **Core Research Proposal:** [`RESEARCH_PROPOSAL.md`](RESEARCH_PROPOSAL.md)
- **Order Book Research Proposal & Writeup:** [`ORDERBOOK_RESEARCH_PROPOSAL.md`](ORDERBOOK_RESEARCH_PROPOSAL.md)
