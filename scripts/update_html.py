import os
import json
import re

def safe_json(data):
    """Generate a JSON string safe for embedding inside <script> tags."""
    s = json.dumps(data, ensure_ascii=True)
    # Escape characters that break HTML parsing inside <script>
    s = s.replace("</", "<\\/")     # Prevent </script> or any closing tag
    s = s.replace("<!--", "<\\!--")  # Prevent HTML comments
    return s

def clean_html_from_fields(items, fields):
    """Strip HTML tags and lone < from text fields to prevent breaking <script>."""
    for item in items:
        for key in fields:
            if key in item and item[key]:
                val = str(item[key])
                # Remove complete HTML tags like <br />, <em>, etc.
                val = re.sub(r'<[^>]+>', ' ', val)
                # Remove any remaining lone < characters (truncated tags)
                val = val.replace('<', '')
                # Clean up extra whitespace
                val = re.sub(r'\s+', ' ', val).strip()
                item[key] = val

def replace_var(html, var_name, json_str):
    """Replace a JS variable declaration regardless of current value.
    
    Matches the full line starting with 'var <var_name> = ' to end of line.
    """
    pattern = r'^(var\s+' + re.escape(var_name) + r'\s*=\s*).*$'
    replacement = r'\g<1>' + repr(json_str).replace('\\', '\\\\') + ';'
    
    # Actually, repr() and regex replacement don't mix well. Do it manually.
    new_val = 'var ' + var_name + ' = ' + repr(json_str) + ';'
    
    lines = html.split('\n')
    found = False
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith('var ' + var_name + ' =') or stripped.startswith('var ' + var_name + '='):
            lines[i] = new_val
            found = True
            print(f"Replaced {var_name} (line {i+1})")
            break
    
    if not found:
        print(f"WARNING: Could not find variable '{var_name}' in HTML!")
    
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
    
    # Clean HTML tags from all text fields to prevent breaking <script>
    clean_html_from_fields(news, ["title", "summary", "source"])
    clean_html_from_fields(trending, ["title", "description", "source"])
    clean_html_from_fields(youtube, ["title", "description", "channel"])
    clean_html_from_fields(podcasts, ["name", "description", "show"])
    
    with open("index.html", "r", encoding="utf-8") as f:
        html = f.read()
    
    # Verify the script section exists
    if '<script>' not in html:
        print("ERROR: No <script> tag found in HTML!")
        return
    
    html = replace_var(html, "defined_news", safe_json(news[:50]))
    html = replace_var(html, "defined_trending", safe_json(trending[:30]))
    html = replace_var(html, "defined_youtube", safe_json(youtube[:50]))
    html = replace_var(html, "defined_podcasts", safe_json(podcasts[:30]))
    
    # Verify the closing script tag still exists
    if '</script>' not in html:
        print("ERROR: </script> tag missing after replacement! Data may contain unsafe content.")
        return
    
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)
    
    print("HTML updated!")

if __name__ == "__main__":
    main()
