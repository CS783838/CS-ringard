import streamlit as st
import yfinance as yf
import matplotlib.pyplot as plt
import datetime


st.title("📈 Stock Quarterly Results Tracker")

ticker_input = st.text_input("Enter a stock ticker (e.g., AAPL, MSFT):", value="AAPL")

if st.button("Get Earnings Data"):
    ticker = yf.Ticker(ticker_input.upper())
    earnings = ticker.quarterly_financials.transpose()
    today = datetime.date.today()
    one_year_ago = today - datetime.timedelta(days=365)
    stock_data = yf.download(ticker_input.upper(), start=one_year_ago, end=today)

    st.subheader("YTD Performance")
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(stock_data.index, stock_data['Close'], label='Closing Price', color='blue')
    ax.set_title(f"{ticker_input.upper()} Stock Closing Prices Past Year")
    ax.set_xlabel("Date")
    ax.set_ylabel("Price (USD)")
    ax.legend()
    ax.grid()
    st.pyplot(fig)
    
    
# ignore this stuff for now

   # if earnings is None or earnings.empty:
        #st.warning("No quarterly financial data found.")
    #else:
       # st.subheader("Quarterly Financials")
        ##st.dataframe(earnings)

        #if "Net Income" in earnings.columns:
            #st.subheader("Net Income Over Time")
            #fig, ax = plt.subplots()
            #earnings["Net Income"].plot(kind='bar', ax=ax)
            #st.pyplot(fig)
        #else:
            #st.warning("Net Income data not available for this ticker.")
