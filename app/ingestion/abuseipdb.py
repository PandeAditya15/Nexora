import logging
import os

import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("ABUSEIPDB_API_KEY")

logger = logging.getLogger(__name__)


def fetch_ip_report(ip):
    """Returns the AbuseIPDB report dict, or None on failure."""
    url = "https://api.abuseipdb.com/api/v2/check"

    headers = {
        "Key": API_KEY,
        "Accept": "application/json"
    }

    params = {
        "ipAddress": ip,
        "maxAgeInDays": 90
    }

    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException:
        logger.exception("AbuseIPDB request failed for %s", ip)
        return None