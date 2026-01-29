import json
import feedparser
import requests
from datetime import datetime, timedelta

def fetch_rss_news():
    """Fetch news from RSS feeds"""
    feeds = [
        ("https://techcrunch.com/category/artificial-intelligence/feed/", "TechCrunch"),
        ("https://www.technologyreview.com/feed/", "MIT Tech Review"),
        ("https://www.theverge.com/rss/ai-artificial-intelligence/index.xml", "The Verge"),
        ("https://www.wired.com/feed/tag/ai/latest/rss", "Wired"),
    ]
    
    news = []
    for url, source in feeds:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:5]:
                news.append({
                    "title": entry.title,
                    "source": source,
                    "summary": entry.get('summary', entry.title)[:300],
                    "url": entry.link,
                    "date": datetime.now().strftime("%Y-%m-%d")
                })
        except Exception as e:
            print(f"Error fetching {source}: {e}")
    
    return news

def fetch_reddit_news():
    """Fetch from Reddit AI subreddits"""
    subreddits = ["artificial", "MachineLearning", "OpenAI", "LocalLLaMA"]
    news = []
    
    headers = {"User-Agent": "AI-News-Bot/1.0"}
    
    for sub in subreddits:
        try:
            url = f"https://www.reddit.com/r/{sub}/hot.json?limit=5"
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                for post in data["data"]["children"]:
                    p = post["data"]
                    if not p.get("stickied"):
                        news.append({
                            "title": p["title"],
                            "source": f"r/{sub}",
                            "summary": p.get("selftext", p["title"])[:300] or p["title"],
                            "url": f"https://reddit.com{p['permalink']}",
                            "date": datetime.now().strftime("%Y-%m-%d")
                        })
        except Exception as e:
            print(f"Error fetching r/{sub}: {e}")
    
    return news

def clean_summary(text):
    """Clean up summary text for TTS"""
    import re
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    # Remove URLs
    text = re.sub(r'http\S+', '', text)
    # Remove extra whitespace
    text = ' '.join(text.split())
    # Limit length
    if len(text) > 300:
        text = text[:297] + "..."
    return text

def main():
    print("Fetching RSS news...")
    rss_news = fetch_rss_news()
    print(f"Got {len(rss_news)} items from RSS")
    
    print("Fetching Reddit news...")
    reddit_news = fetch_reddit_news()
    print(f"Got {len(reddit_news)} items from Reddit")
    
    # Combine and deduplicate
    all_news = rss_news + reddit_news
    
    # Clean summaries
    for item in all_news:
        item["summary"] = clean_summary(item["summary"])
    
    # Remove duplicates by title similarity
    seen_titles = set()
    unique_news = []
    for item in all_news:
        title_lower = item["title"].lower()[:50]
        if title_lower not in seen_titles:
            seen_titles.add(title_lower)
            unique_news.append(item)
    
    # Sort by date and limit to 50
    unique_news = unique_news[:50]
    
    print(f"Saving {len(unique_news)} unique news items")
    
    with open("news_data.json", "w") as f:
        json.dump(unique_news, f, indent=2)
    
    print("Done!")

if __name__ == "__main__":
    main()
