import requests

#OpenWeather API Key
WEATHER_API_KEY = "4280cf0c7e000e8ae9a42913aa06e1c5"

#WAQI API Key
AIR_QUALITY_API_KEY = "1119033840c1a73ffcbba1b0557507f7a961d60f"

#Fetch weather data
def get_weather(city):
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = f"{base_url}q={city}&appid={WEATHER_API_KEY}&units=metric"
    response = requests.get(complete_url)

    if response.status_code == 200:
        data = response.json()
        main = data['main']
        temperature = main['temp']
        pressure = main['pressure']
        humidity = main['humidity']

        weather_descrip = data['weather'][0]['description']

        return {
            'Temperature': temperature,
            'Pressure': pressure,
            'Humidity': humidity,
            'Weather Description': weather_descrip,
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

#Test the function with Chicago
if __name__ == "__main__":
    city = "Chicago"
    weather_data = get_weather(city)
    air_quality_data = get_air_quality(city)

    if weather_data:
        print(f"Weather in {city}:")
        print(f"Temperature: {weather_data['Temperature']} °C")
        print(f"Pressure: {weather_data['Pressure']} hPa")
        print(f"Humidity: {weather_data['Humidity']} %")
        print(f"Description: {weather_data['Weather Description']}")
    else:
        print(f"Could not retrieve weather data for {city}.")

    if air_quality_data:
            print(f"Air Quality Index in {city}: {air_quality_data['Air Quality Index']}")
    else:
        print(f"Could not retrieve air quality data for {city}.")
