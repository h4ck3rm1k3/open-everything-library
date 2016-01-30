#!/usr/bin/python3
import pymongo
from lxml.html import  html5parser
import getopt
import lxml
import pprint
import subprocess
import sys
import time
import urllib.parse
import urllib.request, urllib.error, urllib.parse

import funcs
c = funcs.Context()
sink = funcs.BigWrapper(c.db.sfcats,"s")
sink.db.create_index("s")

ids = sink.load_ids()

def paths(doc, xpath):

    try:
        r = doc.xpath(
            xpath,
            namespaces={
                'html': 'http://www.w3.org/1999/xhtml'
            })
    except Exception as e:
        print("Check",xpath)
        print(e)
        raise e
    return r

seen = {}

# pprint.pprint(o)
def catfile(f):
    print(("Going to parse %s" % f))
    o = html5parser.parse(f)
    #r = o.getroot()

    obj = {
        'f' : [], # facets
        'p' : [],  # projects
        'd' : [],  # directories
        't' : '',  # title
        'r' : '',  # results
        's' : ''  # source
    }

    for d in paths(o,"//html:title"):
        t = d.text.replace('free download - SourceForge','')
        t = t.replace("\n",'')
        #print(("\tTitle:"+ t))
        obj['t']= t

    for d in paths(o,"//html:p[@id='result_count']"):
        #print(("\tResult_count:"+
        obj['r']= d.text.replace("\n",'').replace('    Showing page ','')

    for d in paths(o,"//*[@href]"):
        h = d.attrib["href"]
        if 'data-action' in d.attrib:
            h = d.attrib['data-action']
            h = h.replace('add_facet_filter?','')
            if '&sort=' not in h:
                if h not in seen:
                    seen[h]=1
                    #q = urllib.parse.unquote(h)
                    #o = urlparse(h)
                    o = urllib.parse.parse_qs(h)
                    obj['f'].append(o)

        if h.startswith("/projec") or h.startswith("/directory") :
            if '&sort=' not in h:
                h = h.replace('?source=directory','')
                if h not in seen:
                    h = h.replace('&amp;','&')
                    h = h.replace('&amp=&','&')
                    
                    seen[h]=1
                    #print(("\t\t"+h))
                    if h.startswith("/projec") :
                        obj['p'].append(h)
                    elif h.startswith("/directory") :
                        obj['d'].append(h)
            else:
                #if obj['s'] != '':                
                if 'sort=score' in h:
                    #s = urllib.parse.unquote(h)
                    #print ("Source in:" +h)
                    #print ("Source in:" +s)
                    h = h.replace('&amp;','&')
                    h = h.replace('&amp=&','&')
                    h = h.replace('&sort=score','')
                    obj['s'] = h
                    print ("Source:" +h)

    s = obj['s']

    # pprint.pprint(
    #         {
    #             'dirs'  : obj['d'],
    #             'projects' :obj['p']
    #         }
    #     )
        
    if s not in ids:
        try :
            sink.add(obj['s'],obj)
        except pymongo.errors.DuplicateKeyError as e:
            print ("skip" + obj['s'])
            pass # dont care
        except Exception as e:
            print ("Error",s)
            print (e)
            raise e
        else:
            print ("added " + obj['s'])
    else:
        print ("update existing" + obj['s'])        
        #sink.update(obj)
            
def scan():
    #d = Path('./pages/')
    print ('going to scan')
    p = subprocess.Popen(
        [
            '/usr/bin/find',
            'sources/sf.net/cats/pages' ,
            '-maxdepth' , '1',
            '-type','f',
        ],
        stdout=subprocess.PIPE,
        bufsize = 1,
        universal_newlines = True
    )

    while p.poll:
        if p.stdout:
            #print ("got out")
            for f in iter(p.stdout.readline, ''):
                f = f.replace("\n","")
                #print( "Check:" + f)
                catfile(f)
        else:
            print ("no out")
            time.sleep(1)

    #for f in d.files('*.html'):

def test():
    catfile('sources/sf.net/cats/pages/_directory__q_fps&amp;amp_&amp;page_10.html')
scan()
#test()
