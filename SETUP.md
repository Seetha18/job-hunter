# Job Hunter Setup Guide
## What this does
- Checks Naukri + LinkedIn every 30 minutes, 24/7 (even while you sleep)
- Detects NEW job postings matching your keywords
- Sends you a Telegram notification instantly with job title, company, salary, apply link
- Auto-generates a tailored PDF resume for that specific role and sends it to your Telegram
- Tracks all found jobs in application_log.csv
- Covers walk-in interviews in Hyderabad separately

---

## Step 1 — Create your Telegram Bot (5 minutes)

1. Open Telegram and search for **@BotFather**
2. Send: `/newbot`
3. Give it a name e.g. `Seetha Job Alerts`
4. Give it a username e.g. `seetha_jobs_bot`
5. BotFather will give you a token like: `7123456789:AAFxxx...`  → **Save this (TELEGRAM_TOKEN)**

6. Now get your Chat ID:
   - Search for **@userinfobot** on Telegram
   - Start it, it will reply with your ID e.g. `123456789`  → **Save this (TELEGRAM_CHAT_ID)**

7. Start a conversation with your new bot (search its username, press Start)

---

## Step 2 — Get your Claude API Key (for tailored resumes)

1. Go to: https://console.anthropic.com/
2. Sign up / log in
3. Go to API Keys → Create Key
4. Copy the key → **Save this (CLAUDE_API_KEY)**

Note: Resume tailoring costs ~$0.001 per job (very cheap). You can skip this step
and the bot will still send job alerts — just without auto-tailored resumes.

---

## Step 3 — Upload to GitHub (10 minutes)

1. Go to https://github.com and create a FREE account if you don't have one
2. Click "New repository"
   - Name: `job-hunter`
   - Visibility: **Public** (required for unlimited free GitHub Actions minutes)
   - Click "Create repository"

3. Upload all the files from this `job_hunter` folder to the repo:
   - Click "uploading an existing file"
   - Drag and drop ALL files (including the .github folder)
   - Click "Commit changes"

   OR if you have Git installed, from this folder run:
   ```
   git init
   git add .
   git commit -m "Initial setup"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/job-hunter.git
   git push -u origin main
   ```

---

## Step 4 — Add your secrets to GitHub (3 minutes)

1. In your GitHub repo, go to **Settings → Secrets and variables → Actions**
2. Click "New repository secret" and add each of these:

   | Name             | Value                        |
   |------------------|------------------------------|
   | TELEGRAM_TOKEN   | your bot token from Step 1   |
   | TELEGRAM_CHAT_ID | your chat ID from Step 1     |
   | CLAUDE_API_KEY   | your Claude key from Step 2  |

---

## Step 5 — Enable GitHub Actions

1. In your repo, click the **Actions** tab
2. Click "I understand my workflows, go ahead and enable them"
3. Click on "Job Monitor" → "Run workflow" → "Run workflow" to test it NOW

If everything is set up correctly, you'll get a Telegram message within 1-2 minutes.

---

## That's it! The bot now runs every 30 minutes forever.

You will receive:
- A Telegram alert for every new job posting matching your profile
- A walk-in alert (separate icon) for Hyderabad walk-ins
- A tailored PDF resume for each role, ready to attach and apply

---

## Customise your search (optional)

Edit `config.py` to change:
- `KEYWORDS` — add or remove job titles to search for
- `REGULAR_LOCATIONS` — add more cities
- `WALKIN_LOCATIONS` — cities to search for walk-ins
- `MIN_EXP / MAX_EXP` — experience filter

Commit and push the change — the next run will pick it up automatically.

---

## View your application log

`application_log.csv` in the repo tracks every job that was found.
Download it anytime to see what's been detected.

---

## Troubleshooting

- **No Telegram messages**: Check that you started a chat with your bot (Step 1.7)
- **Actions not running**: Check the Actions tab in GitHub for error logs
- **Resume not attaching**: Your CLAUDE_API_KEY may be missing or invalid
