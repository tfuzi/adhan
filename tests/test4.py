from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="mosque-project")
location = geolocator.reverse("33.7215488, 72.8170496", language="en")

if location:
    address = location.raw["address"]
    print(address)
    city = address.get("city", "")
    country = address.get("country", "")
    if not city:
        city = address.get("town", "")
        if not city:
            city = address.get("county", "")
    
    print(city, country)