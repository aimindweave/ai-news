import os
import json
import requests
import time
import hashlib

ELEVENLABS_API_KEY = os.environ.get('ELEVENLABS_API_KEY')
VOICE_ID = "OYTbf65OHHFELVut7v2H"  # Hope - Natural, Clear and Calm

def get_hash(text):
    return hashlib.md5(text.encode()).hexdigest()[:8]

def generate_audio(text, filename):
    if not ELEVENLABS_API_KEY:
        print("No API key!")
        return False
    
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": ELEVENLABS_API_KEY
    }
    data = {
        "text": text,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {
            "stability": 0.7,
            "similarity_boost": 0.8,
            "style": 0,
            "use_speaker_boost": False
        }
    }
    
    try:
        response = requests.post(url, json=data, headers=headers, timeout=60)
        if response.status_code == 200:
            with open(filename, 'wb') as f:
                f.write(response.content)
            print(f"OK: {filename}")
            return True
        else:
            print(f"Error {response.status_code}: {response.text[:100]}")
            return False
    except Exception as e:
        print(f"Error: {e}")
        return False

def main():
    os.makedirs('audio', exist_ok=True)
    
    # Load manifest (tracks content hashes)
    manifest_file = 'audio/manifest.json'
    manifest = {}
    if os.path.exists(manifest_file):
        with open(manifest_file, 'r') as f:
            manifest = json.load(f)
    
    # Load news
    if not os.path.exists('news_data.json'):
        print("No news_data.json!")
        return
    
    with open('news_data.json', 'r', encoding='utf-8') as f:
        news = json.load(f)
    
    print(f"Found {len(news)} news items")
    print(f"Voice: Hope ({VOICE_ID})")
    
    # Generate audio for top 40 items
    generated = 0
    skipped = 0
    
    for i, item in enumerate(news[:40]):
        # Create script
        title = item.get('title', '')
        source = item.get('source', '')
        summary = item.get('summary', '')[:200]
        
        script = f"Story {i+1}. {title}. From {source}. {summary}"
        if len(script) > 500:
            script = script[:497] + "..."
        
        content_hash = get_hash(script)
        filename = f'audio/news_{i}.mp3'
        
        # Check if content changed
        old_hash = manifest.get(f'news_{i}', '')
        
        if old_hash == content_hash and os.path.exists(filename):
            print(f"[{i}] Unchanged, skip")
            skipped += 1
            continue
        
        # Generate new audio
        print(f"[{i}] Generating: {title[:40]}...")
        if generate_audio(script, filename):
            manifest[f'news_{i}'] = content_hash
            generated += 1
            time.sleep(0.5)
        else:
            print(f"Failed at {i}, stopping")
            break
    
    # Save manifest
    with open(manifest_file, 'w') as f:
        json.dump(manifest, f, indent=2)
    
    # Create audio index
    audio_files = [i for i in range(40) if os.path.exists(f'audio/news_{i}.mp3')]
    with open('audio/index.json', 'w') as f:
        json.dump(audio_files, f)
    
    print(f"\nGenerated: {generated}")
    print(f"Skipped (unchanged): {skipped}")
    print(f"Total audio files: {len(audio_files)}")

if __name__ == "__main__":
    main()
