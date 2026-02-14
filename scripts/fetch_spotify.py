import os
import json
import requests
import base64

CLIENT_ID = os.environ.get('SPOTIFY_CLIENT_ID')
CLIENT_SECRET = os.environ.get('SPOTIFY_CLIENT_SECRET')

# AI 播客搜索词
SEARCH_KEYWORDS = [
    "artificial intelligence",
    "machine learning",
    "AI podcast",
    "deep learning",
    "ChatGPT",
    "large language model",
    "AI technology",
    "data science",
    "neural network",
    "tech AI news",
]

# 知名 AI 播客节目 ID
KNOWN_SHOWS = [
    "2MAi0BvDc6GTFvKFPXnkCL",  # Lex Fridman Podcast
    "44fllCS2FTFr2x2kjP9xeT",  # Hard Fork
    "2IqXAVFR4e0Bmyjsdc8QzF",  # All-In Podcast
    "0e1X4kJVfwQRPF8lZzqqfX",  # The AI Podcast (NVIDIA)
    "6VABdvNnQr42r4NxBdwMhF",  # Practical AI
    "6V5BH7kcwmhBXI3mWqn9Ky",  # Eye on AI
    "7c7YAAXQMSv0BuXGFe4Bvn",  # AI with AI
    "2p7zIfJoBKIQdJO02kdXtj",  # The TWIML AI Podcast
]

def get_access_token():
    if not CLIENT_ID or not CLIENT_SECRET:
        print("No Spotify credentials!")
        return None
    
    url = "https://accounts.spotify.com/api/token"
    auth = base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode()
    headers = {
        "Authorization": f"Basic {auth}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    
    try:
        r = requests.post(url, headers=headers, data=data, timeout=15)
        if r.status_code == 200:
            return r.json().get("access_token")
        else:
            print(f"Token error: {r.status_code} - {r.text[:100]}")
    except Exception as e:
        print(f"Error: {e}")
    return None

def search_shows(token, keyword):
    url = "https://api.spotify.com/v1/search"
    headers = {"Authorization": f"Bearer {token}"}
    params = {
        "q": keyword,
        "type": "show",
        "market": "US",
        "limit": 20
    }
    
    try:
        r = requests.get(url, headers=headers, params=params, timeout=15)
        if r.status_code == 200:
            return r.json().get("shows", {}).get("items", [])
    except Exception as e:
        print(f"Error: {e}")
    return []

def search_episodes(token, keyword):
    url = "https://api.spotify.com/v1/search"
    headers = {"Authorization": f"Bearer {token}"}
    params = {
        "q": keyword,
        "type": "episode",
        "market": "US",
        "limit": 20
    }
    
    try:
        r = requests.get(url, headers=headers, params=params, timeout=15)
        if r.status_code == 200:
            return r.json().get("episodes", {}).get("items", [])
    except Exception as e:
        print(f"Error: {e}")
    return []

def get_show_episodes(token, show_id):
    url = f"https://api.spotify.com/v1/shows/{show_id}/episodes"
    headers = {"Authorization": f"Bearer {token}"}
    params = {"market": "US", "limit": 5}
    
    try:
        r = requests.get(url, headers=headers, params=params, timeout=15)
        if r.status_code == 200:
            return r.json().get("items", [])
    except Exception as e:
        print(f"Error: {e}")
    return []

def main():
    print("Fetching Spotify podcasts...")
    
    token = get_access_token()
    if not token:
        print("Failed to get token!")
        return
    
    print("Got access token")
    
    all_shows = []
    all_episodes = []
    seen_show_ids = set()
    seen_episode_ids = set()
    
    # 从已知节目获取最新单集
    for show_id in KNOWN_SHOWS:
        episodes = get_show_episodes(token, show_id)
        for ep in episodes:
            if ep and ep.get("id") and ep["id"] not in seen_episode_ids:
                seen_episode_ids.add(ep["id"])
                all_episodes.append(ep)
        print(f"  Show {show_id[:8]}: {len(episodes)} episodes")
    
    # 搜索更多节目和单集
    for keyword in SEARCH_KEYWORDS:
        # 搜索节目
        shows = search_shows(token, keyword)
        for show in shows:
            if show and show.get("id") and show["id"] not in seen_show_ids:
                seen_show_ids.add(show["id"])
                all_shows.append(show)
        print(f"  Shows '{keyword}': {len(shows)}")
        
        # 搜索单集
        episodes = search_episodes(token, keyword)
        for ep in episodes:
            if ep and ep.get("id") and ep["id"] not in seen_episode_ids:
                seen_episode_ids.add(ep["id"])
                all_episodes.append(ep)
        print(f"  Episodes '{keyword}': {len(episodes)}")
    
    # 整理节目数据
    shows_data = []
    for show in all_shows:
        if not show:
            continue
        shows_data.append({
            "id": show.get("id"),
            "name": show.get("name", ""),
            "publisher": show.get("publisher", ""),
            "description": show.get("description", "")[:200],
            "total_episodes": show.get("total_episodes", 0),
            "image": show.get("images", [{}])[0].get("url", "") if show.get("images") else "",
            "url": show.get("external_urls", {}).get("spotify", "")
        })
    
    # 整理单集数据
    episodes_data = []
    for ep in all_episodes:
        if not ep:
            continue
        show_name = ""
        if ep.get("show"):
            show_name = ep["show"].get("name", "")
        
        episodes_data.append({
            "id": ep.get("id"),
            "name": ep.get("name", ""),
            "show": show_name,
            "description": ep.get("description", "")[:200],
            "release_date": ep.get("release_date", ""),
            "duration_min": round(ep.get("duration_ms", 0) / 60000),
            "image": ep.get("images", [{}])[0].get("url", "") if ep.get("images") else "",
            "url": ep.get("external_urls", {}).get("spotify", "")
        })
    
    # 按日期排序单集
    episodes_data.sort(key=lambda x: x.get("release_date", ""), reverse=True)
    
    # 保存
    result = {
        "shows": shows_data[:30],
        "episodes": episodes_data[:50]
    }
    
    with open("spotify_data.json", "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    
    print(f"\nSaved {len(result['shows'])} shows, {len(result['episodes'])} episodes")

if __name__ == "__main__":
    main()
