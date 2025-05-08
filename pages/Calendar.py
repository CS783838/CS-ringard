import streamlit as st
import yfinance as yf
from datetime import datetime

st.title("Earnings Calendar")
st.sidebar.markdown("⬆️ Dashboard Navigation ⬆️")

# Example data
upcoming_earnings = [
    {"date": "2025-07-28", "eps": None},
    {"date": "2025-10-28", "eps": None},
    {"date": "2026-01-27", "eps": None},
    {"date": "2026-04-28", "eps": None}
]

past_earnings = [
    {"date": "2025-04-30", "eps": 3.46},
    {"date": "2025-01-29", "eps": 3.23}
]

# User guide
with st.expander("ℹ️ How to use this page"):
    st.write("""
    - Upcoming earnings show estimated dates and EPS (if available).
    - Past earnings include reported EPS values.
    - Results are based on the selected company.
    """)

# UPCOMING EARNINGS
st.subheader("Upcoming Earnings")
#--Sort so earliest date is shown first
upcoming_earnings_sorted = sorted(upcoming_earnings, key=lambda x: x["date"])
if upcoming_earnings_sorted:
    for e in upcoming_earnings_sorted:
        with st.container():
            date = e["date"]
            eps = e["eps"]
            col1, col2 = st.columns([1, 3])
            col1.markdown(f"**{date}**")
            if eps is not None:
                col2.markdown(f"Estimated EPS: **{eps}**")
            else:
                col2.markdown("*Estimated EPS: N/A*", unsafe_allow_html=True)
            st.divider()
else:
    st.info("No upcoming earnings data available.")


# PAST EARNINGS
st.subheader("Past Earnings")
#--Sort so most recent is first
past_earnings_sorted = sorted(past_earnings, key=lambda x: x["date"], reverse=True)
if past_earnings_sorted:
    for e in past_earnings_sorted:
        with st.container():
            date = e["date"]
            eps = e["eps"]
            col1, col2 = st.columns([1, 3])
            col1.markdown(f"**{date}**")
            col2.markdown(f"Reported EPS: **{eps:.2f}**")
            st.divider()
else:
    st.info("No past earnings data available.")
