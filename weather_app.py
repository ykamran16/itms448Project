import requests

#OpenWeather API Key
WEATHER_API_KEY = "4280cf0c7e000e8ae9a42913aa06e1c5"

#WAQI API Key
AIR_QUALITY_API_KEY = "1119033840c1a73ffcbba1b0557507f7a961d60f"

#News API Key
NEWS_API_KEY = "bee063b26e764f1fa847e481e8cbf78f"


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

        weather_desc = data['weather'][0]['description']

        return {
            'Temperature': temperature,
            'Pressure': pressure,
            'Humidity': humidity,
            'Weather Description': weather_desc,
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

#Test the function with Chicago
if __name__ == "__main__":
    city = "Chicago"
    weather_data = get_weather(city)
    air_quality_data = get_air_quality(city)
    forecast_data = get_forecast(city)
    weather_news_data = get_weather_news(city)

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

    if forecast_data:
        print(f"3-Day Weather Forecast in {city}:")
        for i, forecast in enumerate(forecast_data, 1):
            print(f"Day {i}: Temperature {forecast['Temperature']} °C, Description: {forecast['Description']}")
    else:
        print(f"Could not retrieve weather forecast data for {city}.")

    if weather_news_data:
        print(f"Weather-related news in {city}:")
        for i, news in enumerate(weather_news_data, 1):
            print(f"Article {i}: {news['Title']}")
            print(f"  Description: {news['Description']}")
    else:
        print(f"Could not retrieve weather-related news for {city}.")
