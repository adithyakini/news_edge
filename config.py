import streamlit as st

OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]

NEWS_SOURCES = {
    "stocks": [
        "https://feeds.finance.yahoo.com/rss/2.0/headline?s=%5ENSEI&region=US&lang=en-US"
    ],

    "commodities": [
        "https://www.investing.com/rss/news_25.rss"
    ],

    "currency": [
        "https://www.investing.com/rss/news_1.rss"
    ]
}
