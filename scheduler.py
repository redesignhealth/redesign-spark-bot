"""
Scheduler:
  - Monday 9 AM ET (14:00 UTC)  → post ext channel summaries to all Spark threads
  - Thursday 4 PM ET (21:00 UTC) → post targeted reminders where feedback is missing
  - Friday 4 PM ET (21:00 UTC)  → post weekly status update to #proj-redesign-spark
"""
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger


def start_scheduler(post_reminder_fn, post_ext_summaries_fn, post_weekly_update_fn, get_week_fn):
    scheduler = BackgroundScheduler()

    # Monday 9 AM ET — ext channel summaries to each Spark thread
    scheduler.add_job(
        post_ext_summaries_fn,
        CronTrigger(day_of_week="mon", hour=14, minute=0, timezone="UTC"),
        id="monday_ext_summaries",
        replace_existing=True,
    )

    # Thursday 4 PM ET — reminder in threads where feedback is missing
    scheduler.add_job(
        post_reminder_fn,
        CronTrigger(day_of_week="thu", hour=21, minute=0, timezone="UTC"),
        id="weekly_thread_reminder",
        replace_existing=True,
    )

    # Friday 4 PM ET — weekly status update to main channel
    scheduler.add_job(
        lambda: post_weekly_update_fn(get_week_fn()),
        CronTrigger(day_of_week="fri", hour=21, minute=0, timezone="UTC"),
        id="friday_weekly_update",
        replace_existing=True,
    )

    scheduler.start()
    print("Scheduler started:")
    print("  Mon 9 AM ET  → ext channel summaries to Spark threads")
    print("  Thu 4 PM ET  → feedback reminders (missing only)")
    print("  Fri 4 PM ET  → weekly status update to #proj-redesign-spark")
    return scheduler
