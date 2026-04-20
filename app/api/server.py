from fastapi import FastAPI
from app.ingestion.abuseipdb import fetch_ip_report
from app.detection.rules import is_malicious
from app.utils.db import get_events

app = FastAPI()

@app.get("/")
def root():
    return {"status": "Cyber Engine Running"}

@app.get("/check-ip")
def check_ip(ip: str):
    data = fetch_ip_report(ip)
    score = data["data"]["abuseConfidenceScore"]

    return {
        "ip": ip,
        "score": score,
        "malicious": score > 70
    }
@app.get("/events")
def fetch_events():
    return get_events()