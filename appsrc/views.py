import datetime
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from hijri_converter import convert
from geopy.geocoders import Nominatim
from .models import Data
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
def get_city_and_country():
    """
    Retrieve the city and country information based on the IP address of the user.
    @return A tuple containing the city and country information
    """
    import requests
    url = 'https://ipinfo.io/'
    r = requests.get(url)
    data = r.json()
    city = data['city']
    country = data['country']
    # print(data)
    return city, country


@csrf_exempt
def get_lat_lon(request):
    """
    Make a request to the 'https://ipinfo.io/' URL to get the latitude and longitude of the client's IP address.
    @return A JSON response containing the latitude and longitude
    """
    import requests
    url = 'https://ipinfo.io/'
    r = requests.get(url)
    data = r.json()
    location = data['loc'].split(',')
    lat = location[0]
    lon = location[1]
    return JsonResponse({'latitude': lat, 'longitude': lon})

def get_hijri_date(date=None):     
    """
    This function takes an optional date parameter and returns the corresponding Hijri date.
    @param date - (optional) A string representing a date in the format "dd-mm-yyyy".
    @return A string representing the formatted Hijri date in the format "Month Day, Year AH".
    """       
    # Convert a specific date from Gregorian to Hijri
    if date:
        date_now = datetime.datetime.strptime(date, "%d-%m-%Y")
    else:
        date_now = datetime.datetime.now()
    hijri_date = convert.Gregorian(
        day=date_now.day,
        month=date_now.month,
        year=date_now.year
    ).to_hijri()


    # Extract the month and day from the Hijri date
    hijri_year = hijri_date.year
    hijri_month = hijri_date.month
    hijri_day = hijri_date.day


    # Get the Hijri month name
    hijri_month_name = hijri_date.month_name()

    # Format the Hijri date
    hijri_date_formatted = f"{hijri_month_name} {hijri_day}, {hijri_year} AH"

    return hijri_date_formatted

@csrf_exempt
def get_time_and_date(request):
    """
    Given a request, retrieve the user's date and time object from the database. 
    Calculate the current time and add the time difference from the user's date and time object to get the scheduled time. 
    Format the scheduled time and date in the desired format. 
    Get the Hijri date for the scheduled time. 
    Return a JSON response containing the Hijri date, formatted scheduled time, and formatted scheduled date. 
    @param request - the request object
    @return a JSON response containing the Hijri date, formatted scheduled time, and formatted scheduled date
    """
    user_date_time_obj = Data.objects.first()  # Assuming you have stored the user's data
    current_time = datetime.datetime.now()
    scheduled_time = current_time + user_date_time_obj.time_difference
    # print(scheduled_time)
    # convert date to this format string %d-%m-%Y
    hijri_date = scheduled_time.strftime("%d-%m-%Y")
    hijri_date = get_hijri_date(hijri_date)
    # Convert scheduled_time to the desired format
    formatted_scheduled_time = scheduled_time.strftime("%I:%M:%S %p")  # e.g., 12:00:00 AM
    formatted_scheduled_date = scheduled_time.strftime("%A, %B %d, %Y")  # e.g., Saturday, June 10, 2023

    return JsonResponse({
        'hijri_date': hijri_date,
        'time': formatted_scheduled_time,
        'date': formatted_scheduled_date,
    })

def get_calendar(method, city, country):
    """
    Retrieve the prayer times for a given city and country using the Aladhan API.
    @param method - the calculation method for prayer times
    @param city - the city for which to retrieve prayer times
    @param country - the country for which to retrieve prayer times
    @return A dictionary of converted prayer times
    """
    import requests
    # city, country = get_city_and_country()
    month, year = datetime.datetime.now().month, datetime.datetime.now().year
    # method = Data.objects.get(ip="127.0.0.1").school
    print(method, city, country)
    url = f'https://api.aladhan.com/v1/calendarByCity/{year}/{month}?city={city}&country={country}&method={method}'
    r = requests.get(url)
    data = r.json()['data'][0]['timings']
    converted_times = {}

    for key, value in data.items():
        time_str = value.split(' ')[0]  # Extract the time part
        time_obj = datetime.datetime.strptime(time_str, "%H:%M")
        time_formatted = time_obj.strftime("%I:%M %p")
        converted_times[key] = time_formatted

    return converted_times

