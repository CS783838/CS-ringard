import streamlit as st
import yfinance as yf
import requests
import matplotlib.pyplot as plt
import numpy as np

st.title("📊 Key Figures Overview")

# API Keys 
ALPHA_VANTAGE_API_KEY = "KQ8EAFY3QFMIN54B"
ALPHA_VANTAGE_URL = "https://www.alphavantage.co/query"

# Gets ticker from homepage
ticker_input = st.session_state.get("ticker", "").strip().upper()
if not ticker_input:
    st.warning("Please enter a stock ticker on the homepage first.")
    st.stop()

# Get overview stock data from Vantage API
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

# Displays company name from ticker
company_name = overview_data.get("Name", ticker_input)
st.header(f"{company_name} ({ticker_input})")

# Gets Quote Data for Current Price from Vantage API
quote_params = {
    "function": "GLOBAL_QUOTE",
    "symbol": ticker_input,
    "apikey": ALPHA_VANTAGE_API_KEY
}
quote_response = requests.get(ALPHA_VANTAGE_URL, params=quote_params)
quote_data = quote_response.json().get("Global Quote", {})
current_price = quote_data.get("05. price", "N/A")

# Format current price to 2 decimal places if valid
if current_price != "N/A":
    try:
        current_price = f"${float(current_price):,.2f}"
    except ValueError:
        current_price = "N/A"

# Display 3 key figures in columns
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Current Price", current_price)

with col2:
    market_cap = overview_data.get("MarketCapitalization", "N/A")
    if market_cap != "N/A":
        try:
            market_cap_value = int(market_cap)
            market_cap_billion = market_cap_value / 1e9
            market_cap = f"${market_cap_billion:,.2f}B"
        except ValueError:
            market_cap = "N/A"
    st.metric("Market Cap", market_cap)

with col3:
    st.metric("P/E Ratio", overview_data.get("PERatio", "N/A"))

# Drop down with more figures from the API
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

st.subheader("Quarterly Revenue and Profit")

ticker = yf.Ticker(ticker_input)
earnings = ticker.quarterly_financials.transpose()

if earnings.empty:
    st.info("No earnings data available to plot.")
else:
    quarters = earnings.index.astype(str)

    revenue = earnings['Total Revenue'] 
    profit = earnings['Net Income'] 

    revenue = revenue / 1e9
    profit = profit / 1e9

    width = 0.35
    x = np.arange(len(quarters))

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(x - width/2, revenue, width, label='Revenue', color='#4CAF50')
    ax.bar(x + width/2, profit, width, label='Profit', color='#2196F3')

    ax.set_ylabel('USD ($B)')
    ax.set_title(f"{company_name} Revenue and Profit per Quarter")
    ax.set_xticks(x)
    ax.set_xticklabels(quarters, rotation=45)
    ax.legend()

    st.pyplot(fig)
