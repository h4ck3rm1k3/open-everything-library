#! /usr/bin/python3
import bz2
import rdflib
from rdflib import URIRef, Graph, Namespace
import pprint
import time
import requests
import json
import shelve
import os.path
import pprint
import project_list
import generic_lookup as wapi
import sys
import getopt

BASE_URL='http://en.wikipedia.org/w/api.php'

def one_object(ob):
    pass
    # rdflib.term.URIRef('http://localhost/wiki/Special:URIResolver/Property-3AModification_date-23aux'): [
    #     rdflib.term.Literal('2457284.2121065', datatype=rdflib.term.URIRef('http://www.w3.org/2001/XMLSchema#double'))
    # ],
    # rdflib.term.URIRef('http://semantic-mediawiki.org/swivt/1.0#page'): [rdflib.term.URIRef('http://localhost/wiki/Main_Page')],
    # rdflib.term.URIRef('http://semantic-mediawiki.org/swivt/1.0#specialProperty_ASK'): [
    #     rdflib.term.URIRef('http://localhost/wiki/Special:URIResolver/Main_Page-23_QUERY1e27cbc531b46f4199a93f484c9d8f17'),
    #     rdflib.term.URIRef('http://localhost/wiki/Special:URIResolver/Main_Page-23_QUERY0ad07097595841c2fa233109cb832835'),
    #     rdflib.term.URIRef('http://localhost/wiki/Special:URIResolver/Main_Page-23_QUERY62a20cb97fc228dc739d9bc6541bef61'),
    #     rdflib.term.URIRef('http://localhost/wiki/Special:URIResolver/Main_Page-23_QUERY818d33f01555e8b63c35c6bda7569b66'),
    #     rdflib.term.URIRef('http://localhost/wiki/Special:URIResolver/Main_Page-23_QUERY93e690d9e04d7d457ed07ba202702a83'),
    #     rdflib.term.URIRef('http://localhost/wiki/Special:URIResolver/Main_Page-23_QUERY675b9af23ef7b2632f2792c74a3d27cd'),
    #     rdflib.term.URIRef('http://localhost/wiki/Special:URIResolver/Main_Page-23_QUERY62768d38eb858b9dd5c1209b28274a32'),
    #     rdflib.term.URIRef('http://localhost/wiki/Special:URIResolver/Main_Page-23_QUERY53cdcf78d496802a399eed849bfacc8f'),
    #     rdflib.term.URIRef('http://localhost/wiki/Special:URIResolver/Main_Page-23_QUERYd4af894fe0a7ae55a0efe99f1ea669c6'),
    #     rdflib.term.URIRef('http://localhost/wiki/Special:URIResolver/Main_Page-23_QUERY4b92620e5c2c0dd8862d33b76a1bbc99'),
    #     rdflib.term.URIRef('http://localhost/wiki/Special:URIResolver/Main_Page-23_QUERY9f8bb732b91d10d0ff4fd9efc73aaa2b'),
    #     rdflib.term.URIRef('http://localhost/wiki/Special:URIResolver/Main_Page-23_QUERY3a85410a01a720e821224adb0ebe4b79')],
    # rdflib.term.URIRef('http://semantic-mediawiki.org/swivt/1.0#wikiNamespace'): [rdflib.term.Literal('0', datatype=rdflib.term.URIRef('http://www.w3.org/2001/XMLSchema#integer'))],
    # rdflib.term.URIRef('http://semantic-mediawiki.org/swivt/1.0#wikiPageModificationDate'): [rdflib.term.Literal('2015-09-18T17:05:26+00:00', datatype=rdflib.term.URIRef('http://www.w3.org/2001/XMLSchema#dateTime'))],
    # rdflib.term.URIRef('http://semantic-mediawiki.org/swivt/1.0#wikiPageSortKey'): [rdflib.term.Literal('Main Page', datatype=rdflib.term.URIRef('http://www.w3.org/2001/XMLSchema#string'))],
    # rdflib.term.URIRef('http://www.w3.org/1999/02/22-rdf-syntax-ns#type'): [rdflib.term.URIRef('http://semantic-mediawiki.org/swivt/1.0#Subject')],
    # rdflib.term.URIRef('http://www.w3.org/2000/01/rdf-schema#isDefinedBy'): [rdflib.term.URIRef('http://localhost/wiki/Special:ExportRDF/Main_Page')],
    # rdflib.term.URIRef('http://www.w3.org/2000/01/rdf-schema#label'): [rdflib.term.Literal('Main Page')]}

ns_rdf   =Namespace('http://www.w3.org/1999/02/22-rdf-syntax-ns#')
ns_rdfs  =Namespace( 'http://www.w3.org/2000/01/rdf-schema#')
ns_owl   =Namespace( 'http://www.w3.org/2002/07/owl#')
ns_swivt =Namespace( 'http://semantic-mediawiki.org/swivt/1.0#')
ns_wiki  =Namespace( 'http://localhost/wiki/Special:URIResolver/')
ns_property =Namespace( 'http://localhost/wiki/Special:URIResolver/Property-3A')
ns_wikiurl  =Namespace( 'http://localhost/wiki/')

rdfs_label = ns_rdfs['label']
p_Homepage_URL = ns_property['Homepage_URL']

class Project :
    def __init__(self, g):
        self.g = g
        for s in g.subjects():
            self.s = s

    def label(self):
        return self.g.label(self.s)

    def homepage(self):
        return self.g.value(self.s,p_Homepage_URL)


def process(obj):
    # process one rdf object
    g = Graph(identifier="test")
    #s = clean(s)
    #print ("Parse:"+ obj)
    result = g.parse(data=obj)
    yield Project(g)

