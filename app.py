import streamlit as st
import yfinance as yf
import pandas as pd
import datetime as dt
import pytz  # For timezone handling in datetime objects

# Title of the app
st.title("Stock Data Analysis")

# Predefined lists of stock tickers for S&P 500, Nasdaq, and DOW
sp500_tickers = [
    "AAPL", "MSFT", "AMZN", "GOOGL", "TSLA", "BRK-B", "NVDA", "META", "V", "JNJ",
    "WMT", "PG", "MA", "UNH", "HD", "DIS", "PYPL", "ADBE", "NFLX", "CRM",  # Add more S&P 500 tickers
]

nasdaq_tickers = [
    "AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "META", "NVDA", "ADBE", "NFLX", "CRM",
    "INTC", "CSCO", "CMCSA", "PYPL", "AMGN", "TXN", "QCOM", "COST", "SBUX", "AMD",  # Add more Nasdaq tickers
]

dow_tickers = [
    "AAPL", "MSFT", "AMGN", "BA", "CAT", "CRM", "CSCO", "CVX", "DIS", "DOW",
    "GS", "HD", "HON", "IBM", "INTC", "JNJ", "JPM", "KO", "MCD", "MMM",  # Add more DOW tickers
]

# Combine all tickers into a single list
all_tickers = list(set(sp500_tickers + nasdaq_tickers + dow_tickers))
all_tickers.sort()  # Sort the tickers alphabetically

# Sidebar for user input
st.sidebar.header("User Input")
selected_tickers = st.sidebar.multiselect(
    "Select stock tickers (S&P 500, Nasdaq, DOW)",
    all_tickers,
    default=["AAPL"]  # Default selection
)

# Debug: Display selected tickers
st.write(f"Selected Tickers: {selected_tickers}")

start_date = st.sidebar.date_input("Start date", dt.date.today() - dt.timedelta(days=365))
end_date = st.sidebar.date_input("End date", dt.date.today())

# Convert start_date and end_date to timezone-aware datetime objects
timezone = pytz.timezone("UTC")  # Use UTC timezone
start_date = timezone.localize(dt.datetime.combine(start_date, dt.time()))
end_date = timezone.localize(dt.datetime.combine(end_date, dt.time()))

# Toggles for dividends and growth rates
show_dividends = st.sidebar.checkbox("Show Dividends", value=True)
show_growth_rates = st.sidebar.checkbox("Show Growth Rates", value=True)

# Fetch stock data and dividends
def fetch_stock_data(ticker, start_date, end_date):
    """
    Fetch historical stock data and dividends for a given ticker and date range.
    """
    stock_data = yf.download(ticker, start=start_date, end=end_date)
    dividends = yf.Ticker(ticker).dividends[start_date:end_date]
    return stock_data, dividends

# Check if any tickers are selected
if not selected_tickers:
    st.error("Please select at least one stock ticker.")
else:
    # Create columns for each ticker
    columns = st.columns(len(selected_tickers))

    for i, ticker in enumerate(selected_tickers):
        with columns[i]:
            st.header(f"Stock Data for {ticker}")
            data, dividends = fetch_stock_data(ticker, start_date, end_date)

            # Check if data is valid
            if data.empty:
                st.error(f"No data available for {ticker} between {start_date} and {end_date}.")
            else:
                # Calculate historical growth rates
                def calculate_historical_growth_rate(prices_or_dividends):
                    """
                    Calculate the historical growth rate (CAGR) for a given series of prices or dividends.
                    """
                    if len(prices_or_dividends) < 2:
                        st.warning(f"Not enough data to calculate growth rate. Length: {len(prices_or_dividends)}")
                        return 0.0
                    try:
                        years = (prices_or_dividends.index[-1] - prices_or_dividends.index[0]).days / 365.25
                        growth_rate = (prices_or_dividends.iloc[-1] / prices_or_dividends.iloc[0]) ** (1 / years) - 1
                        return float(growth_rate)  # Ensure the result is a float
                    except Exception as e:
                        st.error(f"Error calculating growth rate: {e}")
                        return 0.0

                # Calculate growth rates only if the "Close" column exists
                if "Close" in data.columns:
                    price_growth_rate = calculate_historical_growth_rate(data["Close"])
                else:
                    price_growth_rate = 0.0
                    st.error(f"No 'Close' price data available for {ticker}.")

                if not dividends.empty:
                    dividend_growth_rate = calculate_historical_growth_rate(dividends)
                else:
                    dividend_growth_rate = 0.0
                    st.warning(f"No dividend data available for {ticker}.")

                # Display the data
                st.subheader(f"Stock Data for {ticker}")
                st.write(data)

                # Display growth rates
                if show_growth_rates:
                    st.subheader("Historical Growth Rates")
                    if isinstance(price_growth_rate, (float, int)):
                        st.write(f"Price Growth Rate: {price_growth_rate:.2%}")
                    else:
                        st.error(f"Invalid growth rate value: {price_growth_rate}")

                    if isinstance(dividend_growth_rate, (float, int)):
                        st.write(f"Dividend Growth Rate: {dividend_growth_rate:.2%}")
                    else:
                        st.error(f"Invalid growth rate value: {dividend_growth_rate}")

                # Plot the closing price
                if "Close" in data.columns:
                    st.subheader(f"Closing Price for {ticker}")
                    st.line_chart(data["Close"])

                # Plot the volume
                if "Volume" in data.columns:
                    st.subheader(f"Volume for {ticker}")
                    st.bar_chart(data["Volume"])

                # Plot dividends
                if show_dividends and not dividends.empty:
                    st.subheader(f"Dividends for {ticker}")
                    st.line_chart(dividends)
                    if show_growth_rates:
                        st.write(f"Dividend Growth Rate: {dividend_growth_rate:.2%}")