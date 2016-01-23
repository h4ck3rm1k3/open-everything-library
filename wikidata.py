import sys
import time
#sys.path.append('/mnt/data/home/mdupont/experiments/rdflib/build/lib')
import urllib
import pymongo
import funcs
c = funcs.Context()


import rdflib
from rdflib import URIRef, Graph, Namespace
from rdflib.plugins.parsers.notation3 import N3Parser
import pprint

def prefix(s, prefix, url):
    return s.replace(url, prefix + "_")
    
def clean(s):
    
    s= prefix(s, 'cc', "http://creativecommons.org/ns#")
    s= prefix(s, 'geo', "http://www.opengis.net/ont/geosparql#")
    s= prefix(s, 'owl', "http://www.w3.org/2002/07/owl#")
    s= prefix(s, 'p', "http://www.wikidata.org/prop/")
    s= prefix(s, 'pq', "http://www.wikidata.org/prop/qualifier/")
    s= prefix(s, 'pqv', "http://www.wikidata.org/prop/qualifier/value/")
    s= prefix(s, 'pr', "http://www.wikidata.org/prop/reference/")
    s= prefix(s, 'prov', "http://www.w3.org/ns/prov#")
    s= prefix(s, 'prv', "http://www.wikidata.org/prop/reference/value/")
    s= prefix(s, 'ps', "http://www.wikidata.org/prop/statement/")
    s= prefix(s, 'psv', "http://www.wikidata.org/prop/statement/value/")
    s= prefix(s, 'rdf', "http://www.w3.org/1999/02/22-rdf-syntax-ns#")
    s= prefix(s, 'rdfs', "http://www.w3.org/2000/01/rdf-schema#")
    s= prefix(s, 'schema', "http://schema.org/")
    s= prefix(s, 'skos', "http://www.w3.org/2004/02/skos/core#")
    s= prefix(s, 'wd', "http://www.wikidata.org/entity/")
    s= prefix(s, 'wdata', "https://www.wikidata.org/wiki/Special:EntityData/")
    s= prefix(s, 'wdno', "http://www.wikidata.org/prop/novalue/")
    s= prefix(s, 'wdref', "http://www.wikidata.org/reference/")
    s= prefix(s, 'wds', "http://www.wikidata.org/entity/statement/")
    s= prefix(s, 'wdt', "http://www.wikidata.org/prop/direct/")
    s= prefix(s, 'wdv', "http://www.wikidata.org/value/")
    s= prefix(s, 'wikibase', "http://wikiba.se/ontology-beta#")
    s= prefix(s, 'xsd',  "http://www.w3.org/2001/XMLSchema#")
    
    #s = s.replace("-3A","_")
    #s = s.replace("-2A","_")
    #s = s.replace(":","_")
    return s

def clean2(s):
    s = s.replace('http://www.w3.org/1999/02/22-rdf-syntax-ns#','')
    s = s.replace('http://localhost/wiki/Special:URIResolver/',"")
    s = s.replace('http://semantic-mediawiki.org/swivt/1.0#','')
    s = s.replace('http://www.w3.org/2000/01/rdf-schema#','')
    s = s.replace('http://www.w3.org/2002/07/owl#','')
    s = s.replace('http://localhost/wiki/','')
    s = s.replace('file:///mnt/newdrive2/home/mdupont/experiments/open-everything-library/sources/fsd/','')


    return s

def store(k,v):
    #pass
    c.wikidata.add(k,v)

def process(data, want):
    g = Graph(identifier="test")
    
    prefix = """
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix owl: <http://www.w3.org/2002/07/owl#> .
    @prefix wikibase: <http://wikiba.se/ontology-beta#> .
    @prefix wdata: <https://www.wikidata.org/wiki/Special:EntityData/> .
    @prefix wd: <http://www.wikidata.org/entity/> .
    @prefix wds: <http://www.wikidata.org/entity/statement/> .
@prefix wdref: <http://www.wikidata.org/reference/> .
@prefix wdv: <http://www.wikidata.org/value/> .
@prefix wdt: <http://www.wikidata.org/prop/direct/> .
@prefix p: <http://www.wikidata.org/prop/> .
@prefix ps: <http://www.wikidata.org/prop/statement/> .
@prefix psv: <http://www.wikidata.org/prop/statement/value/> .
@prefix pq: <http://www.wikidata.org/prop/qualifier/> .
@prefix pqv: <http://www.wikidata.org/prop/qualifier/value/> .
@prefix pr: <http://www.wikidata.org/prop/reference/> .
@prefix prv: <http://www.wikidata.org/prop/reference/value/> .
@prefix wdno: <http://www.wikidata.org/prop/novalue/> .
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .
@prefix schema: <http://schema.org/> .
@prefix cc: <http://creativecommons.org/ns#> .
@prefix geo: <http://www.opengis.net/ont/geosparql#> .
@prefix prov: <http://www.w3.org/ns/prov#> .
"""

    #s = clean(s)
    result = g.parse(data=prefix + data, format="turtle")
    ob = {
    }
        
    for s2,p,o in g:
        if isinstance(o,rdflib.term.Literal):
            if o.language:
                if o.language == 'en':
                    #print (o)
                    pass
                else:
                    continue # skip other languages
                
        o = clean2(o)
        p = clean(p).replace("Property_","")            
        ob['__subject']=s2
        
        if p in ob:
            ob[p].append(o)
        else:
            ob[p] = [o]

    # process the object

    if '__subject' in ob:
        s = ob['__subject']
        if 'https://en.wikipedia.org/wiki/' in  s:
            s = s.replace('https://en.wikipedia.org/wiki/','')
            s = urllib.parse.unquote(s)            
            if s in want:
                store(s,ob)
                #pprint.pprint(ob)
        elif 'wikidata' in  s:
            if 'rdfs_label' in ob:

                #pass
                for l in ob['rdfs_label']:
                    if l in want:
                        store(s,ob)
                        pprint.pprint(ob)
                        continue
        else:
            pass
                
    else:
        pass
        #pprint.pprint(ob)
import bz2


def scan_stdin(want):
    k = 0
    try:
        buff = ''
        f  = bz2.BZ2File('sources/wikidata/wikidata-20160111-all-BETA.ttl.bz2')
        while True:
            buff += f.readline().decode('utf8')
            if buff.endswith("\n\n"):
                process( buff[:-1], want)
                buff = ''
                k = k + 1

    except KeyboardInterrupt:
       sys.stdout.flush()
       pass

def load_wanted():
    wanted = {}
    for p in c.pages.pages.db.find({},{'title':1}):
        #print (p)
        wanted[p['title']]=p['_id']
    return wanted

scan_stdin(load_wanted())
