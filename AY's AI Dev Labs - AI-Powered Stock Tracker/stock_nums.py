import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

raw_stock_array : list[list] = []
stock_array : list[list] = []

def get_first_of_month_prices(ticker: str):
    """
    Fetches the closing price of a stock from the first trading day
    of each month for the past 12 months and returns them as an array.
    """
    today = datetime.now().date()
    start_date = (today.replace(day=1) - timedelta(days=365))

    # Download daily historical data for the past year
    data = yf.download(ticker, start=start_date, end=today, interval="1d", progress=False)

    if data.empty:
        print(f"No data available for {ticker}.")
        return []

    # Keep only 'Close' prices
    data = data[['Close']].copy()

    prices = []  # this will store the monthly prices
    dates = []   # optional: keep track of which month each price is for

    # Loop through the last 12 months
    for i in range(13):
        target_month = today.month - i
        target_year = today.year
        while target_month <= 0:
            target_month += 12
            target_year -= 1
        first_day = datetime(target_year, target_month, 1)

        # Find the first available trading day of that month
        month_data = data.loc[data.index >= pd.Timestamp(first_day)]
        month_data = month_data[month_data.index.month == first_day.month]
        if not month_data.empty:
            first_trading_day = month_data.index[0]
            close_price = month_data.iloc[0]["Close"]
            prices.append(round(close_price, 2))
            dates.append(first_trading_day.date())

    # Reverse so it goes oldest → newest
    prices = prices[::-1]
    dates = dates[::-1]

    # Add values to array
    raw_stock_array.append([ticker, dates, prices])

    # Print values
    print(f"\n📈 {ticker} — First Trading Day Prices (Past Year)\n")
    for d, p in zip(dates, prices):
        print(f"{d}: {p}")

    print(f"\n➡️ Price array for {ticker}:")
    print(prices)

    return prices

def draw_line_graph(data, title="Line Graph", xlabel="Index", ylabel="Price of Stock (In USD)"):
    """
    Draws a line graph from an array of floats.
    """
    if not data:
        print("No data to plot.")
        return

    # Generate x-axis indices (0, 1, 2, ...)
    x = list(range(len(data)))

    # Create the line plot
    plt.figure(figsize=(8, 5))
    plt.plot(x, data, marker='o', linestyle='-', color='b', linewidth=2, markersize=6)

    # Add labels and title
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

    # Optional: Add grid and show the values on each point
    plt.grid(True)
    for i, v in enumerate(data):
        plt.text(i, v, f"{v:.2f}", ha='center', va='bottom', fontsize=8)

    # Display the graph
    plt.tight_layout()
    plt.show()



if __name__ == "__main__":
    # Example usage: fetch prices for Apple, Tesla, and Google
    tickers = ["AAPL", "TSLA", "GOOG"]

    for t in tickers:
        get_first_of_month_prices(t)

    print("\n\n\n")

    # Converts the finance "float" values into standard plottable float values
    ticker_count = len(raw_stock_array)
    for i in range(ticker_count):
        price_list = []
        for unfloated_price_value in raw_stock_array[i][2]:
            floated_price_value = unfloated_price_value.iloc[0]
            price_list.append(floated_price_value)
        stock_array.append([raw_stock_array[i][0],price_list])

print(stock_array[0][0])
print(stock_array[0][1])


if __name__ == "__main__":
    # Example array of floats (e.g., monthly stock prices)
    draw_line_graph(stock_array[0][1])