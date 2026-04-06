"""Thin wrapper around Slack API calls using the bot token."""
import json
import logging
import os
import urllib.parse
import urllib.request

logger = logging.getLogger(__name__)

SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]


def _call(method, **params):
    url = f"https://slack.com/api/{method}"
    data = json.dumps(params).encode("utf-8")
    req = urllib.request.Request(
        url, data=data,
        headers={
            "Authorization": f"Bearer {SLACK_BOT_TOKEN}",
            "Content-Type": "application/json; charset=utf-8",
        }
    )
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read())


def _get(method, **params):
    url = f"https://slack.com/api/{method}?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(
        url,
        headers={"Authorization": f"Bearer {SLACK_BOT_TOKEN}"}
    )
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read())


def get_thread_replies(channel, thread_ts):
    """Return all messages in a thread (excluding parent)."""
    result = _get("conversations.replies", channel=channel, ts=thread_ts, limit=200)
    if not result.get("ok"):
        logger.error("Error reading thread %s: %s", thread_ts, result.get("error"))
        return []
    return result.get("messages", [])[1:]  # skip parent


def get_channel_history(channel, oldest=None, limit=100):
    """Return recent messages from a channel."""
    params = dict(channel=channel, limit=limit)
    if oldest:
        params["oldest"] = oldest
    result = _get("conversations.history", **params)
    if not result.get("ok"):
        logger.error("Error reading channel %s: %s", channel, result.get("error"))
        return []
    return result.get("messages", [])


def post_message(channel, text, thread_ts=None):
    """Post a message as SparkBot."""
    params = dict(channel=channel, text=text)
    if thread_ts:
        params["thread_ts"] = thread_ts
    result = _call("chat.postMessage", **params)
    if not result.get("ok"):
        logger.error("Error posting message to %s: %s", channel, result.get("error"))
    return result


def get_user_info(user_id):
    result = _get("users.info", user=user_id)
    return result.get("user", {})
