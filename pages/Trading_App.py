import streamlit as st

st.set_page_config(page_title="Trading App", page_icon="📉", layout="wide")
st.title("Trading Guide : Learn to Trade Like a Pro")
st.header("This is your platform to collect and analyse all informationprior to investing in the stocks.")

st.image("https://t3.ftcdn.net/jpg/03/10/46/56/360_F_310465670_Wy4QCEfxYU2ziHjbeZsNAumKhaZzZS1w.jpg", width=2000)

st.markdown("## We provide the following services:")

st.markdown("#### :one: Stock Information")
st.write("Through this page, you can see all the information about stock. ")

st.markdown("#### :two: Stock Prediction")
st.write("You can explore predicted closing prices for the next 30 days based on historical stock data and advanced forecasting models. Use this tool to gain insights into potential future stock performance and make informed investment decisions.")

st.markdown('#### :three: CAPM Return')
st.write("Discover how the Capital Asset Pricing Model (CAPM) calculates the expected return of different stocks asset based on its risk and market performance.")

st.markdown('#### :four: CAPM Beta')
st.write("Calculates Beta and Expected Return for Individual Stocks.")