
import yfinance as yf
import pandas as pd

def debug_fetch():
    ticker = "SPY"
    print(f"Fetching {ticker}...")
    try:
        df = yf.download(ticker, period="1d", interval="1h", auto_adjust=True, progress=False)
        print("Columns:", df.columns)
        print("Index:", df.index)
        print(df.head())
        
        # Check if it has multi-index columns
        if isinstance(df.columns, pd.MultiIndex):
            print("MultiIndex detected!")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    debug_fetch()
