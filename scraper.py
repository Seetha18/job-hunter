import requests
from bs4 import BeautifulSoup
import hashlib
import time
from config import KEYWORDS, REGULAR_LOCATIONS, WALKIN_LOCATIONS, MIN_EXP, MAX_EXP

# ── Shared ────────────────────────────────────────────────────────────────────

RELEVANT_TERMS = [
    "data analyst", "analytics", "business intelligence", "bi analyst",
    "power bi", "data modeler", "sql analyst", "data engineer",
    "reporting analyst", "insights analyst", "walk-in", "walkin",
]

def make_id(title: str, company: str, source: str) -> str:
    key = f"{title}|{company}|{source}".lower().strip()
    return hashlib.md5(key.encode()).hexdigest()[:14]

def is_relevant(job: dict) -> bool:
    title = job.get("title", "").lower()
    return any(t in title for t in RELEVANT_TERMS)

# ── Naukri ────────────────────────────────────────────────────────────────────

NAUKRI_API = "https://www.naukri.com/api/v2/search/job"
NAUKRI_HEADERS = {
    "appid":        "109",
    "systemid":     "109",
    "User-Agent":   "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept":       "application/json",
    "Content-Type": "application/json",
}

def _naukri_fetch(keyword: str, location: str, is_walkin: bool) -> list:
    search_kw = f"walkin {keyword}" if is_walkin else keyword
    params = {
        "noOfResults": 20,
        "urlType":     "search_by_key_loc",
        "searchType":  "adv",
        "keyword":     search_kw,
        "location":    location,
        "experience":  MIN_EXP,
        "jobAge":      1,
        "sort":        "1",
    }
    try:
        r = requests.get(NAUKRI_API, headers=NAUKRI_HEADERS,
                         params=params, timeout=15)
        r.raise_for_status()
        data = r.json()
    except Exception as e:
        print(f"  [Naukri] error ({keyword}, {location}): {e}")
        return []

    jobs = []
    for j in data.get("jobDetails", []):
        title   = j.get("title", "").strip()
        company = j.get("companyName", "").strip()
        ph      = j.get("placeholders", [])
        loc     = ph[0].get("label", location) if ph else location
        salary  = ph[-1].get("label", "Not disclosed") if len(ph) > 1 else "Not disclosed"
        url     = j.get("jdURL", "") or ""
        if not url.startswith("http"):
            url = "https://www.naukri.com" + url

        jobs.append({
            "id":          make_id(title, company, "naukri"),
            "title":       title,
            "company":     company,
            "location":    loc,
            "salary":      salary,
            "source":      "Naukri",
            "link":        url,
            "is_walkin":   is_walkin,
            "description": j.get("jobDescription", ""),
        })
    return jobs

# ── LinkedIn ──────────────────────────────────────────────────────────────────

LINKEDIN_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept":     "text/html,application/xhtml+xml",
}

def _linkedin_fetch(keyword: str, location: str) -> list:
    params = {
        "keywords": keyword,
        "location": f"{location}, India",
        "f_TPR":    "r86400",
        "start":    0,
    }
    url = "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search"
    try:
        r = requests.get(url, headers=LINKEDIN_HEADERS,
                         params=params, timeout=15)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")
    except Exception as e:
        print(f"  [LinkedIn] error ({keyword}, {location}): {e}")
        return []

    jobs = []
    for card in soup.find_all("li")[:10]:
        t = card.find("h3", class_="base-search-card__title")
        c = card.find("h4", class_="base-search-card__subtitle")
        l = card.find("span", class_="job-search-card__location")
        a = card.find("a", class_="base-card__full-link")
        if not t:
            continue
        title   = t.get_text(strip=True)
        company = c.get_text(strip=True) if c else "Unknown"
        loc     = l.get_text(strip=True) if l else location
        link    = a.get("href", "") if a else ""

        jobs.append({
            "id":          make_id(title, company, "linkedin"),
            "title":       title,
            "company":     company,
            "location":    loc,
            "salary":      "See listing",
            "source":      "LinkedIn",
            "link":        link,
            "is_walkin":   False,
            "description": "",
        })
    return jobs

# ── Main entry point ──────────────────────────────────────────────────────────

def fetch_all_jobs() -> list:
    all_jobs   = []
    seen_ids   = set()

    def add(jobs):
        for j in jobs:
            if j["id"] not in seen_ids and is_relevant(j):
                seen_ids.add(j["id"])
                all_jobs.append(j)

    for kw in KEYWORDS[:5]:                       # cap API calls per run
        for loc in REGULAR_LOCATIONS:
            add(_naukri_fetch(kw, loc, is_walkin=False))
            time.sleep(1.2)
            add(_linkedin_fetch(kw, loc))
            time.sleep(1.2)

        for loc in WALKIN_LOCATIONS:              # walk-ins: Hyderabad
            jobs = _naukri_fetch(kw, loc, is_walkin=True)
            for j in jobs:
                j["is_walkin"] = True
            add(jobs)
            time.sleep(1.2)

    return all_jobs
