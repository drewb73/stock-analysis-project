import streamlit as st
import yfinance as yf
import pandas as pd
import datetime as dt

# Title of the app
st.title("Stock Data Analysis")

# Sidebar for user input
st.sidebar.header("User Input")
ticker = st.sidebar.text_input("Enter the stock ticker", "AAPL")
start_date = st.sidebar.date_input("Start date", dt.date.today() - dt.timedelta(days=365))
end_date = st.sidebar.date_input("End date", dt.date.today())

# Fetch stock data
@st.cache_data  # Cache the data to improve performance
def fetch_stock_data(ticker, start_date, end_date):
    stock_data = yf.download(ticker, start=start_date, end=end_date)
    return stock_data

data = fetch_stock_data(ticker, start_date, end_date)

# Display the data
st.subheader(f"Stock Data for {ticker}")
st.write(data)

# Plot the closing price
st.subheader(f"Closing Price for {ticker}")
st.line_chart(data["Close"])

# Plot the volume
st.subheader(f"Volume for {ticker}")
st.bar_chart(data["Volume"])