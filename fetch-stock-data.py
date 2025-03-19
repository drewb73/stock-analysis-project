import yfinance as yf
import pandas as pd
import datetime as dt

def fetch_stock_data(ticker, start_date, end_date):
    """
    Fetch historical stock data for a given ticker and date range.
    """
    stock_data = yf.download(ticker, start=start_date, end=end_date)
    return stock_data

if __name__ == "__main__":
    # Define the stock ticker and date range
    ticker = input("Enter the stock ticker: ")

    # Calculate yesterdays date and todays date
    today = dt.date.today()
    yesterday = today - dt.timedelta(days=1)
    tomorrow = today + dt.timedelta(days=1)

    # Fetch the data
    data = fetch_stock_data(ticker, yesterday, tomorrow)

  # Check if data is available
    if data.empty:
        print(f"No data available for {ticker} between {yesterday} and {today}.")
    else:
        # Display the first few rows
        print(data.head())

        # Check if today's data is available
        if data.index[-1].date() == today:
            print("Today's data is available.")
        else:
            print("Today's data is not yet available.")


 