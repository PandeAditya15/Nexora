import logging

from fastapi import FastAPI
from app.ingestion.abuseipdb import fetch_ip_report
from app.utils.db import get_events

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()


# ✅ ROOT
@app.get("/")
def root():
    return {"status": "Cyber Engine Running"}


# ✅ BASIC CHECK
@app.get("/check-ip")
def check_ip(ip: str):
    data = fetch_ip_report(ip)
    if not data or "data" not in data:
        return {"ip": ip, "error": "AbuseIPDB lookup failed"}

    score = data["data"]["abuseConfidenceScore"]

    return {
        "ip": ip,
        "score": score,
        "malicious": score > 70
    }


# =========================================================
# 🔥 CLEAN EVENTS (STATIC + DB COMBINED)
# =========================================================
@app.get("/events")
def fetch_events():
    try:
        db_events = get_events()
    except Exception:
        logger.exception("Failed to load live events")
        db_events = []

    # 🔥 STATIC INTEL NODES (clean + meaningful)
    static_nodes = [
        # 🇺🇸 USA
        {"lat": 37.422, "lng": -122.084, "risk_score": 10, "value": "Google HQ", "country": "US"},
        {"lat": 38.9072, "lng": -77.0369, "risk_score": 30, "value": "AWS US-East", "country": "US"},

        # 🇪🇺 Europe
        {"lat": 53.3498, "lng": -6.2603, "risk_score": 20, "value": "Google Europe", "country": "IE"},
        {"lat": 52.3676, "lng": 4.9041, "risk_score": 40, "value": "AMS-IX", "country": "NL"},
        {"lat": 52.5200, "lng": 13.4050, "risk_score": 85, "value": "TOR Node", "country": "DE"},

        # 🌏 Asia
        {"lat": 1.3521, "lng": 103.8198, "risk_score": 25, "value": "Google Asia", "country": "SG"},
        {"lat": 35.6762, "lng": 139.6503, "risk_score": 28, "value": "Tokyo Cloud", "country": "JP"},
        {"lat": 19.0760, "lng": 72.8777, "risk_score": 35, "value": "Mumbai Infra", "country": "IN"},

        # 🇦🇺 Australia
        {"lat": -33.8688, "lng": 151.2093, "risk_score": 32, "value": "Sydney AWS", "country": "AU"},
        {"lat": -37.8136, "lng": 144.9631, "risk_score": 27, "value": "Melbourne Cloud", "country": "AU"},

        # 🇳🇿 New Zealand
        {"lat": -36.8485, "lng": 174.7633, "risk_score": 22, "value": "Auckland IX", "country": "NZ"},
    ]

    # Tag each node's origin so the frontend can distinguish real threat
    # intel from the static reference nodes.
    static_tagged = [{**n, "source": "demo"} for n in static_nodes]
    live_tagged = [{**e, "source": "live"} for e in db_events[-20:]]

    return static_tagged + live_tagged


# =========================================================
# 🔥 ANALYZE + STORE + RETURN (UNCHANGED)
# =========================================================
@app.get("/analyze-ip")
def analyze_ip(ip: str):
    from app.ingestion.ipinfo import get_ip_info
    from app.utils.db import insert_event
    import ipaddress

    try:
        ip_obj = ipaddress.ip_address(ip)
        if ip_obj.is_private:
            return {
                "error": "Private IP not allowed",
                "ip": ip
            }

        data = fetch_ip_report(ip)
        if not data or "data" not in data:
            return {"error": "AbuseIPDB lookup failed", "ip": ip}

        score = data["data"]["abuseConfidenceScore"]

        geo = get_ip_info(ip)

        lat, lng = None, None
        country = None

        if geo:
            country = geo.get("country")

            if geo.get("loc"):
                try:
                    lat, lng = map(float, geo["loc"].split(","))
                except:
                    lat, lng = None, None

        if lat is None or lng is None:
            return {
                "ip": ip,
                "country": country,
                "risk_score": score,
                "error": "No geo coordinates"
            }

        event = {
            "type": "ip",
            "value": ip,
            "risk_score": int(score),
            "country": country,
            "lat": float(lat),
            "lng": float(lng)
        }

        event["stored"] = insert_event(event)

        return event

    except Exception as e:
        logger.exception("analyze_ip failed for %s", ip)
        return {
            "error": str(e),
            "ip": ip
        }