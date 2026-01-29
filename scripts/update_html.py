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
    
    # Create JSON strings
    news_json = json.dumps(news[:50], ensure_ascii=False)
    audio_json = json.dumps(audio_files)
    
    # Replace news array
    html = re.sub(
        r'const news=\[[\s\S]*?\];',
        f'const news={news_json};',
        html
    )
    
    # Replace audio files array
    html = re.sub(
        r'const audioFiles=\[[\s\S]*?\];',
        f'const audioFiles={audio_json};',
        html
    )
    
    # Update timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M UTC")
    html = re.sub(
        r'Last updated:.*?</span>',
        f'Last updated: {timestamp}</span>',
        html
    )
    
    # Write HTML
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"✅ HTML updated with {len(news)} news items")
    print(f"✅ Audio available: {len(audio_files)} files")
    print(f"⏰ Timestamp: {timestamp}\n")

if __name__ == "__main__":
    main()
