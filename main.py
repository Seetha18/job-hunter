import os
from scraper  import fetch_all_jobs
from notifier import send_job_alert, send_document, send_summary, send_message
from tracker  import load_seen, save_seen, is_new, mark_seen, log_job
from config   import CLAUDE_API_KEY


def run():
    print("Job monitor starting...")

    seen     = load_seen()
    all_jobs = fetch_all_jobs()
    print(f"Fetched {len(all_jobs)} total jobs from Naukri + LinkedIn.")

    new_jobs = []
    for job in all_jobs:
        if is_new(job["id"], seen):
            new_jobs.append(job)
            mark_seen(job["id"], seen)
            log_job(job)

    print(f"{len(new_jobs)} new job(s) to alert.")

    for job in new_jobs:
        send_job_alert(job)

        if CLAUDE_API_KEY:
            try:
                from tailor import tailor_resume_text, generate_pdf
                print(f"  Tailoring resume: {job['title']} @ {job['company']}")
                text = tailor_resume_text(job)
                pdf  = generate_pdf(text, job["title"], job["company"])
                send_document(pdf, f"Tailored resume - {job['title']} at {job['company']}")
                os.remove(pdf)
            except Exception as e:
                print(f"  Resume tailoring failed: {e}")
                send_message(f"_Could not generate tailored resume for this role: {e}_")

    send_summary(len(new_jobs))
    save_seen(seen)
    print("Done.")


if __name__ == "__main__":
    run()
