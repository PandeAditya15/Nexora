import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")


def insert_event(event):
    import psycopg2
    from datetime import datetime

    try:
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()

        print("📦 INSERT DATA:", event)

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
            datetime.utcnow()
        ))

        conn.commit()
        print("✅ FULL INSERT SUCCESS")

        cursor.close()
        conn.close()

    except Exception as e:
        print("❌ DB INSERT FAILED:", e)
        
def get_events():
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()

        query = "SELECT lat, lng, risk_score FROM events;"
        cursor.execute(query)

        rows = cursor.fetchall()

        cursor.close()
        conn.close()

        events = []

        for row in rows:
            events.append({
                "lat": row[0],
                "lng": row[1],
                "risk_score": row[2]
            })

        return events

    except Exception as e:
        print(f"❌ DB Fetch Error: {e}")
        return []