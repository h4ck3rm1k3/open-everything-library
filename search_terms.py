import time
import sys
import pprint
import results

sys.path.append('libs/PyOrgMode/') #'git@github.com:h4ck3rm1k3/PyOrgMode.git'
sys.path.append('libs/python-duckduckgo/')#  git clone git@github.com:h4ck3rm1k3/python-duckduckgo.git
#2112  git clone git@github.com:h4ck3rm1k3/extraction.git
sys.path.append('libs/Wikipedia/')# #git clone git@github.com:goldsmith/Wikipedia.git
sys.path.append('libs/yacybot/')#  #git clone git@github.com:h4ck3rm1k3/yacybot.git

sys.path.append('libs/py-web-search')
sys.path.append('libs/extraction')

import YaCyQuery
from pws import Google
from pws import Bing   
from PyOrgMode import PyOrgMode
import wikipedia

import six

from urlparse import urlparse, urlunparse
import duckduckgo
import urllib, urllib2

import requests
from extraction import Extractor
import codecs
import os.path


def wp(x):

    f = open("results_wikipedia.py","a")
    print( "#" + x)
    f.write( "#" + x + "\n")
    f.write(    "WikipediaResult(")
    results = wikipedia.search(x)
    d = pprint.pformat(results)
    print d
    f.write(d)
    f.write( ")\n")
    f.close()  

    
def yacy(x):
    query = YaCyQuery.YaCyQuery("search.yacy.de","80", "\"" + x + "\"")
    numresults = query.request()
    numresults  = 10;
    if len(query.results)> 0 :
        f = open("results_yacy2.py","a")
        print( "#" + x)
        f.write( "#" + x + "\n")
        f.write(    "YacyResult(")
        d = pprint.pformat(query.results)
        print d
        f.write(d)
        f.write( ")\n")
        f.close()  
  
def dduck (x):
    f = open("dduck_results2.py","a")
    print( "#" + x)
    f.write( "#" + x + "\n")
    q = duckduckgo.query(x)
    f.write(    "NewResult(")
    f.write(    pprint.pformat ({ x : (q.json)}))
    f.write( ")\n")
    f.close()

def s_google(x):

    f = open("results_google2.py","a")
    print( "#" + x)
    f.write( "#" + x + "\n")
    #q = duckduckgo.query(x)
    f.write(    "GoogleResult(")
    y = Google.search(query=x, num=100, start=1, country_code="us")
    print y
    f.write(    pprint.pformat ({ x : (y)}))
    f.write( ")\n")
    f.close()
    time.sleep(3)

def s_bing(x):
    f = open("results_bing2.py","a")
    print( "#" + x)
    f.write( "#" + x + "\n")
    #q = duckduckgo.query(x)
    f.write(    "BingResult(")
    y = Bing.search(query=x, num=100, start=1, country_code="us")
    print y
    f.write(    pprint.pformat ({ x : (y)}))
    f.write( ")\n")
    f.close()
    time.sleep(3)


import fileinput

def search (x):
    #s_bing(x)
    #s_google(x)
    #dduck(x)
    #yacy(x)
    wp(x)
    
for line in fileinput.input():
    line = line.replace("\n","")
    print "'%s'" % line
    search(line)
