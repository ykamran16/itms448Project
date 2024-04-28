import tkinter as tk
from tkinter import messagebox
import requests
from datetime import datetime
import pytz

#OpenWeather API Key
WEATHER_API_KEY = "4280cf0c7e000e8ae9a42913aa06e1c5"

#WAQI API Key
AIR_QUALITY_API_KEY = "1119033840c1a73ffcbba1b0557507f7a961d60f"

#News API Key
NEWS_API_KEY = "bee063b26e764f1fa847e481e8cbf78f"

# Sunrise-Sunset API Base URL
SUNRISE_SUNSET_BASE_URL = "https://api.sunrise-sunset.org/json?"


#Fetch weather data
def get_weather(city):
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = f"{base_url}q={city}&appid={WEATHER_API_KEY}&units=metric"
    response = requests.get(complete_url)

    if response.status_code == 200:
        data = response.json()
        main = data['main']
        coord = data['coord']
        temperature = main['temp']
        pressure = main['pressure']
        humidity = main['humidity']
        weather_desc = data['weather'][0]['description']

        latitude = coord['lat']
        longitude = coord['lon']

        return {
            'Temperature': temperature,
            'Pressure': pressure,
            'Humidity': humidity,
            'Weather Description': weather_desc,
            'Latitude': latitude,
            'Longitude': longitude,
        }

    else:
        return None


# Fetch air quality data
def get_air_quality(city):
    base_url = "https://api.waqi.info/feed/"
    complete_url = f"{base_url}{city}/?token={AIR_QUALITY_API_KEY}"
    response = requests.get(complete_url)

    if response.status_code == 200:
        data = response.json()
        aqi = data['data']['aqi']

        return {'Air Quality Index': aqi}
    else:
        return None


#Fetch 3-day forecast data
def get_forecast(city):
    base_url = "http://api.openweathermap.org/data/2.5/forecast?"
    complete_url = f"{base_url}q={city}&appid={WEATHER_API_KEY}&units=metric"
    response = requests.get(complete_url)

    if response.status_code == 200:
        data = response.json()
        forecast_list = data.get('list', [])[:3]  # Get the first 3 forecast entries, or an empty list
        forecasts = []

        for item in forecast_list:
            # Use .get to safely access dictionary keys and set default values
            temp = item.get('main', {}).get('temp', 'N/A')  # Default to 'N/A' if 'temp' is missing
            weather_desc = item.get('weather', [{}])[0].get('description', 'Unknown')  # Safe default

            forecasts.append({'Temperature': temp, 'Description': weather_desc})

        return forecasts
    else:
        return None


# Fetch weather-related news
def get_weather_news(city):
    base_url = "https://newsapi.org/v2/everything?"
    complete_url = f"{base_url}q=weather+{city}&apiKey={NEWS_API_KEY}"
    response = requests.get(complete_url)

    if response.status_code == 200:
        data = response.json()
        articles = data.get('articles', [])[:3] # Get the first three articles
        news_list = []

        for article in articles:
            title = article.get('title', 'No title')
            description = article.get('description', 'No description')

            news_list.append({'Title': title, 'Description': description})

        return news_list
    else:
        return None


# Fetch sunrise and sunset times, convert to local time
def get_sunrise_sunset(latitude, longitude):
    complete_url = f"{SUNRISE_SUNSET_BASE_URL}lat={latitude}&lng={longitude}&formatted=0"
    response = requests.get(complete_url)

    if response.status_code == 200:
        data = response.json()
        sunrise_utc = data['results']['sunrise'] # UTC sunrise time
        sunset_utc = data['results']['sunset'] # UTC sunset time

        # Convert UTC times to datetime
        sunrise_datetime = datetime.fromisoformat(sunrise_utc.replace("Z", "+00:00"))
        sunset_datetime = datetime.fromisoformat(sunset_utc.replace("Z", "+00:00"))

        return {
            'Sunrise UTC': sunrise_utc,
            'Sunset UTC': sunset_utc,
            'Sunrise Local': sunrise_datetime,
            'Sunset Local': sunset_datetime
            }
    else:
        return None


# Function to update the GUI with weather data and other information
def update_weather():
    city = city_entry.get()
    if not city:
        messagebox.showwarning("Invalid Input", "Please enter a city name")
        return

    weather_data = get_weather(city)

    if weather_data:
        latitude = weather_data['Latitude']
        longitude = weather_data['Longitude']

        sunrise_sunset_data = get_sunrise_sunset(latitude, longitude)

        weather_info.set(
            f"Weather in {city}:\n"
            f"Temperature: {weather_data['Temperature']} °C\n"
            f"Pressure: {weather_data['Pressure']} hPa\n"
            f"Humidity: {weather_data['Humidity']} %\n"
            f"Description: {weather_data['Weather Description']}\n"
        )

        if sunrise_sunset_data:
            weather_info.set(
                weather_info.get() +
                f"Sunrise: {sunrise_sunset_data['Sunrise Local'].strftime('%Y-%m-%d %H:%M:%S %Z')}\n"
                f"Sunset: {sunrise_sunset_data['Sunset Local'].strftime('%Y-%m-%d %H:%M:%S %Z')}\n"
            )

    else:
        messagebox.showerror("Error", "Could not retrieve weather data.")


# Create the main GUI window
window = tk.Tk()
window.title("Weather App")

# Create an entry widget for city name
city_entry = tk.Entry(window)
city_entry.pack()

# Create a button to fetch weather information
get_weather_button = tk.Button(window, text="Get Weather", command=update_weather)
get_weather_button.pack()

# Create a label to display weather information
weather_info = tk.StringVar()
weather_label = tk.Label(window, textvariable=weather_info, justify=tk.LEFT)
weather_label.pack()

#Start the GUI event loop
window.mainloop()
