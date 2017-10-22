# -*- coding: utf-8 -*-
import os
from django.core.management.base import BaseCommand, CommandError
from django.template.loader import render_to_string
import sys
from simple import nominatim
from simple import lang

import urllib.request
import bs4

from django.http import HttpResponse
from django.template import loader
import json


def GetArticle(url):
    # Read HTML article
    response = urllib.request.urlopen(url)
    article = response.read()

    return article

def Parse(article):
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

    # Analyz the info

    analysis = lang.Analysis()
    cities = analysis.findCities(core.get_text())
    print("Cities = ", set(cities))

    engine = nominatim.Nominatim()
    result = engine.processCities(set(cities))

    context = {'result': json.dumps(result)}
    #template = loader.get_template('simple/simplified_map.js')

    script = render_to_string('simple/simplified_map.js', context)

    new_script = soup.new_tag("script")
    new_script["src"] = "https://maps.googleapis.com/maps/api/js?key=AIzaSyBQxn1ZTFWJlmIb0oWeHwfL8_Sbr7YJvOY&callback=initMap"
    new_script2 = soup.new_tag("script")
    new_script2.append(script)
    last_script.insert_after(new_script2)
    new_script2.insert_after(new_script)

    html = soup.prettify("utf-8")
    with open("output.html", "wb") as file:
        file.write(html)


class Command(BaseCommand):
    help = 'Processes the article to include there a map'

    def handle(self, *arg, **options):
        #url = "http://montrealgazette.com/travel/checking-in-eastern-townships-farmbb-dishes-up-barn-to-fork-cuisine"
        #url = "http://montrealgazette.com/travel/checking-in-updated-novotel-is-hot-ticket-to-bell-centre"
        #url = "http://montrealgazette.com/travel/small-but-mighty-malta-island-nation-just-below-sicily-turning-into-an-increasingly-popular-stopover/wcm/0fe5e05f-5eb7-49a2-b145-7c6ce096a3ee"
        #url = "http://montrealgazette.com/news/local-news/montreal-elections-coderre-pledges-parity-plante-wonders-what-took-so-long"
        #url = "http://montrealgazette.com/news/local-news/projet-montreal-changes-its-tune-on-cavendish-blvd-extension"
        #url = "http://montrealgazette.com/news/local-news/projet-montreal-vows-to-transform-pool-parking-lot-into-mount-royal-paradise"
        #url = "http://montrealgazette.com/news/local-news/projet-montreal-pledges-to-tackle-dangerous-intersections-in-year-1"
        #url = "http://montrealgazette.com/news/local-news/painted-lady-butterflies-experience-remarkable-migration-to-montreal-area"
        #url = "http://montrealgazette.com/news/local-news/fentanyl-deaths-coalition-lashes-out-against-systemic-barriers-as-overdoses-soar-in-montreal"
        #url = "http://montrealgazette.com/life/social-notes-an-f1-grand-prix-fairy-tale-come-true"
        url = "http://montrealgazette.com/opinion/columnists/celine-cooper-montreal-has-much-to-offer-amazon-as-hq2"
        article = GetArticle(url)
        #print("Article = ", article)
        Parse(article)
    



