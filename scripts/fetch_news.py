import feedparser
import json
from datetime import datetime
import re

FEEDS = [
    ("https://techcrunch.com/category/artificial-intelligence/feed/", "TechCrunch"),
    ("https://www.technologyreview.com/feed/", "MIT Tech Review"),
    ("https://www.theverge.com/ai-artificial-intelligence/rss/index.xml", "The Verge"),
    ("https://www.wired.com/feed/tag/ai/latest/rss", "Wired"),
    ("https://arstechnica.com/ai/feed/", "Ars Technica"),
]

def clean_text(text):
    if not text:
        return ""
    text = re.sub(r'<[^>]+>', '', text)
    text = re.sub(r'&#\d+;', ' ', text)
    text = re.sub(r'&[a-zA-Z]+;', ' ', text)
    text = text.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')
    text = text.replace('"', "'").replace('\\', ' ')
    text = re.sub(r'\s+', ' ', text).strip()
    if len(text) > 300:
        text = text[:297] + "..."
    return text

def main():
    print("Fetching AI news...")
    all_news = []
    today = datetime.now().strftime("%Y-%m-%d")
    
    for url, source in FEEDS:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:15]:
                title = clean_text(entry.get('title', ''))
                summary = clean_text(entry.get('summary', ''))
                link = entry.get('link', '')
                if not title:
                    continue
                all_news.append({
                    "title": title,
                    "source": source,
                    "summary": summary,
                    "url": link,
                    "date": today
                })
            print(f"  {source}: {len(feed.entries[:15])} items")
        except Exception as e:
            print(f"  {source}: Error - {e}")
    
    with open('news_data.json', 'w', encoding='utf-8') as f:
        json.dump(all_news[:50], f, ensure_ascii=True, indent=2)
    
    print(f"Saved {len(all_news[:50])} news items")

if __name__ == "__main__":
    main()
