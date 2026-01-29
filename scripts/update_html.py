import json
import os
from datetime import datetime

def main():
    # Load news
    if not os.path.exists('news_data.json'):
        print("No news data found")
        return
    
    with open('news_data.json', 'r') as f:
        news = json.load(f)
    
    # Check for audio files
    audio_files = []
    for i in range(10):
        if os.path.exists(f'audio/news_{i}.mp3'):
            audio_files.append(i)
    
    print(f"Found {len(audio_files)} audio files")
    
    # Read current HTML
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()
    
    # Generate news JSON for JavaScript
    news_json = json.dumps(news[:50])
    audio_json = json.dumps(audio_files)
    
    # Find and replace the news data in HTML
    # Look for: const news=[...];
    import re
    
    # Update news data
    pattern = r'const news=\[[\s\S]*?\];'
    replacement = f'const news={news_json};'
    html = re.sub(pattern, replacement, html)
    
    # Update audio index
    pattern2 = r'const audioFiles=\[[\s\S]*?\];'
    replacement2 = f'const audioFiles={audio_json};'
    if 'const audioFiles=' in html:
        html = re.sub(pattern2, replacement2, html)
    
    # Update timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M UTC")
    pattern3 = r'Last updated:.*?</span>'
    replacement3 = f'Last updated: {timestamp}</span>'
    html = re.sub(pattern3, replacement3, html)
    
    # Write updated HTML
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"✓ Updated HTML with {len(news)} news items")
    print(f"✓ Audio available for indices: {audio_files}")

if __name__ == "__main__":
    main()
