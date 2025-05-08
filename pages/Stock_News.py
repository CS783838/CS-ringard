import streamlit as st
import requests
from datetime import datetime

st.title("Latest News")
st.sidebar.markdown("⬆ Dashboard Navigation ⬆")

# Gets ticker from homepage
ticker_input = st.session_state.get("ticker", "").strip().upper()

if not ticker_input:
    st.warning("Please enter a stock ticker on the homepage first.")
    st.stop()

# ----------------- NEWS SECTION -----------------

# User Guide
with st.expander("ℹ️ How to use this page"):
    st.write("""
    - Use pagination controls below to navigate news.
    - Click on each headline to expand and read more.
    - Only a few articles are shown per page to make reading easier.
    """)

articles = []

if st.session_state.get("ticker"):
    symbol = st.session_state["ticker"]

    # Finnhub API
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

    # Sort articles (newest first)
    articles.sort(key=lambda x: x["datetime"], reverse=True)

# Pagination setup
articles_per_page = 5
total_articles = len(articles)
total_pages = (total_articles - 1) // articles_per_page + 1

if "news_page" not in st.session_state:
    st.session_state["news_page"] = 1

start = (st.session_state["news_page"] - 1) * articles_per_page
end = start + articles_per_page

st.write(f"Showing {start + 1}-{min(end, total_articles)} of {total_articles} articles")

# Show articles for current page
if total_articles > 0:
    for article in articles[start:end]:
        st.subheader(f"{article['headline']} ({article['source']})")
        if article['summary']:
            st.write(article['summary'])
        st.markdown(f"[Read more]({article['url']})")
        st.caption(f"Published: {article['datetime'].strftime('%Y-%m-%d %H:%M')}")
        st.markdown("---")
else:
    st.info("No recent news found from Finnhub.")

# Pagination controls BELOW
col1, col2, col3 = st.columns(3)
with col1:
    if st.session_state["news_page"] > 1:
        if st.button("Previous"):
            st.session_state["news_page"] -= 1

with col2:
    st.write(f"Page {st.session_state['news_page']} of {total_pages}")

with col3:
    if st.session_state["news_page"] < total_pages:
        if st.button("Next"):
            st.session_state["news_page"] += 1

# Bottom page info
st.write(f"Showing {start + 1}-{min(end, total_articles)} of {total_articles} articles")
