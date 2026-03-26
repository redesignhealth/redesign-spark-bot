import sqlite3
import json
import os
from datetime import datetime

DB_PATH = os.getenv("DB_PATH", "spark_feedback.db")


def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS feedback (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                week INTEGER NOT NULL,
                spark_name TEXT NOT NULL,
                evaluator_key TEXT NOT NULL,
                evaluator_name TEXT NOT NULL,
                section TEXT NOT NULL,
                scores TEXT NOT NULL,
                comments TEXT NOT NULL,
                overall_score INTEGER,
                overall_comment TEXT,
                submitted_at TEXT NOT NULL
            )
        """)
        conn.execute("""
            CREATE UNIQUE INDEX IF NOT EXISTS idx_feedback_unique
            ON feedback(week, spark_name, evaluator_key)
        """)
    print("Database initialised.")


def save_feedback(week, spark_name, evaluator_key, evaluator_name, section,
                  scores, comments, overall_score=None, overall_comment=None):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            INSERT OR REPLACE INTO feedback
              (week, spark_name, evaluator_key, evaluator_name, section,
               scores, comments, overall_score, overall_comment, submitted_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            week, spark_name, evaluator_key, evaluator_name, section,
            json.dumps(scores), json.dumps(comments),
            overall_score, overall_comment,
            datetime.utcnow().isoformat(),
        ))


def get_feedback(week, spark_name=None, section=None):
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        query = "SELECT * FROM feedback WHERE week = ?"
        params = [week]
        if spark_name:
            query += " AND spark_name = ?"
            params.append(spark_name)
        if section:
            query += " AND section = ?"
            params.append(section)
        return [dict(r) for r in conn.execute(query, params).fetchall()]


def has_submitted(week, spark_name, evaluator_key):
    with sqlite3.connect(DB_PATH) as conn:
        row = conn.execute(
            "SELECT id FROM feedback WHERE week=? AND spark_name=? AND evaluator_key=?",
            (week, spark_name, evaluator_key),
        ).fetchone()
        return row is not None
