# make get request to https://api.aladhan.com/v1/calendarByCity/2017/4?city=London&country=United%20Kingdom&method=2
import requests
import datetime

def get_city_and_country():
    import requests
    url = 'https://ipinfo.io/'
    r = requests.get(url)
    data = r.json()
    city = data['city']
    country = data['country']
    # print(data)
    return city, country

def get_calendar():
    import requests
    city, country = get_city_and_country()
    month, year = datetime.datetime.now().month, datetime.datetime.now().year
    url = f'https://api.aladhan.com/v1/calendarByCity/{year}/{month}?city={city}&country={country}&method=2'
    r = requests.get(url)
    data = r.json()['data'][0]['timings']
    return data

print(get_calendar())