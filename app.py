import streamlit as st
import yfinance as yf
import matplotlib.pyplot as plt

st.title("📈 Stock Quarterly Results Tracker")

ticker_input = st.text_input("Enter a stock ticker (e.g., AAPL, MSFT):", value="AAPL")

if st.button("Get Earnings Data"):
    ticker = yf.Ticker(ticker_input.upper())
    earnings = ticker.quarterly_financials.transpose()

    

    if earnings is None or earnings.empty:
        st.warning("No quarterly financial data found.")
    else:
        st.subheader("Quarterly Financials")
        st.dataframe(earnings)

        if "Net Income" in earnings.columns:
            st.subheader("Net Income Over Time")
            fig, ax = plt.subplots()
            earnings["Net Income"].plot(kind='bar', ax=ax)
            st.pyplot(fig)
        else:
            st.warning("Net Income data not available for this ticker.")
