import streamlit as st
import pandas as pd
import yfinance as yf
import datetime
import plotly.graph_objects as go

st.set_page_config(page_title="Stock Analysis", page_icon="📊", layout="wide")

st.title("Stock Analysis")

col1, col2, col3 = st.columns(3)

today=datetime.date.today()

with col1:
    ticker = st.selectbox("Stock Ticker", ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "NFLX", "AMZN", "NVDA", "GOOGL"])   