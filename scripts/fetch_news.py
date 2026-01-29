import json
import feedparser
import requests
from datetime import datetime
import re

def clean_html(text):
    """Remove HTML tags and clean text"""
    text = re.sub(r'<[^>]+>', '', text)
    text = re.sub(r'http\S+', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text[:400] if len(text) > 400 else text

def fetch_rss():
    """Fetch from RSS feeds"""
    feeds = [
        ("https://techcrunch.com/category/artificial-intelligence/feed/", "TechCrunch"),
        ("https://www.technologyreview.com/feed/", "MIT Tech Review"),
        ("https://www.theverge.com/rss/ai-artificial-intelligence/index.xml", "The Verge"),
        ("https://www.wired.com/feed/tag/ai/latest/rss", "Wired"),
        ("https://www.nature.com/subjects/artificial-intelligence.rss", "Nature"),
        ("https://feeds.arstechnica.com/arstechnica/technology-lab", "Ars Technica"),
    ]
    
    news = []
    for url, source in feeds:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:8]:
                summary = entry.get('summary', entry.get('description', entry.title))
                news.append({
                    "title": clean_html(entry.title),
                    "source": source,
                    "summary": clean_html(summary),
                    "url": entry.link,
                    "date": datetime.now().strftime("%Y-%m-%d")
                })
                print(f"  + {source}: {entry.title[:50]}...")
        except Exception as e:
            print(f"  ! Error {source}: {e}")
    return news

def fetch_reddit():
    """Fetch from Reddit AI subreddits"""
    subs = ["artificial", "MachineLearning", "OpenAI", "LocalLLaMA", "ChatGPT"]
    news = []
    headers = {"User-Agent": "AI-News-Bot/2.0"}
    
    for sub in subs:
        try:
            url = f"https://www.reddit.com/r/{sub}/hot.json?limit=8"
            r = requests.get(url, headers=headers, timeout=10)
            if r.status_code == 200:
                for post in r.json()["data"]["children"]:
                    p = post["data"]
                    if not p.get("stickied") and p.get("score", 0) > 50:
                        summary = p.get("selftext", "") or p["title"]
                        news.append({
                            "title": clean_html(p["title"]),
                            "source": f"Reddit r/{sub}",
                            "summary": clean_html(summary),
                            "url": f"https://reddit.com{p['permalink']}",
                            "score": p.get("score", 0),
                            "date": datetime.now().strftime("%Y-%m-%d")
                        })
                        print(f"  + r/{sub}: {p['title'][:50]}... (score: {p.get('score', 0)})")
        except Exception as e:
            print(f"  ! Error r/{sub}: {e}")
    return news

def main():
    print("\n=== Fetching AI News ===\n")
    
    print("📰 Fetching RSS feeds...")
    rss = fetch_rss()
    print(f"   Got {len(rss)} from RSS\n")
    
    print("🔥 Fetching Reddit...")
    reddit = fetch_reddit()
    print(f"   Got {len(reddit)} from Reddit\n")
    
    # Combine all
    all_news = rss + reddit
    
    # Sort Reddit by score, keep RSS at top
    rss_news = [n for n in all_news if "Reddit" not in n["source"]]
    reddit_news = sorted([n for n in all_news if "Reddit" in n["source"]], 
                         key=lambda x: x.get("score", 0), reverse=True)
    
    # Interleave: RSS first, then Reddit by popularity
    combined = []
    for i in range(max(len(rss_news), len(reddit_news))):
        if i < len(rss_news):
            combined.append(rss_news[i])
        if i < len(reddit_news):
            combined.append(reddit_news[i])
    
    # Remove duplicates
    seen = set()
    unique = []
    for item in combined:
        key = item["title"].lower()[:40]
        if key not in seen:
            seen.add(key)
            unique.append(item)
    
    # Take top 50
    final = unique[:50]
    
    print(f"✅ Total unique news: {len(final)}")
    
    with open("news_data.json", "w", encoding="utf-8") as f:
        json.dump(final, f, indent=2, ensure_ascii=False)
    
    print("💾 Saved to news_data.json\n")

if __name__ == "__main__":
    main()