def read_file():
    filepath = "data/fsfd/directory.xml.bz2"
    #filepath = "data/fsfd/test.xml.bz2"
    #with open(filepath, 'rb') as file:

    obj = ""
    state = 0
    header = """<?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE rdf:RDF[
            <!ENTITY rdf 'http://www.w3.org/1999/02/22-rdf-syntax-ns#'>
            <!ENTITY rdfs 'http://www.w3.org/2000/01/rdf-schema#'>
            <!ENTITY owl 'http://www.w3.org/2002/07/owl#'>
            <!ENTITY swivt 'http://semantic-mediawiki.org/swivt/1.0#'>
            <!ENTITY wiki 'http://localhost/wiki/Special:URIResolver/'>
            <!ENTITY property 'http://localhost/wiki/Special:URIResolver/Property-3A'>
            <!ENTITY wikiurl 'http://localhost/wiki/'>
    ]>
    <rdf:RDF
            xmlns:rdf="&rdf;"
            xmlns:rdfs="&rdfs;"
            xmlns:owl ="&owl;"
            xmlns:swivt="&swivt;"
            xmlns:wiki="&wiki;"
            xmlns:property="&property;">
    """

    trailer = """</rdf:RDF>"""

    count = 0

    for l in bz2.BZ2File(filepath, 'rb', 1000 * 1000) :
        l=l.decode('utf8')

        #print ("Check line: " + l)
        if '<swivt:Subject' in l:
            state =1 
            obj = l
        elif '</swivt:Subject>' in l:
            state =0
            obj = obj + l                
            #print ("Done " + obj)
            yield process(header + obj + trailer)
            count = count + 1
            obj = ""
        elif state == 1:
            obj = obj + l                
        else:
            #print ('skip' + str(state) + " :" + l)
            #if count == 0:
                #header = header + l
            pass
            

def process_link(api, wapi, opt, link, seen, sd, wd):
    for k in api.query_all(link): # links
        if k['ns'] == 0:
            if k['title'] not in seen:
                name = k['title']
                seen[name] = 1

                if name in sd:
                    print ("\tProcessed " + name + " for " + link)
                    continue
                else:
                    print ("\tNEW " + name + " for " + link)
                    sd[name]=1

                (langs,c) = api.query_langlinks(k['pageid'])
                #pprint.pprint(langs)
                site = wapi.langlookup[opt['lang']]
                (wikidata,cookie2) = wd.wbgetentities( name , site)
                wd.session.cookie.update(cookie2)

                entities = {}
                for e in wikidata['entities']:
                    print ("\tFound Entity" + e)
                    ed = wikidata['entities'][e]
                    if 'sitelinks' in ed:
                        for s in ed['sitelinks']: 
                            sd = ed['sitelinks'][s]
                            ssite = sd['site']
                            stitle = sd['title']
                            #print (ssite, stitle)
                            entities[ssite]=stitle

                if 'query' in langs:
                    if 'pages' in langs['query']:
                        for p in langs['query']['pages']:
                            if 'langlinks' in langs['query']['pages'][p]:
                                for links in langs['query']['pages'][p]['langlinks']:
                                    #pprint.pprint(links)
                                    oname  =links['*']
                                    olang  =links['lang']

                                    x = wapi.langlookup[olang]
                                    if x in entities :
                                        old  = entities[x]
                                        if old == oname :
                                            # ok
                                            pass
                                        else:
                                            print ("\t\tTo diff " + x + " : '" + oname + "' != '" + old + "'" + " for " + link)
                                    else:
                                        if "#" in oname:
                                            # some subpage
                                            pass
                                        else:
                                            print ("\t\tDouble Check " + x + " : " + oname + " lang " + olang + " for " + link)
                                            osite = wapi.langlookup[olang]
                                            (owikidata,cookie2) = wd.wbgetentities( oname , osite)
                                            exists = False
                                            for e2 in owikidata['entities']:
                                                print ("\tFound Entity" + e2)
                                                ed2 = owikidata['entities'][e2]
                                                if 'sitelinks' in ed2:
                                                    for s2 in ed2['sitelinks']: 
                                                        sd2 = ed2['sitelinks'][s2]
                                                        if  sd2['site'] == osite:
                                                            exists = True
                                                            print ("Found" + oname + ":" + osite)

                                            if not exists :
                                                try:
                                                    print ("\tTo add " + x + " : " + oname + " lang " + olang + " for " + link)
                                                    r = wd.wbeditentity_new_item(oname, olang, x)                                         
                                                    time.sleep(10)
                                                except Exception as e:
                                                    print (e)


def opts():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hsl:v", ["help", "server=", 'lang='])
    except getopt.GetoptError as err:
        # print help information and exit:
        print(err) # will print something like "option -a not recognized"
        usage()
        sys.exit(2)
    server = BASE_URL
    verbose = False
    lang = 'de'
    for o, a in opts:
        if o == "-v":
            verbose = True
        elif o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("-s", "--server"):
             server = a
        elif o in ("-l", "--lang"):
             lang = a
        else:
            assert False, "unhandled option"
    return {
        'server' : server,
        'lang' : lang,
    }

def main():
    opt = opts()
    api = wapi.WikimediaApi(opt['server'])
    wd  = wapi.WikidataApi()
    wd.session.get_token()
    seen = {}
    sd =  shelve.open("wikientities" + opt['lang'] + 'shelve')
    for x in sd:
        print ("Stored"+x)

    for projg in read_file():
        for proj in projg:
            name = proj.label()
            homepage = proj.homepage()
            if homepage:
                homepage = homepage.replace("https://","").replace("http://","")
                print ("\tcheck homepage: " + homepage + " for project " + name)
                process_link(api, wapi, opt, homepage, seen, sd, wd)
                #process_link(wd, wapi, opt, homepage, seen, sd, wd)
  

if __name__ == "__main__":
    main()
