import streamlit as st
import pandas as pd
import yfinance as yf
import datetime
import plotly.express as px
import numpy as np
import CAPM_functions 

st.set_page_config(page_title="Calculate Beta", page_icon="chart_with_upwards_trend", layout="wide")

st.title("Calculate Beta and Return for individual stock")

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
    
    # 1. Calculate daily returns manually to correctly handle Pandas behavior 
    daily_returns_df = pd.DataFrame()
    daily_returns_df['Date'] = df['Date']
    daily_returns_df[stock] = df[stock].pct_change() * 100
    daily_returns_df['sp500'] = df['sp500'].pct_change() * 100
    
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
    st.subheader(f"Beta : {b}")
    st.subheader(f"Return : {round(expected_return, 2)}")
    
    # Visualization matching the expected output
    fig = px.scatter(x=sp500_arr, y=stock_arr, title=stock)
    
    # Sort sp500_arr for a clean line plot
    x_line = np.sort(sp500_arr)
    y_line = b * x_line + a
    fig.add_scatter(x=x_line, y=y_line, mode='lines', name='Expected Return', line=dict(color='red'))
    
    fig.update_layout(xaxis_title="sp500", yaxis_title=stock)
    st.plotly_chart(fig, use_container_width=True)

except Exception as e:
    st.error(f"Error calculating data: {e}")