import streamlit as st
import pandas as pd
import yfinance as yf
import datetime
import plotly.express as px
import numpy as np
import CAPM_functions 

st.set_page_config(page_title="Calculate Beta", page_icon="chart_with_upwards_trend", layout="wide")

st.title("Calculate Beta and Return for Individual Stock")

col1, col2 = st.columns([1, 1])
with col1:
    stock = st.selectbox("Choose a stock", ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "NFLX", "NVDA"])
with col2:
    year = st.number_input("Number of Years", min_value=1, max_value=10, value=1)

@st.cache_data
def get_data(stock, year):
    end = datetime.date.today()
    start = datetime.date(end.year - year, end.month, end.day)
    stock_df = yf.download(stock, start=start, end=end)[['Close']]
    sp500_df = yf.download('^GSPC', start=start, end=end)[['Close']]
    # Explicitly flatten arrays to avoid dimension errors
    df = pd.DataFrame({
        'Date': stock_df.index, 
        stock: stock_df['Close'].values.flatten(), 
        'sp500': sp500_df['Close'].values.flatten()
    })
    return df

try:
    df = get_data(stock, year)
    
    # 1. Calculate daily returns using your existing function
    daily_returns_df = CAPM_functions.daily_return(df)
    
    # 2. Drop NaN values from the first row and ensure 1D arrays
    clean_df = daily_returns_df.iloc[1:].copy()
    stock_arr = clean_df[stock].values.astype(float).flatten()
    sp500_arr = clean_df['sp500'].values.astype(float).flatten()
    
    # 3. Calculate Beta using np.polyfit (linear regression)
    b, a = np.polyfit(sp500_arr, stock_arr, 1)
    
    # 4. CAPM Formula Calculation: E[R] = Rf + Beta * (Rm - Rf)
    # Rf is 0, so Expected Return = Beta * Rm (annualized)
    rm = sp500_arr.mean() * 252 
    expected_return = b * rm 
    
    # Display Metrics
    m1, m2 = st.columns(2)
    m1.metric("Beta", round(b, 4))
    m2.metric("Return", round(expected_return, 2))
    
    # Visualization matching the expected output
    fig = px.scatter(x=sp500_arr, y=stock_arr, trendline="ols")
    fig.update_layout(xaxis_title="sp500", yaxis_title=stock, title=stock)
    st.plotly_chart(fig, use_container_width=True)

except Exception as e:
    st.error(f"Error calculating data: {e}")