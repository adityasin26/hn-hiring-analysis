import pandas as pd

# Load the two normalized CSVs
skills_df = pd.read_csv(r"C:\Users\asus\OneDrive\ドキュメント\hn-hiring-analysis\data\processed\hn_skills.csv")
roles_df = pd.read_csv(r"C:\Users\asus\OneDrive\ドキュメント\hn-hiring-analysis\data\processed\hn_roles.csv")

output_sql = r"C:\Users\asus\OneDrive\ドキュメント\hn-hiring-analysis\sql\insert_data.sql"

with open(output_sql, "w", encoding="utf-8") as f:
    f.write("USE hn_hiring_db;\n\n")
    
    # Write job_skills inserts
    f.write("INSERT INTO job_skills (post_id, skill) VALUES\n")
    skill_values = []
    for row in skills_df.itertuples(index=False):
        clean_skill = str(row.skill).replace("'", "''")
        skill_values.append(f"({int(row.post_id)}, '{clean_skill}')")
    f.write(",\n".join(skill_values) + ";\n\n")
    
    # Write job_roles inserts
    f.write("INSERT INTO job_roles (post_id, role_category) VALUES\n")
    role_values = []
    for row in roles_df.itertuples(index=False):
        clean_role = str(row.role_category).replace("'", "''")
        role_values.append(f"({int(row.post_id)}, '{clean_role}')")
    f.write(",\n".join(role_values) + ";\n")

print(f"Created {output_sql} successfully!")