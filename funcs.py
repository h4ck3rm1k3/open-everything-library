from urllib.parse import urlparse, urlunparse
import codecs
import fileinput
import json
import os.path
import pprint
import requests
#import results
import six
import sys
import time
import urllib.request, urllib.parse, urllib.error, urllib.request, urllib.error, urllib.parse
#from filelock import FileLock
#import pymongo



def lookup(memcache, database, key, obj):
    #pprint.pprint(key)
    #pprint.pprint(obj)
    if key in memcache:
        return True
    else:
        memcache[key]=1
        database.insert(obj)
        print('adding new:', key)
        return False

def load(d,field, alt_fields=None):
    #d = db.pages
    res = {}
    for c in d.find():
        #pprint.pprint(c)
        if field not in c:
            #print "Missing", field, "in", pprint.pformat(c)
            pass
        else:
            cn = c[field]
            res[cn]=c

        if alt_fields:
            for field2 in alt_fields:
                if field2 in c:
                    cn = c[field2]
                    res[cn]=c
    return res

def load_ids(d,field, alt_fields=None):
    res = {}
    flds = { field :1 }
    if alt_fields:
        for field2 in alt_fields:
            flds[field2] =1

    for c in d.find({},flds):
        cn = c[field]
        res[cn]=c
        if alt_fields:
            for field2 in alt_fields:
                if field2 in c:
                    cn = c[field2]
                    res[cn]=c
    return res

def load_data(db, field, target):
    for p in db :
        d = db[p]
        if field in d:
            c = d[field]
            for pg in c:
                target[pg]=1



class Wrapper:
    def __init__(self, db , key, alt_fields=None):
        self.db   = db
        self.data = {}

    def load(self):
        self.data = load(db,key,alt_fields)

    def add(self,k,v):
        return lookup(self.data, self.db, k, v)

class BigWrapper:
    def __init__(self, db , field, alt_fields=None):
        self.db = db
        self.data = {}
        self.field = field
        self.alt_fields = alt_fields

    def load(self):
        for c in self.db.find({},{self.field : 1}):
            if self.field in c:
                cn = c[self.field]
                self.data[cn]=c

    def load_ids(self):
        res = {}
        flds = { self.field :1 }
        if self.alt_fields:
            for field2 in self.alt_fields:
                flds[field2] =1

        for c in self.db.find({},flds):
            cn = c[self.field]
            res[cn]=1
            if self.alt_fields:
                for field2 in self.alt_fields:
                    if field2 in c:
                        cn = c[field2]
                        res[cn]=1
        return res

    def load_last_ids(self):
        res = {}
        flds = { self.field :1 ,
                 "_id" : 1,
        }

        if self.alt_fields:
            for field2 in self.alt_fields:
                flds[field2] =1

                #
        for c in self.db.find({},flds).sort([('_id',-1)]).limit(1):
            cn = c[self.field]
            print ("found last id",cn, pprint.pformat(cn))
            res[cn]=1
            if self.alt_fields:
                for field2 in self.alt_fields:
                    if field2 in c:
                        cn = c[field2]
                        res[cn]=1
        return res


    def load_one(self, k):
        print ("loading", k)
        for c in self.db.find({ self.field : k}):
            self.data[k]=c
            return c
        return None

    def add(self,k,v):
        lookup(self.data, self.db, k, v)

    def update(self, obj):
        key = obj[self.field]
        self.data[key]=1
        self.db.update(
            {
                self.field : key
            },
            obj,
            upsert=True            
        )
        print('updated', key)
        return True

class PageWrapper:
    def __init__(self, pages, redirs):
        self.pages  = pages
        self.redirs = redirs

    def get(self, p2):

        if p2 in  self.pages.data:
            pd = self.pages.data[p2]
            print("found page", p2)
        else:
            if p2 in  self.redirs.data:
                r = self.redirs.data[p2]['to']
                print("follow redirect to ", r)
                return self.get(r)
            else:
                print("missing page", p2)
                fetch_page(p2,self.pages, self.redirs)
            #exit(0)




def categorymembers(cmtype,category):
    url='https://en.wikipedia.org/w/api.php'
    params = {
        'action': 'query',
        'list': 'categorymembers',
        'cmtype': cmtype,
        'cmlimit': 'max',
        'format': 'json',
        'cmtitle': category,
    }

    r = requests.get(url, params=params)
    #pprint.pprint(url)
    #pprint.pprint(params)

    t = r.text
    d = json.loads(t)
    return d

