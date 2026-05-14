import streamlit as st

from config import SEARCH_QUERIES

from services.intelligent_news_search import search_news
from services.ai_analysis import analyze_article
from services.verifier import verify_market_move
from services.narrative_engine import generate_market_narrative

from ui.tiles import render_tile

from streamlit_autorefresh import st_autorefresh

st.set_page_config(
    page_title="AI Macro Intelligence Terminal",
    layout="wide"
)

st_autorefresh(interval=300000)

st.title("AI MACRO MARKET INTELLIGENCE TERMINAL")

all_news = []

for section, queries in SEARCH_QUERIES.items():

    st.header(section)

    section_news = []

    for query in queries:

        news = search_news(query, limit=2)

        section_news.extend(news)

    # remove duplicates
    unique = []

    seen = set()

    for n in section_news:

        if n["title"] not in seen:
            unique.append(n)
            seen.add(n["title"])

    # AI analysis
    analyzed = []

    for article in unique:

        analysis = analyze_article(article)

        if analysis.get("impact_score", 0) >= 7:

            verification = verify_market_move(
                section,
                analysis.get("sentiment")
            )

            analyzed.append({
                "news": article,
                "analysis": analysis,
                "verification": verification
            })

    # sort by impact
    analyzed = sorted(
        analyzed,
        key=lambda x: x["analysis"]["impact_score"],
        reverse=True
    )

    if analyzed:

        narrative = generate_market_narrative(
            [x["news"] for x in analyzed]
        )

        st.info(narrative)

        cols = st.columns(3)

        for idx, item in enumerate(analyzed[:5]):

            with cols[idx % 3]:

                render_tile(
                    item["news"],
                    item["analysis"],
                    item["verification"]
                )
