#! /usr/bin/python3
import funcs
import pprint

def main():
    start_url = 'http://web.archive.org/web/20150905085354/https://lists.debian.org/debian-wnpp/'
    c = funcs.Context()
    u = start_url
    
    if u in c.extern.data:
        del c.extern.data[u]
    funcs.extern(c, u, 10)
    d = c.extern.load_one(c)
    pprint.pprint(d)

main()
