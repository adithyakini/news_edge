from openai import OpenAI
from config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)

def generate_market_narrative(news_list):

    headlines = "\n".join([
        f"- {n['title']}"
        for n in news_list
    ])

    response = client.chat.completions.create(

        model="gpt-4.1-mini",

        messages=[

            {
                "role": "system",
                "content": """
                You are a macro strategist.

                Combine the news into one market narrative.

                Explain:
                - market regime
                - risk sentiment
                - macro direction
                - strongest opportunities
                """
            },

            {
                "role": "user",
                "content": headlines
            }
        ]
    )

    return response.choices[0].message.content
