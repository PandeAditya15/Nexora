from datetime import datetime

def create_event(ip_data, geo_data):
    try:
        ip = ip_data["data"]["ipAddress"]
        score = ip_data["data"]["abuseConfidenceScore"]

        if geo_data and "loc" in geo_data:
            lat, lng = geo_data["loc"].split(",")
            country = geo_data.get("country")
        else:
            lat, lng, country = None, None, None

        event = {
            "type": "ip",
            "value": ip,
            "risk_score": score,
            "country": country,
            "lat": float(lat) if lat else None,
            "lng": float(lng) if lng else None,
            "timestamp": datetime.utcnow().isoformat()
        }

        return event

    except Exception as e:
        print(f"Error creating event: {e}")
        return None