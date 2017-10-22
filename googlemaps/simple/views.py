# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.core import serializers
import urllib.request
import json
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

def jason(request):
    template = loader.get_template('simple/jason_cavendish.html')
    context = {}

    return HttpResponse(template.render(context, request))

def kevin(request):
    template = loader.get_template('simple/kevin_butteflies.html')
    context = {}

    return HttpResponse(template.render(context, request))
