import requests
from dadata import Dadata

from settings import DADATA_API_TOKEN, DADATA_API_SECRET, OPENWEATHER_API_KEY, CHAD_API_KEY


def get_coordinates_by_address(address):
    token = DADATA_API_TOKEN
    secret = DADATA_API_SECRET
    dadata = Dadata(token, secret)
    res = dadata.clean(name="address", source=address)
    if res["result"] is None:
        raise ValueError
    return res["geo_lat"], res["geo_lon"]


def get_weather_by_coordinates(lat, lon):
    api_key = OPENWEATHER_API_KEY
    url = 'http://api.openweathermap.org/data/2.5/weather'
    params = {
        'lat': lat,
        'lon': lon,
        'units': 'metric',
        'appid': api_key
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        weather_info = {
            'city': data.get('name', 'N/A'),
            'temperature': data['main']['temp'],
            'feels_like': data['main']['feels_like'],
            'temp_min': data['main']['temp_min'],
            'temp_max': data['main']['temp_max'],
            'description': data['weather'][0]['description'],
            'icon': data['weather'][0]['icon'],
            'humidity': data['main']['humidity'],
            'pressure': data['main']['pressure'],
            'wind_speed': data['wind']['speed'],
            'wind_direction': data['wind']['deg'],
            'sunrise': data['sys']['sunrise'],
            'sunset': data['sys']['sunset'],
            'visibility': data['visibility'],
            'clouds': data['clouds']['all'],
            'rain': data['rain']['1h'] if 'rain' in data else 0,
            'snow': data['snow']['1h'] if 'snow' in data else 0
        }
        return weather_info
    else:
        raise ValueError("response.status_code != 200")


def format_weather_data(weather_data):
    request_json = {
        "message": f"{str(weather_data)}\nПреобразуй эти' данные о погоде в человеческую форму. "
                   f"Обобщи все до пары небольших предложений. Маловажные пункты отбрось, передай только суть. "
                   f"Кроме этих предложений в ответе ничего не должно быть",
        "api_key": CHAD_API_KEY
    }
    response = requests.post(url='https://ask.chadgpt.ru/api/public/gpt-3.5',
                             json=request_json)
    resp_json = response.json()
    print(resp_json)
    if resp_json["is_success"] is not True:
        raise ValueError
    return resp_json["response"]


if __name__ == "__main__":
    coord = get_coordinates_by_address("Олеко Дундича 20к1, Санкт-Петербург")
    weather_data = get_weather_by_coordinates(*coord)
    res = format_weather_data(weather_data)
