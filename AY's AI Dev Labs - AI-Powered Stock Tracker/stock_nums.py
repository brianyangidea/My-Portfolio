import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt


# Gets a fills in a raw stock array
#
# Parameters:
# - data_arrays: List of lists of floats. Each sub-list is one line.
# - labels: Optional list of labels for each line.
# - title: Title of the graph.
# - xlabel: Label for the X-axis.
# - ylabe
def get_first_of_month_prices(ticker: str):
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

    # Reverse so it goes oldest to newest
    prices = prices[::-1]
    dates = dates[::-1]

    return [ticker, dates, prices]


# Plots lines on a single graph using given data.
#
# Parameters:
# - data_arrays: List of lists of floats. Each sub-list is one line.
# - labels: Optional list of labels for each line.
# - title: Title of the graph.
# - xlabel: Label for the X-axis.
# - ylabel: Label for the Y-axis.
#
def draw_line_graph(data_arrays, labels, title: str, xlabel: str, ylabel: str):
    if not data_arrays:
        print("No data provided.")
        return

    num_lines = len(data_arrays)

    # If no labels provided, generate default ones
    if labels is None or len(labels) != num_lines:
        labels = [f"Line {i+1}" for i in range(num_lines)]

    plt.figure(figsize=(10, 6))

    for i, values in enumerate(data_arrays):
        x = list(range(len(values)))  # X-axis indices
        plt.plot(x, values, marker='o', linestyle='-', linewidth=2, markersize=6, label=labels[i])
        # Optionally show values above each point
        for xi, val in enumerate(values):
            plt.text(xi, val, f"{val:.2f}", ha='center', va='bottom', fontsize=8)

    plt.title(title, fontsize=14)
    plt.xlabel(xlabel, fontsize=12)
    plt.ylabel(ylabel, fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend()
    plt.tight_layout()
    plt.show()


# The main function. Declared for ease and convention.
def main() -> None:
    raw_stock_array : list[list] = []
    stock_array : list[list] = []

    # Example usage: fetch prices for Apple, Amazon, Google, and NVIDIA Corp
    tickers = ["AAPL", "AMZN", "GOOG", "NVDA"]

    for t in tickers:
        raw_stock_array.append(get_first_of_month_prices(t))

    # Converts the finance "float" values into standard plottable float values
    ticker_count = len(raw_stock_array)
    for i in range(ticker_count):
        price_list = []
        for unfloated_price_value in raw_stock_array[i][2]:
            floated_price_value = unfloated_price_value.iloc[0]
            price_list.append(floated_price_value)
        stock_array.append([raw_stock_array[i][0],price_list])

    # Data for the line graph (Last 12 months of stocks for 4 chosen companies)
    line1 = stock_array[0][1]
    line2 = stock_array[1][1]
    line3 = stock_array[2][1]
    line4 = stock_array[3][1]

    data = [line1, line2, line3, line4]
    labels = ["Apple (AAPL)", "Amazon (AMZN)", "Alphabet Inc. (GOOG)", "NVIDIA Corp (NVDA)"]

    draw_line_graph(data, labels=labels, title="Stock Prices Comparison For The Last Year", xlabel="Last 12 Months", ylabel="Price of Stock (In USD)")
    
    return


if __name__ == "__main__":
    main()