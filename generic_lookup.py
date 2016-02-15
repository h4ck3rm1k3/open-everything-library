#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys
sys.path.append('/home/h4ck3rm1k3/experiments/requests/')
import time
import requests
import json
import shelve
import pprint
import secrets;
import time
import logging
import sitematrix

langlookup = sitematrix.getnames()
#pprint.pprint(langlookup)

dry_run = True
debug = 0
if debug:
    # Enabling debugging at http.client level (requests->urllib3->http.client)
    # you will see the REQUEST, including HEADERS and DATA, and RESPONSE with HEADERS but without DATA.
    # the only thing missing will be the response.body which is not logged.
    try: # for Python 3
        from http.client import HTTPConnection
    except ImportError:
        from httplib import HTTPConnection
    HTTPConnection.debuglevel = 1

    logging.basicConfig() # you need to initialize logging, otherwise you will not see anything from requests
    logging.getLogger().setLevel(logging.DEBUG)
    requests_log = logging.getLogger("requests.packages.urllib3")
    requests_log.setLevel(logging.DEBUG)
    requests_log.propagate = True

class Session:

    def login(self, user, passw, token=None, cookies=None):
        params = {
            'action': 'login',
            'format' : 'json',
            'lgname' : user,
            'lgpassword' : passw,
        }
        if token :
            params['lgtoken']=token
        if cookies:
            r = requests.post(self.source.baseurl, params=params, cookies=cookies)
        else:
            r = requests.post(self.source.baseurl, params=params)
        t = r.text
        #print ("login text: " + t)
        d = json.loads(t)
        #print ("logged: ")
        #pprint.pprint(d)
        return (d,r.cookies)

    def dologin(self):
        d = self.login (
            secrets.generic[self.source.baseurl]['user'],
            secrets.generic[self.source.baseurl]['password'],
        )
        token=d[0]
        cookies=d[1]
        d = self.login (
            secrets.generic[self.source.baseurl]['user'],
            secrets.generic[self.source.baseurl]['password'],
            token['login']['token'],
            cookies,
        )
        self.token = d[0]['login']['lgtoken']
        self.cookie = d[1]

    def get_token(self):
        self.dologin()
        #pprint.pprint(cookies)
        (crsft,cookies2) = self.source.query_tokens()
        #pprint.pprint(cookies2)
        edit_cookie = self.cookie.copy()
        edit_cookie.update(cookies2)
        #pprint.pprint(edit_cookie)
        pprint.pprint(crsft)
        #pprint.pprint(crsft['query']['tokens'])
        csrftoken = crsft['query']['tokens']['csrftoken']
        print ("CRSF token" + csrftoken)
        self.cookie=edit_cookie
        self.token =csrftoken

    def __init__(self, source) :
        self.source=source
        self.cookie = None
        self.token = None
        
class WikimediaApi :
    
    DEFAULT_BASE_URL2='http://directory.fsf.org/w/api.php'
    DEFAULT_BASE_URL='https://www.wikidata.org/w/api.php'
    def __init__(self, baseurl=DEFAULT_BASE_URL):
        self.baseurl = baseurl
        self.session = Session(self)

    def pprocess(self,r):
        t = r.text
        try:
            d = json.loads(t)
            if 'error' in d:
                pprint.pformat(r)
                raise Exception(pprint.pformat(d))
            return (d, r.cookies)

        except Exception as e:
            print ("error: " + t + " Err "+ str(e))
            raise e

    def process(self, params):
        return self.pprocess(
            requests.get(
                self.baseurl, 
                params=params, 
                cookies=self.session.cookie))


    def post(self, body):
        try:
            #print("Cookies")
            #pprint.pprint(cookies)
            rs= requests.post(
                self.baseurl,
                #headers = {
                #    'content-type': 'application/json'
                #},
                data=body,
            #json=body,
                cookies=self.session.cookie)
            return self.pprocess(rs)
            #cookies.update(rs.cookies)
            #return r
        except Exception as e:
            pprint.pprint(body)
            raise e

    def query_tokens (self, meta = 'tokens'):
        action = 'query'

        params = {
            'format' : 'json',
            'type' : 'csrf', #|deleteglobalaccount|patrol|rollback|setglobalaccountstatus|userrights|watch
            'action' : action,
            'meta' : meta,
        }
        return self.process(params)



    def query_langlinks (self, pageids, 
                         #meta = 'siteinfo',
               prop = 'langlinks'):
        action = 'query'
        params = {
            'action' : action,
            'format' : 'json',
            #'meta' : meta,
            'pageids' : pageids,
            'prop' : prop,
        }
        return self.process(params)

    def query_external (self, euquery, cont = None, namespace=None, _list = 'exturlusage'):
        action = 'query'
        params = {
            'action' : action,
            'list' : _list,
            # 'prop' : "|".join(
            #     [
            #         'extlinks', 
            #         'iwlinks', 
            #         'langlinks', 
            #         'links', 
            #         'pageprops', 
            #         'pageterms'
            #     ]
            # ),
            'format' : 'json',
            'eulimit': 500,
            'euexpandurl' : 1,
            'euquery' : euquery,
            'generator' : 'allpages'

            #&format=jsonfm
        }
        if namespace :
            params['apnamespace']=namespace

        if cont :
            params.update(cont)

        return self.process(params)


    def query_all (self, x):
        lastContinue = {'continue': ''}
    
        while True :
            print ("#Going to process " + x)
            (r,c) = self.query_external(x, lastContinue, namespace=0)

            count = 0
            if 'query' in r:
                if 'exturlusage' in r['query']:
                    for k in r['query']['exturlusage']:
                        #print (x, k['ns'], k['pageid'], k['title'], k['url'])
                        yield(k)
                        count = count +1
            if count == 0:
                # no new items found
                break
            if 'error' in r: raise Error(r['error'])
            if 'warnings' in r: print(r['warnings'])
            lastContinue = r['continue']

