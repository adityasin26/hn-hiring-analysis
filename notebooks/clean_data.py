import json
import re
import html
import pandas as pd
from bs4 import BeautifulSoup

# 1. Load the raw JSON data
input_path = r"C:\Users\asus\OneDrive\ドキュメント\hn-hiring-analysis\data\raw\hn_posts_raw.json"
with open(input_path, "r", encoding="utf-8") as f:
    raw_posts = json.load(f)

print(f"Loaded {len(raw_posts)} raw posts. Starting cleaning...")

# 2. Define the keywords we want to extract
SKILL_KEYWORDS = [
    "python", "sql", "excel", "power bi", "tableau", "looker", "dbt", "snowflake",
    "javascript", "typescript", "react", "node.js", "java", "go", "golang", "rust",
    "c++", "c#", "ruby", "aws", "gcp", "azure", "docker", "kubernetes", "postgres",
    "mysql", "spark", "airflow", "llm", "machine learning", "ai"
]

ROLE_PATTERNS = {
    "Data / Analytics": r"\b(data analyst|data scientist|data engineer|analytics|bi developer|business intelligence)\b",
    "Customer Success / Support": r"\b(customer success|customer support|support specialist|support engineer|cx|solutions engineer)\b",
    "AI / ML": r"\b(ai engineer|ml engineer|machine learning|llm|nlp)\b",
    "DevOps / Infrastructure": r"\b(devops|sre|site reliability|infrastructure|cloud engineer|platform engineer)\b",
    "Product / Design": r"\b(product manager|product designer|ux|ui designer)\b",
    "Software Engineering": r"\b(software engineer|full[- ]?stack|backend|back[- ]?end|frontend|front[- ]?end|developer|swe)\b"
}

REGION_PATTERNS = {
    "US": r"\b(us|usa|united states|san francisco|sf|nyc|new york|austin|seattle|boston|los angeles|bay area)\b",
    "Europe / UK": r"\b(uk|london|europe|eu|berlin|germany|france|paris|amsterdam|netherlands|spain|switzerland|ireland)\b",
    "Canada": r"\b(canada|toronto|vancouver|montreal)\b",
    "India": r"\b(india|bangalore|bengaluru|mumbai|delhi|hyderabad|pune|bhopal)\b",
    "Global / Multiple": r"\b(global|worldwide|multiple countries|anywhere|international)\b"
}

def clean_html(raw_text):
    # Unescape HTML entities like &#x2F; -> /
    unescaped = html.unescape(raw_text)
    # Strip HTML tags and replace them with spaces
    soup = BeautifulSoup(unescaped, "html.parser")
    return soup.get_text(separator=" ").strip()

def get_month(thread_title):
    # Extracts "November 2026" from "Ask HN: Who is hiring? (November 2026)"
    match = re.search(r"\((.*?)\)", thread_title)
    return match.group(1) if match else "Unknown"

def get_remote_policy(text_lower):
    if "hybrid" in text_lower:
        return "Hybrid"
    elif "remote" in text_lower:
        return "Remote"
    elif "onsite" in text_lower or "on-site" in text_lower or "in-person" in text_lower:
        return "Onsite"
    else:
        return "Not Specified"

def get_matches(text_lower, pattern_dict):
    found = []
    for label, pattern in pattern_dict.items():
        if re.search(pattern, text_lower):
            found.append(label)
    return ", ".join(found) if found else "Other / Not Specified"

def get_skills(text_lower):
    found = []
    for skill in SKILL_KEYWORDS:
        # Use word boundaries so 'go' doesn't match 'good' and 'ai' doesn't match 'email'
        if re.search(rf"\b{re.escape(skill)}\b", text_lower):
            found.append(skill)
    return ", ".join(found) if found else "None Listed"

# 3. Process each post (excluding usernames, emails, and full text)
cleaned_records = []

for post in raw_posts:
    clean_text = clean_html(post.get("text", ""))
    text_lower = clean_text.lower()
    
    cleaned_records.append({
        "post_id": post.get("id"),
        "thread_month": get_month(post.get("thread_title", "")),
        "remote_policy": get_remote_policy(text_lower),
        "region": get_matches(text_lower, REGION_PATTERNS),
        "role_categories": get_matches(text_lower, ROLE_PATTERNS),
        "skills": get_skills(text_lower)
    })

# 4. Save to CSV in data/processed
df = pd.DataFrame(cleaned_records)
output_path = r"C:\Users\asus\OneDrive\ドキュメント\hn-hiring-analysis\data\processed\hn_jobs_clean.csv"
df.to_csv(output_path, index=False, encoding="utf-8")

print(f"\nDone! Saved {len(df)} cleaned records to {output_path}")
print("\n--- Quick Summary ---")
print("\nPosts by Month:")
print(df["thread_month"].value_counts())
print("\nPosts by Remote Policy:")
print(df["remote_policy"].value_counts())