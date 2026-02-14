import os
import json
import requests

API_KEY = os.environ.get('YOUTUBE_API_KEY')

# AI 频道和关键词
CHANNELS = [
    "UCWN3xxRkmTPmbKwht9FuE5A",  # Two Minute Papers
    "UCSHZKyawb77ixDdsGog4iWA",  # Lex Fridman
    "UCZHmQk67mSJgfCCTn7xBfew",  # Yannic Kilcher
    "UCbfYPyITQ-7l4upoX8nvctg",  # AI Explained
    "UCMLtBahI5DMrt0NPvDSoIRQ",  # Matt Wolfe
    "UCvjgXvBlbQiRffWfNazfUHg",  # AI Jason
    "UC0e3QhIYukixgh5VVpKHH9Q",  # Code Bullet
    "UCXZCJLdBC09xxGZ6gcdrc6A",  # TheAIGRID
]

SEARCH_KEYWORDS = ["AI news", "GPT", "Claude AI", "LLM tutorial", "machine learning"]

def fetch_channel_videos(channel_id):
    """获取频道最新视频"""
    url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        "key": API_KEY,
        "channelId": channel_id,
        "part": "snippet",
        "order": "date",
        "maxResults": 5,
        "type": "video"
    }
    try:
        r = requests.get(url, params=params, timeout=15)
        if r.status_code == 200:
            return r.json().get("items", [])
    except Exception as e:
        print(f"Error: {e}")
    return []

def fetch_search_videos(keyword):
    """搜索热门 AI 视频"""
    url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        "key": API_KEY,
        "q": keyword,
        "part": "snippet",
        "order": "viewCount",
        "maxResults": 10,
        "type": "video",
        "publishedAfter": "2025-01-01T00:00:00Z"
    }
    try:
        r = requests.get(url, params=params, timeout=15)
        if r.status_code == 200:
            return r.json().get("items", [])
    except Exception as e:
        print(f"Error: {e}")
    return []

def get_video_stats(video_ids):
    """获取视频统计数据"""
    url = "https://www.googleapis.com/youtube/v3/videos"
    params = {
        "key": API_KEY,
        "id": ",".join(video_ids),
        "part": "statistics,snippet"
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
    
    print("Fetching YouTube videos...")
    
    all_videos = []
    video_ids = []
    
    # 从频道获取
    for channel_id in CHANNELS:
        videos = fetch_channel_videos(channel_id)
        for v in videos:
            vid = v["id"].get("videoId")
            if vid and vid not in video_ids:
                video_ids.append(vid)
                all_videos.append(v)
        print(f"  Channel {channel_id[:8]}: {len(videos)} videos")
    
    # 从搜索获取
    for keyword in SEARCH_KEYWORDS[:3]:
        videos = fetch_search_videos(keyword)
        for v in videos:
            vid = v["id"].get("videoId")
            if vid and vid not in video_ids:
                video_ids.append(vid)
                all_videos.append(v)
        print(f"  Search '{keyword}': {len(videos)} videos")
    
    # 获取统计数据
    stats = {}
    if video_ids:
        for i in range(0, len(video_ids), 50):
            batch = video_ids[i:i+50]
            items = get_video_stats(batch)
            for item in items:
                stats[item["id"]] = item.get("statistics", {})
    
    # 整理数据
    results = []
    for v in all_videos:
        vid = v["id"].get("videoId")
        if not vid:
            continue
        snippet = v.get("snippet", {})
        stat = stats.get(vid, {})
        
        results.append({
            "id": vid,
            "title": snippet.get("title", ""),
            "channel": snippet.get("channelTitle", ""),
            "description": snippet.get("description", "")[:200],
            "publishedAt": snippet.get("publishedAt", ""),
            "thumbnail": snippet.get("thumbnails", {}).get("high", {}).get("url", ""),
            "views": int(stat.get("viewCount", 0)),
            "likes": int(stat.get("likeCount", 0)),
            "url": f"https://youtube.com/watch?v={vid}"
        })
    
    # 按播放量排序
    results.sort(key=lambda x: x["views"], reverse=True)
    results = results[:20]
    
    # 保存
    with open("youtube_data.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\nSaved {len(results)} videos to youtube_data.json")

if __name__ == "__main__":
    main()
