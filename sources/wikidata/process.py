import sys
sys.path.append('/mnt/data/home/mdupont/experiments/rdflib/build/lib')

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


def process(data):
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
        o = clean2(o)
        p = clean(p).replace("Property_","")

        if 'http' in p :
            print (p)
            
        ob['__subject']=s2
        
        if p in ob:
            ob[p].append(o)
        else:
            ob[p] = [o]
    #pprint.pprint(ob)
                   

import sys
import time
k = 0
try:
    buff = ''
    while True:
        buff += sys.stdin.read(1)
        if buff.endswith("\n\n"):
            process( buff[:-1])
            buff = ''
            k = k + 1
            
except KeyboardInterrupt:
   sys.stdout.flush()
   pass
