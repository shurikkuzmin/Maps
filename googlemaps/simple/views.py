from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
import urllib.request
import json

def getOSMCityID(city):
    url = "http://overpass-api.de/api/interpreter?data=[out:json];area[name=\"" + city + "\"];foreach(out;);"
    response = urllib.request.urlopen(url)
    responseBody = response.read()
    obj = json.loads(responseBody.decode("utf-8"))
    
    xLocation = 0.0
    yLocation = 0.0
    numNodes = 0
    coors = []
    for res in obj['elements']:
        if "admin_level" in res["tags"]:
            adminCity = int(res["tags"]["admin_level"]) 
            if adminCity == 8:
                nodes = dict()
                ways = dict()
                initOrder = []

                idCity = int(res["id"])
                relCity = idCity - 3600000000
                print("Relation = ", relCity)

                urlCity = "http://overpass-api.de/api/interpreter?data=[out:json];(relation(" + str(relCity) + ");>;);out;"
                responseCity = urllib.request.urlopen(urlCity)
                responseCityBody = responseCity.read()
                objCity = json.loads(responseCityBody.decode("utf-8"))

                for node in objCity["elements"]:
                    if "type" in node:
                        if node["type"] == "node" and "lat" in node and "lon" in node:
                            nodes[node["id"]] = (node["lat"], node["lon"])    
                        if node["type"] == "way" and "nodes" in node:
                            ways[node["id"]] = node["nodes"]
                        if node["type"] == "relation":
                            rels = node["members"]
                            for rel in rels:
                                if rel["type"] == "way":
                                    initOrder.append(rel["ref"])

                order = []
                directions = []
                if len(initOrder) > 0:
                    for way in initOrder:
                        if way in order:
                            continue
                        currentWay = way
                        order.append(way)
                        directions.append(True)
                        currentNode = ways[currentWay][-1]
                        while currentWay != -1:
                            wayFound = False
                            for otherWay in initOrder:
                                if (currentNode == ways[otherWay][0]) and (currentWay != otherWay) and (not otherWay in order):
                                    wayFound = True
                                    order.append(otherWay)
                                    currentWay = otherWay
                                    currentNode = ways[otherWay][-1]
                                    directions.append(True)
                                    break
                                if (currentNode == ways[otherWay][-1]) and (currentWay != otherWay) and (not otherWay in order):
                                    wayFound = True
                                    order.append(otherWay)
                                    currentWay = otherWay
                                    currentNode = ways[otherWay][0]
                                    directions.append(False)
                                    break
                            if not wayFound:
                                currentWay = -1
                localCoors = []
                for ind, way in enumerate(order):
                    direction = directions[ind]
                    coorsWay = []
                    if direction == True:
                        for node in ways[way]:
                            numNodes = numNodes + 1
                            localCoors.append([nodes[node][0], nodes[node][1]])
                            xLocation = xLocation + nodes[node][0]
                            yLocation = yLocation + nodes[node][1]
                    else:
                        for node in ways[way][::-1]:
                            numNodes = numNodes + 1
                            localCoors.append([nodes[node][0], nodes[node][1]])
                            xLocation = xLocation + nodes[node][0]
                            yLocation = yLocation + nodes[node][1]
                coors.append(localCoors)
    print("Coors = ",coors)
    print("Len(coors) = ", len(coors))
    if numNodes != 0:
        xLocation = xLocation / numNodes
        yLocation = yLocation / numNodes
    location = dict()
    location["lat"] = xLocation
    location["lng"] = yLocation    
    return location, coors
    
def getCityCoordinates(city):
    url = "http://maps.googleapis.com/maps/api/geocode/json?address=" + city
    response = urllib.request.urlopen(url)
    responseBody = response.read()
    obj = json.loads(responseBody.decode("utf-8"))
    location = obj['results'][0]['geometry']['location']
    return location

def index(request):
    city = "Saint-Hubert"
    location, coors = getOSMCityID(city)
    #location = getCityCoordinates(city)
    template = loader.get_template('simple/index.html')
    
    context = {'location': location, 'paths' : coors}

    return HttpResponse(template.render(context, request))

