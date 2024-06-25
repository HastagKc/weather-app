from django.shortcuts import render
import requests  # pip install requests
from datetime import datetime
from django.contrib import messages

# Create your views here.


def index(request):
    # Get city from POST request or default to 'kathmandu'
    city = request.POST.get('city', 'kathmandu')

    api_key = 'bf22686cf11682e29d657b984d138978'
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': city,
        'appid': api_key,
        'units': 'metric'
    }

    try:
        # Fetch data from the API
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an error for bad status codes
        data = response.json()

        # Extract weather data
        temp = data['main']['temp']
        desc = data['weather'][0]['description']
        icon_code = data['weather'][0]['icon']
        icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
        speed = data['wind']['speed']
        humidity = data['main']['humidity']
    except requests.exceptions.RequestException:
        # Handle network-related errors
        messages.error(
            request, "There was a network error. Please try again later.")
        temp = 0
        desc = f"There was an error fetching data for {city}"
        icon_url = "No icon available"
        speed = "Not available"
        humidity = "Not available"
    except KeyError:
        # Handle case where city is not found or other data issues
        messages.error(request, f"There is no such city available: {city}")
        temp = 0
        desc = f"There is no such city available: {city}"
        icon_url = "No icon available"
        speed = "Not available"
        humidity = "Not available"

    date = datetime.now()

    # Render the weather data in the template
    return render(request, 'weatherapp/index.html', {
        'temp': temp,
        'city': city,
        'desc': desc,
        'icon': icon_url,
        'humidity': humidity,
        'speed': speed,
        'date': date
    })
