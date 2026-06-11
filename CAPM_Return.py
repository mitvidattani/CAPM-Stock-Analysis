#importing libraries
import datetime            
import streamlit as st    #for creating the web app
import pandas as pd       #for data manipulation
import yfinance as yf     #for fetching financial data
#import pandas_datareader.data as web - used for fetching financial data from various sources BUT now is outdated and replaced by yfinance

import CAPM_functions #importing the custom functions from CAPM_functions.py


st.set_page_config(page_title="CAPM Return Calculator", page_icon="chart_with_upwards_trend", layout="wide")
#this sets the page configuration for the Streamlit app, including the title, icon, and layout.

st.title("Capital Asset Pricing Model (CAPM) Return Calculator") #To display the title

#To get input from the user and store it in a variable and display as columns
col1, col2 = st.columns([1,1])
with col1:
    stocks_list = st.multiselect("Select the     4 stocks you want to analyze:", ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "NFLX", "AMZN", "NVDA", "GOOGL"], default=["AAPL", "TSLA", "AMZN","GOOGL"])

with col2:
    year = st.number_input("Number of years", min_value=1, max_value=10)


try:
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

    col1, col2 = st.columns([1,1])
    with col1:
        st.markdown("### Price of all the Stocks")
        st.plotly_chart(CAPM_functions.interactive_plot(stocks_df), use_container_width=True) # Display the interactive plot in the Streamlit app
    with col2:
        st.markdown("### Normalized Price of all the Stocks")
        st.plotly_chart(CAPM_functions.interactive_plot(CAPM_functions.normalize(stocks_df)), use_container_width=True) 
        # Normalize the stock prices and display the interactive plot of normalized prices in the Streamlit app

    stocks_daily_returns = CAPM_functions.daily_return(stocks_df)
    print (stocks_daily_returns.head()) # This line prints the first few rows of the daily returns DataFrame to the console

    beta = {}
    alpha = {}

    for i in stocks_daily_returns.columns:
        if i != 'Date' and i != 'sp500': # Loop through each column in the daily returns DataFrame, excluding 'Date' and 'sp500'
            b, a = CAPM_functions.calculate_beta(stocks_daily_returns, i) # Calculate beta and alpha for the stock using the calculate_beta function
            beta[i] = b # Store the calculated beta in the beta dictionary with the stock ticker as the key
            alpha[i] = a # Store the calculated alpha in the alpha dictionary with the stock ticker as the key
    print(beta, alpha) # This line prints the calculated beta and alpha values for each stock to the console        

    beta_df = pd.DataFrame(columns = ['Stock', 'Beta Value'])
    beta_df['Stock'] = beta.keys() 
    # Create a new DataFrame for beta values and populate the 'Stock' column with the stock tickers from the beta dictionary
    beta_df['Beta Value'] = [str(round(i, 2)) for i in beta.values()]

    with col1:
        st.markdown("### Calculated Beta Values")
        st.dataframe(beta_df, use_container_width=True) # Display the beta values DataFrame in the Streamlit app

    rf = 0
    rm = stocks_daily_returns['sp500'].mean()*252 # Calculate the average market return (S&P 500 daily returns annualized)

    return_df = pd.DataFrame()
    return_value = []
    for stock, value in beta.items():
        return_value.append(str(round(rf + value * (rm - rf), 2))) 
        # Calculate the expected return for each stock using the CAPM formula and store it in the return_value list
    return_df['Stock'] = stocks_list # Populate the 'Stock' column of the return DataFrame with the stock tickers

    return_df['Return Value'] = return_value # Populate the 'Return Value' column of the return DataFrame with the calculated expected returns1
    with col2:
        st.markdown("### Calculated Return Values using CAPM")
        st.dataframe(return_df, use_container_width=True) # Display the expected return values DataFrame in the Streamlit app

except:
    st.write("Please select valid inputs")
    