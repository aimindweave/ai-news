import json
import requests
from datetime import datetime
import re

def clean_text(text):
    if not text:
        return ""
    text = re.sub(r'<[^>]+>', '', text)
    text = re.sub(r'&#\d+;', ' ', text)
    text = re.sub(r'&[a-zA-Z]+;', ' ', text)
    text = text.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')
    text = text.replace('"', "'").replace('\\', ' ')
    text = re.sub(r'\s+', ' ', text).strip()
    return text[:300] if len(text) > 300 else text

def fetch_github_trending():
    """获取 GitHub Trending AI 项目"""
    print("Fetching GitHub Trending...")
    items = []
    try:
        # 使用非官方 API
        url = "https://api.gitterapp.com/repositories?language=python&since=daily"
        r = requests.get(url, timeout=15, headers={"User-Agent": "Mozilla/5.0"})
        if r.status_code == 200:
            repos = r.json()
            ai_keywords = ['ai', 'llm', 'gpt', 'claude', 'agent', 'ml', 'machine-learning', 
                          'deep-learning', 'transformer', 'langchain', 'openai', 'anthropic',
                          'chatbot', 'neural', 'model', 'inference']
            for repo in repos[:30]:
                name = repo.get('name', '').lower()
                desc = (repo.get('description') or '').lower()
                if any(kw in name or kw in desc for kw in ai_keywords):
                    items.append({
                        "title": repo.get('name', ''),
                        "source": "GitHub Trending",
                        "description": clean_text(repo.get('description', '')),
                        "url": repo.get('url', ''),
                        "stars": repo.get('stars', 0),
                        "date": datetime.now().strftime("%Y-%m-%d"),
                        "category": "AI Tool"
                    })
            print(f"  GitHub: {len(items)} AI repos")
    except Exception as e:
        print(f"  GitHub error: {e}")
    return items[:10]

def fetch_reddit_ml():
    """获取 Reddit r/MachineLearning 热帖"""
    print("Fetching Reddit r/MachineLearning...")
    items = []
    try:
        url = "https://www.reddit.com/r/MachineLearning/hot.json?limit=20"
        headers = {"User-Agent": "AI-News-Bot/1.0"}
        r = requests.get(url, headers=headers, timeout=15)
        if r.status_code == 200:
            posts = r.json().get('data', {}).get('children', [])
            for post in posts:
                data = post.get('data', {})
                if data.get('stickied'):
                    continue
                items.append({
                    "title": clean_text(data.get('title', '')),
                    "source": "Reddit r/ML",
                    "description": clean_text(data.get('selftext', ''))[:200] or "Discussion on r/MachineLearning",
                    "url": "https://reddit.com" + data.get('permalink', ''),
                    "score": data.get('score', 0),
                    "date": datetime.now().strftime("%Y-%m-%d"),
                    "category": "AI Discussion"
                })
            print(f"  Reddit: {len(items)} posts")
    except Exception as e:
        print(f"  Reddit error: {e}")
    return items[:10]

def fetch_hackernews_ai():
    """获取 Hacker News AI 相关热帖"""
    print("Fetching Hacker News...")
    items = []
    try:
        # 获取首页热帖
        url = "https://hacker-news.firebaseio.com/v0/topstories.json"
        r = requests.get(url, timeout=15)
        if r.status_code == 200:
            story_ids = r.json()[:50]
            ai_keywords = ['ai', 'gpt', 'claude', 'llm', 'openai', 'anthropic', 'machine learning',
                          'deep learning', 'neural', 'chatgpt', 'agent', 'model', 'transformer']
            for sid in story_ids:
                try:
                    story_url = f"https://hacker-news.firebaseio.com/v0/item/{sid}.json"
                    sr = requests.get(story_url, timeout=10)
                    if sr.status_code == 200:
                        story = sr.json()
                        title = (story.get('title') or '').lower()
                        if any(kw in title for kw in ai_keywords):
                            items.append({
                                "title": clean_text(story.get('title', '')),
                                "source": "Hacker News",
                                "description": f"HN Score: {story.get('score', 0)} | {story.get('descendants', 0)} comments",
                                "url": story.get('url') or f"https://news.ycombinator.com/item?id={sid}",
                                "score": story.get('score', 0),
                                "date": datetime.now().strftime("%Y-%m-%d"),
                                "category": "AI News"
                            })
                            if len(items) >= 10:
                                break
                except:
                    continue
            print(f"  HN: {len(items)} AI stories")
    except Exception as e:
        print(f"  HN error: {e}")
    return items[:10]

def fetch_nitter_accounts():
    """尝试从 Nitter 获取 AI 博主推文"""
    print("Fetching Twitter/Nitter...")
    items = []
    
    # AI 领域重要账号
    accounts = [
        "kaborobot",      # AI 实操
        "EMostaque",      # Stability AI
        "DrJimFan",       # NVIDIA AI
        "svpino",         # ML 教程
        "bindureddy",     # AI 应用
        "hwchase17",      # LangChain
        "jeaborot",       # AI Agent
        "sahar_abdelnabi", # AI 研究
    ]
    
    # Nitter 实例列表（可能不稳定）
    nitter_instances = [
        "nitter.net",
        "nitter.privacydev.net", 
        "nitter.poast.org",
    ]
    
    for account in accounts[:5]:
        for instance in nitter_instances:
            try:
                url = f"https://{instance}/{account}/rss"
                r = requests.get(url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
                if r.status_code == 200 and '<item>' in r.text:
                    # 简单解析 RSS
                    import xml.etree.ElementTree as ET
                    root = ET.fromstring(r.content)
                    for item in root.findall('.//item')[:2]:
                        title = item.findtext('title', '')
                        link = item.findtext('link', '')
                        pub_date = item.findtext('pubDate', '')
                        
                        if title and len(title) > 20:
                            items.append({
                                "title": clean_text(title)[:150],
                                "source": f"@{account}",
                                "description": "",
                                "url": link,
                                "date": datetime.now().strftime("%Y-%m-%d"),
                                "category": "Twitter"
                            })
                    break  # 成功获取，跳出实例循环
            except Exception as e:
                continue
    
    print(f"  Twitter/Nitter: {len(items)} tweets")
    return items

def main():
    print("Fetching AI trending content...")
    
    all_items = []
    
    # 获取各来源
    all_items.extend(fetch_github_trending())
    all_items.extend(fetch_reddit_ml())
    all_items.extend(fetch_hackernews_ai())
    all_items.extend(fetch_nitter_accounts())
    
    # 按来源分组排序
    github = [x for x in all_items if x['source'] == 'GitHub Trending']
    reddit = [x for x in all_items if x['source'] == 'Reddit r/ML']
    hn = [x for x in all_items if x['source'] == 'Hacker News']
    twitter = [x for x in all_items if x['category'] == 'Twitter']
    
    # 合并，保持多样性
    final = []
    for i in range(max(len(github), len(reddit), len(hn), len(twitter))):
        if i < len(github): final.append(github[i])
        if i < len(twitter): final.append(twitter[i])
        if i < len(reddit): final.append(reddit[i])
        if i < len(hn): final.append(hn[i])
    
    # 保存
    with open('trending_data.json', 'w', encoding='utf-8') as f:
        json.dump(final[:30], f, ensure_ascii=True, indent=2)
    
    print(f"\nSaved {len(final[:30])} trending items")

if __name__ == "__main__":
    main()
