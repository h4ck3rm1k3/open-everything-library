#!/usr/bin/python3
# -*- coding: utf-8 -*-


#import MySQLdb
#import pywikibot
import time

#site = pywikibot.Site('wikidata','wikidata')
#header = 'Test\n'
#query1="";
#import sys
#sys.path.append('/home/h4ck3rm1k3/experiments/requests/')
import requests
import json
import shelve
sd = shelve.open("wikidatacats_shelve")


def wanted():
    filename = 'data/allcats.txt'
    f = open(filename)
    count = 0
    for l in f.readlines():
        l = l.replace("\n","")
        if l.startswith("#"):
            next
        else:
            yield "Category:" +l
    f.close()

def makeReport(db,query):
    cursor = db.cursor()
    cursor.execute(query)
    text = ''
    #for val, cnt in cursor:
        #text += table_row.format(val,('{:,}'.format(cnt)))
    return text

def api_lookup(x):
    url='https://www.wikidata.org/w/api.php'
    params = {
        'action': 'wbgetentities',
        'sites' : 'enwiki',
        'titles' : x,
        'format' : 'json',
        'props': ''
    }
    r = requests.get(url, params=params)
    t = r.text
    d = json.loads(t)
    sd[x]=d
    print ("done: " +x)


# select * from category where cat_title like '%Wikibooks%'limit 10;
# select * from categorylinks where cl_to like '%Wikibooks%'limit 10;

def main():
    #page = pywikibot.Page(site,'Wikidata:Database reports/User preferences')
    #db = MySQLdb.connect(host="wikidatawiki.labsdb",db="wikidatawiki_p", read_default_file="~/replica.my.cnf")
    for x in wanted():
        if x not in sd:
            api_lookup(x)
        else:
            d = sd[x]
            if '-1' in d['entities']:
                print ("todo: " +x)

    #report1 = makeReport(db,query1)
    #report2 = makeReport(db,query2)
    #report3 = makeReport(db,query3)
    #text = header.format(time.strftime("%H:%M, %d %B %Y (%Z)")) + subheader1 + report1 + subfooter + subheader2 +report2 + subfooter + subheader3 + report3 +subfooter + footer
    #page.put(text.decode('UTF-8'),comment='Bot:Updating database report',minorEdit=False)

if __name__ == "__main__":
    main()
