
from django.shortcuts import render
from django.contrib import messages
from django.http import JsonResponse
import requests
import datetime
import os

# Load API keys from environment variables
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
SEARCH_ENGINE_ID = os.getenv('GOOGLE_SEARCH_ENGINE_ID')

def get_city_image(city: str) -> str:
    """Return a landmark image for *city* using Wikipedia.
    If Wikipedia does not have a suitable image, fall back to loremflickr.
    """
    try:
        wiki_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{city.replace(' ', '_')}"
        resp = requests.get(
            wiki_url,
            timeout=6,
            headers={"User-Agent": "WeatherApp/1.0 (educational project)"},
        )
        if resp.status_code == 200:
            data = resp.json()
            image = (data.get("originalimage") or {}).get("source") or (
                data.get("thumbnail") or {}
            ).get("source")
            if image:
                return image
    except Exception:
        pass
    city_tag = city.replace(' ', ',').lower()
    return f"https://loremflickr.com/1920/1080/{city_tag},city"


def home(request):
    city = request.POST.get('city', 'Nairobi')

    # ---------- Weather ----------
    weather_url = "https://api.openweathermap.org/data/2.5/weather"
    weather_params = {'q': city, 'appid': WEATHER_API_KEY, 'units': 'metric'}

    try:
        weather_resp = requests.get(weather_url, params=weather_params, timeout=10)
        weather_data = weather_resp.json()
        if weather_data.get('cod') != 200:
            raise KeyError('city not found')

        description = weather_data['weather'][0]['description']
        icon = weather_data['weather'][0]['icon']
        temp = weather_data['main']['temp']
        country_code = weather_data['sys']['country']
        city_name = weather_data['name']
        utc_now = datetime.datetime.utcnow()
        city_time = utc_now + datetime.timedelta(seconds=weather_data['timezone'])
        image_url = get_city_image(city_name)

        return render(
            request,
            'index.html',
            {
                'description': description,
                'icon': icon,
                'temp': temp,
                'day': datetime.date.today(),
                'ctime': city_time.strftime('%H:%M:%S'),
                'time': city_time.strftime('%H:%M:%S'),
                'city': city_name,
                'country': country_code,
                'exception_occurred': False,
                'image_url': image_url,
                'timezone_offset': weather_data['timezone'],  # seconds from UTC
            },
        )
    except requests.RequestException:
        messages.error(request, 'Network error occurred. Please try again.')
    except KeyError:
        messages.error(
            request,
            f"City '{city}' not found. Showing weather for Nairobi instead.",
        )

    fallback_image = get_city_image('Nairobi')
    now = datetime.datetime.now()
    return render(
        request,
        'index.html',
        {
            'description': 'clear sky',
            'icon': '01d',
            'temp': 25,
            'day': datetime.date.today(),
            'ctime': now.strftime('%H:%M:%S'),
            'time': now.strftime('%H:%M:%S'),
            'city': 'Nairobi',
            'country': 'KE',
            'exception_occurred': True,
            'image_url': fallback_image,
            'timezone_offset': 10800,  # EAT = UTC+3
        },
    )


def location_weather(request):
    """AJAX endpoint used by the front‑end to get weather data for the
    user's current lat/lon. Returns a JSON payload containing
    the same fields the normal ``home`` view uses.
    """
    lat = request.GET.get('lat')
    lon = request.GET.get('lon')
    if not lat or not lon:
        return JsonResponse({
            'error': 'Missing latitude or longitude parameters'
        }, status=400)

    weather_url = 'https://api.openweathermap.org/data/2.5/weather'
    weather_params = {
        'lat': lat,
        'lon': lon,
        'appid': WEATHER_API_KEY,
        'units': 'metric',
    }

    try:
        resp = requests.get(weather_url, params=weather_params, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        if data.get('cod') != 200:
            raise ValueError('OpenWeatherMap did not return a successful result')
        result = {
            'city': data['name'],
            'country': data['sys']['country'],
            'temp': data['main']['temp'],
            'description': data['weather'][0]['description'],
            'icon': data['weather'][0]['icon'],
            'timezone': data['timezone'],
        }
        return JsonResponse(result)
    except (requests.RequestException, ValueError) as exc:
        print(f'[location_weather] error: {exc}')
        return JsonResponse({
            'error': 'Could not retrieve weather for current location'
        }, status=500)

