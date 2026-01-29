import os
import json
import requests
import time

ELEVENLABS_API_KEY = os.environ.get('ELEVENLABS_API_KEY')
VOICE_ID = "21m00Tcm4TlvDq8ikWAM"  # Rachel - natural female voice

def generate_audio(text, filename):
    """Generate audio using ElevenLabs API"""
    if not ELEVENLABS_API_KEY:
        print("No API key found!")
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
            "stability": 0.5,
            "similarity_boost": 0.75
        }
    }
    
    try:
        response = requests.post(url, json=data, headers=headers, timeout=30)
        
        if response.status_code == 200:
            with open(filename, 'wb') as f:
                f.write(response.content)
            print(f"✓ Generated: {filename}")
            return True
        else:
            print(f"✗ Error {response.status_code}: {response.text[:100]}")
            return False
    except Exception as e:
        print(f"✗ Exception: {e}")
        return False

def main():
    # Create audio directory
    os.makedirs('audio', exist_ok=True)
    
    # Load news
    if not os.path.exists('news_data.json'):
        print("No news_data.json found")
        return
    
    with open('news_data.json', 'r') as f:
        news = json.load(f)
    
    print(f"Found {len(news)} news items")
    
    # Generate audio for top 10 only (to save API quota)
    # 10 stories * ~300 chars = ~3000 chars per run
    # Free tier: 10,000 chars/month = ~3 runs per month
    
    generated = 0
    for i, item in enumerate(news[:10]):
        filename = f"audio/news_{i}.mp3"
        
        # Create script
        script = f"Story {i+1}. {item['title']}. From {item['source']}. {item['summary']}"
        
        # Limit to 500 chars per story
        if len(script) > 500:
            script = script[:497] + "..."
        
        print(f"\nGenerating audio {i+1}/10...")
        success = generate_audio(script, filename)
        
        if success:
            generated += 1
            time.sleep(1)  # Rate limiting
        else:
            print("Stopping due to error (may have hit API limit)")
            break
    
    print(f"\n✓ Generated {generated} audio files")
    
    # Save audio index
    audio_index = []
    for i in range(generated):
        audio_index.append({
            "index": i,
            "file": f"audio/news_{i}.mp3",
            "title": news[i]["title"]
        })
    
    with open('audio/index.json', 'w') as f:
        json.dump(audio_index, f, indent=2)
    
    print("✓ Saved audio index")

if __name__ == "__main__":
    main()
