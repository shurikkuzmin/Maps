from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
import urllib.request
import json
import numpy
import pymorphy2
from . import places
from . import nominatim
from . import lang

def index(request):
    template = loader.get_template('simple/index.html')
    context = {}

    return HttpResponse(template.render(context, request))

def process_text(request):
    article_text = ""
    cities = []
    analysis = lang.Analysis()
    if request.method == "POST":
        if "article_text" in request.POST:
            article_text = request.POST["article_text"]

    cities = analysis.findCities(article_text)

    engine = nominatim.Nominatim()

    result = engine.processCities(cities)

    context = {'article_text': article_text, 'geos': cities, 'result': json.dumps(result)}
    template = loader.get_template('simple/text_process.html')
    
    return HttpResponse(template.render(context, request))
