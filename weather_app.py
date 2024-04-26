import requests

#OpenWeather API Key
API_KEY = "4280cf0c7e000e8ae9a42913aa06e1c5"

#Fetch weather data
def get_weather(city):
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = f"{base_url}q={city}&appid={API_KEY}&units=metric"
    response = requests.get(complete_url)

    if response.status_code == 200:
        data = response.json()
        main = data['main']
        tempeature = main['temp']
        pressure = main['pressure']
        humidity = main['humidity']

        weather_descrip = data['weather'][0]['description']

        return {
            'Temperature': tempeature,
            'Pressure': pressure,
            'Humidity': humidity,
            'Weather Description': weather_descrip,
        }

    else:
        return None

#Test the function with Chicago
if __name__ == "__main__":
    city = "Chicago"
    weather_data = get_weather(city)

    if weather_data:
        print(f"Weather in {city}:")
        print(f"Temperature: {weather_data['Temperature']} °C")
        print(f"Pressure: {weather_data['Pressure']} hPa")
        print(f"Humidity: {weather_data['Humidity']} %")
        print(f"Description: {weather_data['Weather Description']}")
    else:
        print(f"Could not retrieve weather data for {city}.")
