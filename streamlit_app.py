import streamlit as st
from config import NEWS_SOURCES

from services.news_fetcher import fetch_news
from services.ai_engine import analyze_news
from services.market_verifier import verify_prediction

from ui.tiles import render_tile

st.set_page_config(
    page_title="AI Market News Impact Engine",
    layout="wide"
)

st.title("AI ENHANCED MARKET NEWS IMPACT ENGINE")

st.markdown("---")

sections = {
    "NSE STOCKS": NEWS_SOURCES["stocks"],
    "COMMODITIES": NEWS_SOURCES["commodities"],
    "CURRENCY": NEWS_SOURCES["currency"]
}

for section_name, feeds in sections.items():

    st.header(section_name)

    news_items = fetch_news(feeds, limit=5)

    cols = st.columns(3)

    for idx, news in enumerate(news_items):

        ai_data = analyze_news(news)

        verification = verify_prediction(
            ai_data.get("instrument"),
            ai_data.get("sentiment")
        )

        with cols[idx % 3]:

            render_tile(
                news,
                ai_data,
                verification
            )
