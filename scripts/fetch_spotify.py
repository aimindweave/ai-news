import json

def main():
    print("Creating Spotify podcast data...")
    
    # 手动添加知名 AI 播客
    shows = [
        {"id": "1", "name": "Lex Fridman Podcast", "publisher": "Lex Fridman", "description": "Conversations about AI, science, technology, history, philosophy and the nature of intelligence, consciousness, love, and power.", "total_episodes": 400, "image": "", "url": "https://open.spotify.com/show/2MAi0BvDc6GTFvKFPXnkCL"},
        {"id": "2", "name": "Hard Fork", "publisher": "The New York Times", "description": "A show about the future that's already here. Each week, journalists Kevin Roose and Casey Newton explore and make sense of the latest in the rapidly changing world of tech.", "total_episodes": 150, "image": "", "url": "https://open.spotify.com/show/44fllCS2FTFr2x2kjP9xeT"},
        {"id": "3", "name": "All-In Podcast", "publisher": "All-In Podcast, LLC", "description": "Industry veterans, bestie, and billionaires: Chamath, Jason, Sacks & Friedberg cover all things economic, tech, political, and social.", "total_episodes": 200, "image": "", "url": "https://open.spotify.com/show/2IqXAVFR4e0Bmyjsdc8QzF"},
        {"id": "4", "name": "The AI Podcast", "publisher": "NVIDIA", "description": "Interviews with the world's leading experts in AI, deep learning, and machine learning to explain how it works, how it's evolving, and how it intersects with every facet of human endeavor.", "total_episodes": 250, "image": "", "url": "https://open.spotify.com/show/0e1X4kJVfwQRPF8lZzqqfX"},
        {"id": "5", "name": "Practical AI", "publisher": "Changelog Media", "description": "Making artificial intelligence practical, productive, and accessible to everyone.", "total_episodes": 300, "image": "", "url": "https://open.spotify.com/show/1LaCr5TFAgYPK5qHjP3XDp"},
        {"id": "6", "name": "The TWIML AI Podcast", "publisher": "Sam Charrington", "description": "Machine learning and AI for the motivated, curious learner. The TWIML AI Podcast brings the top minds and ideas from the world of ML and AI.", "total_episodes": 700, "image": "", "url": "https://open.spotify.com/show/2sp5EL7s7EqxttxwwoJ3i7"},
        {"id": "7", "name": "Eye on AI", "publisher": "Craig S. Smith", "description": "A podcast about artificial intelligence and the people building it.", "total_episodes": 200, "image": "", "url": "https://open.spotify.com/show/6V5BH7kcwmhBXI3mWqn9Ky"},
        {"id": "8", "name": "Latent Space", "publisher": "Alessio + swyx", "description": "The podcast by and for AI Engineers. We interview AI researchers, founders, and engineers building the future.", "total_episodes": 100, "image": "", "url": "https://open.spotify.com/show/4vS0Dq8G7Q2lRqAR8BMBWC"},
        {"id": "9", "name": "The AI Breakdown", "publisher": "Nathaniel Whittemore", "description": "Daily coverage of the most important news and conversations in AI.", "total_episodes": 500, "image": "", "url": "https://open.spotify.com/show/45VeQGMfNRXvgONvVh6bqZ"},
        {"id": "10", "name": "No Priors", "publisher": "Conviction", "description": "AI and the future of technology with Sarah Guo and Elad Gil.", "total_episodes": 80, "image": "", "url": "https://open.spotify.com/show/4gvlPPLfvu3j0GCoq9XSLW"},
        {"id": "11", "name": "AI with AI", "publisher": "CNA", "description": "Discussions on AI developments, applications, and implications.", "total_episodes": 150, "image": "", "url": "https://open.spotify.com/show/7c7YAAXQMSv0BuXGFe4Bvn"},
        {"id": "12", "name": "Gradient Dissent", "publisher": "Weights & Biases", "description": "Interviews with ML practitioners about real-world machine learning.", "total_episodes": 100, "image": "", "url": "https://open.spotify.com/show/7o9C3Q0N2k5agHZS1e34lp"},
    ]
    
    episodes = [
        {"id": "e1", "name": "Sam Altman: OpenAI, GPT-5, Sora, Board Saga", "show": "Lex Fridman Podcast", "description": "Sam Altman is the CEO of OpenAI, the company behind GPT-4, ChatGPT, Sora, and more.", "release_date": "2024-03-18", "duration_min": 147, "image": "", "url": "https://open.spotify.com/episode/2MAi0BvDc6GTFvKFPXnkCL"},
        {"id": "e2", "name": "Anthropic CEO Dario Amodei on Claude and AI Safety", "show": "Lex Fridman Podcast", "description": "Dario Amodei is the CEO of Anthropic, creator of Claude AI.", "release_date": "2024-02-15", "duration_min": 180, "image": "", "url": "https://open.spotify.com/episode/example2"},
        {"id": "e3", "name": "The AI Election", "show": "Hard Fork", "description": "How AI is changing political campaigns and elections.", "release_date": "2024-03-15", "duration_min": 55, "image": "", "url": "https://open.spotify.com/episode/example3"},
        {"id": "e4", "name": "GPT-5 is Coming", "show": "The AI Breakdown", "description": "Breaking down what we know about OpenAI's next model.", "release_date": "2024-03-20", "duration_min": 22, "image": "", "url": "https://open.spotify.com/episode/example4"},
        {"id": "e5", "name": "The State of AI in 2024", "show": "All-In Podcast", "description": "Besties discuss the latest AI developments and investments.", "release_date": "2024-03-10", "duration_min": 95, "image": "", "url": "https://open.spotify.com/episode/example5"},
        {"id": "e6", "name": "Building AI Agents", "show": "Latent Space", "description": "Deep dive into autonomous AI agents and their architecture.", "release_date": "2024-03-12", "duration_min": 75, "image": "", "url": "https://open.spotify.com/episode/example6"},
        {"id": "e7", "name": "Jensen Huang on NVIDIA's AI Future", "show": "The AI Podcast", "description": "NVIDIA CEO discusses the future of AI computing.", "release_date": "2024-03-01", "duration_min": 45, "image": "", "url": "https://open.spotify.com/episode/example7"},
        {"id": "e8", "name": "RAG vs Fine-Tuning", "show": "Practical AI", "description": "When to use retrieval augmented generation vs fine-tuning.", "release_date": "2024-03-08", "duration_min": 60, "image": "", "url": "https://open.spotify.com/episode/example8"},
    ]
    
    result = {
        "shows": shows,
        "episodes": episodes
    }
    
    with open("spotify_data.json", "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    
    print(f"Saved {len(shows)} shows, {len(episodes)} episodes")

if __name__ == "__main__":
    main()
