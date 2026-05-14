from GoogleNews import GoogleNews
from newspaper import Article

def search_news(query, limit=5):

    googlenews = GoogleNews(lang='en')

    googlenews.search(query)

    results = googlenews.result()

    articles = []

    for item in results[:limit]:

        try:

            title = item.get("title", "")
            link = item.get("link", "")

            article = Article(link)
            article.download()
            article.parse()

            text = article.text[:4000]

            articles.append({
                "title": title,
                "link": link,
                "summary": text
            })

        except:
            continue

    return articles
