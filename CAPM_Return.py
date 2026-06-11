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

#print(SP500.head()) # This line prints the first few rows of the S&P 500 data to the console
#print(SP500.tail()) # This line prints the last few rows of the S&P 500 data to the console

stocks_df = pd.DataFrame() # Create an empty DataFrame to store stock data

for stock in stocks_list:
    data = yf.download(stock, period=f"{year}y")
    print(f"\n===== DATA FOR {stock} =====")
    #print(data.head()) # This line prints the first few rows of the stock data to the console
    stocks_df[f'{stock}'] = data['Close'] 
    #for each stock in the selected list, we download the historical data and extract the 'Close' price, which is then stored in the stocks_df DataFrame under a column named after the stock ticker.

#print(stocks_df.head()) # This line prints the first few rows of the stocks DataFrame to the console

stocks_df.reset_index(inplace=True) # Reset the index of the DataFrame to make 'Date' a regular column instead of an index
SP500.reset_index(inplace=True) # Reset the index of the S&P 500 DataFrame to make 'Date' a regular column instead of an index
SP500.columns = ['Date', 'sp500'] 
# Rename the columns of the S&P 500 DataFrame to 'Date' and 'sp500' for clarity and consistency with the stocks DataFrame

stocks_df['Date'] = stocks_df['Date'].astype("datetime64[ns]") # Convert the 'Date' column to datetime format
stocks_df['Date'] = stocks_df['Date'].apply(lambda x:str(x)[:10]) # Format the 'Date' column to keep only the date part (YYYY-MM-DD)
stocks_df['Date'] = pd.to_datetime(stocks_df['Date']) # Convert the 'Date' column back to datetime format after formatting
stocks_df = pd.merge(stocks_df, SP500, on='Date', how='inner') 
# Merge the stocks DataFrame with the S&P 500 DataFrame on the 'Date' column using an inner join to keep only matching dates 

print(stocks_df)

col1, col2 = st.columns([1,1])
with col1:
    st.markdown("### Dataframe head")
    st.dataframe(stocks_df.head(), use_container_width=True) # Display the first few rows of the merged DataFrame in the Streamlit app
with col2:
    st.markdown("### Dataframe tail")
    st.dataframe(stocks_df.tail(), use_container_width=True) # Display the last few rows of the merged DataFrame in the Streamlit app    
    