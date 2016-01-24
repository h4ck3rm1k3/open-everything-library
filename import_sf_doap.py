#!/usr/bin/python3
        #!/usr/bin/python3

import pymongo
import pprint 
import funcs

import re
import pprint
import os
import requests
import os.path
import json
import time
import codecs
import sys
import pymongo
import pprint 
import funcs
import json

import rdflib
from rdflib import URIRef, Graph, Namespace
from rdflib.plugins.parsers.notation3 import N3Parser
import pprint

namespaces = {
    'beer' : 'http://www.purl.org/net/ontology/beer.owl#',
    'doap' : 'http://usefulinc.com/ns/doap#',
    'foaf' : 'http://xmlns.com/foaf/0.1/',
    'sf' : 'http://sourceforge.net/api/sfelements.rdf#',
    'owl'  : "http://www.w3.org/2002/07/owl#",
    'rdf'  : "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
    'rdfs' : "http://www.w3.org/2000/01/rdf-schema#",
    'dc' : 'http://dublincore.org/documents/dcmi-namespace/',
}

def clean(s):
    for ns in namespaces:
        u = namespaces[ns]
        s = s.replace(u,ns + '_')
    return s

c = funcs.Context()
sink = funcs.BigWrapper(c.db.sfnet,"dc_title")
sink.db.create_index("dc_title")

filename_pattern = re.compile(r'.+')
            
def scan_files():
    dirname = 'sources/sf.net/doap/'
    files = os.listdir(dirname)
    for x in files:
        if filename_pattern.match(x):
            yield dirname + x

def parse(data):
    g = Graph(identifier="test")
    result = g.parse(data=data)
    ob = {    }
    s = None
    for s2,p,o in g:
        s = s2
        o = clean(o)
        p = clean(p).replace("Property_","")
        if p in ob:
            ob[p].append(o)
        else:
            ob[p] = [o]
    ob['__source__'] = s
    n = ob['dc_title'][0]
    try :
        #pprint.pprint(n)
        #pprint.pprint(ob)
        sink.add(n,ob)
    except pymongo.errors.DuplicateKeyError as e:
        pass # dont care
    except Exception as e:
            print ("Error",s)
            print (e)
            raise e

def process_doap(f):
    t = ""
    data = ""
    for l in f.readlines():
        data = data + l
    parse(data)


def process_file(fn):      
    if (os.path.isfile(fn)):
        print("opening",fn)
        f = codecs.open(fn,'r',"utf-8")
        d= process_doap(f)


def process_files():
    for f in scan_files():
        process_file(f)

process_files()
