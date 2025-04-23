import requests
from .errors import NotCompleted

def get_country(ip=requests.get("https://ipinfo.io/json").json().get("ip", "8.8.8.8")):
    import requests

    url = f"https://ipapi.co/{ip}/json/"
    response = requests.get(url).json()
    return response.get("country_name", "Unknown")

@NotCompleted("This function is not completed.")
def bind_web(web_path:str, port:int = 5000, ip:str = "127.0.0.1"):
    pass