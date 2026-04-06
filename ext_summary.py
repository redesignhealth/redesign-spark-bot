"""
Feature 3: Read each ext-spark-* channel, summarize with Claude API,
and post the summary to the corresponding Spark thread in #proj-redesign-spark.
Runs every Monday and Friday.
"""
import json
import logging
import os
import time
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

import anthropic

from config import EVALUATORS
from slack_client import get_channel_history, get_thread_replies, post_message

THREADS_FILE = os.path.join(os.path.dirname(__file__), "spark_threads.json")
SUMMARY_CHANNEL = os.environ.get("SUMMARY_CHANNEL_ID", "C0A3P3Z55GQ")

# CV mentors (user IDs) — used to detect if they've already posted this week
CV_MENTOR_IDS = {
    ev["slack_user_id"]
    for ev in EVALUATORS.values()
    if ev["section"] == "concept_vision"
}

SPARKBOT_USER_ID = "U0AP3776CM6"


def _get_ext_messages(channel_id, days_back=7):
    """Fetch messages from the ext channel from the last N days."""
    oldest = str((datetime.utcnow() - timedelta(days=days_back)).timestamp())
    messages = get_channel_history(channel_id, oldest=oldest, limit=100)
    # Filter out join/leave events
    return [m for m in messages if m.get("type") == "message" and "subtype" not in m]


def _format_messages_for_claude(messages, spark_name):
    """Format Slack messages into a readable transcript for Claude."""
    lines = []
    for m in reversed(messages):  # oldest first
        ts = datetime.utcfromtimestamp(float(m["ts"])).strftime("%b %d")
        user = m.get("user", "Unknown")
        text = m.get("text", "").strip()
        if text:
            lines.append(f"[{ts}] {user}: {text}")
    return "\n".join(lines)


def _summarize_with_claude(transcript, spark_name):
    """Use Claude API to generate a summary of the ext channel."""
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

    prompt = f"""You are summarizing activity in a mentorship channel for a startup founder named {spark_name} who is in a 4-week accelerator program.

Here are the recent messages from their channel:

{transcript}

Write a concise SparkBot update (3-5 bullet points max) covering:
- What concept/idea they're working on
- What research or calls happened this week
- Key decisions or pivots
- Any blockers or asks from mentors
- Tone/vibe (1 sentence on their energy and momentum)

Format as plain text with bullet points using •. Be factual and specific. No intro/outro fluff. Bold key phrases using *bold*."""

    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=400,
        messages=[{"role": "user", "content": prompt}]
    )
    return message.content[0].text.strip()


def _cv_mentors_for_spark(spark_name):
    """Return list of (slack_user_id,) for CV mentors assigned to this Spark."""
    return [
        ev["slack_user_id"]
        for ev in EVALUATORS.values()
        if ev["section"] == "concept_vision" and spark_name in ev["assigned_sparks"]
        and not ev["slack_user_id"].startswith("PLACEHOLDER")
    ]


def _has_cv_feedback_this_week(thread_replies):
    """Check if any CV mentor has posted in the thread (not SparkBot)."""
    for msg in thread_replies:
        uid = msg.get("user", "")
        if uid in CV_MENTOR_IDS and uid != SPARKBOT_USER_ID:
            return True
    return False


def post_ext_summary_to_thread(spark_name, info):
    """Read ext channel, summarize, post to Spark's thread."""
    ext_channel = info.get("ext_channel")
    if not ext_channel:
        logger.warning("No ext channel configured for %s, skipping", spark_name)
        return

    logger.info("Processing ext summary for %s...", spark_name)
    messages = _get_ext_messages(ext_channel, days_back=7)

    if not messages:
        logger.info("No recent messages in ext channel for %s, skipping", spark_name)
        return

    transcript = _format_messages_for_claude(messages, spark_name)
    summary = _summarize_with_claude(transcript, spark_name)

    # Check if CV mentors have posted feedback
    thread_replies = get_thread_replies(info["channel"], info["ts"])
    cv_mentors = _cv_mentors_for_spark(spark_name)
    missing = [uid for uid in cv_mentors if not any(
        m.get("user") == uid for m in thread_replies
    )]

    text = f":sparkles: *SparkBot update — week of {datetime.utcnow().strftime('%B %d')}*\n\n"
    text += f"Here's what's been happening in {spark_name.split()[0]}'s channel this week:\n\n"
    text += summary

    if missing:
        tags = " ".join(f"<@{uid}>" for uid in missing)
        text += f"\n\n:bell: {tags} — no notes from this week yet in this thread. Drop a few bullets when you get a chance! :sparkles:"

    post_message(info["channel"], text, thread_ts=info["ts"])
    logger.info("Posted ext summary for %s", spark_name)
    time.sleep(1)  # rate limit


def run_ext_summaries():
    """Post ext channel summaries for all 8 Sparks."""
    with open(THREADS_FILE) as f:
        threads = json.load(f)

    for spark_name, info in threads.items():
        try:
            post_ext_summary_to_thread(spark_name, info)
        except Exception as e:
            logger.error("Error processing ext summary for %s: %s", spark_name, e)