def get_ip():
    # get request to https://api.ipgeolocation.io/getip
    # return ip address
    import requests
    url = 'https://api.ipgeolocation.io/getip'
    r = requests.get(url)
    ip = r.json()['ip']
    return ip

def get_hijri_date(date=None):        
    """
    Convert a given Gregorian date to Hijri (Islamic) date.
    @param date - the Gregorian date to convert (optional, default is current date)
    @return The formatted Hijri date in the format "Month Day, Year AH"
    """
    # Convert a specific date from Gregorian to Hijri
    if date:
        date_now = datetime.datetime.strptime(date, "%d-%m-%Y")
    else:
        date_now = datetime.datetime.now()
    hijri_date = convert.Gregorian(
        day=date_now.day,
        month=date_now.month,
        year=date_now.year
    ).to_hijri()


    # Extract the month and day from the Hijri date
    hijri_year = hijri_date.year
    hijri_month = hijri_date.month
    hijri_day = hijri_date.day


    # Get the Hijri month name
    hijri_month_name = hijri_date.month_name()

    # Format the Hijri date
    hijri_date_formatted = f"{hijri_month_name} {hijri_day}, {hijri_year} AH"

    return hijri_date_formatted

@csrf_exempt
def get_hijri(request):
    """
    Given a date parameter from a GET request, retrieve the corresponding Hijri date using the `get_hijri_date` function. Return the Hijri date as a JSON response.
    @param date - the date parameter from the GET request
    @return A JSON response containing the Hijri date
    """
    date = request.GET.get('date')
    hijri_date = get_hijri_date(date)
    return JsonResponse({'hijri_date': hijri_date})

@csrf_exempt
def get_timings(request):
    """
    This code snippet handles a POST request. It retrieves the values of 'method', 'city', and 'country' from the request's POST data. It then prints these values. The code then calls a function called 'get_calendar' with the method, city, and country as arguments, and stores the returned timings in a variable called 'timings'. 
    """
    if request.method == 'POST':
        method = request.POST.get('method')
        city = request.POST.get('city')
        country = request.POST.get('country')
        print(method, city, country)
        timings = get_calendar(method, city, country)
        timings['FajrEnd'] = timings['Sunrise']
        timings['DhuhrEnd'] = timings['Asr']
        timings['AsrEnd'] = timings['Sunset']
        timings['MaghribEnd'] = timings['Isha']
        timings['IshaEnd'] = timings['Fajr']
        return JsonResponse(timings)
    # RETURN 500 ERROR
    return JsonResponse({'error': 'Something went wrong.'}, status=500)

@csrf_exempt
def get_city_country(request):
    """
    This function takes latitude and longitude as input parameters from a GET request and uses the Nominatim geocoding service to reverse geocode the location. It retrieves the address information such as city, country, and postcode from the location data. If the location is successfully reverse geocoded, it returns a JSON response containing the city, country, and postcode. If the location cannot be reverse geocoded, it returns a JSON response with an error message.
    """
    latitude = request.GET.get('lat', '33.7235488')
    longitude = request.GET.get('lng', '72.8470496')

    geolocator = Nominatim(user_agent="mosque-project")
    location = geolocator.reverse(f"{latitude}, {longitude}", language="en")
    
    if location:
        address = location.raw["address"]
        print(address)
        city = address.get("city", "")
        country = address.get("country", "")
        if not city:
            city = address.get("town", "")
            if not city:
                city = address.get("county", "")
                if not city:
                    city = address.get("village", "")
                    if not city:
                        city = address.get("state", "")
        postcode = address.get("postcode", "")

        data = {
            "city": city,
            "country": country,
            "postcode": postcode,
        }
        return JsonResponse(data)
    else:
        return JsonResponse({"error": "Unable to retrieve city and country information."})

