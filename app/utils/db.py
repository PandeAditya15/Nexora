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