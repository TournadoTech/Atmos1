from flask import Flask, render_template, request
import requests

app = Flask(__name__)

def get_weather(city):
    # Trouve les coordonnées de la ville
    geo_url = "https://geocoding-api.open-meteo.com/v1/search"
    geo_response = requests.get(
        geo_url,
        params={"name": city, "count": 1, "language": "fr", "format": "json"},
        timeout=10,
    )
    geo_response.raise_for_status()
    results = geo_response.json().get("results", [])

    if not results:
        return None

    place = results[0]

    # Récupère la météo actuelle
    weather_response = requests.get(
        "https://api.open-meteo.com/v1/forecast",
        params={
            "latitude": place["latitude"],
            "longitude": place["longitude"],
            "current": "temperature_2m,relative_humidity_2m,apparent_temperature,wind_speed_10m,weather_code",
            "timezone": "auto",
        },
        timeout=10,
    )
    weather_response.raise_for_status()
    current = weather_response.json()["current"]

    return {
        "city": place["name"],
        "country": place.get("country", ""),
        "temperature": current["temperature_2m"],
        "feels_like": current["apparent_temperature"],
        "humidity": current["relative_humidity_2m"],
        "wind": current["wind_speed_10m"],
        "code": current["weather_code"],
        "time": current["time"],
    }


@app.route("/", methods=["GET", "POST"])
def home():
    city = "Paris"
    weather = None
    error = None

    if request.method == "POST":
        city = request.form.get("city", "").strip()[:100]

    if city:
        try:
            weather = get_weather(city)
            if weather is None:
                error = "Ville introuvable. Essaie avec un autre nom."
        except requests.RequestException:
            error = "Impossible de récupérer la météo. Vérifie ta connexion puis réessaie."
    else:
        error = "Entre le nom d'une ville."

    return render_template("index.html", city=city, weather=weather, error=error)


if __name__ == "__main__":
    # debug=True pratique en local ; désactive-le pour un déploiement public.
    app.run(debug=True)
