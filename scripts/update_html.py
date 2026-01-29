import json
import os
from datetime import datetime

def main():
    print("=== Updating HTML ===")
    
    if not os.path.exists('news_data.json'):
        print("No news_data.json found!")
        return
    
    with open('news_data.json', 'r', encoding='utf-8') as f:
        news = json.load(f)
    
    audio_files = []
    for i in range(50):
        if os.path.exists(f'audio/news_{i}.mp3'):
            audio_files.append(i)
    
    print(f"News: {len(news)}, Audio: {len(audio_files)}")
    
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()
    
    if not html.strip().startswith('<!DOCTYPE') and not html.strip().startswith('<html'):
        print("ERROR: index.html is not valid HTML!")
        return
    
    news_json = json.dumps(news[:50], ensure_ascii=False)
    audio_json = json.dumps(audio_files)
    
    news_start = html.find('const news=[')
    if news_start == -1:
        print("Could not find news array")
        return
    
    news_end = html.find('];', news_start)
    if news_end == -1:
        print("Could not find end of news array")
        return
    
    new_html = html[:news_start] + 'const news=' + news_json + html[news_end+1:]
    
    audio_start = new_html.find('const audioFiles=[')
    if audio_start != -1:
        audio_end = new_html.find('];', audio_start)
        if audio_end != -1:
            new_html = new_html[:audio_start] + 'const audioFiles=' + audio_json + new_html[audio_end+1:]
    
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(new_html)
    
    print("HTML updated!")

if __name__ == "__main__":
    main()
