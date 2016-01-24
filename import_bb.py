#!/usr/bin/python3

import pymongo
import pprint 
import funcs

import re
import pprint
import os
import requests
import os.path
import json
import time
import codecs
import sys

c = funcs.Context()
bb = funcs.BigWrapper(c.db.bitbucket,"full_name")

filename_pattern = re.compile(r'projects_\d+.html')

def scan_files():
    dirname = 'sources/bitbucket/'
    files = os.listdir(dirname)
    
    for x in files:
        if filename_pattern.match(x):
            yield dirname + x


def process_file(fn):  
    
    if (os.path.isfile(fn)):
        print("opening",fn)
        f = codecs.open(fn,'r',"utf-8")
        t = f.read()
        d= json.loads(t)

        for x in d['values']:

            n = x['full_name']
            try :
                print("Process", n)
                #pprint.pprint(x)
                bb.add(n,x)
            except pymongo.errors.DuplicateKeyError as e:
                pass # dont care
            except Exception as e:
                print ("Error",n)
                print (e)
                raise e

def process_files():
    for f in scan_files():
        process_file(f)

process_files()