def clean(d):
    #print "clean"
    #pprint.pprint(d)
    if not 'query' in d:
        return []
    _pages = []
    for x in d['query']['categorymembers']:
        t =  x['title']
        _pages.append(t)
    return _pages

def pages(category):
    return clean(categorymembers('page',category))

def subcat(category):
    return clean(categorymembers('subcat',category))


# old = c.db.categories.find_one(
#     {'_id':
#      _id
#     })

# pprint.pprint(old)

# def update():
#     c.db.categories.update(
#         {'_id':
#          _id
#         },
#         {
#             '$set':
#             {
#                 'done': False
#         }
#         }
#     )


# {u'_id': ObjectId('56911021570fd4017fc6c99e'),
#  u'name': u'Category:Open content',
#  u'pages': [u'Open content',
#             u'Openness',
#             u'360Learning',
#],
#  u'subcats': [u'Category:Open access (publishing)',
#]}

import re
skip = (
    '3dml',
    '3g2',
    '3gp',
    '7z',
    'aab',
    'aac',
    'aam',
    'aas',
    'abw',
    'ac',
    'acc',
    'ace',
    'acu',
    'adp',
    'aep',
    'afp',
    'ahead',
    'ai',
    'aif',
    'air',
    'ait',
    'ami',
    'apk',
    'application',
    'apr',
    'asf',
    'aso',
    'atc',
    'atomcat',
    'atomsvc',
    'atx',
    'au',
    'avi',
    'aw',
    'azf',
    'azs',
    'azw',
    'bcpio',
    'bdf',
    'bdm',
    'bed',
    'bh2',
    'bin',
    'bmi',
    'bmp',
    'box',
    'btif',
    'bz',
    'bz2',
    'c11amc',
    'c11amz',
    'c4g',
    'cab',
    'car',
    'cat',
    'ccxml',
    'cdbcmsg',
    'cdkey',
    'cdmia',
    'cdmic',
    'cdmid',
    'cdmio',
    'cdmiq',
    'cdx',
    'cdxml',
    'cdy',
    'cer',
    'cgm',
    'chat',
    'chrt',
    'cif',
    'cii',
    'cil',
    'cla',
    'class',
    'clkk',
    'clkp',
    'clkt',
    'clkw',
    'clkx',
    'clp',
    'cmc',
    'cmdf',
    'cml',
    'cmp',
    'cmx',
    'cod',
    'cpio',
    'cpt',
    'crl',
    'cryptonote',
    'csh',
    'csml',
    'csp',
    'cu',
    'curl',
    'cww',
    'dae',
    'daf',
    'davmount',
    'dcurl',
    'dd2',
    'ddd',
    'deb',
    'der',
    'dfac',
    'dir',
    'dis',
    'djvu',
    'dna',
    'docm',
    'dotm',
    'dp',
    'dpg',
    'dra',
    'dsc',
    'dssc',
    'dtb',
    'dts',
    'dtshd',
    'dvi',
    'dwf',
    'dwg',
    'dxf',
    'dxp',
    'ecelp4800',
    'ecelp7470',
    'ecelp9600',
    'edm',
    'edx',
    'efif',
    'ei6',
    'eml',
    'emma',
    'eol',
    'eot',
#    'epub',
    'es',
    'es3',
    'esf',
    'etx',
    'exe',
    'exe',
    'exi',
    'ext',
    'ez2',
    'ez3',
    'f',
    'f4v',
    'fbs',
    'fcs',
    'fdf',
    'fe_launch',
    'fg5',
    'fh',
    'fig',
    'xdf',
    'fli',
    'flo',
    'flv',
    'flv',
    'flw',
    'flx',
    'fly',
    'fm',
    'fnc',
    'fpx',
    'fsc',
    'fst',
    'ftc',
    'fti',
    'fvt',
    'fxp',
    'fzs',
    'g2w',
    'g3',
    'g3w',
    'gac',
    'gdl',
    'geo',
    'gex',
    'ggb',
    'ggt',
    'ghf',
    'gif',
    'gim',
    'gmx',
    'gnumeric',
    'gph',
    'gqf',
    'gram',
    'grv',
    'grxml',
    'gsf',
    'gtar',
    'gtm',
    'gtw',
    'gv',
    'gxt',
    'h261',
    'h263',
    'h264',
    'hal',
    'hbci',
    'hdf',
    'hlp',
    'hpgl',
    'hpid',
    'hps',
    'hqx',
    'htke',
    'hvd',
    'hvp',
    'hvs',
    'i2g',
    'icc',
    'ice',
    'ico',
    'ief',
    'ifm',
    'igl',
    'igm',
    'igs',
    'igx',
    'iif',
    'imp',
    'ims',
    'ipfix',
    'ipk',
    'irm',
    'irp',
    'itp',
    'ivp',
    'ivu',
    'jad',
    'jam',
    'jar',
    'jisp',
    'jlt',
    'jnlp',
    'joda',
    'jpeg, .jpg',
    'jpgv',
    'jpm',
    'karbon',
    'kfo',
    'kia',
    'kml',
    'kmz',
    'kne',
    'kon',
    'kpr',
    'ksp',
    'ktx',
    'ktz',
    'kwd',
    'lasxml',
    'latex',
    'lbd',
    'lbe',
    'les',
    'link66',
    'lrm',
    'ltf',
    'lvp',
    'lwp',
    'm21',
    'm3u',
    'm3u8',
    'm4v',
    'ma',
    'mads',
    'mag',
    'mathml',
    'mbk',
    'mbox',
    'mc1',
    'mcd',
    'mcurl',
    'mdb',
    'mdi',
    'meta4',
    'mets',
    'mfm',
    'mgp',
    'mgz',
    'mid',
    'mif',
    'mj2',
    'mlp',
    'mmd',
    'mmf',
    'mmr',
    'mny',
    'mods',
    'movie',
    'mp3',
    'mp4',
    'mp4',
    'mp4a',
    'mpc',
    'mpeg',
    'mpga',
    'mpkg',
    'mpm',
    'mpn',
    'mpp',
    'mpy',
    'mqy',
    'mrc',
    'mrcx',
    'mscml',
    'mseq',
    'msf',
    'msh',
    'msl',
    'msty',
    'mts',
    'mus',
    'musicxml',
    'mvb',
    'mwf',
    'mxf',
    'mxl',
    'mxml',
    'mxs',
    'mxu',
    'n-gage',
    'n3',
    'nbp',
    'nc',
    'ncx',
    'ngdat',
    'nlu',
    'nml',
    'nnd',
    'nns',
    'nnw',
    'npx',
    'nsf',
    'oa2',
    'oa3',
    'oas',
    'oda',
    'odb',
    'odc',
    'odf',
    'odft',
    'odg',
    'odi',
    'odm',
    'odp',
    'ods',
#    'odt',
    'oga',
    'ogg',
    'ogv',
    'ogx',
    'opf',
#    'org',
    'osf',
    'osfpvg',
    'otc',
    'otf',
    'otg',
    'oth',
    'oti',
    'otp',
    'ots',
    'ott',
    'oxt',
    'p',
    'p10',
    'p12',
    'p7b',
    'p7m',
    'p7r',
    'p7s',
    'p8',
    'par',
    'paw',
    'pbd',
    'pbm',
    'pcf',
    'pcl',
    'pclxl',
    'pcurl',
    'pcx',
    'pdb',
#    'pdf',
    'pfa',
    'pfr',
    'pgm',
    'pgn',
    'pgp',
    'pic',
    'pki',
    'pkipath',
    'plb',
    'plc',
    'plf',
    'pls',
    'pml',
    'png',
    'pnm',
    'portpkg',
    'potm',
    'ppam',
    'ppd',
    'ppm',
    'ppsm',
    'ppt',
    'pptm',
    'prc',
    'pre',
    'prf',
    'psb',
    'psd',
    'psf',
    'pskcxml',
    'ptid',
    'pub',
    'pvb',
    'pwn',
    'pya',
    'pyv',
    'qam',
    'qbo',
    'qfx',
    'qps',
    'qt',
    'qxd',
    'ram',
    'rar',
    'ras',
    'rcprofile',
    'rdf',
    'rdz',
    'rep',
    'res',
    'rgb',
    'rif',
    'rip',
    'rl',
    'rlc',
    'rld',
    'rm',
    'rmp',
    'rms',
    'rnc',
    'rp9',
    'rpss',
    'rpst',
    'rq',
    'rs',
    'rsd',
    'rtx',
    's',
    'saf',
    'sbml',
    'sc',
    'scd',
    'scm',
    'scq',
    'scs',
    'scurl',
    'sda',
    'sdc',
    'sdd',
    'sdkm',
    'sdp',
    'sdw',
    'see',
    'seed',
    'sema',
    'semd',
    'semf',
    'ser',
    'setpay',
    'setreg',
    'sfd-hdstx',
    'sfs',
    'sgl',
    'shar',
    'shf',
    'sis',
    'sit',
    'sitx',
    'skp',
    'sldm',
    'slt',
    'sm',
    'smf',
    'smi',
    'snf',
    'spf',
    'spl',
    'spot',
    'spp',
    'spq',
    'src',
    'sru',
    'srx',
    'sse',
    'ssf',
    'ssml',
    'st',
    'stc',
    'std',
    'stf',
    'sti',
    'stk',
    'stl',
    'str',
    'stw',
    'sub',
    'sus',
    'sv4cpio',
    'sv4crc',
    'svc',
    'svd',
    'svg',
    'swf',
    'swi',
    'sxc',
    'sxd',
    'sxg',
    'sxi',
    'sxm',
    'sxw',
    't',
    'tao',
    'tar',
    'tcap',
    'tcl',
    'teacher',
    'tei',
    'tfi',
    'tfm',
    'tiff',
    'tmo',
    'torrent',
    'tpl',
    'tpt',
    'tra',
    'trm',
    'tsd',
    'tsv',
    'ttf',
    'ttl',
    'twd',
    'txd',
    'txf',
    'ufd',
    'umj',
    'unityweb',
    'uoml',
    'uri',
    'ustar',
    'utz',
    'uu',
    'uva',
    'uvh',
    'uvi',
    'uvm',
    'uvp',
    'uvs',
    'uvu',
    'uvv',
    'vcd',
    'vcf',
    'vcg',
    'vcs',
    'vcx',
    'vis',
    'viv',
    'vsd',
    'vsf',
    'vtu',
    'vxml',
    'wad',
    'wav',
    'wax',
    'wbmp',
    'wbs',
    'wbxml',
    'weba',
    'webm',
    'webp',
    'wg',
    'wgt',
    'wm',
    'wma',
    'wmd',
    'wmf',
    'wml',
    'wmlc',
    'wmls',
    'wmlsc',
    'wmv',
    'wmx',
    'wmz',
    'woff',
    'wpd',
    'wpl',
    'wqd',
    'wrl',
    'wsdl',
    'wspolicy',
    'wtb',
    'wvx',
    'x3d',
    'xap',
    'xar',
    'xbap',
    'xbd',
    'xbm',
    'xdm',
    'xdp',
    'xdssc',
    'xdw',
    'xenc',
    'xer',
    'xfdf',
    'xfdl',
    'xif',
    'xo',
    'xop',
    'xpi',
    'xpm',
    'xpr',
    'xps',
    'xpw',
    'xslt',
    'xsm',
    'xspf',
    'xul',
    'xwd',
    'xyz',
    'yang',
    'yin',
    'zaz'
    'zip',
    'zip',
    'zir',
    'zmm',
)
# build a res
skip_y = ("\." + x for x in skip)
skip_res = '.+(' +  "|".join( skip_y)  + ")+$"
skip_resre = re.compile(skip_res)

