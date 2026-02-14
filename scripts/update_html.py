import os
import json
import re

def main():
    print("Updating HTML...")
    
    # 加载新闻
    news = []
    if os.path.exists('news_data.json'):
        with open('news_data.json', 'r', encoding='utf-8') as f:
            news = json.load(f)
    print(f"News: {len(news)}")
    
    # 加载 YouTube
    youtube = []
    if os.path.exists('youtube_data.json'):
        with open('youtube_data.json', 'r', encoding='utf-8') as f:
            youtube = json.load(f)
    print(f"YouTube: {len(youtube)}")
    
    # 加载 Spotify
    spotify = {"shows": [], "episodes": []}
    if os.path.exists('spotify_data.json'):
        with open('spotify_data.json', 'r', encoding='utf-8') as f:
            spotify = json.load(f)
    print(f"Spotify shows: {len(spotify.get('shows', []))}")
    print(f"Spotify episodes: {len(spotify.get('episodes', []))}")
    
    # 加载音频索引
    audio_files = []
    if os.path.exists('audio/index.json'):
        with open('audio/index.json', 'r') as f:
            audio_files = json.load(f)
    print(f"Audio files: {len(audio_files)}")
    
    # 读取 HTML
    if not os.path.exists('index.html'):
        print("No index.html!")
        return
    
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()
    
    # 验证 HTML
    if not html.strip().startswith('<!DOCTYPE') and not html.strip().startswith('<html'):
        print("ERROR: Invalid HTML!")
        return
    
    # 替换数据
    def replace_array(html, var_name, data):
        pattern = rf'const {var_name}=\[.*?\];'
        replacement = f'const {var_name}=' + json.dumps(data, ensure_ascii=False) + ';'
        new_html, count = re.subn(pattern, replacement, html, flags=re.DOTALL)
        if count == 0:
            print(f"Warning: {var_name} not found")
        return new_html
    
    html = replace_array(html, 'news', news[:50])
    html = replace_array(html, 'audioFiles', audio_files)
    html = replace_array(html, 'ytVideos', youtube[:50])
    html = replace_array(html, 'spotifyShows', spotify.get('shows', [])[:30])
    html = replace_array(html, 'spotifyEpisodes', spotify.get('episodes', [])[:50])
    
    # 保存
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    
    print("HTML updated!")

if __name__ == "__main__":
    main()
