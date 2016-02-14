#! /usr/bin/python3


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

BASE_URL='http://de.wikipedia.org/w/api.php'

def projects():
    for p in project_list.plist:
        yield p

def cache_list(name,f):
    fn = name+"_shelve"
    if not os.path.isfile(fn) :
        sd = shelve.open(fn)
        for x in f():
            sd[x]=1
        return sd
    else:
        return shelve.open(fn)

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

    for p in projects():
        for k in api.query_all(p):
            if k['ns'] == 0:
                
                if k['title'] not in seen:
                    name = k['title']
                    seen[name] = 1


                    if name in sd:
                        print ("Processed " + name)
                        continue
                    else:
                        print ("NEW " + name)

                    (langs,c) = api.query_langlinks(k['pageid'])
                    #pprint.pprint(langs)
                    site = wapi.langlookup[opt['lang']]
                    (wikidata,cookie2) = wd.wbgetentities( name , site)
                    wd.session.cookie.update(cookie2)
                    sd[name]=1
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
                                                print ("\tTo diff " + x + " : '" + oname + "' != '" + old + "'")
                                        else:
                                            if "#" in oname:
                                                # some subpage
                                                pass
                                            else:
                                                print ("\tTo add " + x + " : " + oname + " lang " )
                                                try:
                                                    r = wd.wbeditentity_new_item(oname, olang, x)                                         
                                                except Exception as e:
                                                    print (e)
                                                #exit(0)
                                                time.sleep(10)
                time.sleep(1)

if __name__ == "__main__":
    main()

