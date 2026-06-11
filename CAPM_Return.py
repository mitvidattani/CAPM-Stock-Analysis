#importing libraries
import datetime            
import streamlit as st    #for creating the web app
import pandas as pd       #for data manipulation
import yfinance as yf     #for fetching financial data
#import pandas_datareader.data as web - used for fetching financial data from various sources BUT now is outdated and replaced by yfinance

st.set_page_config(page_title="CAPM Return Calculator", page_icon="chart_with_upwards_trend", layout="wide")
#this sets the page configuration for the Streamlit app, including the title, icon, and layout.

st.title("Capital Asset Pricing Model (CAPM) Return Calculator") #To display the title

#To get input from the user and store it in a variable and display as columns
col1, col2 = st.columns([1,1])
with col1:
    stocks_list = st.multiselect("Select the     4 stocks you want to analyze:", ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "NFLX", "AMZN", "NVDA", "GOOGL"], default=["AAPL", "TSLA", "AMZN","GOOGL"])

with col2:
    year = st.number_input("Number of years", min_value=1, max_value=10)

#downloading the stock data for SP500
end = datetime.date.today()
start = datetime.date(end.year - year, end.month, end.day) #to subtract and get start date based on the number of years input by the user

# Fetch the S&P 500 data from Yahoo Finance instead of FRED
# We rename the column to 'sp500' to match your original FRED data format
SP500 = yf.download('^GSPC', start=start, end=end)[['Close']]
SP500.columns = ['sp500']

print(SP500.head()) # This line prints the first few rows of the S&P 500 data to the console
print(SP500.tail()) # This line prints the last few rows of the S&P 500 data to the console
