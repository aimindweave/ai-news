import json
import requests
import xml.etree.ElementTree as ET
from datetime import datetime

# AI 播客 RSS Feeds
PODCAST_FEEDS = [
    {"name": "Lex Fridman Podcast", "rss": "https://lexfridman.com/feed/podcast/", "spotify": "https://open.spotify.com/show/2MAi0BvDc6GTFvKFPXnkCL"},
    {"name": "Hard Fork", "rss": "https://feeds.simplecast.com/l2i9YnTd", "spotify": "https://open.spotify.com/show/44fllCS2FTFr2x2kjP9xeT"},
    {"name": "All-In Podcast", "rss": "https://feeds.megaphone.fm/all-in-with-chamath-jason-sacks-friedberg", "spotify": "https://open.spotify.com/show/2IqXAVFR4e0Bmyjsdc8QzF"},
    {"name": "The AI Podcast (NVIDIA)", "rss": "https://feeds.soundcloud.com/users/soundcloud:users:264034133/sounds.rss", "spotify": "https://open.spotify.com/show/0e1X4kJVfwQRPF8lZzqqfX"},
    {"name": "Latent Space", "rss": "https://api.substack.com/feed/podcast/1084089.rss", "spotify": "https://open.spotify.com/show/4vS0Dq8G7Q2lRqAR8BMBWC"},
    {"name": "The AI Breakdown", "rss": "https://feeds.transistor.fm/the-ai-breakdown-daily-artificial-intelligence-news-and-discussions", "spotify": "https://open.spotify.com/show/45VeQGMfNRXvgONvVh6bqZ"},
    {"name": "Practical AI", "rss": "https://changelog.com/practicalai/feed", "spotify": "https://open.spotify.com/show/1LaCr5TFAgYPK5qHjP3XDp"},
    {"name": "The TWIML AI Podcast", "rss": "https://twimlai.com/feed/", "spotify": "https://open.spotify.com/show/2sp5EL7s7EqxttxwwoJ3i7"},
    {"name": "No Priors", "rss": "https://feeds.transistor.fm/no-priors-ai-machine-learning-tech-and-the-future", "spotify": "https://open.spotify.com/show/4gvlPPLfvu3j0GCoq9XSLW"},
    {"name": "a]6z Podcast", "rss": "https://feeds.simplecast.com/JGE3yC0V", "spotify": "https://open.spotify.com/show/5bC65RDvs3oxnLyqqvkUYX"},
]

def parse_rss(feed_info):
    """解析 RSS Feed 获取最新单集"""
    episodes = []
    try:
        r = requests.get(feed_info["rss"], timeout=15, headers={"User-Agent": "Mozilla/5.0"})
        if r.status_code != 200:
            print(f"  {feed_info['name']}: HTTP {r.status_code}")
            return []
        
        root = ET.fromstring(r.content)
        channel = root.find("channel")
        if channel is None:
            return []
        
        for item in channel.findall("item")[:3]:  # 每个播客取最新3集
            title = item.findtext("title", "")
            desc = item.findtext("description", "")[:200] if item.findtext("description") else ""
            pub_date = item.findtext("pubDate", "")
            link = item.findtext("link", feed_info["spotify"])
            
            # 解析日期
            release_date = ""
            if pub_date:
                try:
                    for fmt in ["%a, %d %b %Y %H:%M:%S %z", "%a, %d %b %Y %H:%M:%S %Z", "%Y-%m-%d"]:
                        try:
                            dt = datetime.strptime(pub_date.strip(), fmt)
                            release_date = dt.strftime("%Y-%m-%d")
                            break
                        except:
                            continue
                    if not release_date:
                        release_date = pub_date[:10]
                except:
                    release_date = ""
            
            # 获取时长
            duration = item.findtext("{http://www.itunes.com/dtds/podcast-1.0.dtd}duration", "0")
            try:
                if ":" in str(duration):
                    parts = duration.split(":")
                    if len(parts) == 3:
                        duration_min = int(parts[0]) * 60 + int(parts[1])
                    else:
                        duration_min = int(parts[0])
                else:
                    duration_min = int(duration) // 60
            except:
                duration_min = 0
            
            episodes.append({
                "id": f"{feed_info['name'][:8]}_{len(episodes)}",
                "name": title,
                "show": feed_info["name"],
                "description": desc.replace("<p>", "").replace("</p>", "")[:200],
                "release_date": release_date,
                "duration_min": duration_min,
                "image": "",
                "url": feed_info["spotify"]
            })
        
        print(f"  {feed_info['name']}: {len(episodes)} episodes")
    except Exception as e:
        print(f"  {feed_info['name']}: Error - {e}")
    
    return episodes

def main():
    print("Fetching podcasts via RSS...")
    
    all_episodes = []
    shows = []
    
    for feed in PODCAST_FEEDS:
        episodes = parse_rss(feed)
        all_episodes.extend(episodes)
        
        shows.append({
            "id": feed["name"][:8],
            "name": feed["name"],
            "publisher": "",
            "description": f"Latest AI and tech discussions",
            "total_episodes": 0,
            "image": "",
            "url": feed["spotify"]
        })
    
    # 按日期排序
    all_episodes.sort(key=lambda x: x.get("release_date", ""), reverse=True)
    
    result = {
        "shows": shows,
        "episodes": all_episodes[:30]
    }
    
    with open("spotify_data.json", "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    
    print(f"\nSaved {len(shows)} shows, {len(all_episodes[:30])} episodes")

if __name__ == "__main__":
    main()
