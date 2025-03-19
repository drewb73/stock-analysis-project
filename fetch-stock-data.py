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
    delta = tomorrow - yesterday

    #check if todays data is available
    if delta.days == 1:
        print("Data for today is not available yet")
    else:
        print("Data for today is available")

    # Display the first few rows
    print(data.head())

 