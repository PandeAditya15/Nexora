import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")


def insert_event(event):
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()

        query = """
        INSERT INTO events (type, value, risk_score, country, lat, lng, timestamp)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """

        cursor.execute(query, (
            event["type"],
            event["value"],
            event["risk_score"],
            event["country"],
            event["lat"],
            event["lng"],
            event["timestamp"]
        ))

        conn.commit()
        cursor.close()
        conn.close()

        print("✅ Event stored in database")

    except Exception as e:
        print(f"❌ DB Error: {e}")
        
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