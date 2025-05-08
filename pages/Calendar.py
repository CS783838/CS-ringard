import streamlit as st
import yfinance as yf
from datetime import datetime
import pandas as pd
import requests


st.title("Earnings Calendar")
st.sidebar.markdown("⬆ Dashboard Navigation ⬆")

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

# User Guide
with st.expander("ℹ️ How to use this page"):
    st.write("""
    - Upcoming earnings show estimated report dates and EPS (predicted or N/A).
    - Past earnings show reported EPS.
    - Dates are ordered for clarity.
    """)

# UPCOMING EARNINGS TABLE
st.subheader("Upcoming Earnings")
if upcoming_earnings:
    upcoming_sorted = sorted(upcoming_earnings, key=lambda x: x["date"])
    df_upcoming = pd.DataFrame(upcoming_sorted)

    # Add status and format EPS
    df_upcoming["Status"] = "Upcoming"
    df_upcoming["Estimated EPS"] = df_upcoming["eps"].apply(lambda x: f"{x:.2f}" if x is not None else "N/A")
    df_upcoming = df_upcoming.drop(columns=["eps"])

    # Order columns
    df_upcoming = df_upcoming[["date", "Status", "Estimated EPS"]]
    df_upcoming.columns = ["Date", "Status", "Estimated EPS"]

    # Display table
    st.table(df_upcoming.reset_index(drop=True))

else:
    st.info("No upcoming earnings available.")

# PAST EARNINGS TABLE
st.subheader("Past Earnings")
if past_earnings:
    past_sorted = sorted(past_earnings, key=lambda x: x["date"], reverse=True)
    df_past = pd.DataFrame(past_sorted)

    df_past["Reported EPS"] = df_past["eps"].apply(lambda x: f"{x:.2f}")
    df_past = df_past.drop(columns=["eps"])
    df_past = df_past[["date", "Reported EPS"]]
    df_past.columns = ["Date", "Reported EPS"]

    # Display table
    st.table(df_past.reset_index(drop=True))

else:
    st.info("No past earnings available.")
