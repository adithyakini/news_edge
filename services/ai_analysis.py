import streamlit as st
from openai import OpenAI
from config import OPENAI_API_KEY
import json

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

SYSTEM_PROMPT = """
You are a professional macro strategist.

Analyze the market significance of the article.

Determine:

1. Impact score (1-10)
2. Priority:
   LOW / MEDIUM / HIGH / CRITICAL
3. Affected instruments
4. Bullish/Bearish/Neutral
5. Trade implication
6. Why this matters
7. Confidence score
8. Expected market reaction

Return ONLY valid JSON.
"""

def analyze_article(article):

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

        content = content.replace("```json", "")
        content = content.replace("```", "")

        return json.loads(content)

    except Exception as e:

        return {
            "impact_score": 0,
            "priority": "LOW",
            "affected_instruments": [],
            "sentiment": "Neutral",
            "trade_implication": "Analysis failed",
            "why_this_matters": str(e),
            "confidence_score": 0
        }
