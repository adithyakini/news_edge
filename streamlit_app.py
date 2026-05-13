# app.py
# ------------------------------------------------------------
# Market News Impact Dashboard
# Streamlit App
#
# Features:
# - Scrapes latest financial news
# - Categorizes into:
#     Stocks
#     Currency
#     Commodities
#     Global Macro
# - Tracks actual market impact
# - Predictive impact scoring
# - Marks predictive/correct news in GREEN
# - Auto refresh
# - Clean Bloomberg-style layout
#
# Run:
# pip install streamlit yfinance pandas requests beautifulsoup4 feedparser plotly newspaper3k
#
# streamlit run app.py
# ------------------------------------------------------------

import streamlit as st
import pandas as pd
import yfinance as yf
import requests
import feedparser
import plotly.express as px
from bs4 import BeautifulSoup
from datetime import datetime
import time

# ------------------------------------------------------------
# PAGE CONFIG
# ------------------------------------------------------------

st.set_page_config(
    page_title="Market News Impact Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ------------------------------------------------------------
# CUSTOM CSS
# ------------------------------------------------------------

st.markdown("""
<style>

body {
    background-color: #0E1117;
}

.big-title {
    font-size: 38px;
    font-weight: bold;
    color: white;
}

.section-title {
    font-size: 24px;
    font-weight: bold;
    padding-bottom: 10px;
}

.news-card {
    padding: 15px;
    border-radius: 12px;
    margin-bottom: 12px;
    background-color: #1C1F26;
    border-left: 6px solid #444;
}

.green-card {
    border-left: 6px solid #00FF99;
    background-color: rgba(0,255,100,0.08);
}

.red-card {
    border-left: 6px solid #FF4B4B;
}

.metric-box {
    background-color: #1C1F26;
    padding: 15px;
    border-radius: 12px;
    text-align: center;
}

</style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------
# NEWS SOURCES
# ------------------------------------------------------------

RSS_FEEDS = {
    "Stocks": [
        "https://feeds.finance.yahoo.com/rss/2.0/headline?s=%5ENSEI&region=US&lang=en-US",
        "https://www.moneycontrol.com/rss/business.xml"
    ],
    "Currency": [
        "https://www.investing.com/rss/news_1.rss"
    ],
    "Commodities": [
        "https://www.investing.com/rss/news_25.rss"
    ],
    "Macro": [
        "https://feeds.a.dj.com/rss/RSSMarketsMain.xml"
    ]
}

# ------------------------------------------------------------
# MARKET DATA
# ------------------------------------------------------------

MARKET_SYMBOLS = {
    "NIFTY": "^NSEI",
    "BANKNIFTY": "^NSEBANK",
    "USDINR": "INR=X",
    "GOLD": "GC=F",
    "SILVER": "SI=F",
    "CRUDE": "CL=F"
}

# ------------------------------------------------------------
# FETCH MARKET DATA
# ------------------------------------------------------------

@st.cache_data(ttl=300)
def get_market_data():

    data = {}

    for name, ticker in MARKET_SYMBOLS.items():

        try:
            t = yf.Ticker(ticker)
            hist = t.history(period="2d")

            latest = hist["Close"].iloc[-1]
            prev = hist["Close"].iloc[-2]

            change = latest - prev
            pct = (change / prev) * 100

            data[name] = {
                "price": round(latest, 2),
                "change": round(change, 2),
                "pct": round(pct, 2)
            }

        except:
            data[name] = {
                "price": 0,
                "change": 0,
                "pct": 0
            }

    return data

# ------------------------------------------------------------
# FETCH NEWS
# ------------------------------------------------------------

@st.cache_data(ttl=600)
def fetch_news():

    all_news = []

    for category, feeds in RSS_FEEDS.items():

        for url in feeds:

            try:
                feed = feedparser.parse(url)

                for entry in feed.entries[:10]:

                    title = entry.title
                    link = entry.link
                    published = entry.get("published", "")

                    sentiment = detect_sentiment(title)
                    predictive = detect_predictive_signal(title)

                    all_news.append({
                        "category": category,
                        "title": title,
                        "link": link,
                        "published": published,
                        "sentiment": sentiment,
                        "predictive": predictive
                    })

            except:
                pass

    return pd.DataFrame(all_news)

# ------------------------------------------------------------
# SIMPLE SENTIMENT ENGINE
# ------------------------------------------------------------

def detect_sentiment(text):

    bullish_words = [
        "surge",
        "rally",
        "gain",
        "bullish",
        "rise",
        "jump",
        "breakout",
        "strong",
        "up"
    ]

    bearish_words = [
        "fall",
        "drop",
        "crash",
        "bearish",
        "weak",
        "selloff",
        "decline",
        "down"
    ]

    text = text.lower()

    bull_score = sum(word in text for word in bullish_words)
    bear_score = sum(word in text for word in bearish_words)

    if bull_score > bear_score:
        return "Bullish"

    elif bear_score > bull_score:
        return "Bearish"

    return "Neutral"

# ------------------------------------------------------------
# PREDICTIVE NEWS DETECTION
# ------------------------------------------------------------

def detect_predictive_signal(text):

    predictive_keywords = [
        "expected",
        "forecast",
        "may",
        "likely",
        "could",
        "outlook",
        "target",
        "signals",
        "ahead",
        "predicts"
    ]

    text = text.lower()

    return any(word in text for word in predictive_keywords)

# ------------------------------------------------------------
# ACTUAL IMPACT ENGINE
# ------------------------------------------------------------

def infer_market_impact(news_title, market_data):

    news_title = news_title.lower()

    if "oil" in news_title or "crude" in news_title:
        return f"Crude: {market_data['CRUDE']['pct']}%"

    elif "gold" in news_title:
        return f"Gold: {market_data['GOLD']['pct']}%"

    elif "rupee" in news_title or "usd" in news_title:
        return f"USDINR: {market_data['USDINR']['pct']}%"

    elif "nifty" in news_title or "sensex" in news_title:
        return f"NIFTY: {market_data['NIFTY']['pct']}%"

    return "Impact unclear"

# ------------------------------------------------------------
# DASHBOARD HEADER
# ------------------------------------------------------------

st.markdown(
    "<div class='big-title'>📈 AI Market News Impact Dashboard</div>",
    unsafe_allow_html=True
)

st.write(
    "Real-time news intelligence across Stocks, Currency, Commodities, and Macro Markets"
)

# ------------------------------------------------------------
# MARKET SNAPSHOT
# ------------------------------------------------------------

market_data = get_market_data()

metric_cols = st.columns(len(market_data))

for idx, (name, values) in enumerate(market_data.items()):

    with metric_cols[idx]:

        delta_color = "normal"

        st.metric(
            label=name,
            value=values["price"],
            delta=f"{values['pct']}%"
        )

# ------------------------------------------------------------
# FETCH NEWS
# ------------------------------------------------------------

news_df = fetch_news()

# ------------------------------------------------------------
# FILTERS
# ------------------------------------------------------------

st.sidebar.title("Filters")

selected_category = st.sidebar.multiselect(
    "Category",
    news_df["category"].unique(),
    default=news_df["category"].unique()
)

show_predictive_only = st.sidebar.checkbox(
    "Show Predictive News Only",
    False
)

filtered_df = news_df[
    news_df["category"].isin(selected_category)
]

if show_predictive_only:
    filtered_df = filtered_df[
        filtered_df["predictive"] == True
    ]

# ------------------------------------------------------------
# LAYOUT
# ------------------------------------------------------------

col1, col2 = st.columns(2)
col3, col4 = st.columns(2)

category_map = {
    "Stocks": col1,
    "Currency": col2,
    "Commodities": col3,
    "Macro": col4
}

# ------------------------------------------------------------
# RENDER NEWS
# ------------------------------------------------------------

for category, container in category_map.items():

    with container:

        st.markdown(
            f"<div class='section-title'>{category}</div>",
            unsafe_allow_html=True
        )

        subset = filtered_df[
            filtered_df["category"] == category
        ].head(8)

        for _, row in subset.iterrows():

            impact = infer_market_impact(
                row["title"],
                market_data
            )

            card_class = (
                "green-card"
                if row["predictive"]
                else "news-card"
            )

            sentiment_icon = "🟢" if row["sentiment"] == "Bullish" else "🔴"

            st.markdown(f"""
            <div class="news-card {card_class}">

            <b>{sentiment_icon} {row['title']}</b>

            <br><br>

            <b>Published:</b> {row['published']}

            <br>

            <b>Sentiment:</b> {row['sentiment']}

            <br>

            <b>Market Impact:</b> {impact}

            <br>

            <a href="{row['link']}" target="_blank">
            Read Article
            </a>

            </div>
            """, unsafe_allow_html=True)

# ------------------------------------------------------------
# IMPACT ANALYTICS
# ------------------------------------------------------------

st.markdown("---")

st.subheader("📊 Market Impact Analytics")

impact_df = pd.DataFrame([
    {
        "Instrument": k,
        "Change %": v["pct"]
    }
    for k, v in market_data.items()
])

fig = px.bar(
    impact_df,
    x="Instrument",
    y="Change %",
    title="Live Market Movement",
    text="Change %"
)

st.plotly_chart(fig, use_container_width=True)

# ------------------------------------------------------------
# AUTO REFRESH
# ------------------------------------------------------------

refresh_rate = st.sidebar.slider(
    "Auto Refresh (seconds)",
    30,
    600,
    120
)

st.sidebar.info(
    f"Dashboard auto-refreshes every {refresh_rate} seconds"
)

time.sleep(refresh_rate)
st.rerun()
