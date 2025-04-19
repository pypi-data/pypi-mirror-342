import requests


def get_time_by_ip():
    url = "http://ip-api.com/json"
    response = requests.get(url)
    data = response.json()
    if data["status"] == "success":
        return {
            "city": data["city"],
            "timezone": data["timezone"],
            "current_time": data["query"]  # IP-адрес
        }
