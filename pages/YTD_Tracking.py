import streamlit as st
import yfinance as yf
import matplotlib.pyplot as plt
import datetime

st.title("YTD Performance & Comparison")
st.sidebar.markdown("⬆️ Dashboard Navigation ⬆️")

with st.expander("ℹ️ How to use this page"):
    st.write("""
    - Enter or select a stock ticker from the homepage to begin.
    - View the stock's Year-To-Date (YTD) price performance chart.
    - Compare the selected stock's performance with popular indices or custom tickers.
    - Check the summary for positive or negative performance indicators.
    - Use the comparison feature to understand relative performance.
    """)

# Gets ticker from homepage
ticker_input = st.session_state.get("ticker", "").strip().upper()

if not ticker_input:
    st.warning("Please enter a stock ticker on the homepage first.")
    st.stop()

# Initializes date variables for YTD calculation
today = datetime.date.today()
one_year_ago = today - datetime.timedelta(days=365)

# Get stock data from the pervious year with yfinance
try:
    stock_data = yf.download(ticker_input, start=one_year_ago, end=today)
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

st.subheader("Year-To-Date (YTD) Performance Summary")

# Calculate YTD return for main ticker
ytd_return_main = (stock_data['Close'].iloc[-1] - stock_data['Close'].iloc[0]) / stock_data['Close'].iloc[0] * 100
ytd_return_main = float(ytd_return_main)

# Determine color and symbol
main_color = "green" if ytd_return_main >= 0 else "red"
main_symbol = "+" if ytd_return_main >= 0 else "-"
st.markdown(f"<span style='color:{main_color}'><b>{ticker_input}:</b> {main_symbol}{abs(ytd_return_main):.2f}%</span>", unsafe_allow_html=True)

# If comparison data exists
if 'comp_data' in locals() and not comp_data.empty:
    ytd_return_comp = (comp_data['Close'].iloc[-1] - comp_data['Close'].iloc[0]) / comp_data['Close'].iloc[0] * 100
    ytd_return_comp = float(ytd_return_comp)

    comp_color = "green" if ytd_return_comp >= 0 else "red"
    comp_symbol = "+" if ytd_return_comp >= 0 else "-"
    st.markdown(f"<span style='color:{comp_color}'><b>{comparison_ticker}:</b> {comp_symbol}{abs(ytd_return_comp):.2f}%</span>", unsafe_allow_html=True)




# 2nd Chart: Compares desired stock with another ticker
st.markdown("### Comparison Mode")

compare_mode = st.radio("Select Comparison Mode:", ["None", "Compare with famous ticker", "Custom ticker"])

comparison_ticker = None

if compare_mode == "Compare with famous ticker":
    comparison_ticker = st.selectbox("Select a comparison ticker:", ["SPY", "QQQ", "MSFT", "AAPL", "META", "AMZN"])

elif compare_mode == "Custom ticker":
    comparison_ticker = st.text_input("Enter a custom ticker:")

if comparison_ticker:
    comparison_ticker = comparison_ticker.strip().upper()
    try:
        comp_data = yf.download(comparison_ticker, start=one_year_ago, end=today)
    except Exception as e:
        st.error(f"Error fetching data for {comparison_ticker}: {e}")
        st.stop()

    if comp_data.empty:
        st.error(f"No data found for {comparison_ticker}.")
    else:
        # Normalize both stocks
        stock_norm = stock_data['Close'] / stock_data['Close'].iloc[0] * 100
        comp_norm = comp_data['Close'] / comp_data['Close'].iloc[0] * 100

        # Comparison chart
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

