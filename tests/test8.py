import requests
import json
import random
from datetime import date

# global variable to store the current date and Hadith
current_date = None
current_hadith = None

def get_hadith_of_the_day():
    global current_date
    global current_hadith

    # check if we have already retrieved a Hadith today
    if current_date == date.today():
        return current_hadith

    # if not, retrieve a new Hadith
    response = requests.get("https://api.hadith.sutanlab.id/books/bukhari?range=1-7000")
    data = json.loads(response.text)
    hadiths = data['data']['hadiths']
    
    # randomize the order of hadiths
    random.shuffle(hadiths)
    
    for hadith in hadiths:
        # assuming the 'content' field contains the Hadith text
        if len(hadith['content']) <= 200:
            current_hadith = hadith
            break

    # store the current date
    current_date = date.today()

    return current_hadith

print(get_hadith_of_the_day())