def find_closest_time(time_list, time_now):
    """
    Given a list of time strings and the current time, find the closest time in the list to the current time.
    @param time_list - a list of time strings in the format "%I:%M %p"
    @param time_now - the current time
    @return The closest time string to the current time
    """
    from datetime import datetime, timedelta

    current_time = time_now

    # Convert current_time to a datetime object with today's date
    current_datetime = datetime.combine(datetime.now().date(), current_time)

    # Initialize variables to track the closest time and its difference
    closest_time = None
    min_difference = timedelta.max

    # Iterate over the time_list and find the closest time
    for time_str in time_list:
        # Parse the time string to a datetime object
        time_obj = datetime.strptime(time_str, "%I:%M %p").time()

        # Convert the time_obj to a datetime object with today's date
        time_datetime = datetime.combine(datetime.now().date(), time_obj)

        # Calculate the difference between current_datetime and time_datetime
        difference = abs(current_datetime - time_datetime)

        # Update closest_time and min_difference if a closer time is found
        if difference < min_difference:
            closest_time = time_str
            min_difference = difference

    return closest_time


def find_next_time(time_list, current_time):
    """
    Find the next time in a list of times that comes after the current time.
    @param time_list - a list of time strings in the format "%I:%M %p"
    @param current_time - the current time as a string in the format "%I:%M %p"
    @return The next time in the list that comes after the current time
    """
    from datetime import datetime, timedelta

    current_time_obj = current_time

    # Initialize variables to track the next time and its difference
    next_time = None
    min_difference = timedelta.max

    # Iterate over the time_list and find the next time
    for time_str in time_list:
        # Parse the time string to a datetime object
        time_obj = datetime.strptime(time_str, "%I:%M %p").time()

        # Calculate the difference between current_time_obj and time_obj
        difference = (datetime.combine(datetime.now().date(), time_obj) -
                      datetime.combine(datetime.now().date(), current_time_obj))

        # Ignore times that are equal to or before the current_time
        if difference <= timedelta(0):
            continue

        # Update next_time and min_difference if a closer time is found
        if difference < min_difference:
            next_time = time_str
            min_difference = difference
            
    if next_time == None:
        next_time = time_list[0]

    return next_time

def find_previous_time(time_list, current_time):
    """
    Given a list of time strings and a current time, find the previous time in the list that is earlier than the current time.
    @param time_list - a list of time strings in the format "%I:%M %p"
    @param current_time - the current time as a datetime object
    @return The previous time as a string in the format "%I:%M %p"
    """
    from datetime import datetime, timedelta
    # Convert current_datetime to a time object
    current_time_obj = current_time

    # Initialize variables to track the previous time and its difference
    previous_time = None
    min_difference = timedelta.max

    # Iterate over the time_list and find the previous time
    for time_str in time_list:
        # Parse the time string to a datetime object
        time_obj = datetime.strptime(time_str, "%I:%M %p").time()

        # Calculate the difference between current_time_obj and time_obj
        difference = (datetime.combine(datetime.now().date(), current_time_obj) -
                      datetime.combine(datetime.now().date(), time_obj))

        # Ignore times that are equal to or after the current_time
        if difference <= timedelta(0):
            continue

        # Update previous_time and min_difference if a closer time is found
        if difference < min_difference:
            previous_time = time_str
            min_difference = difference

    if previous_time == None:
        previous_time = time_list[-1]

    return previous_time


