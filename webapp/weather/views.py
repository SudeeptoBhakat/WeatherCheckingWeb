from django.shortcuts import render
from django.http import JsonResponse
import urllib.request
import json
# Create your views here.
def homePage(request):
    return render(request, "index.html")

def aboutUs(request):
    return render(request, "aboutus.html")

def forecast(request):
    if request.method == 'POST':
        city = request.POST['city']
        days = request.POST['days']
        if ' ' in city:
            city = city.replace(' ', '%20')
        # print(city,' ',days)
        source = urllib.request.urlopen('http://api.weatherapi.com/v1/forecast.json?key=f4f067e12659433a88152648232407&q='+city+'&days='+days+'&aqi=yes&alerts=yes').read()
        data_list = json.loads(source)
        icon = data_list['current']['condition']['icon']
        get_icon = icon.split("/")
        icon_path = '/'.join(get_icon[-2:])
        days = []
        for item in data_list['forecast']['forecastday']:
            _data = []
            # for i in range(0, 24):
            #     time_stap = item['hour'][i]['time']
            #     time = time_stap.split(' ')
            #     _data.append({"time": time[1], "temp_c":"", "icon": ""})
            iconsplit = item['day']['condition']['icon'].split("/")
            days.append({
                "date": item['date'],
                "avgTempC": item['day']['maxtemp_c'],
                "min": item['day']['mintemp_c'],
                "max": item['day']['avgtemp_c'],
                "text": item['day']['condition']['text'],
                "icon": '/'.join(iconsplit[-2:])
            })
                # temp = data_list['forecast']['forecastday'][item]['hour'][i]['temp_c']
                # temp_list.append(temp)
                # icon = data_list['forecast']['forecastday'][item]['hour'][i]['condition']['icon']
                # get_icon = icon.split("/")
                # icon_path = '/'.join(get_icon[-2:])
                # icon_list.append(icon_path)
        
        data = {
            "name": data_list['location']['name'],
            "country": data_list['location']['country'],
            "uv": data_list['current']['uv'],
            "localtime": data_list['location']['localtime'],
            "temp_c": data_list['current']['temp_c'],
            "humidity": data_list['current']['humidity'],
            "wind_kph": data_list['current']['wind_kph'],
            "text": data_list['current']['condition']['text'],
            "icon": icon_path,
            "date": data_list['forecast']['forecastday'][0]['date'],
            "maxtemp_c" : data_list['forecast']['forecastday'][0]['day']['maxtemp_c'],
            "mintemp_c" : data_list['forecast']['forecastday'][0]['day']['mintemp_c'],
            "days": days,
            # "temp_list": temp_list,
            # "icon_list": icon_list
        }
        return JsonResponse(data)

    return render(request, "forecast.html")

def history(request):
    if request.method == 'POST':
        city = request.POST['city']
        date = request.POST['date']
        time = request.POST['time']
        if ' ' in city:
            city = city.replace(' ', '%20')
        source = urllib.request.urlopen('http://api.weatherapi.com/v1/history.json?key=f4f067e12659433a88152648232407&q='+city+'&dt='+date).read()
        data_list = json.loads(source)
        hour_data = []
        if len(time) is not 0:
            for data in data_list["forecast"]["forecastday"][0]["hour"]:
                if time.split(":")[0] in data["time"].split(" ")[1]: 
                    split_icon = data["condition"]["icon"].split("/")
                    icon_path = '/'.join(split_icon[-2:])
                    hour_data.append({
                        "date_time": data["time"],
                        "temp_c": data["temp_c"],
                        "text": data["condition"]["text"],
                        "icon": icon_path,
                        "humidity": data["humidity"],
                        "wind_kph": data["wind_kph"],
                        "uv": data["uv"],
                    })
        else:
            split_icon = data_list['forecast']['forecastday'][0]['day']["condition"]["icon"].split("/")
            icon_path = '/'.join(split_icon[-2:])
            hour_data.append({
                "temp_c": data_list['forecast']['forecastday'][0]['day']["avgtemp_c"],
                "text": data_list['forecast']['forecastday'][0]['day']["condition"]["text"],
                "icon": icon_path,
                "humidity": data_list['forecast']['forecastday'][0]['day']["avghumidity"],
                "uv": data_list['forecast']['forecastday'][0]['day']["uv"],
                "wind_kph": data_list['forecast']['forecastday'][0]['day']["maxwind_kph"],
                "date_time": data_list['forecast']['forecastday'][0]['date'], 
            })
        data = {
            "name": data_list['location']['name'],
            "country": data_list['location']['country'],
            "hour": hour_data,
        }
        return JsonResponse(data)
    

    return render(request, "history.html")

def suggest_cities(request):
    query = request.GET.get('query')
    source = urllib.request.urlopen('http://api.weatherapi.com/v1/search.json?key=f4f067e12659433a88152648232407&q='+query).read()
    data_list = json.loads(source)
    temp = []
    for value in data_list:
        temp.append(value['name'])
    # print(temp)
    return JsonResponse({'city': temp})    

def realtime(request):
    if request.method == 'POST':
        city = request.POST['city']

        if ' ' in city:
            city = city.replace(' ', '%20')
        
        source = urllib.request.urlopen('http://api.weatherapi.com/v1/current.json?key=f4f067e12659433a88152648232407&q='+city+'&aqi=no').read()
        data_list = json.loads(source)
        icon = data_list['current']['condition']['icon']
        get_icon = icon.split("/")
        icon_path = '/'.join(get_icon[-2:])
        data = {
            "name": data_list['location']['name'],
            "country": data_list['location']['country'],
            "uv": data_list['current']['uv'],
            "localtime": data_list['location']['localtime'],
            "temp_c": data_list['current']['temp_c'],
            "humidity": data_list['current']['humidity'],
            "wind_kph": data_list['current']['wind_kph'],
            "text": data_list['current']['condition']['text'],
            "icon": icon_path,
        }
        return JsonResponse(data)
    
    return render(request, "realtime.html")