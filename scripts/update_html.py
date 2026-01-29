import json
import os
import re
from datetime import datetime

def main():
    print("\n=== Updating HTML ===\n")
    
    # Load news
    if not os.path.exists('news_data.json'):
        print("❌ No news_data.json found!")
        return
    
    with open('news_data.json', 'r', encoding='utf-8') as f:
        news = json.load(f)
    
    # Check audio files
    audio_files = []
    for i in range(50):
        if os.path.exists(f'audio/news_{i}.mp3'):
            audio_files.append(i)
    
    print(f"📰 News items: {len(news)}")
    print(f"🎙️ Audio files: {len(audio_files)}")
    
    # Read HTML
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()
    
    # Update news data
    news_json = json.dumps(news[:50], ensure_ascii=False)
    html = re.sub(r'const news=\[[\s\S]*?\];', f'const news={news_json};', html)
    
    # Update audio index
    audio_json = json.dumps(audio_files)
    html = re.sub(r'const audioFiles=\[[\s\S]*?\];', f'const audioFiles={audio_json};', html)
    
    # Update timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M UTC")
    html = re.sub(r'Last updated:.*?</span>', f'Last updated: {timestamp}</span>', html)
    
    # Write HTML
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"✅ HTML updated!")
    print(f"⏰ Timestamp: {timestamp}\n")

if __name__ == "__main__":
    main()