@csrf_exempt
def get_data(request):
    """
    This function retrieves data based on a request and returns a JSON response containing various information related to prayer times and other details.
    @param request - the request object
    @return a JSON response containing various information related to prayer times and other details
    """
    from datetime import datetime
    ip = get_ip()
    hijri_date = get_hijri_date()
    data = Data.objects.get(ip="127.0.0.1")
    hadith = data.hadith
    notice = data.notice
    fajrAdhan = data.fajarAdhan
    fajrIqama = data.fajarIqama
    fajrEnds = data.fajarEnds
    duhurAdhan = data.duhurAdhan
    duhurIqama = data.duhurIqama
    duhurEnds = data.duhurEnds
    asarAdhan = data.asarAdhan
    asarIqama = data.asarIqama
    asarEnds = data.asarEnds
    maghribAdhan = data.maghribAdhan
    maghribIqama = data.maghribIqama
    maghribEnds = data.maghribEnds
    ishaAdhan = data.ishaAdhan
    ishaIqama = data.ishaIqama
    ishaEnds = data.ishaEnds
    sunrise = data.sunrise
    sunset = data.sunset
    audio = data.audio
    school = data.school
    zipcode = data.zipcode
    city = data.city
    country = data.country
    location = data.location

    user_date_time_obj = data  # Assuming you have stored the user's data
    current_time = datetime.now()
    scheduled_time = current_time + user_date_time_obj.time_difference

    prev_time = find_previous_time([fajrAdhan, duhurAdhan, asarAdhan, maghribAdhan, ishaAdhan], scheduled_time.time())
    next_time = find_next_time([fajrAdhan, fajrEnds, duhurAdhan, asarAdhan, maghribAdhan, ishaAdhan], scheduled_time.time())

    # convert date to this format string %d-%m-%Y
    hijri_date = scheduled_time.strftime("%d-%m-%Y")
    hijri_date = get_hijri_date(hijri_date)
    # Convert scheduled_time to the desired format
    formatted_scheduled_time = scheduled_time.strftime("%I:%M %p")  # e.g., 12:00 AM
    formatted_scheduled_date = scheduled_time.strftime("%A, %B %d, %Y")  # e.g., Saturday, June 10, 2023

    fajr_time = datetime.strptime(data.fajarAdhan, "%I:%M %p")
    fajr_time = fajr_time.replace(year=scheduled_time.year, month=scheduled_time.month, day=scheduled_time.day)

    duhur_time = datetime.strptime(data.duhurAdhan, "%I:%M %p")
    duhur_time = duhur_time.replace(year=scheduled_time.year, month=scheduled_time.month, day=scheduled_time.day)

    asar_time = datetime.strptime(data.asarAdhan, "%I:%M %p")
    asar_time = asar_time.replace(year=scheduled_time.year, month=scheduled_time.month, day=scheduled_time.day)
    
    maghrib_time = datetime.strptime(data.maghribAdhan, "%I:%M %p")
    maghrib_time = maghrib_time.replace(year=scheduled_time.year, month=scheduled_time.month, day=scheduled_time.day)

    isha_time = datetime.strptime(data.ishaAdhan, "%I:%M %p")
    isha_time = isha_time.replace(year=scheduled_time.year, month=scheduled_time.month, day=scheduled_time.day)

    sunrise_time = datetime.strptime(data.sunrise, "%I:%M %p")
    sunrise_time = sunrise_time.replace(year=scheduled_time.year, month=scheduled_time.month, day=scheduled_time.day)

    sunset_time = datetime.strptime(data.sunset, "%I:%M %p")
    sunset_time = sunset_time.replace(year=scheduled_time.year, month=scheduled_time.month, day=scheduled_time.day)

    time_now = scheduled_time

    time_difference = sunrise_time - time_now

    next_time_text = "Preferred Prayer Time Ends In"
    next_time = "00:00:00"
    
    rt = False
    if time_now > sunrise_time:      
        time_difference = time_now - sunrise_time
        if time_difference.total_seconds() <= 720:  # 12 minutes in seconds
            seconds = time_difference.seconds
            minutes, seconds = (seconds % 3600) // 60, seconds % 60
            minutes = 11 - minutes
            seconds = 60 - seconds
            next_time = f"00:{minutes if minutes > 9 else '0' +str(minutes)}:{seconds if seconds > 9 else '0' + str(seconds)}"
            next_time_text = "Prohibited Time Ends In:"
            rt = True

    if rt == False and time_now < duhur_time:      
        time_difference = duhur_time - time_now
        if time_difference.total_seconds() <= 720:  # 12 minutes in seconds
            seconds = time_difference.seconds
            minutes, seconds = (seconds % 3600) // 60, seconds % 60
            next_time = f"00:{minutes if minutes > 9 else '0' +str(minutes)}:{seconds if seconds > 9 else '0' + str(seconds)}"
            next_time_text = "Prohibited Time Ends In:"
            rt = True
        
    if rt == False and time_now < sunset_time:  
        time_difference = sunset_time - time_now
        if time_difference.total_seconds() <= 1500:  # 25 minutes in seconds
            seconds = time_difference.seconds
            hours, minutes, seconds = seconds // 3600, (seconds % 3600) // 60, seconds % 60

            next_time = f"00:{minutes if minutes > 9 else '0' +str(minutes)}:{seconds if seconds > 9 else '0' + str(seconds)}"
            next_time_text = "Prohibited Time Ends In:"
            rt = True
        



    return JsonResponse({
        'hijri_date': hijri_date,
        'hadith': hadith,
        'notice': notice,
        'fajr': fajrAdhan,
        'fajrIqama': fajrIqama,
        'fajrEnds': fajrEnds,
        'dhuhr': duhurAdhan,
        'dhuhrIqama': duhurIqama,
        'asr': asarAdhan,
        'asrIqama': asarIqama,
        'maghrib': maghribAdhan,
        'maghribIqama': maghribIqama,
        'isha': ishaAdhan,
        'ishaIqama': ishaIqama,
        'sunrise': sunrise,
        'sunset': sunset,
        'audio': audio,
        'school': school,
        'zipcode': zipcode,
        'city': city,
        'country': country,
        'closest_time': prev_time,
        'next_time_text': next_time_text,
        'next_time': next_time,
        'location': location,
        'hijri_date': hijri_date,
        'time': formatted_scheduled_time,
        'date': formatted_scheduled_date,
        'color': '#00ff00' if rt else 'white'
        }
    )



