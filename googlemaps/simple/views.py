# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.template import loader, Template, Context
from django.core import serializers
from django.template.loader import render_to_string
import urllib.request
import json
import pymorphy2
import bs4
from . import places
from . import nominatim
from . import lang

import re

from .models import MontrealGazetteArticle

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

def montreal_gazette(request):
    template = loader.get_template('simple/montreal_gazette.html')
    context = {}
    return HttpResponse(template.render(context, request))

def process_gazette(request):
    
    url_post = None
    if "url-montreal-gazette" in request.POST:
        url_post = request.POST["url-montreal-gazette"]
    #else 
    #   return montreal_gazette(request)

    # Uncomment if you want to get a slug
    #pattern = re.compile("/[^/]*$")
    #slug_url_list = pattern.findall(url_post)

    #if len(slug_url_list) > 0:
    #    slug_url = slug_url_list[0][1:]
    #else:
    #    return montreal_gazette(request)
    print("URL = ", url_post)
    try:
        article = MontrealGazetteArticle.objects.get(url = url_post)
        html = article.modified_text
    except MontrealGazetteArticle.DoesNotExist:
        # Get right now the article

        response = urllib.request.urlopen(url_post)
        article = response.read()

        soup = bs4.BeautifulSoup(article.decode("utf-8"), "html.parser")
        core = soup.find(itemprop="articleBody")
    
        paragraphs = core.find_all("p")

        num = len(paragraphs)
        median = paragraphs[int(num/2)]

        # Create a new tag
        tag = soup.new_tag("p")
        tag.append(soup.new_tag("div"))
        tag.div["id"] = "map"
        tag.div["style"] = "height: 500px;"
        median.insert_after(tag)

        # Add right now a proper script
        first_script = soup.script
        last_script = soup.find_all("script")[-1]

        # Analyze the info

        analysis = lang.Analysis()
        cities = analysis.findCities(core.get_text())
        print("Cities = ", set(cities))

        engine = nominatim.Nominatim()
        result = engine.processCities(set(cities))

        context = {'result': json.dumps(result)}

        script = render_to_string('simple/simplified_map.js', context)

        new_script = soup.new_tag("script")
        new_script["src"] = "https://maps.googleapis.com/maps/api/js?key=AIzaSyBQxn1ZTFWJlmIb0oWeHwfL8_Sbr7YJvOY&callback=initMap"
        new_script2 = soup.new_tag("script")
        new_script2.append(script)
        last_script.insert_after(new_script2)
        new_script2.insert_after(new_script)

        html = soup.prettify("utf-8")
        processed_article = MontrealGazetteArticle()
        processed_article.url = url_post
        processed_article.original_text = article
        processed_article.modified_text = html
        processed_article.save()

    webpage = Template(html)
    context = Context()
    return HttpResponse(webpage.render(context))


    # Analyze url

    print(request.POST['url-montreal-gazette'])
    #except:
    #    pass
    template = loader.get_template('simple/process_gazette.html')
    context = {}
    return HttpResponse(template.render(context, request))

def view_montreal_gazette(request, slug):
    template = loader.get_template('simple/view_gazette.html')
    article = get_object_or_404(MontrealGazetteArticle, slug = slug)
    context = {"slug" : slug}
    return HttpResponse(template.render(context, request))

def jason(request):
    template = loader.get_template('simple/jason_cavendish.html')
    context = {}
    return HttpResponse(template.render(context, request))

def kevin(request):
    template = loader.get_template('simple/kevin_butteflies.html')
    context = {}
    return HttpResponse(template.render(context, request))

def charlie(request):
    template = loader.get_template('simple/charlie_overdose.html')
    context = {}
    return HttpResponse(template.render(context, request))

def jennifer(request):
    template = loader.get_template('simple/jennifer_grandprix.html')
    context = {}
    return HttpResponse(template.render(context, request))

def celine(request):
    template = loader.get_template('simple/celine_amazon.html')
    context = {}
    return HttpResponse(template.render(context, request))



