import urllib.request
    
def getCityCoordinates(city):
    url = "http://maps.googleapis.com/maps/api/geocode/json?address=" + city
    response = urllib.request.urlopen(url)
    responseBody = response.read()
    obj = json.loads(responseBody.decode("utf-8"))
    location = obj['results'][0]['geometry']['location']
    return location
