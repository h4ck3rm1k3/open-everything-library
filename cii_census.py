#!/usr/bin/python3
import sys
import csv
import pprint
import json
import codecs
import time
import os
import argparse
# from

import funcs
c = funcs.Context()
ofa = funcs.BigWrapper(c.db.ciicensus,"project_name")
ofa.load()

input_f = 'sources/cii-census/results.csv'

seen = {}
print ("Reading file", input_f)
f = open(input_f)
d = csv.DictReader(f, dialect=csv.excel, delimiter=",")
for y in d:
    #pprint.pprint(y)
    k = y['project_name']
    if k not in seen :
        seen[k]=1
        if "." in k:    
            k2 = k.replace(".","_")
        ofa.add(k,y)
