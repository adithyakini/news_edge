import feedparser
from newspaper import Article

def fetch_news(feed_urls, limit=5):

    articles = []

    for url in feed_urls:

        print(f"Fetching feed: {url}")

        try:

            feed = feedparser.parse(url)

            if not feed.entries:
                print(f"No entries found in {url}")
                continue

            for entry in feed.entries[:10]:

                try:

                    print(f"Processing: {entry.title}")

                    summary = ""

                    try:
                        article = Article(entry.link)
                        article.download()
                        article.parse()
                        summary = article.text[:3000]

                    except Exception as e:
                        print(f"Article parse failed: {e}")
                        summary = entry.get("summary", "")

                    articles.append({
                        "title": entry.title,
                        "link": entry.link,
                        "published": entry.get("published", "Unknown"),
                        "summary": summary
                    })

                except Exception as e:
                    print(f"Entry error: {e}")

        except Exception as e:
            print(f"Feed error: {e}")

    # remove duplicates
    unique = []
    seen = set()

    for a in articles:

        if a["title"] not in seen:
            unique.append(a)
            seen.add(a["title"])

    print(f"TOTAL ARTICLES FETCHED: {len(unique)}")

    return unique[:limit]
