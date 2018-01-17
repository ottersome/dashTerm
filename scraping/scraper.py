#!/usr/bin/env python3
from bs4 import BeautifulSoup
import urllib.request,urllib.error, urllib.parse
import time
from random import randint
import json
import logging
class Scraper:
    
    def scrapeNews(quers):
        time.sleep(randint(0,1))
        a = (('hl','en'),('q',quers),('tbm','nws'))
        final_url = "http://www.google.com.tw/search?"+urllib.parse.urlencode(a)
        r = urllib.request.Request(final_url, headers={'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(urllib.request.urlopen(r).read(),'html.parser')
        container  = soup.find("div",{"class":"g"})
        link= container.find('a',href=True)
        link = "https://www.google.com.tw"+link['href']
        #link = link['href'][7:]
        st_divs = container.find("div",{"class":"st"})
        return (quers,st_divs.text,link)

    def scrapeTweets(quers):
        time.sleep(randint(0,1))
        a = (('q',quers),('src','typd'))
        final_url = "https://twitter.com/search?"+urllib.parse.urlencode(a)
        logging.debug("FINAL FURL : "+final_url)
        r = urllib.request.Request(final_url, headers={'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(urllib.request.urlopen(r).read(),'html.parser')
        contexto = soup.find("div",{"class":"tweet"})
        tweettext = contexto.find("p",{"class":"tweet-text"})
    
        username = contexto['data-screen-name']
        url = "https://twitter.com"+contexto['data-permalink-path']
        
        return((quers,username,tweettext.text,url))
        

