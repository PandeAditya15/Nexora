import logging
import os
from contextlib import contextmanager
from datetime import datetime, timezone

import psycopg2
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

logger = logging.getLogger(__name__)


@contextmanager
def _db_cursor():
    conn = psycopg2.connect(DATABASE_URL)
    try:
        cursor = conn.cursor()
        try:
            yield cursor
            conn.commit()
        finally:
            cursor.close()
    finally:
        conn.close()


def insert_event(event) -> bool:
    """Insert an event row. Returns True on success, False on failure."""
    try:
        with _db_cursor() as cursor:
            cursor.execute("""
                INSERT INTO events (type, value, risk_score, country, lat, lng, timestamp)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                event.get("type"),
                event.get("value"),
                event.get("risk_score"),
                event.get("country"),
                event.get("lat"),
                event.get("lng"),
                datetime.now(timezone.utc)
            ))
        logger.info("Stored event for %s", event.get("value"))
        return True
    except Exception:
        logger.exception("DB insert failed for event: %s", event)
        return False


def get_events():
    try:
        with _db_cursor() as cursor:
            cursor.execute("SELECT lat, lng, risk_score FROM events;")
            rows = cursor.fetchall()

        return [
            {"lat": row[0], "lng": row[1], "risk_score": row[2]}
            for row in rows
        ]
    except Exception:
        logger.exception("DB fetch failed")
        return []