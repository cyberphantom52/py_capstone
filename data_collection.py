import pandas as pd
import yfinance as yf

nifty_50 = ["ADANIENT", "ADANIPORTS", "APOLLOHOSP", "ASIANPAINT", "AXISBANK", "BAJAJ-AUTO", "BAJFINANCE", "BAJAJFINSV", "BEL", "BPCL", "BHARTIARTL", "BRITANNIA", "CIPLA", "COALINDIA", "DRREDDY", "EICHERMOT", "GRASIM", "HCLTECH", "HDFCBANK", "HDFCLIFE", "HEROMOTOCO", "HINDALCO", "HINDUNILVR", "ICICIBANK", "ITCHOTELS", "ITC", "INDUSINDBK", "INFY", "JSWSTEEL", "KOTAKBANK", "LT", "M&M", "MARUTI", "NTPC", "NESTLEIND", "ONGC", "POWERGRID", "RELIANCE", "SBILIFE", "SHRIRAMFIN", "SBIN", "SUNPHARMA", "TCS", "TATACONSUM", "TATAMOTORS", "TATASTEEL", "TECHM", "TITAN", "TRENT", "ULTRACEMCO", "WIPRO"]

# Fetch historical data for 1 year
dfs = []
for symbol in nifty_50:
    stock = yf.Ticker(f"{symbol}.NS")
    df = stock.history(period="1y")  # Get 1-year data
    df["Symbol"] = symbol
    dfs.append(df)

# Combine all stocks into one DataFrame
if dfs:
    full_data = pd.concat(dfs)
    full_data.to_csv("nifty_stock_data.csv")  # Save to CSV
    print("Data saved to nifty_stock_data.csv")
else:
    print("No data fetched.")
