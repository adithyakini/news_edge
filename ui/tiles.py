import streamlit as st

def render_tile(news, ai_data, verification):

    sentiment = ai_data.get("sentiment", "Neutral")

    if sentiment == "Bullish":
        color = "#0f5132"

    elif sentiment == "Bearish":
        color = "#842029"

    else:
        color = "#664d03"

    st.markdown(
        f"""
        <div style="
            background-color:{color};
            padding:18px;
            border-radius:16px;
            margin-bottom:20px;
            color:white;
            min-height:350px;
            box-shadow:0px 4px 15px rgba(0,0,0,0.3);
        ">

        <h4>{news['title']}</h4>

        <p>
        <b>Published:</b> {news['published']}
        </p>

        <hr>

        <p><b>Instrument:</b> {ai_data.get('instrument')}</p>

        <p><b>AI Bias:</b> {sentiment}</p>

        <p><b>Confidence:</b> {ai_data.get('confidence')}%</p>

        <p><b>Trade Idea:</b> {ai_data.get('trade_idea')}</p>

        <p><b>Time Horizon:</b> {ai_data.get('time_horizon')}</p>

        <hr>

        <p><b>Actual Move:</b> {verification.get('actual_move')}%</p>

        <p><b>Actual Direction:</b> {verification.get('actual_direction')}</p>

        <p>
        <b>Prediction Correct:</b>
        {verification.get('prediction_correct')}
        </p>

        </div>
        """,

        unsafe_allow_html=True
    )
