import os
import json

def main():
    print("Updating HTML...")
    
    news = []
    if os.path.exists('news_data.json'):
        with open('news_data.json', 'r', encoding='utf-8') as f:
            news = json.load(f)
    print(f"News: {len(news)}")
    
    youtube = []
    if os.path.exists('youtube_data.json'):
        with open('youtube_data.json', 'r', encoding='utf-8') as f:
            youtube = json.load(f)
    print(f"YouTube: {len(youtube)}")
    
    spotify = {"shows": [], "episodes": []}
    if os.path.exists('spotify_data.json'):
        with open('spotify_data.json', 'r', encoding='utf-8') as f:
            spotify = json.load(f)
    print(f"Spotify shows: {len(spotify.get('shows', []))}")
    print(f"Spotify episodes: {len(spotify.get('episodes', []))}")
    
    audio_files = []
    if os.path.exists('audio/index.json'):
        with open('audio/index.json', 'r') as f:
            audio_files = json.load(f)
    print(f"Audio files: {len(audio_files)}")
    
    news_js = json.dumps(news[:50], ensure_ascii=True)
    audio_js = json.dumps(audio_files, ensure_ascii=True)
    yt_js = json.dumps(youtube[:50], ensure_ascii=True)
    shows_js = json.dumps(spotify.get('shows', [])[:30], ensure_ascii=True)
    episodes_js = json.dumps(spotify.get('episodes', [])[:50], ensure_ascii=True)
    
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI News Podcast</title>
    <style>
        *{{margin:0;padding:0;box-sizing:border-box}}
        body{{font-family:system-ui,sans-serif;background:#0a0a0a;color:#fff;line-height:1.6}}
        .header{{background:linear-gradient(180deg,#1a1a2e,#0a0a0a);padding:40px 20px;text-align:center}}
        .badge{{display:inline-block;padding:6px 12px;background:rgba(139,92,246,0.2);border:1px solid #8b5cf6;border-radius:20px;font-size:12px;color:#8b5cf6;margin-bottom:16px}}
        h1{{font-size:2.5rem;margin-bottom:8px}}
        .subtitle{{color:#888;font-size:14px}}
        .nav{{background:#111;padding:12px 20px;position:sticky;top:0;z-index:100;border-bottom:1px solid #222}}
        .nav-inner{{max-width:1200px;margin:0 auto;display:flex;gap:8px;flex-wrap:wrap}}
        .nav-btn{{padding:8px 16px;background:#1a1a1a;border:1px solid #333;border-radius:20px;color:#888;font-size:13px;cursor:pointer}}
        .nav-btn.active{{background:#8b5cf6;color:#fff;border-color:#8b5cf6}}
        .section{{max-width:1200px;margin:0 auto;padding:24px 20px;display:none}}
        .section.active{{display:block}}
        .play-all{{background:linear-gradient(135deg,#1a1a2e,#0f0f1a);border:2px solid #8b5cf6;border-radius:12px;padding:20px;margin-bottom:20px}}
        .play-all h3{{color:#8b5cf6;margin-bottom:4px}}
        .play-all p{{color:#888;font-size:13px}}
        .play-btn{{padding:12px 24px;background:#8b5cf6;color:#fff;border:none;border-radius:20px;font-size:14px;cursor:pointer;margin-top:12px}}
        .play-btn:hover{{background:#7c3aed}}
        .item{{background:#161616;border-radius:8px;padding:16px;margin-bottom:12px;border-left:3px solid #8b5cf6}}
        .item:hover{{background:#1a1a1a}}
        .item-title{{font-size:15px;font-weight:600;margin-bottom:6px}}
        .item-meta{{color:#888;font-size:12px;margin-bottom:8px}}
        .item-desc{{color:#aaa;font-size:13px;margin-bottom:12px}}
        .item-btn{{padding:6px 14px;background:#8b5cf6;color:#fff;border:none;border-radius:12px;font-size:12px;cursor:pointer;text-decoration:none;display:inline-block}}
        .item-btn.green{{background:#1db954}}
        .item-btn.red{{background:#ff0000}}
        .grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:16px}}
        .card{{background:#161616;border-radius:12px;overflow:hidden}}
        .card img{{width:100%;height:180px;object-fit:cover;background:#222}}
        .card-body{{padding:16px}}
        .card-title{{font-size:14px;font-weight:600;margin-bottom:4px;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}}
        .card-meta{{color:#888;font-size:12px;margin-bottom:8px}}
        .card-stats{{color:#8b5cf6;font-size:12px;margin-bottom:12px}}
        footer{{text-align:center;padding:24px;color:#666;font-size:12px;border-top:1px solid #222;margin-top:40px}}
    </style>
</head>
<body>
    <div class="header">
        <div class="badge">AI NEWS AGGREGATOR</div>
        <h1>AI News Podcast</h1>
        <p class="subtitle">News - YouTube - Podcasts - Updated automatically</p>
    </div>
    <nav class="nav">
        <div class="nav-inner">
            <button class="nav-btn active" onclick="showTab('news')">News</button>
            <button class="nav-btn" onclick="showTab('youtube')">YouTube</button>
            <button class="nav-btn" onclick="showTab('spotify')">Podcasts</button>
        </div>
    </nav>
    <div class="section active" id="news">
        <div class="play-all">
            <h3>Listen to All News</h3>
            <p>Browser TTS playback</p>
            <button class="play-btn" id="playAllBtn" onclick="togglePlayAll()">Play All</button>
        </div>
        <div id="newsList"></div>
    </div>
    <div class="section" id="youtube">
        <h2 style="margin-bottom:20px">Top AI YouTube Videos</h2>
        <div class="grid" id="ytList"></div>
    </div>
    <div class="section" id="spotify">
        <h2 style="margin-bottom:20px">AI Podcasts</h2>
        <h3 style="color:#1db954;margin-bottom:16px">Latest Episodes</h3>
        <div id="episodesList"></div>
        <h3 style="color:#1db954;margin:24px 0 16px">Popular Shows</h3>
        <div id="showsList"></div>
    </div>
    <footer>
        <p>Last updated: <span id="updateTime">Loading...</span></p>
        <p>Auto-updates every 2 hours</p>
    </footer>
<script>
var news={news_js};
var audioFiles={audio_js};
var ytVideos={yt_js};
var spotifyShows={shows_js};
var spotifyEpisodes={episodes_js};
var synth=window.speechSynthesis;
var playAllMode=false;
var playIdx=0;
function speak(text,onEnd){{synth.cancel();var u=new SpeechSynthesisUtterance(text);u.rate=1;u.onend=onEnd;synth.speak(u);}}
function stopAll(){{synth.cancel();playAllMode=false;document.getElementById("playAllBtn").textContent="Play All";}}
function togglePlayAll(){{if(playAllMode){{stopAll();return;}}playAllMode=true;playIdx=0;document.getElementById("playAllBtn").textContent="Stop";playNext();}}
function playNext(){{if(!playAllMode||playIdx>=news.length){{stopAll();return;}}var item=news[playIdx];var script="Story "+(playIdx+1)+". "+item.title+". From "+item.source+". "+(item.summary||"");speak(script,function(){{playIdx++;if(playAllMode)setTimeout(playNext,500);}});}}
function renderNews(){{var html="";for(var i=0;i<news.length;i++){{var item=news[i];html+="<div class=item><div class=item-title>"+item.title+"</div><div class=item-meta>"+item.source+" - "+(item.date||"")+"</div><div class=item-desc>"+(item.summary||"")+"</div><a href="+item.url+" target=_blank class=item-btn>Read</a></div>";}}document.getElementById("newsList").innerHTML=html||"<p>No news</p>";}}
function renderYouTube(){{var html="";for(var i=0;i<ytVideos.length;i++){{var v=ytVideos[i];var views=v.views?(v.views/1000).toFixed(0)+"K":"";html+="<div class=card><img src="+(v.thumbnail||"https://via.placeholder.com/320x180")+"><div class=card-body><div class=card-title>"+v.title+"</div><div class=card-meta>"+v.channel+"</div><div class=card-stats>"+views+" views</div><a href="+v.url+" target=_blank class='item-btn red'>Watch</a></div></div>";}}document.getElementById("ytList").innerHTML=html||"<p>No videos</p>";}}
function renderSpotify(){{var epHtml="";for(var i=0;i<spotifyEpisodes.length;i++){{var ep=spotifyEpisodes[i];epHtml+="<div class=item style=border-left-color:#1db954><div class=item-title>"+ep.name+"</div><div class=item-meta>"+ep.show+" - "+ep.release_date+" - "+ep.duration_min+" min</div><div class=item-desc>"+(ep.description||"")+"</div><a href="+ep.url+" target=_blank class='item-btn green'>Listen</a></div>";}}document.getElementById("episodesList").innerHTML=epHtml||"<p>No episodes</p>";var showHtml="";for(var i=0;i<spotifyShows.length;i++){{var s=spotifyShows[i];showHtml+="<div class=item style=border-left-color:#1db954><div class=item-title>"+s.name+"</div><div class=item-meta>"+(s.publisher||"")+" - "+(s.total_episodes||0)+" episodes</div><div class=item-desc>"+(s.description||"")+"</div><a href="+s.url+" target=_blank class='item-btn green'>Open</a></div>";}}document.getElementById("showsList").innerHTML=showHtml||"<p>No shows</p>";}}
function showTab(id){{stopAll();var sections=document.querySelectorAll(".section");for(var i=0;i<sections.length;i++)sections[i].classList.remove("active");var btns=document.querySelectorAll(".nav-btn");for(var i=0;i<btns.length;i++)btns[i].classList.remove("active");document.getElementById(id).classList.add("active");event.target.classList.add("active");}}
document.getElementById("updateTime").textContent=new Date().toLocaleString();
renderNews();
renderYouTube();
renderSpotify();
</script>
</body>
</html>'''
    
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    
    print("HTML updated!")

if __name__ == "__main__":
    main()
