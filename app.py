import streamlit as st
import yfinance as yf

st.title("📈 Stock Quarterly Results Tracker")

ticker_input = st.text_input("Enter a stock ticker (e.g., AAPL, MSFT):", value="AAPL")

if st.button("Get Earnings Data"):
    ticker = yf.Ticker(ticker_input.upper())
    earnings = ticker.quarterly_earnings

    if earnings.empty:
        st.warning("No quarterly earnings data found.")
    else:
        st.subheader("Quarterly Earnings")
        st.dataframe(earnings)

        
        st.subheader("Earnings Over Time")
        fig, ax = plt.subplots()
        earnings['Earnings'].plot(kind='bar', ax=ax)
        st.pyplot(fig)
