import yfinance as yf

# Download 1 month of SPY data
df = yf.download('SPY', period='1mo', interval='1d')

if not df.empty:
    df.to_csv('data/sp500.csv')
    print("✅ SPY data saved to data/sp500.csv")
else:
    print("❌ Failed to fetch SPY data")
