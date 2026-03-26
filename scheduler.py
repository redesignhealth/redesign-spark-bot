"""
Scheduler:
  - Thursday 4 PM ET (21:00 UTC) → post targeted reminders in Spark threads where feedback is missing
"""
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger


def start_scheduler(post_reminder_fn):
    scheduler = BackgroundScheduler()

    scheduler.add_job(
        post_reminder_fn,
        CronTrigger(day_of_week="thu", hour=21, minute=0, timezone="UTC"),
        id="weekly_thread_reminder",
        replace_existing=True,
    )

    scheduler.start()
    print("Scheduler started — reminders: Thu 4 PM ET")
    return scheduler
