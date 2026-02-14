import os
import json
import requests
import base64

CLIENT_ID = os.environ.get('SPOTIFY_CLIENT_ID')
CLIENT_SECRET = os.environ.get('SPOTIFY_CLIENT_SECRET')

SEARCH_KEYWORDS = [
    "artificial intelligence",
    "machine learning podcast",
    "AI news",
    "deep learning",
    "GPT LLM"
]

def get_access_token():
    """获取 Spotify Access Token"""
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
            print(f"Token error: {r.status_code}")
    except Exception as e:
        print(f"Error: {e}")
    return None

def search_podcasts(token, keyword):
    """搜索播客"""
    url = "https://api.spotify.com/v1/search"
    headers = {"Authorization": f"Bearer {token}"}
    params = {
        "q": keyword,
        "type": "show",
        "market": "US",
        "limit": 10
    }
    
    try:
        r = requests.get(url, headers=headers, params=params, timeout=15)
        if r.status_code == 200:
            return r.json().get("shows", {}).get("items", [])
    except Exception as e:
        print(f"Error: {e}")
    return []

def search_episodes(token, keyword):
    """搜索最新单集"""
    url = "https://api.spotify.com/v1/search"
    headers = {"Authorization": f"Bearer {token}"}
    params = {
        "q": keyword,
        "type": "episode",
        "market": "US",
        "limit": 10
    }
    
    try:
        r = requests.get(url, headers=headers, params=params, timeout=15)
        if r.status_code == 200:
            return r.json().get("episodes", {}).get("items", [])
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
    
    for keyword in SEARCH_KEYWORDS:
        # 获取播客节目
        shows = search_podcasts(token, keyword)
        for show in shows:
            if show["id"] not in seen_show_ids:
                seen_show_ids.add(show["id"])
                all_shows.append(show)
        print(f"  Shows '{keyword}': {len(shows)}")
        
        # 获取单集
        episodes = search_episodes(token, keyword)
        for ep in episodes:
            if ep and ep.get("id") and ep["id"] not in seen_episode_ids:
                seen_episode_ids.add(ep["id"])
                all_episodes.append(ep)
        print(f"  Episodes '{keyword}': {len(episodes)}")
    
    # 整理播客节目数据
    shows_data = []
    for show in all_shows:
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
        episodes_data.append({
            "id": ep.get("id"),
            "name": ep.get("name", ""),
            "show": ep.get("show", {}).get("name", "") if ep.get("show") else "",
            "description": ep.get("description", "")[:200],
            "release_date": ep.get("release_date", ""),
            "duration_min": round(ep.get("duration_ms", 0) / 60000),
            "image": ep.get("images", [{}])[0].get("url", "") if ep.get("images") else "",
            "url": ep.get("external_urls", {}).get("spotify", "")
        })
    
    # 按时间排序单集
    episodes_data.sort(key=lambda x: x.get("release_date", ""), reverse=True)
    
    # 保存
    result = {
        "shows": shows_data[:20],
        "episodes": episodes_data[:20]
    }
    
    with open("spotify_data.json", "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    
    print(f"\nSaved {len(shows_data[:20])} shows, {len(episodes_data[:20])} episodes")

if __name__ == "__main__":
    main()
