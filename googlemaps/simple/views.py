from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
import urllib.request
import json
import nltk
import numpy
from . import places


def index(request):
    #city = "Brossard"
    #location = getCityCoordinates(city)
    template = loader.get_template('simple/index.html')
    context = {}

    return HttpResponse(template.render(context, request))


def process_text(request):
    article_text = ''
    cities = []
    realCities = []
    if request.method == 'POST':
        if "article_text" in request.POST:
            article_text = request.POST["article_text"]

            print("Text = ",article_text)

            text = nltk.word_tokenize(article_text)
            chunks = nltk.ne_chunk(nltk.pos_tag(text))

            #article_text = chunks.pprint()
            for chunk in chunks:
                if len(chunk) == 1:
                    if (chunk.label() == "GPE" or chunk.label() == "GEO") and (chunk[0][1] == "NNP"):
                        cities.append(chunk[0][0])

        # Activate below if you want to get additional information about cities and countries it belongs to
        #db = places.Places()
        #realCities = db.findCities(cities)

    print("Cities = ", cities)

    cities = numpy.array(cities)
    #realCities = cities[numpy.where(realCities == True)]

    location = {"lat": 0.0, "lng": 0.0}
    coors = []
    boundaries = {"type": "FeatureCollection", "features": []}
    numCities = int(0)
    cities = ["Орел"]
    for city in cities:
        #Old and not effective method with the boundary reconstruction
        #location, coors = getOSMCityID(city)
        boundary = getNominatimCityID(city)
        if len(boundary) != 0:
            for bound in boundary:
                boundaries["features"].append(bound)
                location["lat"] = location["lat"] + bound["lat"]
                location["lng"] = location["lng"] + bound["lng"]
                print("City",city,bound["lat"], bound["lng"])
                numCities = numCities + 1
    if numCities != 0:
        location["lat"] = location["lat"] / numCities
        location["lng"] = location["lng"] / numCities
    print("Number of Cities = ", numCities)
    #print("Dump = ", json.dumps(boundaries).encode("ascii", errors = "ignore"))
    context = {'article_text': article_text, 'geos': cities, 'location': location, 'paths' : coors, 'boundaries': json.dumps(boundaries).encode("ascii", errors = "ignore")}
    template = loader.get_template('simple/text_process.html')
    return HttpResponse(template.render(context, request))
