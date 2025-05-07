import streamlit as st
import yfinance as yf
import matplotlib.pyplot as plt
import datetime

st.title("YTD Performance & Comparison")

# Gets ticker from homepage
ticker_input = st.session_state.get("ticker", "").strip().upper()

if not ticker_input:
    st.warning("Please enter a stock ticker on the homepage first.")
    st.stop()

# Date range selection
st.subheader("Select Time Range")
today = datetime.date.today()

start_date = st.date_input("Start Date", value=today - datetime.timedelta(days=365))
end_date = st.date_input("End Date", value=today)

if start_date >= end_date:
    st.error("Start date must be before end date.")
    st.stop()

# Get stock data from the pervious year with yfinance
try:
    stock_data = yf.download(ticker_input, start=start_date, end=end_date)
except Exception as e:
    st.error(f"Error fetching data for {ticker_input}: {e}")
    st.stop()

if stock_data.empty:
    st.error(f"No data found for {ticker_input}.")
    st.stop()

# 1st Chart: YTD performance of entered stock
st.subheader("YTD Performance")
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(stock_data.index, stock_data['Close'], label='Closing Price', color='blue')
ax.set_title(f"{ticker_input} Stock Closing Prices (Past Year)")
ax.set_xlabel("Date")
ax.set_ylabel("Price (USD)")
ax.legend()
ax.grid()
st.pyplot(fig)

# 2nd Chart: Compares desired stock with another ticker
compare = st.checkbox("Compare with another ticker", value=True)

if compare:
    comparison_ticker = st.text_input("Enter a comparison ticker (e.g., SPY, QQQ, MSFT):", value="SPY").strip().upper()
    # Get second ticker's data from yfinance
    if comparison_ticker:
        try:
            comp_data = yf.download(comparison_ticker, start=start_date, end=end_date)
        except Exception as e:
            st.error(f"Error fetching data for {comparison_ticker}: {e}")
            st.stop()

        if comp_data.empty:
            st.error(f"No data found for {comparison_ticker}.")
        else:
            # normalizes both to 100 for proper comparison
            stock_norm = stock_data['Close'] / stock_data['Close'].iloc[0] * 100
            comp_norm = comp_data['Close'] / comp_data['Close'].iloc[0] * 100

            # generates second chart with both tickers
            st.subheader(f"YTD Comparison: {ticker_input} vs {comparison_ticker}")
            fig2, ax2 = plt.subplots(figsize=(10, 6))
            ax2.plot(stock_data.index, stock_norm, label=f"{ticker_input} (Normalized)", color='blue')
            ax2.plot(comp_data.index, comp_norm, label=f"{comparison_ticker} (Normalized)", color='orange')
            ax2.set_xlabel("Date")
            ax2.set_ylabel("Normalized Price (Start = 100)")
            ax2.set_title(f"{ticker_input} vs {comparison_ticker} - YTD Performance")
            ax2.legend()
            ax2.grid()
            st.pyplot(fig2)
