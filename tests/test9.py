def get_random_hadith():
    import http.client
    import json

    conn = http.client.HTTPSConnection("api.sunnah.com")

    payload = "{}"

    headers = { 'x-api-key': "SqD712P3E82xnwOAEOkGd5JZH8s9wRR24TqNFzjk" }

    conn.request("GET", "/v1/hadiths/random", payload, headers)

    res = conn.getresponse()
    data = res.read()

    data = json.loads(data.decode("utf-8"))
    data = data['hadith'][0]['body']
    return data

print(get_random_hadith())