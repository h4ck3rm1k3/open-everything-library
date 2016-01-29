#!/usr/bin/python3

import pymongo
import pprint 
import funcs
import json
c = funcs.Context()

import rdflib
from rdflib import URIRef, Graph, Namespace
from rdflib.plugins.parsers.notation3 import N3Parser
import pprint
 
f= open("sources/fsd/directory.n3", "r")
t = ""
data = ""

def clean(s):
    s = s.replace('http://www.w3.org/1999/02/22-rdf-syntax-ns#','')
    s = s.replace('http://localhost/wiki/Special:URIResolver/',"")
    s = s.replace('http://semantic-mediawiki.org/swivt/1.0#','')
    s = s.replace('http://www.w3.org/2000/01/rdf-schema#','')
    s = s.replace('http://www.w3.org/2002/07/owl#','')
    s = s.replace('http://localhost/wiki/','')

    s = s.replace('file:///mnt/newdrive2/home/mdupont/experiments/open-everything-library/sources/fsd/','')
    s = s.replace("-3A","_")
    s = s.replace("-2A","_")
    s = s.replace(":","_")

         
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

for l in f.readlines():
    #print l
    p = l.split(" ")
    s = p[0]


    if not s == t:
        
        print("Check",s)
        t = s
        #s= s.replace('>',"")
        #print(s)
        #print (data)

        g = Graph(identifier="test")
        s = clean(s)
        result = g.parse(data=data, format="n3")
        ob = {
            '__subject__' : clean(s)
        }
        
        for s2,p,o in g:           
            o = clean2(o)
            p = clean(p).replace("Property_","")
            
            if p in ob:
                ob[p].append(o)
            else:
                ob[p] = [o]
        #pprint.pprint(ob)
        c.fsd.add(s,ob)
        data =  l
        
    else:
        
        data = data + l
        #print "Data", data
