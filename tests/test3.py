import requests

def get_city_country_from_zip(zip_code):
    url = f"http://api.zippopotam.us/us/{zip_code}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        city = data["places"][0]["place name"]
        country = data["country"]
        return city, country
    else:
        return None, None

# Example usage
zip_code = "47080"
city, country = get_city_country_from_zip(zip_code)
if city and country:
    print("City:", city)
    print("Country:", country)
else:
    print("Invalid zip code or data not found.")
