import streamlit as st
import requests
from datetime import datetime
import yfinance as yf

# Gets ticker from homepage
ticker_input = st.session_state.get("ticker", "").strip().upper()

if not ticker_input:
    st.warning("Please enter a stock ticker on the homepage first.")
    st.stop()

# ----------------- NEWS SECTION -----------------
st.header("Latest News")

articles = []

if st.session_state.get("ticker"):
    symbol = st.session_state["ticker"]

    # 1️⃣ Finnhub API
    api_key = "d0cctm1r01ql2j3cb5t0d0cctm1r01ql2j3cb5tg"
    finnhub_url = f"https://finnhub.io/api/v1/company-news?symbol={symbol}&from=2024-05-01&to=2025-05-05&token={api_key}"
    response = requests.get(finnhub_url)
    if response.status_code == 200:
        news_data = response.json()
        for article in news_data:
            articles.append({
                "source": "Finnhub",
                "headline": article["headline"],
                "summary": article["summary"],
                "url": article["url"],
                "datetime": datetime.fromtimestamp(article["datetime"])
            })
    else:
        st.error("Failed to fetch Finnhub news.")

    # 2️⃣ Yahoo Finance (using yfinance)
    try:
        ticker_obj = yf.Ticker(symbol)
        yahoo_news = ticker_obj.news
        for article in yahoo_news:
            articles.append({
                "source": "Yahoo Finance",
                "headline": article.get("title", ""),
                "summary": "",  # yfinance has no summary
                "url": article.get("link", ""),
                "datetime": datetime.fromtimestamp(article["providerPublishTime"])
            })
    except Exception as e:
        st.error(f"Failed to fetch Yahoo Finance news: {e}")

    # 3️⃣ Sort all articles by datetime, descending
    articles.sort(key=lambda x: x["datetime"], reverse=True)

    # 4️⃣ Display top 10 articles
    if articles:
        for article in articles[:10]:
            st.subheader(f"{article['headline']} ({article['source']})")
            if article['summary']:
                st.write(article['summary'])
            st.markdown(f"[Read more]({article['url']})")
            st.caption(f"Published: {article['datetime'].strftime('%Y-%m-%d %H:%M')}")
            st.markdown("---")
    else:
        st.info("No recent news found from both sources.")
