import streamlit as st
import yfinance as yf
import matplotlib.pyplot as plt
import datetime


st.title("📈 Stock Quarterly Results Tracker")

ticker_input = st.text_input("Enter a stock ticker (e.g., AAPL, MSFT):", value="AAPL")

if "earnings_fetched" not in st.session_state:
    st.session_state.earnings_fetched = False

if st.button("Get Earnings Data"):
    st.session_state.earnings_fetched = True




if st.session_state.earnings_fetched:
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

    compare_sp500 = st.checkbox("Compare with S&P 500 (SPY)")

    if compare_sp500:
        spy_data = yf.download('SPY', start=one_year_ago, end=today)

        # Normalize both to start at 100
        stock_norm = stock_data['Close'] / stock_data['Close'].iloc[0] * 100
        spy_norm = spy_data['Close'] / spy_data['Close'].iloc[0] * 100

        st.subheader("YTD Performance (Normalized to 100)")
        fig2, ax2 = plt.subplots(figsize=(10, 6))
        ax2.plot(stock_data.index, stock_norm, label=f'{ticker_input.upper()} (Normalized)', color='blue')
        ax2.plot(spy_data.index, spy_norm, label='S&P 500 (SPY) (Normalized)', color='orange')
        ax2.set_title(f"{ticker_input.upper()} vs S&P 500 - YTD Normalized Performance")
        ax2.set_xlabel("Date")
        ax2.set_ylabel("Normalized Price (Start=100)")
        ax2.legend()
        ax2.grid()
        st.pyplot(fig2)



    
    
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
