import os
import json

def main():
    print("Updating HTML...")
    
    # 加载数据
    news = []
    if os.path.exists('news_data.json'):
        with open('news_data.json', 'r', encoding='utf-8') as f:
            news = json.load(f)
    print(f"News: {len(news)}")
    
    youtube = []
    if os.path.exists('youtube_data.json'):
        with open('youtube_data.json', 'r', encoding='utf-8') as f:
            youtube = json.load(f)
    print(f"YouTube: {len(youtube)}")
    
    spotify = {"shows": [], "episodes": []}
    if os.path.exists('spotify_data.json'):
        with open('spotify_data.json', 'r', encoding='utf-8') as f:
            spotify = json.load(f)
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
    
    # 简单字符串替换（不用正则）
    def replace_array(html, var_name, data):
        start_marker = f'const {var_name}=['
        start_idx = html.find(start_marker)
        if start_idx == -1:
            print(f"Warning: {var_name} not found")
            return html
        
        # 找到数组结束位置
        bracket_count = 0
        end_idx = start_idx + len(start_marker) - 1
        for i in range(start_idx + len(start_marker) - 1, len(html)):
            if html[i] == '[':
                bracket_count += 1
            elif html[i] == ']':
                bracket_count -= 1
                if bracket_count == 0:
                    end_idx = i + 1
                    break
        
        # 找到分号
        if end_idx < len(html) and html[end_idx] == ';':
            end_idx += 1
        
        # 生成新 JSON
        json_str = json.dumps(data, ensure_ascii=True)
        new_declaration = f'const {var_name}={json_str};'
        
        return html[:start_idx] + new_declaration + html[end_idx:]
    
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
