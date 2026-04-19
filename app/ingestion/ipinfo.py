import requests

def get_ip_info(ip):
    try:
        url = f"https://ipinfo.io/{ip}/json"
        response = requests.get(url)

        if response.status_code != 200:
            print("Error fetching IP info")
            return None

        return response.json()

    except Exception as e:
        print(f"Error: {e}")
        return None