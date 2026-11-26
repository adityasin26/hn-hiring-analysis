import requests
import json
import time
import os

# The most recent IDs from the whoishiring account
recent_ids = [50338728, 50338726, 49922569, 49922568, 49522897, 49522896, 49156683, 49156682]

target_threads = []

print("Finding the 3 most recent 'Who is hiring?' threads...")
for item_id in recent_ids:
    if len(target_threads) == 3:
        break
    url = f"https://hacker-news.firebaseio.com/v0/item/{item_id}.json"
    response = requests.get(url).json()
    
    if response and "Who is hiring?" in response.get("title", ""):
        target_threads.append({
            "id": item_id,
            "title": response.get("title"),
            "kids": response.get("kids", [])
        })
        print(f"Found: {response.get('title')} with {len(response.get('kids', []))} posts.")

print("\nStarting data collection. This will take about 3 to 5 minutes to respect the API...")

all_posts = []

for thread in target_threads:
    print(f"\nFetching posts for: {thread['title']}...")
    
    for i, post_id in enumerate(thread['kids']):
        post_url = f"https://hacker-news.firebaseio.com/v0/item/{post_id}.json"
        
        try:
            post_data = requests.get(post_url).json()
            
            # We only keep posts that have text and haven't been deleted
            if post_data and not post_data.get("deleted") and post_data.get("text"):
                # Add the thread month so we can track trends over time later
                post_data['thread_title'] = thread['title']
                all_posts.append(post_data)
                
        except Exception as e:
            print(f"Failed to fetch post {post_id}: {e}")
            
        # Print progress every 100 posts so you know it isn't frozen
        if (i + 1) % 100 == 0:
            print(f"  Fetched {i + 1} posts...")
            
        # Be polite to the API (0.1 second pause)
        time.sleep(0.1)

# Save everything to the data/raw folder
output_path = r"C:\Users\asus\OneDrive\ドキュメント\hn-hiring-analysis\data\raw\hn_posts_raw.json"

with open(output_path, "w", encoding="utf-8") as f:
    json.dump(all_posts, f, indent=4)

print(f"\nDone! Saved {len(all_posts)} posts to {output_path}")