import os
import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def time_it(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"[INFO] Execution of '{func.__name__}' took {end_time - start_time:.4f} seconds.")
        return result
    return wrapper


@time_it
def load_and_clean_data(filename):
    try:
        f = open(filename, 'r')
        df = pd.read_csv(f)
    except Exception as e:
        print(f"[ERROR] Could not read file: {e}")
        f.close()
        return None

    # Ensure required columns are present
    required_columns = ["Date", "Open", "High", "Low", "Close", "Volume", "Symbol"]
    for col in required_columns:
        if col not in df.columns:
            print(f"[ERROR] Missing required column: {col}")
            return None

    # Convert Date column to datetime
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

    # Drop rows with invalid dates
    df = df.dropna(subset=['Date'])

    # Sort by date to ensure time-series integrity
    df = df.sort_values(by='Date')

    # Handle any missing numeric values (e.g., fill with zero or mean)
    numeric_cols = ["Open", "High", "Low", "Close", "Volume", "Dividends", "Stock Splits"]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')
        df[col].fillna(0, inplace=True)

    return df


@time_it
def exploratory_data_analysis(df):
    # Identify top and bottom performing stocks by average close price
    stock_performance = df.groupby('Symbol')['Close'].mean().sort_values(ascending=False)
    top_stocks = stock_performance.head(5)
    bottom_stocks = stock_performance.tail(5)

    print("[INFO] Top 5 Stocks by Average Close Price:")
    print(top_stocks)
    print("\n[INFO] Bottom 5 Stocks by Average Close Price:")
    print(bottom_stocks)

    # Calculate daily percentage change
    df['Pct_Change'] = df.groupby('Symbol')['Close'].pct_change() * 100

    # Determine volatility by standard deviation of daily returns
    volatility = df.groupby('Symbol')['Pct_Change'].std().sort_values(ascending=False)
    print("\n[INFO] Stocks by Volatility (Std Dev of Daily % Change):")
    print(volatility.head(5))


@time_it
def data_aggregation(df):
    grouped_by_symbol = df.groupby('Symbol').agg({
        'Volume': 'mean',
        'Close': 'mean'
    }).rename(columns={'Volume': 'Avg_Volume', 'Close': 'Avg_Close'})
    print("\n[INFO] Average Volume and Close by Stock Symbol:")
    print(grouped_by_symbol.head())

    df['Month'] = df['Date'].dt.to_period('M')
    monthly_data = df.groupby(['Symbol', 'Month']).agg({
        'Close': 'mean',
        'Volume': 'sum'
    }).rename(columns={'Close': 'Monthly_Avg_Close', 'Volume': 'Monthly_Total_Volume'})
    print("\n[INFO] Monthly Aggregated Data (first few rows):")
    print(monthly_data.head())


@time_it
def create_visualizations(df):
    # Plot closing prices for top 3 symbols by average close
    top_symbols = df.groupby('Symbol')['Close'].mean().nlargest(3).index
    plt.figure(figsize=(10, 6))
    for symbol in top_symbols:
        symbol_data = df[df['Symbol'] == symbol]
        plt.plot(symbol_data['Date'], symbol_data['Close'], label=symbol)
    plt.title("Closing Prices for Top 3 Stocks")
    plt.xlabel("Date")
    plt.ylabel("Close Price")
    plt.legend()
    plt.tight_layout()
    plt.show()

    # Bar chart of average trading volume for top 5 symbols
    volume_df = df.groupby('Symbol')['Volume'].mean().nlargest(5).reset_index()
    plt.figure(figsize=(8, 5))
    plt.bar(volume_df['Symbol'], volume_df['Volume'], color='green')
    plt.title("Top 5 Stocks by Average Volume")
    plt.xlabel("Stock Symbol")
    plt.ylabel("Average Volume")
    plt.tight_layout()
    plt.show()

    # Correlation heatmap of closing prices (pivot data for correlation calculation)
    pivot_df = df.pivot_table(values='Close', index='Date', columns='Symbol').fillna(method='ffill')
    corr_matrix = pivot_df.corr()
    plt.figure(figsize=(12, 10))
    sns.heatmap(corr_matrix, cmap='coolwarm', annot=False)
    plt.title("Correlation Heatmap of Stocks (Closing Prices)")
    plt.tight_layout()
    plt.show()

def main():
    filename = "nifty_stock_data.csv"
    csv_file_path = os.path.join("data", filename)

    df = load_and_clean_data(csv_file_path)
    if df is None or df.empty:
        print("[ERROR] Data loading failed. Exiting...")
        return

    exploratory_data_analysis(df)

    data_aggregation(df)

    create_visualizations(df)


main()
