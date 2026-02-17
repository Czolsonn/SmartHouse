import requests
import collections
from datetime import datetime
import time

_last_fetch_forecast = 0
_last_result_forecast = None

API_KEY = "b23482a61b0f00b677789afa837d3826"
CITY = "Swidnica"
URL_FORECAST = f"https://api.openweathermap.org/data/2.5/forecast?q={CITY}&appid={API_KEY}&units=metric&lang=pl"
URL_CURRENT = f"https://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric&lang=pl"

def read_data_from_server():
    global _last_fetch_forecast, _last_result_forecast
    now = time.time()
    if _last_result_forecast is not None and now - _last_fetch_forecast < 600:  # 600 sekund = 10 minut
        return _last_result_forecast

    collection = []
    try:
        res = requests.get(URL_CURRENT)
        res.raise_for_status()
        data = res.json()
        collection.append(data)
    except Exception as e:
        print("Błąd podczas pobierania danych z API:", e)
        if _last_result_forecast is not None:
            return _last_result_forecast
        return None
    
    try:
        res = requests.get(URL_FORECAST)
        res.raise_for_status()
        data = res.json()
        collection.append(data)
    except Exception as e:
        print("Błąd podczas pobierania danych z API:", e)
        if _last_result_forecast is not None:
            return _last_result_forecast
        return None
    
    _last_result_forecast = collection
    _last_fetch_forecast = now
    return collection



def get_5day_forecast(collection):
    
    data = collection[1]
    forecast = {}

    for entry in data["list"]:
        date = entry["dt_txt"].split(" ")[0]
        temp_max = entry["main"]["temp_max"]
        temp_min = entry["main"]["temp_min"]
        icon = entry["weather"][0]["icon"]
        if date not in forecast:
            forecast[date] = {"temp_max": [], "temp_min": [], "icons": []}
        forecast[date]["temp_max"].append(temp_max)
        forecast[date]["temp_min"].append(temp_min)
        forecast[date]["icons"].append(icon)

    dni_pl = {
        "Monday": "Poniedziałek",
        "Tuesday": "Wtorek",
        "Wednesday": "Środa",
        "Thursday": "Czwartek",
        "Friday": "Piątek",
        "Saturday": "Sobota",
        "Sunday": "Niedziela"
    }

    result = []
    days = list(forecast.keys())[:5]
    for day in days:
        icons = forecast[day]["icons"]
        max_temp = max(forecast[day]["temp_max"])
        min_temp = min(forecast[day]["temp_min"])
        icon_id = collections.Counter(icons).most_common(1)[0][0]
        day_name = dni_pl[datetime.strptime(day, "%Y-%m-%d").strftime("%A")]
        if not icon_id.endswith('d'):
            icon_id = icon_id[:-1] + 'd'
        result.append({
            "day": day_name,
            "max_temp": max_temp,
            "min_temp": min_temp,
            "icon_id": icon_id
        })
    return result

def get_hourly_forecast(collection):

    data = collection[1]
    hourly_forecast = []

    for entry in data["list"][:40]:  # Dane pogody co 3 godziny na 5 dni (łącznie 40 wpisów)
        time_str = entry["dt_txt"].split(" ")[1][:5]  # Pobierz tylko godzinę i minutę
        temp_max = entry["main"]["temp_max"]
        temp_min = entry["main"]["temp_min"]
        icon = entry["weather"][0]["icon"]
        hourly_forecast.append({
            "time": time_str,
            "temp_max": temp_max,
            "temp_min": temp_min,
            "icon_id": icon
        })

    return hourly_forecast

def get_current_weather(collection):

    data = collection[0]
    weather = []

    temp = data["main"]["temp"]
    feels_like = data["main"]["feels_like"]
    temp_min = data["main"]["temp_min"]
    temp_max = data["main"]["temp_max"]
    humidity = data["main"]["humidity"]
    pressure = data["main"]["pressure"]
    icon = data["weather"][0]["icon"]
    description = data["weather"][0]["description"]
    wind_speed = data["wind"]["speed"]
    sunrise = data["sys"]["sunrise"]
    sunset = data["sys"]["sunset"]

    weather.append({
        "temp": temp,
        "feels_like": feels_like,
        "temp_min": temp_min,
        "temp_max": temp_max,
        "humidity": humidity,
        "pressure": pressure,
        "icon": icon,
        "description": description,
        "wind_speed": wind_speed,
        "sunrise": sunrise,
        "sunset": sunset
    })

    return weather

def get_current_date():
    now = datetime.now()
    dni_pl = {
        "Monday": "Poniedziałek",
        "Tuesday": "Wtorek",
        "Wednesday": "Środa",
        "Thursday": "Czwartek",
        "Friday": "Piątek",
        "Saturday": "Sobota",
        "Sunday": "Niedziela"
    }
    month_name_pl = {
        "01": "Stycznia",
        "02": "Lutego",
        "03": "Marca",
        "04": "Kwietnia",
        "05": "Maja",
        "06": "Czerwca",
        "07": "Lipca",
        "08": "Sierpnia",
        "09": "Września",
        "10": "Października",
        "11": "Listopada",
        "12": "Grudnia"
    }
    day_name_pl = dni_pl[now.strftime("%A")]
    month_name = month_name_pl[now.strftime("%m")]
    day_number = now.strftime("%d")
    month_number = now.strftime("%m")
    year_number = now.strftime("%Y")
    date = {
        "day_name": day_name_pl,
        "month_name": month_name,
        "day_number": day_number,
        "month_number": month_number,
        "year_number": year_number
    }
    return date

def unix_to_time(unix_timestamp):
    return datetime.fromtimestamp(unix_timestamp).strftime('%H:%M')