class WikidataApi (WikimediaApi ):

    BASEURL='https://www.wikidata.org/w/api.php'

    def wbcreateclaim (entity,
                       _property,
                       snaktype,
                       value):
        action = 'wbcreateclaim'

        params = {
            #'utf8': '',
            'value': json.dumps({
                'entity-type':'item',
                'numeric-id': value
            }),
            #'bot': '',
            'action' : action,
            'entity' : entity,
            'format' : 'json',
            'property' : _property,
            'snaktype' : snaktype,
            #'value' : value,
            'token': token,
        }

        return post(self.baseurl,params)

    def wbcreateclaim_instance_of_FreeSoftware (
            entity,
            _property = 'P31',
            snaktype = 'value',
            value = 341): # Q341 is free software
        return wbcreateclaim (entity, _property,snaktype,value)

    def wbcreateclaim_instance_of_Wikimedia_category (
            entity,
            _property = 'P31',
            snaktype = 'value',
            value = 4167836):
        return wbcreateclaim (entity, _property,snaktype,value)

    def wbgetentities(self, x, sites = 'enwiki'):
        params = {
            'action': 'wbgetentities',
            'sites' : sites,
            'titles' : x,
            'redirects': 'yes',
            'format' : 'json',
            'props': 'info|sitelinks|aliases|labels|descriptions|claims|datatype'
        }
        return self.process(params)

    def wbgetentities_by_id(self, x):

        params = {
            'action': 'wbgetentities',
            'ids' : x,
            'redirects': 'yes',
            'format' : 'json',
            'props': 'info|sitelinks|aliases|labels|descriptions|claims|datatype'
        }
        return self.process(params)


    def check_claims(self,d, site):
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
                        #print ("to add: " +x)
                        #wbcreateclaim_instance_of_Wikimedia_category(e,csrftoken,edit_cookie)
                        #                    time.sleep(5)
                        return e
                    else:
                        #pprint.pprint(ed)
                        #print ("Ok"+ x)
                        return 1

    def wbeditentity_new_item (
            self,
            name,
            lang,
            site
    ):
        action = 'wbeditentity'
        bot = '1'
        maxlag = '5'
        _format = 'json'
        _assert = 'user'
        new = 'item',
        summary = 'Bot: New item with sitelink from [[wikipedia:{lang}:{name}]]'.format(name=name,lang=lang)
        data = {
            "labels": 
            {
                lang: 
                {
                    "value": name, 
                    "language": lang
                }
            }, 
            "sitelinks": 
            {
                site: 
                {
                    "site": site, 
                    "title": name
                }
            }
        }

        params = {
            'action' : action,
            'maxlag' : maxlag,
            'format' : _format,
            'new' : new,
            'assert' : _assert,
            'bot' : bot,
            'token' : self.session.token,
            'summary' : summary,
            'data' : json.dumps(data)
        }
        return self.post(params)

    def add_instance(self, x):
        if x not in sd:
            print ("fetch new " + x)
            (d,c) = wbgetentities(x)
            time.sleep(1)
            sd[x]=d
        else:
            d=sd[x]
        e = check_claims(d)
        if e and e != 1:
            print ("fetch check: " + x)
            (d,c) = wbgetentities(x)
            sd[x]=d
            time.sleep(1)
            e= check_claims(d) # check again after fetch
            if e and e != 1:
                print ("To Fix: "+ x)
                wbcreateclaim_instance_of_Wikimedia_category(e)
                (d,c) = wbgetentities(x)
                sd[x]=d
                time.sleep(10)
                return d
            else:
                return d
        else:
            print ("Ok:"+ x)
            return d

    def check_entity(self, sc, site):
        e = self.check_claims(d, site)
        if e is None:
            print ("#Missing, adding: " + sc )
            #sd[sc]=d # save it
            self.session.cookie.update(cookie2)
            try :
                if not dry_run:
                    r = self.wbeditentity_new_item(sc, site)
                    time.sleep(15)
                else:
                    print ("#skipping in dry run: " + sc )
            except Exception as e:
                print ("Error" + sc, e)

def main():
    pass

if __name__ == "__main__":
    main()