#seen = {}

def extern(c, url, timeout = 1):
    if url  in c.extern.data:
        print ("exists",url)
        return

    print ("loading link",url)

    try:
        resp = requests.head(url, timeout=timeout)
        head = {
            'code': resp.status_code,
            'text' : resp.text,
            'hdrs' :  resp.headers
        };

    except Exception as e:
        pprint.pprint(e)
        c.extern.add(url,
                     {
                         'data': None,
                         'url': url,
                         #'head' : head,
                         'error' : str(e),
                     })
        return None

    clen = 0
    tlen = 0
    if  'Content-Length' in resp.headers:
        tlen = resp.headers['Content-Length']
        g = re.match('(\d+)', tlen)
        clen = 0
        if  g:
            tp = g.groups()[0]
            print(tp, tlen)
            clen = int(tp)

    print("getting size", url, clen, tlen)
          #, pprint.pformat(resp.headers))


    try:
        html = requests.get(url, timeout=1,verify=False, stream=True).text
        head = {
            'code': resp.status_code,
            'text' : resp.text,
            'hdrs' :  resp.headers
        };
        # truncat
        if len(html) <  20000:
            print ("Truncating html",len(html), url)
            html = None

        c.extern.add(url,
                     {
                         'data':html,
                         'url': url,
                         'head' : head
                     })


    except Exception as e:
        pprint.pprint(e)
        c.extern.add(url,
                     {
                         'data': None,
                         'url': url,
                         #'head' : head,
                         'error' : str(e),
                     } )
        return
