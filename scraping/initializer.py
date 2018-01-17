#!/usr/bin/env python3
from scraper import Scraper
import pprint
import json
data =json.load(open('../top_artists.json'))
Scraper.scrapeNews('Tom Misch')
'''for item in data:
    print("\nNow Loading : "+item['name'])
    Scraper.scrapeNews('Tom Misch')'''
