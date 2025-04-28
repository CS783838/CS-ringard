import streamlit as st
import yfinance as yf
import matplotlib.pyplot as plt

st.title("📈 Stock Quarterly Results Tracker")

ticker_input = st.text_input("Enter a stock ticker (e.g., AAPL, MSFT):", value="AAPL")

if st.button("Get Earnings Data"):
    ticker = yf.Ticker(ticker_input.upper())
    earnings = ticker.quarterly_financials.transpose()
    stock_data = yf.download(ticker_input.upper(), start = "2024-04-28", end = "2025-04-28")

    st.subheader("Price Chart")
    plt.figure(figsize=(10, 6))
    plt.plot(stock_data['Close'], label='Closing Price', color='blue')
    plt.title(ticker + " Stock Closing Prices Past Year")
    plt.xlabel("Date")
    plt.ylabel("Price (USD)")
    plt.legend()
    plt.grid()
    plt.show()
    

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
