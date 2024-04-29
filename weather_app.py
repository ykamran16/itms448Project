import tkinter as tk
from tkinter import messagebox
import requests
from datetime import datetime
import pytz
from timezonefinder import TimezoneFinder

# Create the main GUI window
window = tk.Tk()
window.title("Weather App")

# Create a variable for temeprature units
temperature_unit = tk.StringVar(value="Celsius") #Default to Celsius

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
    unit = "metric" if temperature_unit.get() == "Celsius" else "imperial"
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = f"{base_url}q={city}&appid={WEATHER_API_KEY}&units={unit}"
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
    unit = "metric" if temperature_unit.get() == "Celsius" else "imperial"
    base_url = "http://api.openweathermap.org/data/2.5/forecast?"
    complete_url = f"{base_url}q={city}&appid={WEATHER_API_KEY}&units={unit}"
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
        sunrise_dt = datetime.fromisoformat(sunrise_utc.replace("Z", "+00:00"))
        sunset_dt = datetime.fromisoformat(sunset_utc.replace("Z", "+00:00"))

        # Get the correct time zone from coordinates
        timezone_finder = TimezoneFinder()
        timezone_str = timezone_finder.timezone_at(lat=latitude, lng=longitude)

        if timezone_str is not None:
            local_tz = pytz.timezone(timezone_str)

            # Convert to local time
            sunrise_local = sunrise_dt.astimezone(local_tz).strftime("%Y-%m-%d %H:%M:%S %Z")
            sunset_local = sunset_dt.astimezone(local_tz).strftime("%Y-%m-%d %H:%M:%S %Z")

            return {
                'Sunrise Local': sunrise_local,
                'Sunset Local': sunset_local,
            }
        else:
            raise Exception("Unable to determine the time zone.")

    else:
        return None


# Function to update the GUI with weather data and other information
def update_weather():
    city = city_entry.get() # Get city name
    if not city:
        messagebox.showwarning("Invalid Input", "Please enter a city name")
        return

    # Fetch weather data
    weather_data = get_weather(city)

    if weather_data:
        unit_symbol = "°C" if temperature_unit.get() == "Celsius" else "°F"
        temperature = weather_data['Temperature']
        pressure = weather_data['Pressure']
        humidity = weather_data['Humidity']
        weather_desc = weather_data['Weather Description']

        latitude = weather_data['Latitude']
        longitude = weather_data['Longitude']


        weather_info.set(
            f"Weather in {city}:\n"
            f"Temperature: {temperature} {unit_symbol}\n"
            f"Pressure: {weather_data['Pressure']} hPa\n"
            f"Humidity: {weather_data['Humidity']} %\n"
            f"Description: {weather_data['Weather Description']}\n"
        )

        #Fetch and display sunrise/sunset times
        sunrise_sunset_data = get_sunrise_sunset(latitude, longitude)
        if sunrise_sunset_data:
            weather_info.set(
                weather_info.get() +
                f"Sunrise (Local): {sunrise_sunset_data['Sunrise Local']}\n"
                f"Sunset (Local): {sunrise_sunset_data['Sunset Local']}\n"
            )

        # Fetch weather forecast data
        forecast_data = get_forecast(city)
        if forecast_data:
            for i, forecast in enumerate(forecast_data, 1):
                forecast_temp = forecast['Temperature']
                weather_info.set(
                    weather_info.get() +
                    f"Day {i}: Temperature: {forecast_temp} {unit_symbol}, "
                    f"Description: {forecast['Description']}\n"
                )

        # Fetch weather-related news
        news_data = get_weather_news(city)
        if news_data:
            news_info = ""
            for i, news in enumerate(news_data, 1):
                news_info += f"Article {i}: {news['Title']}\n  Description: {news['Description']}\n"

            news_var.set(news_info)

    else:
        messagebox.showerror("Error", "Could not retrieve weather data.")


# Create an entry widget for city name
city_entry = tk.Entry(window)
city_entry.pack()

# Dropdown menu for temperature unit selection
unit_menu = tk.OptionMenu(window, temperature_unit, "Celsius", "Fahrenheit")
unit_menu.pack()

# Create a button to fetch weather information
get_weather_button = tk.Button(window, text="Get Weather", command=update_weather)
get_weather_button.pack()

# Create a label to display weather information
weather_info = tk.StringVar()
weather_label = tk.Label(window, textvariable=weather_info, justify=tk.LEFT)
weather_label.pack()

# Create a label to display news articles
news_var = tk.StringVar()
news_label = tk.Label(window, textvariable=news_var, justify=tk.LEFT)
news_label.pack()

#Start the GUI event loop
window.mainloop()
