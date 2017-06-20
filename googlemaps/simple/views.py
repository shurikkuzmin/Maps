from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
import urllib.request
import json
import nltk
import numpy
from . import places
from . import nominatim


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


    print("Cities = ", cities)

    cities = numpy.array(cities)
    #realCities = cities[numpy.where(realCities == True)]

    cities = ["Орел"]
    engine = nominatim.Nominatim()

    res = engine.processCities(cities)

    #print("Dump = ", json.dumps(boundaries).encode("ascii", errors = "ignore"))
    #context = {'article_text': article_text, 'geos': cities, 'result': json.dumps(res).encode("ascii", errors = "ignore")}
    context = {'article_text': article_text, 'geos': cities, 'result': json.dumps(res)}
    template = loader.get_template('simple/text_process.html')
    return HttpResponse(template.render(context, request))
