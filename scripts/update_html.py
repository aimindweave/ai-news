import os
import json
import re

def clean_text(text):
    """清理文本中的特殊字符"""
    if not text:
        return ""
    # 移除可能破坏 JS 的字符
    text = text.replace('\\', '\\\\')
    text = text.replace('\n', ' ')
    text = text.replace('\r', ' ')
    text = text.replace('\t', ' ')
    text = text.replace('</script>', '<\\/script>')
    # 移除 HTML 实体
    text = re.sub(r'&#\d+;', ' ', text)
    text = re.sub(r'&[a-zA-Z]+;', ' ', text)
    return text

def clean_data(data):
    """递归清理数据"""
    if isinstance(data, str):
        return clean_text(data)
    elif isinstance(data, list):
        return [clean_data(item) for item in data]
    elif isinstance(data, dict):
        return {k: clean_data(v) for k, v in data.items()}
    return data

def main():
    print("Updating HTML...")
    
    # 加载数据
    news = []
    if os.path.exists('news_data.json'):
        with open('news_data.json', 'r', encoding='utf-8') as f:
            news = json.load(f)
    news = clean_data(news)
    print(f"News: {len(news)}")
    
    youtube = []
    if os.path.exists('youtube_data.json'):
        with open('youtube_data.json', 'r', encoding='utf-8') as f:
            youtube = json.load(f)
    youtube = clean_data(youtube)
    print(f"YouTube: {len(youtube)}")
    
    spotify = {"shows": [], "episodes": []}
    if os.path.exists('spotify_data.json'):
        with open('spotify_data.json', 'r', encoding='utf-8') as f:
            spotify = json.load(f)
    spotify = clean_data(spotify)
    print(f"Spotify shows: {len(spotify.get('shows', []))}")
    print(f"Spotify episodes: {len(spotify.get('episodes', []))}")
    
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
    
    if '<!DOCTYPE' not in html and '<html' not in html:
        print("ERROR: Invalid HTML!")
        return
    
    # 替换数据
    def replace_array(html, var_name, data):
        pattern = rf'const {var_name}=\[.*?\];'
        json_str = json.dumps(data, ensure_ascii=True)
        replacement = f'const {var_name}={json_str};'
        new_html, count = re.subn(pattern, replacement, html, flags=re.DOTALL)
        if count == 0:
            print(f"Warning: {var_name} not found")
        return new_html
    
    html = replace_array(html, 'news', news[:50])
    html = replace_array(html, 'audioFiles', audio_files)
    html = replace_array(html, 'ytVideos', youtube[:50])
    html = replace_array(html, 'spotifyShows', spotify.get('shows', [])[:30])
    html = replace_array(html, 'spotifyEpisodes', spotify.get('episodes', [])[:50])
    
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    
    print("HTML updated!")

if __name__ == "__main__":
    main()
