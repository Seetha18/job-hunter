import os

# ── Telegram ─────────────────────────────────────────────────────────────────
TELEGRAM_TOKEN   = os.environ.get("TELEGRAM_TOKEN", "")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "")

# ── Claude API (for resume tailoring) ────────────────────────────────────────
CLAUDE_API_KEY = os.environ.get("CLAUDE_API_KEY", "")
CLAUDE_MODEL   = "claude-haiku-4-5-20251001"

# ── Job search keywords ───────────────────────────────────────────────────────
KEYWORDS = [
    "data analyst",
    "power bi analyst",
    "business intelligence analyst",
    "BI analyst",
    "data modeler",
    "analytics analyst",
    "sql analyst",
    "reporting analyst",
]

# ── Locations ─────────────────────────────────────────────────────────────────
REGULAR_LOCATIONS = ["bengaluru", "hyderabad", "remote"]
WALKIN_LOCATIONS  = ["hyderabad"]   # walk-ins: Hyderabad only

# ── Filters ───────────────────────────────────────────────────────────────────
MIN_EXP      = 0
MAX_EXP      = 7
JOB_AGE_DAYS = 1   # only jobs posted in the last 24 hours
