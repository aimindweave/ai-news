import os
import json
import re
import base64

def clean_fields(items, fields):
    for item in items:
        for key in fields:
            if key in item and item[key]:
                val = str(item[key])
                val = re.sub(r'<[^>]*?>?', ' ', val)
                val = val.replace('<', '')
                val = re.sub(r'\s+', ' ', val).strip()
                item[key] = val

def to_base64(data):
    j = json.dumps(data, ensure_ascii=True)
    return base64.b64encode(j.encode()).decode()

def replace_var(html, var_name, b64_str):
    lines = html.split('\n')
    new_val = "var " + var_name + " = '" + b64_str + "';"
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith('var ' + var_name + ' =') or stripped.startswith('var ' + var_name + '='):
            lines[i] = new_val
            print(f"Replaced {var_name} (line {i+1})")
            break
    return '\n'.join(lines)

def main():
    print("Updating HTML...")
    
    news = []
    if os.path.exists("news_data.json"):
        with open("news_data.json", "r", encoding="utf-8") as f:
            news = json.load(f)
    print(f"News: {len(news)}")
    
    trending = []
    if os.path.exists("trending_data.json"):
        with open("trending_data.json", "r", encoding="utf-8") as f:
            trending = json.load(f)
    print(f"Trending: {len(trending)}")
    
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
    
    clean_fields(news, ["title", "summary", "source"])
    clean_fields(trending, ["title", "description", "source"])
    clean_fields(youtube, ["title", "description", "channel"])
    clean_fields(podcasts, ["name", "description", "show"])
    
    with open("index.html", "r", encoding="utf-8") as f:
        html = f.read()
    
    html = replace_var(html, "defined_news", to_base64(news[:50]))
    html = replace_var(html, "defined_trending", to_base64(trending[:30]))
    html = replace_var(html, "defined_youtube", to_base64(youtube[:50]))
    html = replace_var(html, "defined_podcasts", to_base64(podcasts[:30]))
    
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)
    
    print("HTML updated!")

if __name__ == "__main__":
    main()
