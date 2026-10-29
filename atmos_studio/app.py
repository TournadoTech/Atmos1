from flask import Flask, render_template, request
import requests
from datetime import datetime

app = Flask(__name__)
API = "https://api.open-meteo.com/v1/forecast"
GEO = "https://geocoding-api.open-meteo.com/v1/search"

def weather_label(code):
    if code == 0: return "Ciel dégagé"
    if code in (1, 2): return "Peu nuageux"
    if code == 3: return "Couvert"
    if code in (45, 48): return "Brouillard"
    if code in (51, 53, 55, 56, 57): return "Bruine"
    if code in (61, 63, 65, 66, 67, 80, 81, 82): return "Pluie"
    if code in (71, 73, 75, 77, 85, 86): return "Neige"
    if code in (95, 96, 99): return "Orage"
    return "Conditions variables"

def weather_icon(code):
    if code == 0: return "☀️"
    if code in (1, 2): return "🌤️"
    if code == 3: return "☁️"
    if code in (45, 48): return "🌫️"
    if code in (51, 53, 55, 56, 57, 61, 63, 65, 66, 67, 80, 81, 82): return "🌧️"
    if code in (71, 73, 75, 77, 85, 86): return "❄️"
    if code in (95, 96, 99): return "⛈️"
    return "🌥️"

def get_forecast(latitude, longitude):
    response = requests.get(API, params={
        "latitude": latitude, "longitude": longitude,
        "current": "temperature_2m,relative_humidity_2m,apparent_temperature,wind_speed_10m,weather_code,is_day",
        "hourly": "temperature_2m,apparent_temperature,precipitation_probability,relative_humidity_2m,wind_speed_10m,weather_code",
        "daily": "weather_code,temperature_2m_max,temperature_2m_min,precipitation_probability_max,sunrise,sunset,uv_index_max",
        "timezone": "auto", "forecast_days": 7
    }, timeout=15)
    response.raise_for_status()
    return response.json()

def get_city(city):
    r = requests.get(GEO, params={"name": city, "count": 8, "language": "fr", "format": "json"}, timeout=12)
    r.raise_for_status()
    results = r.json().get("results", [])
    if not results: return None
    # Prefer exact-ish match, otherwise first result
    place = next((p for p in results if p["name"].lower() == city.lower()), results[0])
    data = get_forecast(place["latitude"], place["longitude"])
    c = data["current"]
    return {
        "city": place["name"], "country": place.get("country", ""),
        "admin": place.get("admin1", ""), "latitude": place["latitude"], "longitude": place["longitude"],
        "temperature": round(c["temperature_2m"]), "feels_like": round(c["apparent_temperature"]),
        "humidity": c["relative_humidity_2m"], "wind": round(c["wind_speed_10m"]),
        "code": c["weather_code"], "label": weather_label(c["weather_code"]), "icon": weather_icon(c["weather_code"]),
        "time": c["time"], "is_day": c.get("is_day", 1), "hourly": data["hourly"], "daily": data["daily"]
    }

FRANCE_CITIES = [
    ("Brest",48.3904,-4.4861), ("Rennes",48.1173,-1.6778), ("Lille",50.6292,3.0573),
    ("Paris",48.8566,2.3522), ("Strasbourg",48.5734,7.7521), ("Nantes",47.2184,-1.5536),
    ("Limoges",45.8336,1.2611), ("Lyon",45.7640,4.8357), ("Bordeaux",44.8378,-0.5792),
    ("Toulouse",43.6047,1.4442), ("Montpellier",43.6119,3.8772), ("Marseille",43.2965,5.3698),
    ("Nice",43.7102,7.2620), ("Ajaccio",41.9192,8.7386), ("Clermont-Ferrand",45.7772,3.0870)
]

def get_france_map():
    # Open-Meteo supports multiple coordinates in one request, avoiding 15 separate calls.
    params = {
        "latitude": ",".join(str(c[1]) for c in FRANCE_CITIES),
        "longitude": ",".join(str(c[2]) for c in FRANCE_CITIES),
        "current": "temperature_2m,weather_code",
        "timezone": "Europe/Paris"
    }
    try:
        r = requests.get(API, params=params, timeout=15)
        r.raise_for_status()
        result = r.json()
        if isinstance(result, dict): result = [result]
        points = []
        for city, lat, lon, data in zip(FRANCE_CITIES, [x[1] for x in FRANCE_CITIES], [x[2] for x in FRANCE_CITIES], result):
            cur = data.get("current", {})
            points.append({"name": city, "lat": lat, "lon": lon, "temp": round(cur.get("temperature_2m", 0)), "icon": weather_icon(cur.get("weather_code", -1))})
        return points
    except (requests.RequestException, ValueError, TypeError):
        return []

@app.route("/", methods=["GET", "POST"])
def home():
    city = request.form.get("city", "Paris").strip()[:100] if request.method == "POST" else request.args.get("city", "Paris").strip()[:100]
    weather, error = None, None
    try:
        weather = get_city(city or "Paris")
        if weather is None: error = "Ville introuvable. Essaie Paris, Tokyo, Montréal…"
    except requests.RequestException:
        error = "Les données météo sont temporairement indisponibles. Réessaie dans un instant."
    return render_template("index.html", city=city, weather=weather, error=error, map_points=get_france_map())

if __name__ == "__main__":
    app.run(debug=True)
