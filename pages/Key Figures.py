import streamlit as st
import yfinance as yf
import requests
import matplotlib.pyplot as plt

st.title("📋 Key Figures Overview")

# --- API Keys ---
ALPHA_VANTAGE_API_KEY = "KQ8EAFY3QFMIN54B"
ALPHA_VANTAGE_URL = "https://www.alphavantage.co/query"

# --- Ticker ---
ticker_input = st.session_state.get("ticker", "").strip().upper()
if not ticker_input:
    st.warning("Please enter a stock ticker on the homepage first.")
    st.stop()

# --- Fetch Overview Data ---
params_overview = {
    "function": "OVERVIEW",
    "symbol": ticker_input,
    "apikey": ALPHA_VANTAGE_API_KEY
}
overview_response = requests.get(ALPHA_VANTAGE_URL, params=params_overview)

if overview_response.status_code != 200:
    st.error("Failed to fetch company overview data.")
    st.stop()

overview_data = overview_response.json()
if not overview_data:
    st.warning("No overview data found for this ticker.")
    st.stop()

company_name = overview_data.get("Name", ticker_input)
st.header(f"{company_name} ({ticker_input})")

# --- Fetch Quote Data for Current Price ---
quote_params = {
    "function": "GLOBAL_QUOTE",
    "symbol": ticker_input,
    "apikey": ALPHA_VANTAGE_API_KEY
}
quote_response = requests.get(ALPHA_VANTAGE_URL, params=quote_params)
quote_data = quote_response.json().get("Global Quote", {})
current_price = quote_data.get("05. price", "N/A")

# --- Metric Display ---
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Current Price", f"${current_price}")

with col2:
    market_cap = overview_data.get("MarketCapitalization", "N/A")
    if market_cap != "N/A":
        market_cap = f"${int(market_cap):,}"
    st.metric("Market Cap", market_cap)

with col3:
    st.metric("P/E Ratio", overview_data.get("PERatio", "N/A"))

# --- More Financial Info ---
with st.expander("More Financial Data"):
    st.write(f"**EPS (Earnings Per Share):** {overview_data.get('EPS', 'N/A')}")
    st.write(f"**Revenue/Share:** {overview_data.get('RevenuePerShareTTM', 'N/A')}")
    st.write(f"**Book Value:** {overview_data.get('BookValue', 'N/A')}")
    st.write(f"**PEG Ratio:** {overview_data.get('PEGRatio', 'N/A')}")
    st.write(f"**Dividend Yield:** {overview_data.get('DividendYield', 'N/A')}")
    st.write(f"**Beta:** {overview_data.get('Beta', 'N/A')}")
    st.write(f"**Profit Margin:** {overview_data.get('ProfitMargin', 'N/A')}")
    st.write(f"**ROE (Return on Equity):** {overview_data.get('ReturnOnEquityTTM', 'N/A')}")
    st.write(f"**52-Week Range:** {overview_data.get('52WeekLow', 'N/A')} - {overview_data.get('52WeekHigh', 'N/A')}")

# --- Quarterly Revenue and Profit Chart ---
st.subheader("📊 Quarterly Revenue and Profit")

ticker = yf.Ticker(ticker_input)
earnings = ticker.quarterly_financials.transpose()

if earnings.empty:
    st.info("No earnings data available to plot.")
else:
    quarters = earnings.index.astype(str)
    revenue = earnings.iloc[:, 0]
    profit = earnings.iloc[:, 1] if earnings.shape[1] > 1 else [0] * len(earnings)

    colors = ['#4CAF50', '#2196F3']

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.bar(quarters, revenue, color=colors[0], label='Revenue')
    ax.bar(quarters, profit, color=colors[1], bottom=revenue, label='Profit')
    ax.set_ylabel('USD ($B)')
    ax.set_title(f"{company_name} Revenue and Profit per Quarter")
    ax.legend()

    st.pyplot(fig)