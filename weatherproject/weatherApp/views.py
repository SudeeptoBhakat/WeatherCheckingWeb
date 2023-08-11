import json
import urllib.request
import requests
from django.shortcuts import render
from django.http import JsonResponse

API_KEY = 'Give Your key hare'
BASE_URL = 'http://api.weatherapi.com/v1/'

def make_request(endpoint, params=None):
    url = f'{BASE_URL}{endpoint}'
    params = params or {}
    params['key'] = API_KEY
    response = requests.get(url, params=params)
    return response.json()

def extract_icon_path(icon_url):
    icon_parts = icon_url.split("/")[-2:] 
    return '/'.join(icon_parts)

def suggest_cities(request):
    query = request.GET.get('query')
    source = requests.get(f'{BASE_URL}search.json?key={API_KEY}&q={query}').text
    data_list = json.loads(source)
    city_suggestions = [value['name'] for value in data_list]
    return JsonResponse({'city': city_suggestions})

def weatherReport(params):
    data_list = make_request('forecast.json', params=params)
    current = data_list['current']

    days_data = [{
        "date": item['date'],
        "avgTempC": item['day']['avgtemp_c'],
        "maxtemp_c": item['day']['maxtemp_c'],
        "mintemp_c": item['day']['mintemp_c'],
        "maxwind_kph": item['day']['maxwind_kph'],
        "avghumidity": item['day']['avghumidity'],
        "uv": item['day']['uv'],
        "text": item['day']['condition']['text'],
        "icon": extract_icon_path(item['day']['condition']['icon'])
    } for item in data_list['forecast']['forecastday']]

    data = {
        "name": data_list['location']['name'],
        "country": data_list['location']['country'],
        "uv": current['uv'],
        "localtime": data_list['location']['localtime'],
        "temp_c": current['temp_c'],
        "humidity": current['humidity'],
        "wind_kph": current['wind_kph'],
        "text": current['condition']['text'],
        "icon": extract_icon_path(current['condition']['icon']),
        "date": data_list['forecast']['forecastday'][0]['date'],
        "maxtemp_c": data_list['forecast']['forecastday'][0]['day']['maxtemp_c'],
        "mintemp_c": data_list['forecast']['forecastday'][0]['day']['mintemp_c'],
        "days": days_data,
    }
    return data

def realtime(request):
    if request.method == 'POST':
        city = request.POST['city']
        city = city.replace(' ', '%20') if ' ' in city else city
        params = {'q': city, 'days': 1, 'aqi': 'yes', 'alerts': 'yes'}
        data = weatherReport(params)
        return JsonResponse(data)

    return render(request, "index.html")

def forecast(request):
    if request.method == 'POST':
        city = request.POST['city']
        days = request.POST['days']
        city = city.replace(' ', '%20') if ' ' in city else city
        params = {'q': city, 'days': days, 'aqi': 'yes', 'alerts': 'yes'}
        data = weatherReport(params)
        return JsonResponse(data)
    return render(request, "forecast.html")


def history(request):
    if request.method == 'POST':
        city = request.POST['city']
        date = request.POST['date']
        time = request.POST['time']
        city = city.replace(' ', '%20') if ' ' in city else city

        params = {'q': city, 'dt': date}
        data_list = make_request('history.json', params=params)
        hour_data = []
        if len(time) != 0:
            for data in data_list["forecast"]["forecastday"][0]["hour"]:
                if time.split(":")[0] in data["time"].split(" ")[1]:
                    icon = extract_icon_path(data["condition"]["icon"])
                    hour_data.append({
                        "date_time": data["time"],
                        "temp_c": data["temp_c"],
                        "text": data["condition"]["text"],
                        "icon": icon,
                        "humidity": data["humidity"],
                        "wind_kph": data["wind_kph"],
                        "uv": data["uv"],
                    }) 
        else:
            weather_history = data_list['forecast']['forecastday'][0]
            hour_data.append({
                            "temp_c": weather_history['day']["avgtemp_c"],
                            "text": weather_history['day']["condition"]["text"],
                            "icon": extract_icon_path(weather_history['day']["condition"]["icon"]),
                            "humidity": weather_history['day']["avghumidity"],
                            "uv": weather_history['day']["uv"],
                            "wind_kph": weather_history['day']["maxwind_kph"],
                            "date_time": weather_history['date'], 
                        })
        data = {
            "name": data_list['location']['name'],
            "country": data_list['location']['country'],
            "maxtemp_c": data_list['forecast']['forecastday'][0]['day']["maxtemp_c"],
            "mintemp_c": data_list['forecast']['forecastday'][0]['day']["mintemp_c"],
            "hour": hour_data,
        }
        return JsonResponse(data)

    return render(request, "history.html")