@csrf_exempt
def index(request):
    """
    Render the 'index.html' template with the current Hijri date and return the rendered template as a response.
    @param request - the HTTP request object
    @return The rendered 'index.html' template with the Hijri date
    """
    hijri_date = get_hijri_date()

    return render(request , 'index.html', {
        'hijri_date': hijri_date,
        }
    )

@csrf_exempt
def get_hadith():
    """
    This function makes an HTTP GET request to the "api.sunnah.com" API to retrieve a random hadith. It uses the "x-api-key" header for authentication. The response is then parsed as JSON and the body of the first hadith is extracted and returned.
    @return The body of a random hadith
    """
    
    import http.client
    import json

    conn = http.client.HTTPSConnection("api.sunnah.com")

    payload = "{}"

    headers = { 'x-api-key': "SqD712P3E82xnwOAEOkGd5JZH8s9wRR24TqNFzjk" }

    conn.request("GET", "/v1/hadiths/random", payload, headers)

    res = conn.getresponse()
    data = res.read()

    data = json.loads(data.decode("utf-8"))
    """
    This function is a view function that handles a request to retrieve a hadith. It retrieves the hadith data using the `get_hadith()` function and checks if the length of the data is greater than or equal to 350. If the length is greater than or equal to 350, it continues to retrieve the hadith data until the length is less than 350. Finally, it returns a JSON response containing the retrieved hadith data.
    """
    data = data['hadith'][0]['body']
    return data

@csrf_exempt
def get_random_hadith(request):
    """
    Generate a random hadith and return it as a JSON response.
    @param request - the HTTP request
    @return a JSON response containing a random hadith
    """
    data = get_hadith()    
    while len(data) >= 350:
        data = get_hadith()
        print(len(data))
    return JsonResponse({'hadith': data})


