import streamlit as st

st.set_page_config(page_title="Stock Dashboard", layout="wide")
st.sidebar.markdown("⬆️ Dashboard Navigation ⬆️")

st.title("🏠 Welcome to the Trade Zone")

# Welcome text
st.markdown(
    """
    This dashboard helps you explore the financial performance of public companies using real-time market data.

    **To begin**, enter a US stock ticker below, then navigate through the analysis pages using the sidebar:
    -  **Industry Analysis**
    -  **Key Figures**
    -  **YTD Tracking**
    """
)

# User inputs ticker, it is saved in session state so streamlit doesn't reset with every interaction
st.markdown("Select a Company")
default_value = st.session_state.get("ticker", "")
ticker = st.text_input("Enter stock ticker (e.g., AAPL)", value=default_value)

if ticker:
    st.session_state["ticker"] = ticker.strip().upper()

# Visual indication of ticker being entered
if st.session_state.get("ticker"):
    st.info(f"Currently analyzing: **{st.session_state['ticker']}**")
else:
    st.warning("Please enter a valid stock ticker to get started.")

# Validate ticker
    try:
        data = yf.Ticker(st.session_state["ticker"]).info

        if data and "regularMarketPrice" in data and data["regularMarketPrice"] is not None:
            st.success(f"✅ Valid ticker: **{st.session_state['ticker']}**")
        else:
            st.error("❌ Invalid ticker, please try again.")
    except Exception as e:
        st.error("❌ Error fetching data. Please try another ticker.")

# Recent tickets viewed
if "recent_tickers" not in st.session_state:
    st.session_state["recent_tickers"] = []

if ticker and ticker not in st.session_state["recent_tickers"]:
    st.session_state["recent_tickers"].insert(0, ticker)
    st.session_state["recent_tickers"] = st.session_state["recent_tickers"][:5]  # keep last 5

if st.session_state["recent_tickers"]:
    st.markdown("**Recently searched tickers:**")

    for ticker in st.session_state["recent_tickers"]:
        if st.button(ticker):
            st.session_state["ticker"] = ticker
            st.success(f"✅ {ticker} selected!")

# Onboarding tips expander
with st.expander("ℹ️ How to use this page"):
    st.write("""
        - Enter a valid stock ticker in the input box
        - Navigate using the sidebar
        - Use the recent tickers for quick access
        - Explore YTD, Key Figures and Competitors, News, Dates and more
    """)