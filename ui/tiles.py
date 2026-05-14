import streamlit as st

def render_tile(news, analysis, verification):

    priority = analysis.get("priority", "LOW")

    colors = {
        "LOW": "#3d3d3d",
        "MEDIUM": "#8a6d3b",
        "HIGH": "#0b5394",
        "CRITICAL": "#7f0000"
    }

    bg = colors.get(priority)

    st.markdown(
        f"""
        <div style="
            background:{bg};
            padding:20px;
            border-radius:20px;
            margin-bottom:20px;
            color:white;
            min-height:480px;
            box-shadow:0px 6px 20px rgba(0,0,0,0.4);
        ">

        <h3>{news['title']}</h3>

        <hr>

        <p><b>Priority:</b> {priority}</p>

        <p><b>Impact Score:</b> {analysis.get('impact_score')}/10</p>

        <p><b>Sentiment:</b> {analysis.get('sentiment')}</p>

        <p><b>Confidence:</b> {analysis.get('confidence_score')}%</p>

        <p><b>Trade Implication:</b></p>
        <p>{analysis.get('trade_implication')}</p>

        <hr>

        <p><b>Why This Matters</b></p>

        <p>{analysis.get('why_this_matters')}</p>

        <hr>

        <p><b>Actual Market Move:</b>
        {verification.get('move')}%</p>

        <p><b>Prediction Correct:</b>
        {verification.get('correct')}</p>

        </div>
        """,

        unsafe_allow_html=True
    )
