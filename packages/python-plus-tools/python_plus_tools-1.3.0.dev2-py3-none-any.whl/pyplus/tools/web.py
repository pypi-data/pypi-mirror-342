raise ModuleNotFoundError('This moudle is not completed.')

def get_country(ip=requests.get("https://ipinfo.io/json").json().get("ip", "8.8.8.8")):
    import requests

    url = f"https://ipapi.co/{ip}/json/"
    response = requests.get(url).json()
    return response.get("country_name", "Unknown")

def bind_web(web_path):
    pass