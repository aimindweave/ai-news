import os
import json
import requests

ELEVENLABS_API_KEY = os.environ.get('ELEVENLABS_API_KEY')
VOICE_ID = "21m00Tcm4TlvDq8ikWAM"  # Rachel - 自然女声

def generate_audio(text, filename):
    """Generate audio using ElevenLabs API"""
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
    
    response = requests.post(url, json=data, headers=headers)
    
    if response.status_code == 200:
        with open(filename, 'wb') as f:
            f.write(response.content)
        print(f"Generated: {filename}")
        return True
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return False

def main():
    # Create audio directory
    os.makedirs('audio', exist_ok=True)
    
    # Load news from JSON (we'll create this)
    news_file = 'news_data.json'
    if not os.path.exists(news_file):
        print("No news data found")
        return
    
    with open(news_file, 'r') as f:
        news = json.load(f)
    
    # Generate audio for top 10 news (to save API quota)
    for i, item in enumerate(news[:10]):
        filename = f"audio/news_{i}.mp3"
        
        # Skip if already exists
        if os.path.exists(filename):
            print(f"Skipping {filename} - already exists")
            continue
        
        # Create script with intro
        script = f"Story {i+1}. {item['title']}. From {item['source']}. {item['summary']}"
        
        success = generate_audio(script, filename)
        if not success:
            print(f"Failed to generate audio for story {i+1}")
            break  # Stop if we hit API limits

if __name__ == "__main__":
    main()
