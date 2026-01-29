#!/usr/bin/env python3
"""
AI News Fetcher - Fetch latest AI news every 2 hours
"""

import json
import requests
from datetime import datetime
import feedparser
import time

NEWS_SOURCES = {
    'rss_feeds': [
        'https://techcrunch.com/tag/artificial-intelligence/feed/',
        'https://www.technologyreview.com/feed/',
        'https://www.theverge.com/ai-artificial-intelligence/rss/index.xml',
        'https://www.wired.com/feed/tag/ai/latest/rss',
    ],
    'reddit': [
        'https://www.reddit.com/r/artificial/.json',
        'https://www.reddit.com/r/MachineLearning/.json',
    ]
}

def fetch_rss_news():
    """Fetch news from RSS feeds"""
    news_items = []
    
    for feed_url in NEWS_SOURCES['rss_feeds']:
        try:
            feed = feedparser.parse(feed_url)
            for entry in feed.entries[:5]:
                news_items.append({
                    'platform': 'twitter',
                    'title': entry.get('title', 'No title'),
                    'author': entry.get('author', feed.feed.get('title', 'Unknown')),
                    'engagement': 0,
                    'engagement_type': 'likes',
                    'date': datetime.now().strftime('%Y-%m-%d'),
                    'url': entry.get('link', '#'),
                    'thumbnail': None
                })
        except Exception as e:
            print(f"Error fetching RSS {feed_url}: {e}")
    
    return news_items

def fetch_reddit_news():
    """Fetch AI discussions from Reddit"""
    news_items = []
    headers = {'User-Agent': 'AI News Bot 1.0'}
    
    for subreddit_url in NEWS_SOURCES['reddit']:
        try:
            response = requests.get(subreddit_url, headers=headers)
            if response.status_code == 200:
                data = response.json()
                for post in data['data']['children'][:10]:
                    post_data = post['data']
                    news_items.append({
                        'platform': 'twitter',
                        'title': post_data.get('title', 'No title'),
                        'author': f"r/{post_data.get('subreddit', 'unknown')}",
                        'engagement': post_data.get('score', 0),
                        'engagement_type': 'likes',
                        'date': datetime.now().strftime('%Y-%m-%d'),
                        'url': f"https://reddit.com{post_data.get('permalink', '')}",
                        'thumbnail': None
                    })
            time.sleep(1)
        except Exception as e:
            print(f"Error fetching Reddit {subreddit_url}: {e}")
    
    return news_items

def main():
    print("Fetching AI news...")
    
    all_news = []
    
    # Fetch from RSS
    rss_news = fetch_rss_news()
    all_news.extend(rss_news)
    print(f"Got {len(rss_news)} items from RSS")
    
    # Fetch from Reddit
    reddit_news = fetch_reddit_news()
    all_news.extend(reddit_news)
    print(f"Got {len(reddit_news)} items from Reddit")
    
    # Remove duplicates
    seen_titles = set()
    unique_news = []
    for item in all_news:
        if item['title'] not in seen_titles:
            seen_titles.add(item['title'])
            unique_news.append(item)
    
    # Sort by engagement
    unique_news.sort(key=lambda x: x['engagement'], reverse=True)
    
    # Save to JSON
    with open('news_data.json', 'w', encoding='utf-8') as f:
        json.dump(unique_news, f, ensure_ascii=False, indent=2)
    
    print(f"Saved {len(unique_news)} unique news items")

if __name__ == '__main__':
    main()
```

4. 点击 **"Commit new file"**

---

### 第3步：上传第二个Python脚本

1. 再次点击 **"Add file"** → **"Create new file"**

2. 文件名输入：
```
   scripts/update_html.py
