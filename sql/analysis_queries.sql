USE hn_hiring_db;

-- 1. Monthly Hiring Volume & Remote Share
SELECT 
    thread_month,
    COUNT(*) AS total_posts,
    SUM(CASE WHEN remote_policy = 'Remote' THEN 1 ELSE 0 END) AS remote_posts,
    ROUND(100.0 * SUM(CASE WHEN remote_policy = 'Remote' THEN 1 ELSE 0 END) / COUNT(*), 1) AS remote_pct
FROM jobs
GROUP BY thread_month
ORDER BY FIELD(thread_month, 'September 2026', 'October 2026', 'November 2026');

-- 2. Top 10 Most In-Demand Skills Overall
SELECT 
    skill,
    COUNT(DISTINCT post_id) AS post_count,
    ROUND(100.0 * COUNT(DISTINCT post_id) / (SELECT COUNT(*) FROM jobs), 1) AS pct_of_all_posts
FROM job_skills
GROUP BY skill
ORDER BY post_count DESC
LIMIT 10;

-- 3. Demand by Role Category
SELECT 
    role_category,
    COUNT(DISTINCT post_id) AS post_count,
    ROUND(100.0 * COUNT(DISTINCT post_id) / (SELECT COUNT(*) FROM jobs), 1) AS pct_of_all_posts
FROM job_roles
GROUP BY role_category
ORDER BY post_count DESC;

-- 4. Remote Policy Breakdown by Role Category (JOIN)
SELECT 
    r.role_category,
    COUNT(DISTINCT j.post_id) AS total_posts,
    SUM(CASE WHEN j.remote_policy = 'Remote' THEN 1 ELSE 0 END) AS remote_count,
    ROUND(100.0 * SUM(CASE WHEN j.remote_policy = 'Remote' THEN 1 ELSE 0 END) / COUNT(DISTINCT j.post_id), 1) AS remote_pct
FROM jobs j
JOIN job_roles r ON j.post_id = r.post_id
GROUP BY r.role_category
ORDER BY total_posts DESC;

-- 5. Top Skills for Data / Analytics & Customer Success Roles (Multi-Table JOIN)
SELECT 
    r.role_category,
    s.skill,
    COUNT(DISTINCT s.post_id) AS post_count
FROM job_roles r
JOIN job_skills s ON r.post_id = s.post_id
WHERE r.role_category IN ('Data / Analytics', 'Customer Success / Support')
GROUP BY r.role_category, s.skill
ORDER BY r.role_category, post_count DESC;