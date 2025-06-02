# news.py
import feedparser

def get_headlines():
    feed_url = "https://www.npr.org/rss/rss.php?id=1001"
    feed = feedparser.parse(feed_url)

    headlines = []
    for entry in feed.entries[:3]:
        headlines.append(entry.title)
    return headlines