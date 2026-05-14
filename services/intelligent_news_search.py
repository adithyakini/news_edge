import feedparser
from newspaper import Article
from urllib.parse import quote


def search_news(query, limit=5):

    encoded_query = quote(query)

    rss_url = (
        f"https://news.google.com/rss/search?"
        f"q={encoded_query}&hl=en-IN&gl=IN&ceid=IN:en"
    )

    feed = feedparser.parse(rss_url)

    articles = []

    for entry in feed.entries[:limit]:

        try:

            link = entry.link
            title = entry.title

            summary = ""

            try:

                article = Article(link)

                article.download()
                article.parse()

                summary = article.text[:4000]

            except Exception as e:

                print(f"Article parse failed: {e}")

                summary = entry.get("summary", "")

            articles.append({

                "title": title,
                "link": link,
                "summary": summary
            })

        except Exception as e:

            print(f"Entry failed: {e}")

    return articles
