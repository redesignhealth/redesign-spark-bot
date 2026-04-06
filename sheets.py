"""
Google Sheets integration.

Auth: place a service-account credentials.json in the project root, OR set
GOOGLE_CREDENTIALS_JSON env var to the JSON string of the credentials.
Then share the spreadsheet with the service-account email (Editor access).
"""
import logging
import os

import gspread

logger = logging.getLogger(__name__)
from google.oauth2.service_account import Credentials

from config import RUBRIC, SECTION_LABELS

SCOPES = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive",
]
SHEET_ID = os.getenv("GOOGLE_SHEET_ID", "10wE47RRFzQskufiCOLrUxKVcQtWhORkiN9XpRcjyJSg")


def _get_client():
    client_email = os.getenv("GOOGLE_CLIENT_EMAIL")
    private_key = os.getenv("GOOGLE_PRIVATE_KEY")
    if client_email and private_key:
        info = {
            "type": "service_account",
            "client_email": client_email,
            "private_key": private_key.replace("\\n", "\n"),
            "private_key_id": os.getenv("GOOGLE_PRIVATE_KEY_ID", ""),
            "project_id": os.getenv("GOOGLE_PROJECT_ID", ""),
            "token_uri": "https://oauth2.googleapis.com/token",
        }
        creds = Credentials.from_service_account_info(info, scopes=SCOPES)
    else:
        creds = Credentials.from_service_account_file("credentials.json", scopes=SCOPES)
    return gspread.authorize(creds)


def _get_or_create_sheet(spreadsheet, week):
    name = f"Week {week} Feedback"
    try:
        return spreadsheet.worksheet(name)
    except gspread.WorksheetNotFound:
        sheet = spreadsheet.add_worksheet(title=name, rows=20, cols=50)
        sheet.update_cell(1, 1, "Spark")
        return sheet


def write_feedback_to_sheet(week, spark_name, evaluator_name, section,
                             comments, overall_score=None):
    try:
        client = _get_client()
        spreadsheet = client.open_by_key(SHEET_ID)
        sheet = _get_or_create_sheet(spreadsheet, week)

        # Row: find existing or append
        spark_col = sheet.col_values(1)
        if spark_name in spark_col:
            row_idx = spark_col.index(spark_name) + 1
        else:
            row_idx = len(spark_col) + 1
            sheet.update_cell(row_idx, 1, spark_name)

        # Column: find existing or append
        header = sheet.row_values(1)
        col_key = f"{evaluator_name} — {SECTION_LABELS[section]}"
        if col_key in header:
            col_idx = header.index(col_key) + 1
        else:
            col_idx = len(header) + 1
            sheet.update_cell(1, col_idx, col_key)

        # Build cell content
        questions = RUBRIC[week][section]
        lines = []
        for i, q in enumerate(questions):
            comment = comments[i] if i < len(comments) else ""
            short_q = (q[:70] + "...") if len(q) > 70 else q
            lines.append(f"Q{i + 1}: {short_q}")
            if comment:
                lines.append(f"  → {comment}")

        if overall_score:
            lines.append(f"\nOverall Score: {overall_score}/10")

        sheet.update_cell(row_idx, col_idx, "\n".join(lines))
        logger.info("Sheet updated: Week %d | %s | %s", week, spark_name, evaluator_name)
    except Exception as e:
        logger.error("Error writing feedback to sheet: %s", e)
