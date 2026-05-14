import streamlit as st
from openai import OpenAI
from config import OPENAI_API_KEY
import json

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

SYSTEM_PROMPT = """
You are a professional financial analyst.

Analyze the article and return ONLY valid JSON.

Format:

{
    "instrument": "",
    "sentiment": "",
    "confidence": 0,
    "trade_idea": "",
    "time_horizon": "",
    "high_impact": true
}
"""

def analyze_news(article):

    try:

        response = client.chat.completions.create(
            model="gpt-4.1-mini",

            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                },

                {
                    "role": "user",
                    "content": f"""
                    HEADLINE:
                    {article['title']}

                    ARTICLE:
                    {article['summary']}
                    """
                }
            ],

            temperature=0.2
        )

        content = response.choices[0].message.content

        print("AI RESPONSE:")
        print(content)

        # clean markdown json blocks if present
        content = content.replace("```json", "")
        content = content.replace("```", "")

        return json.loads(content)

    except Exception as e:

        print(f"AI ERROR: {e}")

        return {
            "instrument": "Unknown",
            "sentiment": "Neutral",
            "confidence": 0,
            "trade_idea": "AI analysis failed",
            "time_horizon": "-",
            "high_impact": False
        }
