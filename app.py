import streamlit as st

st.set_page_config(page_title="Stock Dashboard", layout="wide")



st.title("📊 Welcome to the Trade Zone")

# Step 1: Get ticker from session state (or empty string)
default_value = st.session_state.get("ticker", "")

# Step 2: Show input and update session state
ticker = st.text_input("Enter a stock ticker (e.g., AAPL):", value=default_value)

if ticker:
    st.session_state["ticker"] = ticker.strip().upper()

st.markdown("---")
st.markdown("Use the sidebar to explore:")
st.markdown("- 📈 YTD Performance and SPY Comparison")
st.markdown("- 📋 Key Figures Overview")
st.markdown("- 🤝 Competitor Analysis")

# Step 3: Show ticker if it exists
if "ticker" in st.session_state and st.session_state["ticker"]:
    st.success(f"✅ Current ticker set to: `{st.session_state['ticker']}`")