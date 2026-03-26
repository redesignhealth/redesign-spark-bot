# SparkBot

Weekly Slack bot that collects structured feedback from 4 teams on Spark participants.

## Who gets notified about what

| Team | Section | People | Sparks |
|---|---|---|---|
| New Ventures | Concept Vision | Kienan, Neil, Neharika, Aron/Dan, Patrick, Jorge, Moz, Akash, Preston | Assigned per Spark only |
| Founder Strategy | Founder DNA | Tom, Sarah | All 8 Sparks |
| Tech | Tech / AI-Innateness | Dan, Prithvi | All 8 Sparks |
| Venture Traction | Commercial Acumen | Leland, Matt Ripkey | All 8 Sparks |

Feedback fires every **Friday at 5 PM ET** via DM. Each person only sees their own section and assigned Sparks.

---

## Setup

### 1. Install dependencies
```bash
cd redesign-spark-bot
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
```

### 2. Create Slack App

1. Go to https://api.slack.com/apps → **Create New App** → **From scratch**
2. Name it `SparkBot`, pick your Redesign Health workspace
3. Under **Socket Mode** → Enable Socket Mode → Generate an App-Level Token with `connections:write` scope → copy as `SLACK_APP_TOKEN`
4. Under **OAuth & Permissions** → add these Bot Token Scopes:
   - `chat:write`
   - `im:write`
   - `im:read`
   - `channels:read`
   - `commands`
5. Install to workspace → copy **Bot User OAuth Token** as `SLACK_BOT_TOKEN`
6. Under **Interactivity & Shortcuts** → Enable Interactivity (no URL needed in Socket Mode)
7. Under **Slash Commands** → create:
   - `/spark-send-feedback` — manually trigger feedback DMs
   - `/spark-status` — show submission status for current week

### 3. Add Slack User IDs to config.py

For each evaluator in `config.py`, replace `PLACEHOLDER_*` with their real Slack user ID.

To find a user's ID: click their Slack profile → `...` → **Copy member ID**

### 4. Set up Google Sheets access

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Create a project → enable **Google Sheets API** and **Google Drive API**
3. Create a **Service Account** → download JSON key as `credentials.json` in project root
4. Share the spreadsheet with the service account email (Editor access)

### 5. Configure environment

```bash
cp .env.example .env
# Fill in SLACK_BOT_TOKEN, SLACK_APP_TOKEN, SUMMARY_CHANNEL_ID
# Set CURRENT_WEEK=2 (or leave blank to auto-detect)
```

### 6. Run
```bash
python app.py
```

The bot starts in Socket Mode. **No notifications are sent on startup.**

---

## Triggering feedback manually

Once you're ready to send:
```
/spark-send-feedback        # sends for current week (auto-detected)
/spark-send-feedback 2      # sends for a specific week
```

Check submission status:
```
/spark-status
/spark-status 2
```

The Friday 5 PM ET scheduler runs automatically once the bot is live.

---

## Data storage

- **SQLite** (`spark_feedback.db`) — local, all submissions persisted
- **Google Sheets** — new tab per week (`Week 2 Feedback`, etc.), one row per Spark, one column per evaluator
- **Slack channel** — summary posted to `SUMMARY_CHANNEL_ID` once all 4 sections have at least one submission for a Spark
