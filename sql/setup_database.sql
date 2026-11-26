CREATE DATABASE IF NOT EXISTS hn_hiring_db;
USE hn_hiring_db;

-- 1. Main table (one row per job post)
CREATE TABLE IF NOT EXISTS jobs (
    post_id INT PRIMARY KEY,
    thread_month VARCHAR(50),
    remote_policy VARCHAR(50),
    region VARCHAR(255),
    role_categories VARCHAR(255),
    skills TEXT
);

-- 2. Normalized skills table
CREATE TABLE IF NOT EXISTS job_skills (
    post_id INT,
    skill VARCHAR(100),
    FOREIGN KEY (post_id) REFERENCES jobs(post_id)
);

-- 3. Normalized roles table
CREATE TABLE IF NOT EXISTS job_roles (
    post_id INT,
    role_category VARCHAR(100),
    FOREIGN KEY (post_id) REFERENCES jobs(post_id)
);