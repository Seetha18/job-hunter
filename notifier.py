import requests
from config import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID

_BASE = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"

def _post(endpoint: str, **kwargs):
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        print(f"[TELEGRAM] {kwargs}")
        return {}
    try:
        r = requests.post(f"{_BASE}/{endpoint}", timeout=20, **kwargs)
        return r.json()
    except Exception as e:
        print(f"[TELEGRAM] send failed: {e}")
        return {}

def send_message(text: str):
    _post("sendMessage", json={
        "chat_id":                  TELEGRAM_CHAT_ID,
        "text":                     text,
        "parse_mode":               "Markdown",
        "disable_web_page_preview": True,
    })

def send_document(pdf_path: str, caption: str = ""):
    with open(pdf_path, "rb") as f:
        _post("sendDocument",
              data={"chat_id": TELEGRAM_CHAT_ID, "caption": caption},
              files={"document": f})

def send_job_alert(job: dict):
    icon  = "🚶" if job.get("is_walkin") else "🎯"
    label = "*WALK-IN ALERT*" if job.get("is_walkin") else "*NEW JOB ALERT*"

    msg = (
        f"{icon} {label}\n\n"
        f"📌 *{job['title']}*\n"
        f"🏢 {job['company']}\n"
        f"📍 {job['location']}\n"
        f"💰 {job['salary']}\n"
        f"🌐 Source: {job['source']}\n\n"
        f"[Apply Now]({job['link']})\n\n"
        f"_Sending tailored resume..._"
    )
    send_message(msg)

def send_summary(n_new: int):
    if n_new > 0:
        send_message(f"✅ *{n_new} new job(s) found* — check alerts above.")
    else:
        print("No new jobs this run.")