@csrf_exempt
def setting(request):
    """
    This function handles a POST request to update the settings. It retrieves the values from the request and updates the corresponding fields in the Data object. It also calculates the time difference between the user-selected date and time and the current time. After saving the updated data, it retrieves the Data object again and calculates the scheduled time based on the current time and the time difference. Finally, it renders the 'setting.html' template with the updated data.
    """
    if request.method == "POST":
        hadith = request.POST.get('hadith')
        data = Data.objects.get(ip="127.0.0.1")
        data.hadith = hadith.strip()
        notice = request.POST.get('notice')
        data.notice = notice.strip()

        data.fajarAdhan = request.POST.get('fajarAdhan', '').strip()
        data.fajarIqama = request.POST.get('fajarIqama', '').strip()
        # data.fajarEnds = request.POST.get('fajarEnds', '').strip()
        data.duhurAdhan = request.POST.get('duhurAdhan', '').strip()
        data.duhurIqama = request.POST.get('duhurIqama', '').strip()
        # data.duhurEnds = request.POST.get('duhurEnds', '').strip()
        data.asarAdhan = request.POST.get('asarAdhan', '').strip()
        data.asarIqama = request.POST.get('asarIqama', '').strip()
        # data.asarEnds = request.POST.get('asarEnds', '').strip()
        data.maghribAdhan = request.POST.get('maghribAdhan', '').strip()
        data.maghribIqama = request.POST.get('maghribIqama', '').strip()
        # data.maghribEnds = request.POST.get('maghribEnds', '').strip()
        data.ishaAdhan = request.POST.get('ishaAdhan', '').strip()
        data.ishaIqama = request.POST.get('ishaIqama', '').strip()
        # data.ishaEnds = request.POST.get('ishaEnds', '').strip()

        data.sunrise = request.POST.get('sunrise', '').strip()
        data.sunset = request.POST.get('sunset', '').strip()

        data.audio = request.POST.get('audio', '').strip()
        data.school = request.POST.get('school', '').strip()
        data.zipcode = request.POST.get('zipcode', '').strip()
        data.city = request.POST.get('city', '').strip()
        data.country = request.POST.get('country', '').strip()
        data.location = request.POST.get('location', '').strip()
        
        user_date_time = request.POST.get('user_date', '').strip()
        user_date_time = datetime.datetime.strptime(user_date_time, '%Y-%m-%dT%H:%M')  # Convert string to datetime object

        data.user_date_time = user_date_time

        current_time = datetime.datetime.now()
        time_difference = user_date_time - current_time
        
        data.time_difference = time_difference
        data.save()
    data = Data.objects.get(ip="127.0.0.1")
    user_date_time = data.user_date_time
    
    current_time = datetime.datetime.now()
    scheduled_time = current_time + data.time_difference

    user_date_time = scheduled_time.strftime("%Y-%m-%dT%H:%M")

    user_date_time_obj = data  # Assuming you have stored the user's data
    current_time = datetime.datetime.now()
    scheduled_time = current_time + user_date_time_obj.time_difference

    # user_date_time = datetime.datetime.strptime(scheduled_time, '%Y-%m-%dT%H:%M')  # Convert string to datetime object

    # print(user_date_time)
    return render(request , 'setting.html', {
        'hadith': data.hadith,
        'notice': data.notice,
        'azan': data.audio,
        'fajrAdhan': data.fajarAdhan,
        'fajrIqama': data.fajarIqama,
        'fajrEnds': data.fajarEnds,
        'duhurAdhan': data.duhurAdhan,
        'duhurIqama': data.duhurIqama,
        'duhurEnds': data.duhurEnds,
        'asarAdhan': data.asarAdhan,
        'asarIqama': data.asarIqama,
        'asarEnds': data.asarEnds,
        'maghribAdhan': data.maghribAdhan,
        'maghribIqama': data.maghribIqama,
        'maghribEnds': data.maghribEnds,
        'ishaAdhan': data.ishaAdhan,
        'ishaIqama': data.ishaIqama,
        'ishaEnds': data.ishaEnds,
        'sunrise': data.sunrise,
        'sunset': data.sunset,
        'audio': data.audio,
        'school': data.school,
        'zipcode': data.zipcode,
        'city': data.city,
        'country': data.country,
        'location': data.location,
        'user_date_time': user_date_time
    })

