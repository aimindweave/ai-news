#!/usr/bin/env python3
"""
Update HTML with fetched news data
"""

import json
from datetime import datetime

def update_html():
    """Read news data and update HTML"""
    
    # Read news data
    with open('news_data.json', 'r', encoding='utf-8') as f:
        news_data = json.load(f)
    
    # Read HTML template
    with open('index.html', 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # Find and replace data
    start_marker = "const episodes = ["
    end_marker = "];"
    
    start_idx = html_content.find(start_marker)
    end_idx = html_content.find(end_marker, start_idx)
    
    if start_idx != -1 and end_idx != -1:
        # Generate new data string
        new_data = json.dumps(news_data, ensure_ascii=False, indent=2)
        
        # Replace
        new_html = (
            html_content[:start_idx + len(start_marker)] +
            "\n" + new_data + "\n        " +
            html_content[end_idx:]
        )
        
        # Update timestamp
        update_time = datetime.now().strftime('%B %d, %Y')
        new_html = new_html.replace(
            'Updated January 29, 2026',
            f'Updated {update_time}'
        )
        
        # Write file
        with open('index.html', 'w', encoding='utf-8') as f:
            f.write(new_html)
        
        print(f"HTML updated with {len(news_data)} news items")
    else:
        print("Could not find data placeholder in HTML")

if __name__ == '__main__':
    update_html()
