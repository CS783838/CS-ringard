import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

st.title("Industry Comparison")

# Dictionnary of sectors with benchmarks for easy comparison
INDUSTRY_BENCHMARKS = {
    "Technology": {
        "PE_Ratio": 27.5, "MarketCap_B": 500,
        "ROE": 25.0, "ProfitMargin": 18.0, "DividendYield": 1.0, "Beta": 1.2
    },
    "Healthcare": {
        "PE_Ratio": 18.0, "MarketCap_B": 350,
        "ROE": 15.0, "ProfitMargin": 13.0, "DividendYield": 1.8, "Beta": 0.8
    },
    "Financial Services": {
        "PE_Ratio": 13.0, "MarketCap_B": 300,
        "ROE": 12.0, "ProfitMargin": 20.0, "DividendYield": 2.5, "Beta": 1.1
    },
    "Consumer Cyclical": {
        "PE_Ratio": 20.5, "MarketCap_B": 280,
        "ROE": 18.0, "ProfitMargin": 10.0, "DividendYield": 1.6, "Beta": 1.3
    },
    "Consumer Defensive": {
        "PE_Ratio": 22.0, "MarketCap_B": 240,
        "ROE": 17.0, "ProfitMargin": 9.0, "DividendYield": 2.3, "Beta": 0.6
    },
    "Communication Services": {
        "PE_Ratio": 19.5, "MarketCap_B": 400,
        "ROE": 14.0, "ProfitMargin": 11.0, "DividendYield": 1.2, "Beta": 1.1
    },
    "Energy": {
        "PE_Ratio": 9.0, "MarketCap_B": 250,
        "ROE": 16.0, "ProfitMargin": 15.0, "DividendYield": 3.5, "Beta": 1.3
    },
    "Industrials": {
        "PE_Ratio": 17.0, "MarketCap_B": 200,
        "ROE": 13.0, "ProfitMargin": 8.0, "DividendYield": 1.9, "Beta": 1.1
    },
    "Utilities": {
        "PE_Ratio": 15.5, "MarketCap_B": 150,
        "ROE": 10.0, "ProfitMargin": 12.0, "DividendYield": 3.0, "Beta": 0.5
    },
    "Real Estate": {
        "PE_Ratio": 25.0, "MarketCap_B": 100,
        "ROE": 9.0, "ProfitMargin": 7.0, "DividendYield": 3.8, "Beta": 0.7
    },
    "Basic Materials": {
        "PE_Ratio": 14.0, "MarketCap_B": 120,
        "ROE": 11.0, "ProfitMargin": 10.0, "DividendYield": 2.2, "Beta": 1.0
    }
}

# Gets ticker from main app.py
ticker = st.session_state.get("ticker", "").strip().upper()
if not ticker:
    st.warning("Please enter a stock ticker on the homepage first.")
    st.stop()

# Gets necessary stock information from yfinance
try:
    stock = yf.Ticker(ticker)
    info = stock.info
    sector = info.get("sector", "Unknown")
    stock_pe = info.get("trailingPE")
    stock_mc = info.get("marketCap")
    stock_roe = info.get("returnOnEquity")
    stock_margin = info.get("profitMargins")
    stock_div = info.get("dividendYield")
    stock_beta = info.get("beta")
except:
    st.error("Failed to fetch data from yfinance.")
    st.stop()

# Error if theres no sector / its not in the dictionnary
if not sector or sector not in INDUSTRY_BENCHMARKS:
    st.warning(f"No benchmark data for sector: {sector}")
    st.stop()

bench = INDUSTRY_BENCHMARKS[sector]

# Convert and round metrics for better comparison
stock_data = {
    "PE_Ratio": round(float(stock_pe), 2) if stock_pe is not None else None,
    "MarketCap_B": round(float(stock_mc) / 1e9, 2) if stock_mc is not None else None,
    "ROE": round(float(stock_roe) * 100, 2) if stock_roe is not None else None,
    "ProfitMargin": round(float(stock_margin) * 100, 2) if stock_margin is not None else None,
    "DividendYield": round(float(stock_div), 2) if stock_div is not None else None,
    "Beta": round(float(stock_beta), 2) if stock_beta is not None else None
}

st.markdown(f"**Sector:** {sector}")

st.subheader("P/E Comparison")

# --- P/E Ratio Chart ---
pe_diff = round(stock_data["PE_Ratio"] - bench["PE_Ratio"], 2)
if pe_diff > 0:
    st.markdown(f"<span style='color:green'>{ticker} is {pe_diff} points above the industry average.</span>", unsafe_allow_html=True)
