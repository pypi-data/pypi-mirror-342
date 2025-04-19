import requests

def get_weather(city: str, api_key: str):

    url = f"http://api.openweathermap.org/data/2.5/weather"
    params = {"q": city, "appid": api_key, "units": "metric", "lang": "ru"}

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        return {
            "city": data["name"],
            "temperature": data["main"]["temp"],
            "description": data["weather"][0]["description"]
        }
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}