import requests

# The most recent IDs from the whoishiring account
recent_ids = [50338728, 50338726, 49922569, 49922568, 49522897, 49522896]
target_thread_id = None

print("Checking recent threads for 'Who is hiring?'...")
for item_id in recent_ids:
    url = f"https://hacker-news.firebaseio.com/v0/item/{item_id}.json"
    response = requests.get(url).json()
    
    # Look for the specific hiring thread
    if response and "Who is hiring?" in response.get("title", ""):
        target_thread_id = item_id
        print(f"Found thread ID: {target_thread_id} | Title: {response.get('title')}")
        break

if target_thread_id:
    # 'kids' contains the IDs of all the comments (job posts) in the thread
    kids = response.get("kids", [])
    if kids:
        first_post_id = kids[0]
        print(f"\nFetching post ID: {first_post_id} to inspect its structure...")
        post_url = f"https://hacker-news.firebaseio.com/v0/item/{first_post_id}.json"
        post_data = requests.get(post_url).json()
        
        print("\n--- Available Data Fields ---")
        print(list(post_data.keys()))
        
        print("\n--- Raw HTML Text (First 500 characters) ---")
        # We slice the first 500 characters so it doesn't flood your terminal
        text = post_data.get("text", "")
        print(text[:500])
else:
    print("Could not find a 'Who is hiring?' thread in the provided IDs.")