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
filename_pattern = re.compile(r'gem_[\w\-]+\.json')
            
def scan_files():
    dirname = 'sources/ruby/'
    files = os.listdir(dirname)
    
    for x in files:
        if filename_pattern.match(x):
            yield dirname + x
        else:
            print ("skip", x)

# {'authors': 'Yuya Takeyama',
#  'bug_tracker_uri': None,
#  'dependencies': {'development': [{'name': 'bundler',
#                                    'requirements': '~> 1.6'},
#                                   {'name': 'rake', 'requirements': '>= 0'},
#                                   {'name': 'test-unit',
#                                    'requirements': '>= 0'}],
#                   'runtime': []},
#  'documentation_uri': 'http://www.rubydoc.info/gems/get_in/0.0.1',
#  'downloads': 423,
#  'gem_uri': 'https://rubygems.org/gems/get_in-0.0.1.gem',
#  'homepage_uri': 'https://github.com/yuya-takeyama/get_in',
#  'info': "Get a value from nested Hash like Clojure's get-in.",
#  'licenses': ['MIT'],
#  'mailing_list_uri': None,
#  'metadata': {},
#  'name': 'get_in',
#  'platform': 'ruby',
#  'project_uri': 'https://rubygems.org/gems/get_in',
#  'sha': '2cb8eb120759df2e2504b2ba13514f5be466fe0c3520aeed32bee6cd6c64b1eb',
#  'source_code_uri': None,
#  'version': '0.0.1',
#  'version_downloads': 423,
#  'wiki_uri': None}

def process_file(fn):
    if (os.path.isfile(fn)):

        f = codecs.open(fn,'r',"utf-8")
        t = f.read()
        if 'This rubygem could not be found' in t:
            print ("Skipping", fn)
            return
        d= json.loads(t)

        #pprint.pprint(d)
        n = d['name']
        n = n.replace(".","_")
        for m in d['metadata']:
            if '.' in m: 
                print ("metadata",  m)
                m2 = m.replace(".","_")
                t= d['metadata'][m]
                del d['metadata'][m]
                d['metadata'][m2]=t
        #print ("check",n)
        try:
            c.ruby.add(n,d)
        except pymongo.errors.DuplicateKeyError as e:
            pass # dont care
        
def process_files():
    for f in scan_files():
        process_file(f)

#c.ruby.load()
process_files()


