# make get request to https://api.aladhan.com/v1/calendarByCity/2017/4?city=London&country=United%20Kingdom&method=2
import requests
import datetime

def get_lat_long():
    import requests
    url = 'https://ipinfo.io/'
    r = requests.get(url)
    data = r.json()
    location = data['loc'].split(',')
    lat = location[0]
    lon = location[1]
    return lat, lon

print(get_lat_long())