# -*- coding: utf-8 -*-
import json
import urllib.request

class Nominatim(object):
    def __init__(self):
      pass

    def getNominatimGeoID(self, geo_object):
        url = "http://nominatim.openstreetmap.org/search?q="+urllib.request.quote(geo_object)+"&polygon_geojson=1&format=json"
        response = urllib.request.urlopen(url)
        responseBody = response.read()
        responseJSON = json.loads(responseBody.decode("utf-8"))

        boundary = []
        lat = 0
        lon = 0
        for obj in responseJSON:
            if 'type' in obj:
                print("Type=", obj["type"])
                if obj["type"] == "city" or obj["type"] == "administrative" or obj["type"] == "town" or obj["type"] == "village" or obj["type"] =="hamlet":
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
                        "label" : geo_object,
                        "type" : obj["type"]
                    }
                    boundary.append(boundaryJSON)

        return boundary

    def processCities(self, geo_objects):
   
        center = {"lat" : 0.0, "lng" : 0.0}
        coors = []
        boundariesAdmins = {"type" : "FeatureCollection", "features" : []}
        boundariesCities = {"type" : "FeatureCollection", "features" : []}
        boundariesVillages = {"type" : "FeatureCollection", "features" : []}
        boundariesInfo = {"labels" : [], "locations" : []}
        numObjs = int(0)

        # Prepare a mega object
        boundaries = {
            "admins" : boundariesAdmins,
            "cities" : boundariesCities,
            "villages" : boundariesVillages,
            "info" : boundariesInfo,
            "center" : center
        }
        
        if geo_objects == None:
            return boundaries

        for geo_object in geo_objects:
            boundary = self.getNominatimGeoID(geo_object)
            if len(boundary) != 0:
                for bound in boundary:
                    if bound["type"] == "administrative":
                        boundariesAdmins["features"].append(bound["geojson"])
                    elif bound["type"] == "city":
                        boundariesCities["features"].append(bound["geojson"])
                    else: 
                        boundariesVillages["features"].append(bound["geojson"])
                    boundariesInfo["labels"].append(bound["label"])
                    boundariesInfo["locations"].append(bound["location"])
                    center["lat"] = center["lat"] + bound["location"]["lat"]
                    center["lng"] = center["lng"] + bound["location"]["lng"]
                    print("Geo Object", geo_object, bound["type"], bound["location"]["lat"], bound["location"]["lng"])
                    numObjs = numObjs + 1
        if numObjs != 0:
            center["lat"] = center["lat"] / numObjs
            center["lng"] = center["lng"] / numObjs
        else:
            center["lat"] = 55.755826
            center["lng"] = 37.6173

        print("Number of Objects = ", numObjs)
        
        return boundaries
