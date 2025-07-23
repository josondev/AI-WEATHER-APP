# import requests

# # Step 1: Get the coordinates of the location using Google Maps Geocoding API
# def get_coordinates(address, google_maps_token):
#     geocoding_url = "https://maps.googleapis.com/maps/api/geocode/json"
    
#     params = {
#         'address': address,
#         'key': google_maps_token  # Your Google Maps API key
#     }
    
#     response = requests.get(geocoding_url, params=params)
#     data = response.json()
    
#     if data['status'] == 'OK':
#         location = data['results'][0]['geometry']['location']
#         latitude = location['lat']
#         longitude = location['lng']
#         return latitude, longitude
#     else:
#         raise Exception(f"Geocoding error: {data['status']} - {data.get('error_message', '')}")

# # Step 2: Get the weather data using OpenWeatherMap API
# def get_weather(latitude, longitude, openweather_api_key):
#     weather_url = "https://api.openweathermap.org/data/2.5/weather"
    
#     params = {
#         'lat': latitude,
#         'lon': longitude,
#         'appid': openweather_api_key,  # Your OpenWeatherMap API key
#         'units': 'metric'  # Celsius
#     }
    
#     response = requests.get(weather_url, params=params)
#     data = response.json()
    
#     if response.status_code == 200:
#         weather_description = data['weather'][0]['description']
#         temperature = data['main']['temp']
#         feels_like = data['main']['feels_like']
#         humidity = data['main']['humidity']
#         wind_speed = data['wind']['speed']
        
#         weather_info = (f"Weather at coordinates ({latitude}, {longitude}):\n"
#                         f"Description: {weather_description.capitalize()}\n"
#                         f"Temperature: {temperature}°C\n"
#                         f"Feels like: {feels_like}°C\n"
#                         f"Humidity: {humidity}%\n"
#                         f"Wind speed: {wind_speed} m/s")
#         return weather_info
#     else:
#         raise Exception(f"Weather API error: {data['message']}")

# # Main function
# if _name_ == "_main_":
#     try:
#         google_maps_token = "AIzaSyBlJfGgpP2kN06cTUkpcY1VZLsflD2_ux0"  # Replace with your actual Google Maps API key
#         openweather_api_key = "dff8a714e30a29e438b4bd2ebb11190f"  # Replace with your actual OpenWeatherMap API key
        
#         # User input for address
#         address = input("Enter the address or location name: ")
        
#         # Step 1: Get coordinates for the location
#         latitude, longitude = get_coordinates(address, google_maps_token)
#         print(f"Coordinates for '{address}': Latitude {latitude}, Longitude {longitude}")
        
#         # Step 2: Get the weather data using the coordinates
#         weather_info = get_weather(latitude, longitude, openweather_api_key)
#         print(weather_info)
        
#     except Exception as e:
#         print("Error:", str(e))


import requests,os
from dotenv import load_dotenv
load_dotenv()

# Step 1: Get the coordinates of the location using Google Maps Geocoding API
def get_coordinates(address, google_maps_token):
    geocoding_url = "https://maps.googleapis.com/maps/api/geocode/json"
    
    params = {
        'address': address,
        'key': google_maps_token  # Your Google Maps API key
    }
    
    response = requests.get(geocoding_url, params=params)
    data = response.json()
    
    if data['status'] == 'OK':
        location = data['results'][0]['geometry']['location']
        latitude = location['lat']
        longitude = location['lng']
        return latitude, longitude
    else:
        raise Exception(f"Geocoding error: {data['status']} - {data.get('error_message', '')}")

# Step 2: Get the weather data using OpenWeatherMap API
def get_weather(latitude, longitude, openweather_api_key):
    weather_url = "https://api.openweathermap.org/data/2.5/weather"
    
    params = {
        'lat': latitude,
        'lon': longitude,
        'appid': openweather_api_key,  # Your OpenWeatherMap API key
        'units': 'metric'  # Celsius
    }
    
    response = requests.get(weather_url, params=params)
    data = response.json()
    
    if response.status_code == 200:
        weather_description = data['weather'][0]['description']
        temperature = data['main']['temp']
        feels_like = data['main']['feels_like']
        humidity = data['main']['humidity']
        wind_speed = data['wind']['speed']
        
        weather_info = (f"Weather at coordinates ({latitude}, {longitude}):\n"
                        f"Description: {weather_description.capitalize()}\n"
                        f"Temperature: {temperature}°C\n"
                        f"Feels like: {feels_like}°C\n"
                        f"Humidity: {humidity}%\n"
                        f"Wind speed: {wind_speed} m/s")
        return weather_info
    else:
        raise Exception(f"Weather API error: {data['message']}")

# Step 3: Get the soil moisture data using Open-Meteo API
def get_soil_moisture(latitude, longitude):
    soil_moisture_url = "https://api.open-meteo.com/v1/forecast"
    
    params = {
        'latitude': latitude,
        'longitude': longitude,
        'hourly': 'soil_moisture_0_1cm',  # Get soil moisture at 0-1cm depth
        'start': '2024-10-19T00:00',  # Use current date
        'end': '2024-10-19T23:00',    # Same day for simplicity
        'timezone': 'auto'
    }
    
    response = requests.get(soil_moisture_url, params=params)
    data = response.json()

    if 'hourly' in data and 'soil_moisture_0_1cm' in data['hourly']:
        # Extract soil moisture data
        soil_moisture = data['hourly']['soil_moisture_0_1cm'][0]  # Get the first available value
        return f"Soil Moisture at coordinates ({latitude}, {longitude}): {soil_moisture} m³/m³"
    else:
        return "No soil moisture data available for the specified location."

# Main function
if __name__ == "__main__":
    try:
        # Replace with your actual API keys
        google_maps_token = os.getenv("google_maps_token")
        openweather_api_key = os.getenv("openweather_api_key")
        
        # User input for address
        address = input("Enter the address or location name: ")
        
        # Step 1: Get coordinates for the location
        latitude, longitude = get_coordinates(address, google_maps_token)
        print(f"Coordinates for '{address}': Latitude {latitude}, Longitude {longitude}")
        
        # Step 2: Get the weather data using the coordinates
        weather_info = get_weather(latitude, longitude, openweather_api_key)
        print(weather_info)
        
        # Step 3: Get the soil moisture data using the coordinates
        soil_moisture_info = get_soil_moisture(latitude, longitude)
        print(soil_moisture_info)
        
    except Exception as e:
        print("Error:", str(e))
