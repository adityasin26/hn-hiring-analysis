import pandas as pd

# Load the cleaned CSV
input_path = r"C:\Users\asus\OneDrive\ドキュメント\hn-hiring-analysis\data\processed\hn_jobs_clean.csv"
df = pd.read_csv(input_path)

# 1. Create a normalized skills table (one row per post + skill)
skills_df = df[["post_id", "skills"]].copy()
skills_df["skill"] = skills_df["skills"].str.split(", ")
skills_df = skills_df.explode("skill")[["post_id", "skill"]]
skills_df = skills_df[skills_df["skill"] != "None Listed"]

skills_path = r"C:\Users\asus\OneDrive\ドキュメント\hn-hiring-analysis\data\processed\hn_skills.csv"
skills_df.to_csv(skills_path, index=False, encoding="utf-8")

# 2. Create a normalized roles table (one row per post + role)
roles_df = df[["post_id", "role_categories"]].copy()
roles_df["role_category"] = roles_df["role_categories"].str.split(", ")
roles_df = roles_df.explode("role_category")[["post_id", "role_category"]]

roles_path = r"C:\Users\asus\OneDrive\ドキュメント\hn-hiring-analysis\data\processed\hn_roles.csv"
roles_df.to_csv(roles_path, index=False, encoding="utf-8")

print(f"Saved {len(skills_df)} rows to hn_skills.csv")
print(f"Saved {len(roles_df)} rows to hn_roles.csv")