#! /usr/bin/python3
import bz2
import rdflib
from rdflib import URIRef, Graph, Namespace

filepath = "data/fsfd/directory.xml.bz2"
with open(filepath, 'rb') as file:
    decompressor = bz2.BZ2Decompressor()
    for data in iter(lambda : file.read(100 * 1024), b''):
        d = decompressor.decompress(data)
        d=d.decode('utf8')

        state = 0
        obj = ""
        for l in d.split("\n"):
            #print (l)
            if '<swivt:Subject' in l:
                state =1 
                obj = obj + l
            elif '</swivt:Subject>' in l:
                state =0
                obj = obj + l                
                #print ("Done " + obj)
                obj = ""
            elif state == 1:
                obj = obj + l                
            else:
                #print ('skip' + str(state) + " :" + l)
                pass
            