elif pe_diff < 0:
    st.markdown(f"<span style='color:red'>{ticker} is {abs(pe_diff)} points below the industry average.</span>", unsafe_allow_html=True)
else:
    st.markdown(f"{ticker} is exactly in line with the industry average.")

pe_df = pd.DataFrame({
    "P/E Ratio": [stock_data["PE_Ratio"], bench["PE_Ratio"]]
}, index=[ticker, f"{sector} Avg"])
st.write("**P/E Ratio**")
st.bar_chart(pe_df)

st.subheader("Market Cap Comparison")

# --- Market Cap Chart ---
mc_diff = round(stock_data["MarketCap_B"] - bench["MarketCap_B"], 2)
if mc_diff > 0:
    st.markdown(f"<span style='color:green'>{ticker} is {mc_diff} billion USD above the industry average.</span>", unsafe_allow_html=True)
elif mc_diff < 0:
    st.markdown(f"<span style='color:red'>{ticker} is {abs(mc_diff)} billion USD below the industry average.</span>", unsafe_allow_html=True)
else:
    st.markdown(f"{ticker}'s market cap is exactly in line with the industry average.")

mc_df = pd.DataFrame({
    "Market Cap ($B)": [stock_data["MarketCap_B"], bench["MarketCap_B"]]
}, index=[ticker, f"{sector} Avg"])
st.write("**Market Capitalization**")
st.bar_chart(mc_df)


st.subheader("Profitability & Dividend Yield")

# Table (keep as-is)
profit_df = pd.DataFrame({
    "Metric": ["ROE (%)", "Profit Margin (%)", "Dividend Yield (%)"],
    ticker: [stock_data["ROE"], stock_data["ProfitMargin"], stock_data["DividendYield"]],
    f"{sector} Avg": [bench["ROE"], bench["ProfitMargin"], bench["DividendYield"]]
}).set_index("Metric")
st.dataframe(profit_df)

# --- ROE Chart ---
roe_diff = round(stock_data["ROE"] - bench["ROE"], 2)
if roe_diff > 0:
    st.markdown(f"<span style='color:green'>{ticker} is {roe_diff}% above the industry average.</span>", unsafe_allow_html=True)
elif roe_diff < 0:
    st.markdown(f"<span style='color:red'>{ticker} is {abs(roe_diff)}% below the industry average.</span>", unsafe_allow_html=True)
else:
    st.markdown(f"{ticker} is exactly in line with the industry average.")

st.write("**Return on Equity (ROE %)**")
roe_df = pd.DataFrame({
    "ROE (%)": [stock_data["ROE"], bench["ROE"]]
}, index=[ticker, f"{sector} Avg"])
st.bar_chart(roe_df)


# --- Profit Margin Chart ---
pm_diff = round(stock_data["ProfitMargin"] - bench["ProfitMargin"], 2)
if pm_diff > 0:
    st.markdown(f"<span style='color:green'>{ticker} has a profit margin {pm_diff}% above the industry average.</span>", unsafe_allow_html=True)
elif pm_diff < 0:
    st.markdown(f"<span style='color:red'>{ticker} has a profit margin {abs(pm_diff)}% below the industry average.</span>", unsafe_allow_html=True)
else:
    st.markdown(f"{ticker}'s profit margin is exactly at the industry average.")

st.write("**Profit Margin (%)**")
pm_df = pd.DataFrame({
    "Profit Margin (%)": [stock_data["ProfitMargin"], bench["ProfitMargin"]]
}, index=[ticker, f"{sector} Avg"])
st.bar_chart(pm_df)


# --- Dividend Yield Chart ---
div_diff = round(stock_data["DividendYield"] - bench["DividendYield"], 2)
if div_diff > 0:
    st.markdown(f"<span style='color:green'>{ticker} offers a dividend yield {div_diff}% above the industry average.</span>", unsafe_allow_html=True)
elif div_diff < 0:
    st.markdown(f"<span style='color:red'>{ticker}'s dividend yield is {abs(div_diff)}% below the industry average.</span>", unsafe_allow_html=True)
else:
    st.markdown(f"{ticker}'s dividend yield is exactly in line with the industry average.")

st.write("**Dividend Yield (%)**")
div_df = pd.DataFrame({
    "Dividend Yield (%)": [stock_data["DividendYield"], bench["DividendYield"]]
}, index=[ticker, f"{sector} Avg"])
st.bar_chart(div_df)


# --- Risk Table & Chart ---
risk_df = pd.DataFrame({
    "Metric": ["Beta"],
    ticker: [stock_data["Beta"]],
    f"{sector} Avg": [bench["Beta"]]
}).set_index("Metric")

st.subheader("Risk")
st.dataframe(risk_df)
st.bar_chart(risk_df)