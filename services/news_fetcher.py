import feedparser
from newspaper import Article
from datetime import datetime

def fetch_news(feed_urls, limit=5):

    articles = []

    for url in feed_urls:

        try:
            feed = feedparser.parse(url)

            for entry in feed.entries[:10]:

                try:
                    article = Article(entry.link)
                    article.download()
                    article.parse()

                    articles.append({
                        "title": entry.title,
                        "link": entry.link,
                        "published": entry.get("published", ""),
                        "summary": article.text[:3000]
                    })

                except:
                    continue

        except:
            continue

    # Remove duplicates
    unique = []
    seen = set()

    for a in articles:

        if a["title"] not in seen:
            unique.append(a)
            seen.add(a["title"])

    return unique[:limit]
