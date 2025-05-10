import streamlit as st
import yfinance as yf
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression

st.set_page_config(page_title="Forecasts", layout="wide")
st.title("Machine Learning Forecasts")

# Get ticker from session state
ticker_input = st.session_state.get("ticker", "").strip().upper()

if not ticker_input:
    st.warning("Please enter a stock ticker on the homepage first.")
    st.stop()

st.header(f"Forecast for {ticker_input}")

# Fetch quarterly financials
ticker = yf.Ticker(ticker_input)
financials = ticker.quarterly_financials.transpose()

if financials.empty:
    st.error("No quarterly financial data available for this ticker.")
    st.stop()

# Extract data
quarters = financials.index.astype(str)

# Regression analysis function, takes slope of the desired figure for the last 4 quarters
# and analyzes the slope, if its positive buy, flat hold etc.
def run_regression(data_series, label):
    # sorts most recent clean data for the analysis
    clean = data_series.dropna().tail(4).sort_index()
    if len(clean) == 4:
        X = np.arange(4).reshape(-1, 1)
        y = clean.values
        # runes linear regression function on the data and takes the slope
        model = LinearRegression().fit(X, y)
        slope = model.coef_[0]

        if slope > 0.5:
            rec = "BUY"
        elif slope < -0.5:
            rec = "SELL"
        else:
            rec = "HOLD"

        st.metric(f"{label} Trend", rec, f"slope: {slope:.2f}")
        return rec
    else:
        st.info(f"Not enough clean {label.lower()} data to generate a forecast.")
        return "HOLD"

st.subheader("Revenue Forecast")
revenue = financials.get('Total Revenue') / 1e9 if 'Total Revenue' in financials else None
revenue_rec = run_regression(revenue, "Revenue")

st.subheader("Profit Forecast")
profit = financials.get('Net Income') / 1e9 if 'Net Income' in financials else None
profit_rec = run_regression(profit, "Profit")

st.subheader("EPS Forecast")
eps = ticker.earnings_per_share.get('quarterly') if hasattr(ticker, 'earnings_per_share') else None
eps_rec = "HOLD"  # placeholder, since EPS data may not be available

# Final recommendation
recommendations = [revenue_rec, profit_rec, eps_rec]
final = "HOLD"
if recommendations.count("BUY") >= 2:
    final = "BUY"
elif recommendations.count("SELL") >= 2:
    final = "SELL"

st.markdown("---")
st.subheader("Final Recommendation")
if final == "BUY":
    st.success("Final ML-based Recommendation: **BUY**")
elif final == "SELL":
    st.error("Final ML-based Recommendation: **SELL**")
else:
    st.info("Final ML-based Recommendation: **HOLD**")
