import os
import json
import requests
import time

API_KEY = os.environ.get('ELEVENLABS_API_KEY')
VOICE_ID = "OYTbf65OHHFELVut7v2H"  # Hope - Natural, Clear and Calm

def generate_audio(text, filename):
    """Generate audio using ElevenLabs API with Hope voice"""
    if not API_KEY:
        print("❌ No ELEVENLABS_API_KEY found!")
        return False
    
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
    
    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": API_KEY
    }
    
    data = {
        "text": text,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.8,
            "style": 0.5,
            "use_speaker_boost": True
        }
    }
    
    try:
        response = requests.post(url, json=data, headers=headers, timeout=60)
        
        if response.status_code == 200:
            with open(filename, 'wb') as f:
                f.write(response.content)
            print(f"✅ Generated: {filename}")
            return True
        else:
            print(f"❌ Error {response.status_code}: {response.text[:200]}")
            return False
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False

def main():
    print("\n=== Generating Audio with ElevenLabs ===\n")
    print(f"🎙️ Using Voice: Hope (ID: {VOICE_ID})\n")
    
    # Create audio directory
    os.makedirs('audio', exist_ok=True)
    
    # Load news
    if not os.path.exists('news_data.json'):
        print("❌ No news_data.json found!")
        return
    
    with open('news_data.json', 'r', encoding='utf-8') as f:
        news = json.load(f)
    
    print(f"📰 Found {len(news)} news items\n")
    
    # Generate audio for all 50 news items
    generated = 0
    failed = 0
    total_chars = 0
    
    for i, item in enumerate(news[:50]):
        filename = f"audio/news_{i}.mp3"
        
        # Create natural script
        script = f"Story {i+1}. {item['title']}. Source: {item['source']}. {item['summary']}"
        
        # Limit characters
        if len(script) > 600:
            script = script[:597] + "..."
        
        total_chars += len(script)
        
        print(f"🎙️ [{i+1}/50] Generating audio ({len(script)} chars)...")
        
        success = generate_audio(script, filename)
        
        if success:
            generated += 1
            time.sleep(0.5)  # Rate limiting
        else:
            failed += 1
            if failed >= 3:
                print("⚠️ Too many failures, stopping...")
                break
    
    print(f"\n=== Summary ===")
    print(f"✅ Generated: {generated} audio files")
    print(f"❌ Failed: {failed}")
    print(f"📊 Total characters used: {total_chars}")
    
    # Save audio index
    audio_index = []
    for i in range(50):
        if os.path.exists(f"audio/news_{i}.mp3"):
            audio_index.append(i)
    
    with open('audio/index.json', 'w') as f:
        json.dump(audio_index, f)
    
    print(f"💾 Audio index saved: {len(audio_index)} files\n")

if __name__ == "__main__":
    main()
