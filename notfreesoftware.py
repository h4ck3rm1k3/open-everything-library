import sys
#sys.path.append("../sparql-client")
#sys.path.append("../eventlet")
sys.path.append("../sparqlwrapper")

#import sparql
#import SPARQLWrapper
from SPARQLWrapper import SPARQLWrapper, JSON


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
    ?item p:P1324 ?stmt.
    ?stmt v:P1324 ?url_node.
    FILTER fn:not(EXISTS { ?item wdt:P31 wd:Q341 }).   
    FILTER isIRI(?url_node).
    FILTER regex(str(?url_node), "github")
   SERVICE wikibase:label {
     bd:serviceParam wikibase:language "en" .
   }
}
LIMIT 100
"""


import logging
logging.basicConfig()
endpoint = 'https://query.wikidata.org/sparql'
sparql = SPARQLWrapper(endpoint)
sparql.setQuery(q)
sparql.setReturnFormat(JSON)
#sparql.setMethod(method)

import pprint

try:
    result = sparql.query()
    #result = sparql.query(, q)
    results = result.convert()
    pprint.pprint(results)
    for row in results['results']:
        print 'row:', pprint.pformat(row)

except Exception as e:
    print "error"
    print e
    print str(e)
