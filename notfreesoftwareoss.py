#! /usr/bin/python3
import time
import sys
#sys.path.append("../sparql-client")
#sys.path.append("../eventlet")
sys.path.append("../sparqlwrapper")

#import sparql
#import SPARQLWrapper
from SPARQLWrapper import SPARQLWrapper, JSON

import wikidatabase_lookup as wb 

q = """
PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX wdt: <http://www.wikidata.org/prop/direct/>
PREFIX wikibase: <http://wikiba.se/ontology#>
PREFIX p: <http://www.wikidata.org/prop/>
PREFIX v: <http://www.wikidata.org/prop/statement/>
PREFIX q: <http://www.wikidata.org/prop/qualifier/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX psv: <http://www.wikidata.org/prop/statement/value/>
prefix schema: <http://schema.org/>
select ?item
WHERE
{
FILTER fn:not(EXISTS { ?item wdt:P31 wd:Q341 }).   
?item wdt:P31 wd:Q1130645.
}
"""
#LIMIT 100

# to add P31 Q341 instance of free software

def check_claims(d):
    if 'entities' in d:
        if '-1' in d['entities']:
            #print ("todo: " +x)
            return None
        else:
            for e in d['entities']:
                if not e:
                    continue
                ed = d['entities'][e]
                #for c in ed['claims']:
                if 'P31' not in ed['claims']:
                    print ("to add: instance of")
                    #wbcreateclaim_instance_of_Wikimedia_category(e,csrftoken,edit_cookie)
                    #                    time.sleep(5)
                    return e
                else:
                    for item in ed['claims']['P31']:
                        if 'mainsnak' in item :
                            if 'datavalue' in item['mainsnak']:
                                if 'value' in item['mainsnak']['datavalue']:
                                    if 'numeric-id' in item['mainsnak']['datavalue']['value']:
                                        value = item['mainsnak']['datavalue']['value']['numeric-id']
                                        if value == 341:
                                            print ("Ok")
                                            return 1 # found it!
                    # did not find it
                    print ("No free software found")
                    return e
sd = {}

def add_instance(x, s):
    if x not in sd:
        print(("fetch new " + x))
        (d,c) = wb.wbgetentities_by_id(x)
        s.cookie.update(c)
        time.sleep(1)
        sd[x]=d
    else:
        d=sd[x]
    e = check_claims(d)
    if e and e != 1:
        print(("fetch check: " + x))
        (d,c) = wb.wbgetentities_by_id(x)
        s.cookie.update(c)
        sd[x]=d
        time.sleep(1)
        e= check_claims(d) # check again after fetch
        if e and e != 1:
            print(("To Fix: "+ x))
            wb.wbcreateclaim_instance_of_FreeSoftware(e,s.token,s.cookie)
            (d,c) = wb.wbgetentities_by_id(x)
            s.cookie.update(c)
            #sd[x]=d
            time.sleep(20)
            #exit(0)
            return d
        else:
            return d
    else:
        print(("Ok:"+ x))
        return d

import logging
logging.basicConfig()
endpoint = 'https://query.wikidata.org/sparql'
sparql = SPARQLWrapper(endpoint)
sparql.setQuery(q)
sparql.setReturnFormat(JSON)
#sparql.setMethod(method)

import pprint
import load_cat_pages_into_wikidata as ld

try:
    s = ld.Session()
    result = sparql.query()
    #result = sparql.query(, q)
    results = result.convert()
    #pprint.pprint(results)
    for row in results['results']['bindings']:
        print('row:', row['item']['value'])
        qid=row['item']['value']
        qid = qid.replace('http://www.wikidata.org/entity/','')
        add_instance(qid, s)

except Exception as e:
    print("error")
    print(e)
    print(str(e))
