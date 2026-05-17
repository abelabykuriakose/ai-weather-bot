import requests
from langchain_core.tools import tool

@tool
def get_current_weather(location: str) -> str:
    """
    Fetches the current weather data for a given city location. 
    Use this tool whenever the user asks about live weather, rain, temperature, or if they need an umbrella.
    """
    print(f"📡 [Tool Activated] Searching coordinates and weather data for: {location}...")
    
    try:
        # Step 1: Convert City Name to Latitude/Longitude (Geocoding)
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={location}&count=1&language=en&format=json"
        geo_res = requests.get(geo_url).json()
        
        if not geo_res.get("results"):
            return f"Could not find coordinates for location: {location}"
            
        lat = geo_res["results"][0]["latitude"]
        lon = geo_res["results"][0]["longitude"]
        
        # Step 2: Fetch Live Weather Data from Open-Meteo
        weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
        weather_res = requests.get(weather_url).json()
        
        current = weather_res["current_weather"]
        temp = current["temperature"]
        wind = current["windspeed"]
        weather_code = current["weathercode"]
        
        # Open-Meteo weather codes: 51-67 are rain, 71-86 are snow, 95-99 are thunderstorms
        is_raining = weather_code in [51, 53, 55, 56, 57, 61, 63, 65, 66, 67, 80, 81, 82, 95, 96, 97, 99]
        rain_status = "raining or about to rain" if is_raining else "not raining"
        
        return f"The current temperature in {location} is {temp}°C, wind speed is {wind} km/h, and it is currently {rain_status}."
        
    except Exception as e:
        return f"Error retrieving weather data: {str(e)}"