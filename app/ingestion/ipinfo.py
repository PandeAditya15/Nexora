import logging

import requests

logger = logging.getLogger(__name__)


def get_ip_info(ip):
    try:
        url = f"https://ipinfo.io/{ip}/json"
        response = requests.get(url, timeout=10)

        if response.status_code != 200:
            logger.warning("ipinfo lookup for %s failed: HTTP %s", ip, response.status_code)
            return None

        return response.json()

    except requests.RequestException:
        logger.exception("ipinfo request failed for %s", ip)
        return None