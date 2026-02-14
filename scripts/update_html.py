import os
import json

def safe_json(data):
    s = json.dumps(data, ensure_ascii=True)
    s = s.replace("</script>", "<\\/script>")
    return s

def main():
    print("Updating HTML...")
    
    news = []
    if os.path.exists("news_data.json"):
        with open("news_data.json", "r", encoding="utf-8") as f:
            news = json.load(f)
    print(f"News: {len(news)}")
    
    youtube = []
    if os.path.exists("youtube_data.json"):
        with open("youtube_data.json", "r", encoding="utf-8") as f:
            youtube = json.load(f)
    print(f"YouTube: {len(youtube)}")
    
    podcasts = []
    if os.path.exists("spotify_data.json"):
        with open("spotify_data.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            podcasts = data.get("episodes", [])
    print(f"Podcasts: {len(podcasts)}")
    
    with open("index.html", "r", encoding="utf-8") as f:
        html = f.read()
    
    html = html.replace('var defined_news = "__NEWS_DATA__";', 
                        'var defined_news = ' + repr(safe_json(news[:50])) + ';')
    html = html.replace('var defined_youtube = "__YOUTUBE_DATA__";', 
                        'var defined_youtube = ' + repr(safe_json(youtube[:50])) + ';')
    html = html.replace('var defined_podcasts = "__PODCAST_DATA__";', 
                        'var defined_podcasts = ' + repr(safe_json(podcasts[:30])) + ';')
    
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)
    
    print("HTML updated!")

if __name__ == "__main__":
    main()
