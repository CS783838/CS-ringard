# --- Imports ---
import streamlit as st
import yfinance as yf
import matplotlib.pyplot as plt
import datetime
import requests

# --- API Konfiguration ---
ALPHA_VANTAGE_API_KEY = "KQ8EAFY3QFMIN54B"
EODHD_API_KEY = "68100167ba5145.26409130"

# URLs
ALPHA_VANTAGE_URL = "https://www.alphavantage.co/query"
EODHD_URL = "https://eodhd.com/api/eod"

# --- Streamlit App ---
st.title("📈 Stock Quarterly Results Tracker + APIs")

ticker_input = st.text_input("Enter a stock ticker (e.g., AAPL, MSFT):", value="AAPL")

if ticker_input:
    # --- Alpha Vantage Overview Daten abrufen ---
    params_overview = {
        "function": "OVERVIEW",
        "symbol": ticker_input.upper(),
        "apikey": ALPHA_VANTAGE_API_KEY
    }
    overview_response = requests.get(ALPHA_VANTAGE_URL, params=params_overview)

    if overview_response.status_code == 200:
        overview_data = overview_response.json()

        if overview_data:
            company_name = overview_data.get("Name", ticker_input.upper())
            st.header(f"{company_name} ({ticker_input.upper()})")

            # Oben: Current Price (aus GLOBAL_QUOTE), Market Cap, P/E Ratio
            quote_params = {
                "function": "GLOBAL_QUOTE",
                "symbol": ticker_input.upper(),
                "apikey": ALPHA_VANTAGE_API_KEY
            }
            quote_response = requests.get(ALPHA_VANTAGE_URL, params=quote_params)
            if quote_response.status_code == 200:
                quote_data = quote_response.json().get("Global Quote", {})
                current_price = quote_data.get("05. price", "N/A")
            else:
                current_price = "N/A"

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

            # Untere Werte: Ausklappbar
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
        else:
            st.warning("No overview data found for this ticker.")
    else:
        st.error("Failed to fetch company overview data.")

# --- Session State Button für Earnings + Charts ---
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

        stock_norm = stock_data['Close'] / stock_data['Close'].iloc[0] * 100
        spy_norm = spy_data['Close'] / spy_data['Close'].iloc[0] * 100

        st.subheader("YTD Performance vs SPY (Normalized to 100)")
        fig2, ax2 = plt.subplots(figsize=(10, 6))
        ax2.plot(stock_data.index, stock_norm, label=f'{ticker_input.upper()} (Normalized)', color='blue')
        ax2.plot(spy_data.index, spy_norm, label='S&P 500 (SPY) (Normalized)', color='orange')
        ax2.set_title(f"{ticker_input.upper()} vs S&P 500 - YTD Normalized Performance")
        ax2.set_xlabel("Date")
        ax2.set_ylabel("Normalized Price (Start=100)")
        ax2.legend()
        ax2.grid()
        st.pyplot(fig2)

# --- 📊 Quarterly Revenue and Profit Chart ---
    if not earnings.empty:
        st.subheader("📊 Quarterly Revenue and Profit (Sample Data)")

        quarters = earnings.index.astype(str)
        revenue = earnings.iloc[:, 0]
        profit = earnings.iloc[:, 1] if earnings.shape[1] > 1 else [0] * len(earnings)

        colors = ['#4CAF50', '#2196F3']

        fig3, ax3 = plt.subplots(figsize=(8, 6))
        ax3.bar(quarters, revenue, color=colors[0], label='Revenue')
        ax3.bar(quarters, profit, color=colors[1], bottom=revenue, label='Profit')
        ax3.set_ylabel('USD ($B)')
        ax3.set_title(f"{company_name} Revenue and Profit per Quarter")
        ax3.legend()

        st.pyplot(fig3)
    else:
        st.info("No earnings data available to plot.")
