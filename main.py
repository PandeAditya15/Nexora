from app.ingestion.abuseipdb import fetch_ip_report
from app.detection.rules import is_malicious
from app.alerts.cli_alert import alert
from app.ingestion.ipinfo import get_ip_info
from app.models.event import create_event
from app.utils.db import insert_event

def run_pipeline(ip: str):
    # 🔹 Step 1: Fetch data (Ingestion)
    ip_data = fetch_ip_report(ip)
    geo_data = get_ip_info(ip)

    if not ip_data or "data" not in ip_data:
        print("❌ Failed to fetch IP data")
        return

    # 🔹 Step 2: Detection
    score = ip_data["data"]["abuseConfidenceScore"]

    if is_malicious(ip_data):
        alert(ip, score)
    else:
        print("✅ Safe IP")

    # 🔹 Step 3: Event creation (Normalization)
    event = create_event(ip_data, geo_data)

    if event:
        print("\n📦 Event Created:")
        print(event)
    else:
        print("❌ Failed to create event")

    insert_event(event)


# 🔹 Entry point
if __name__ == "__main__":
    ip = "117.200.0.0"  # change this for testing
    run_pipeline(ip)