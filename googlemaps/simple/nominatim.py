import json
import urllib.request

class Nominatim(object):
    def __init__(self):
      pass

    def getNominatimCityID(self, city):
        url = "http://nominatim.openstreetmap.org/search?q="+urllib.request.quote(city)+"&polygon_geojson=1&format=json"
        response = urllib.request.urlopen(url)
        responseBody = response.read()
        responseJSON = json.loads(responseBody.decode("utf-8"))

        boundary = []
        lat = 0
        lon = 0
        for obj in responseJSON:
            if 'type' in obj:
                print("Type=", obj["type"])
                if obj["type"] == "city" or obj["type"] == "administrative":
                    lat = float(obj["lat"])
                    lng = float(obj["lon"])
                    boundaryJSON = {
                        "geojson" : 
                        {
                            "type" : "Feature", "geometry" : obj["geojson"]                                        
                        },
                        "location" :
                        {
                            "lat" : lat, 
                            "lng" : lng 
                        },
                        "label" : city
                    }
                    boundary.append(boundaryJSON)

        return boundary

    def processCities(self, cities):
   
        center = {"lat" : 0.0, "lng" : 0.0}
        coors = []
        boundariesGeo = {"type" : "FeatureCollection", "features" : []}
        boundariesInfo = {"labels" : [], "locations" : []}
        numCities = int(0)

        # Prepare a mega object
        boundaries = {
            "geojson" : boundariesGeo,
            "info" : boundariesInfo,
            "center" : center
        }
        
        if cities == None:
            return boundaries

        for city in cities:
            boundary = self.getNominatimCityID(city)
            if len(boundary) != 0:
                for bound in boundary:
                    boundariesGeo["features"].append(bound["geojson"])
                    boundariesInfo["labels"].append(bound["label"])
                    boundariesInfo["locations"].append(bound["location"])
                    center["lat"] = center["lat"] + bound["location"]["lat"]
                    center["lng"] = center["lng"] + bound["location"]["lng"]
                    print("City", city, bound["location"]["lat"], bound["location"]["lng"])
                    numCities = numCities + 1
        if numCities != 0:
            center["lat"] = center["lat"] / numCities
            center["lng"] = center["lng"] / numCities
        else:
            center["lat"] = 55.755826
            center["lng"] = 37.6173

        print("Number of Cities = ", numCities)
        
        return boundaries
