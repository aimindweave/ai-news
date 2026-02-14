import os
import json
import requests

API_KEY = os.environ.get('YOUTUBE_API_KEY')

# AI 知识类频道
CHANNELS = [
    "UCWN3xxRkmTPmbKwht9FuE5A",  # Two Minute Papers
    "UCSHZKyawb77ixDdsGog4iWA",  # Lex Fridman
    "UCZHmQk67mSJgfCCTn7xBfew",  # Yannic Kilcher
    "UCbfYPyITQ-7l4upoX8nvctg",  # AI Explained
    "UCMLtBahI5DMrt0NPvDSoIRQ",  # Matt Wolfe
    "UC0e3QhIYukixgh5VVpKHH9Q",  # Code Bullet
    "UCXZCJLdBC09xxGZ6gcdrc6A",  # TheAIGRID
    "UCZeYliWDCuw36PnHKdJARjA",  # AI Advantage
    "UC9-y-6csu5WGm29I7JiwpnA",  # Computerphile
    "UCYO_jab_esuFRV4b17AJtAw",  # 3Blue1Brown
    "UCHnyfMqiRRG1u-2MsSQLbXA",  # Veritasium
    "UCsvn_Po0SmunchJYOWpOxMg",  # AI Coffee Break with Letitia
    "UCddiUEpeqJcYeBxX1IVBKvQ",  # The AI Epiphany
    "UC4UJ26WkceqONNF5S26OiVw",  # StatQuest
    "UCr8O8l5cCX85Oem1d18EezQ",  # David Shapiro
    "UCbXgNpp0jedKWcQiULLbDTA",  # Sebastian Raschka
    "UCyHM6Y7tXrRH4lvOO_IMBcg",  # 吴恩达 DeepLearning.AI
    "UCNIkB2IeJ-6AmZv7bQ1oBYg",  # Andrej Karpathy
]

# AI 知识类搜索词
SEARCH_KEYWORDS = [
    "Claude AI tutorial",
    "OpenAI GPT tutorial",
    "LLM explained",
    "AI agent tutorial",
    "machine learning course",
    "deep learning tutorial",
    "transformer explained",
    "RAG tutorial",
    "prompt engineering",
    "AI coding assistant",
    "Anthropic Claude",
    "ChatGPT tutorial",
    "LangChain tutorial",
    "AI工具教程",
    "人工智能教程",
    "大模型教程",
]

def fetch_channel_videos(channel_id):
    url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        "key": API_KEY,
        "channelId": channel_id,
        "part": "snippet",
        "order": "date",
        "maxResults": 10,
        "type": "video",
        "videoDuration": "medium",
    }
    try:
        r = requests.get(url, params=params, timeout=15)
        if r.status_code == 200:
            return r.json().get("items", [])
    except Exception as e:
        print(f"Error: {e}")
    return []

def fetch_search_videos(keyword):
    url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        "key": API_KEY,
        "q": keyword,
        "part": "snippet",
        "order": "relevance",
        "maxResults": 15,
        "type": "video",
        "videoDuration": "medium",
        "publishedAfter": "2024-01-01T00:00:00Z",
        "relevanceLanguage": "en",
        "safeSearch": "strict",
    }
    try:
        r = requests.get(url, params=params, timeout=15)
        if r.status_code == 200:
            return r.json().get("items", [])
    except Exception as e:
        print(f"Error: {e}")
    return []

def get_video_stats(video_ids):
    if not video_ids:
        return []
    url = "https://www.googleapis.com/youtube/v3/videos"
    params = {
        "key": API_KEY,
        "id": ",".join(video_ids[:50]),
        "part": "statistics,contentDetails"
    }
    try:
        r = requests.get(url, params=params, timeout=15)
        if r.status_code == 200:
            return r.json().get("items", [])
    except Exception as e:
        print(f"Error: {e}")
    return []

def main():
    if not API_KEY:
        print("No YOUTUBE_API_KEY!")
        return
    
    print("Fetching YouTube AI videos...")
    
    all_videos = []
    video_ids = set()
    
    # 从知识频道获取
    for channel_id in CHANNELS:
        videos = fetch_channel_videos(channel_id)
        for v in videos:
            vid = v.get("id", {}).get("videoId")
            if vid and vid not in video_ids:
                video_ids.add(vid)
                all_videos.append(v)
        print(f"  Channel {channel_id[:10]}: {len(videos)}")
    
    # 从搜索获取
    for keyword in SEARCH_KEYWORDS:
        videos = fetch_search_videos(keyword)
        for v in videos:
            vid = v.get("id", {}).get("videoId")
            if vid and vid not in video_ids:
                video_ids.add(vid)
                all_videos.append(v)
        print(f"  Search '{keyword}': {len(videos)}")
    
    print(f"Total unique videos: {len(all_videos)}")
    
    # 获取统计
    stats = {}
    id_list = list(video_ids)
    for i in range(0, len(id_list), 50):
        batch = id_list[i:i+50]
        items = get_video_stats(batch)
        for item in items:
            stats[item["id"]] = item.get("statistics", {})
    
    # 整理数据
    results = []
    for v in all_videos:
        vid = v.get("id", {}).get("videoId")
        if not vid:
            continue
        snippet = v.get("snippet", {})
        stat = stats.get(vid, {})
        
        views = int(stat.get("viewCount", 0))
        likes = int(stat.get("likeCount", 0))
        
        results.append({
            "id": vid,
            "title": snippet.get("title", ""),
            "channel": snippet.get("channelTitle", ""),
            "description": snippet.get("description", "")[:200],
            "publishedAt": snippet.get("publishedAt", ""),
            "thumbnail": snippet.get("thumbnails", {}).get("high", {}).get("url", ""),
            "views": views,
            "likes": likes,
            "url": f"https://youtube.com/watch?v={vid}"
        })
    
    # 按播放量排序，取前50
    results.sort(key=lambda x: x["views"], reverse=True)
    results = results[:50]
    
    with open("youtube_data.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"Saved {len(results)} videos")

if __name__ == "__main__":
    main()
