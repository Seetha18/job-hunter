import json
import os
import csv
from datetime import datetime

SEEN_FILE = "seen_jobs.json"
LOG_FILE  = "application_log.csv"

def load_seen() -> set:
    if os.path.exists(SEEN_FILE):
        with open(SEEN_FILE, encoding="utf-8") as f:
            return set(json.load(f))
    return set()

def save_seen(seen: set):
    with open(SEEN_FILE, "w", encoding="utf-8") as f:
        json.dump(list(seen), f)

def is_new(job_id: str, seen: set) -> bool:
    return job_id not in seen

def mark_seen(job_id: str, seen: set):
    seen.add(job_id)

def log_job(job: dict):
    exists = os.path.exists(LOG_FILE)
    with open(LOG_FILE, "a", newline="", encoding="utf-8") as f:
        fields = ["date", "title", "company", "location", "salary",
                  "source", "is_walkin", "link"]
        w = csv.DictWriter(f, fieldnames=fields)
        if not exists:
            w.writeheader()
        w.writerow({
            "date":      datetime.now().strftime("%Y-%m-%d %H:%M"),
            "title":     job.get("title", ""),
            "company":   job.get("company", ""),
            "location":  job.get("location", ""),
            "salary":    job.get("salary", ""),
            "source":    job.get("source", ""),
            "is_walkin": "Yes" if job.get("is_walkin") else "No",
            "link":      job.get("link", ""),
        })
