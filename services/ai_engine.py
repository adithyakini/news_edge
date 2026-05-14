from openai import OpenAI
from config import OPENAI_API_KEY
import json

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

SYSTEM_PROMPT = """
You are a professional financial analyst.

Analyze the article and determine:

1. Which instrument is impacted
2. Bullish/Bearish/Neutral
3. Confidence score (1-100)
4. Short actionable trade idea
5. Expected time horizon
6. Whether this is HIGH IMPACT

Return valid JSON only.
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

        return json.loads(content)

    except Exception as e:

        return {
            "instrument": "Unknown",
            "sentiment": "Neutral",
            "confidence": 0,
            "trade_idea": str(e),
            "time_horizon": "-",
            "high_impact": False
        }
