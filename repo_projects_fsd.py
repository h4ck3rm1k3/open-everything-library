#! /usr/bin/python3
# look for projects that are in


plist = """alioth.debian.org
apache.org
archlinux.org
assembla.com
asterisk.org
bazaar.canonical.com
betavine.net
bitbucket.org
blender.org
bt747.org
centos.org
civicrm.org
cloudforge.com
code.google.com
codemen.com
codeplex.com
codeproject.com
cpan.org
cran.rstudio.com
creativecommons.org
curl.haxx.se
cygwin.com
dboost.org
debian.net
debian.org
delphosproject.org
developers.google.com
directory.fsf.org
drupal.org
ebian.org
eclipse.org
eff.org
ekiga.org
emacswiki.org
europython.eu
fabric8.io
fedoraproject.org
fossil.include-once.org
foswiki.org
freebsd.org
freecode.com
freepository.com
freetype.org
freshcode.club
freshmeat.net
fsf.org
fsfe.org
fsfla.org
gcc.gnu.org
gdal.org
getfedora.org
gimp.org
git-scm.com
github.com
gitlab
gitorious.org
gna.org
gnome.org
gnu.org
gnucash.org
gnumed.de
gpsbabel.org
gradle.org
icdevgroup.org
imagemagick.org
impresscms.org
inkscape.org
joinup.ec.europa.eu
joomla.org
jpilot.org
kde.org
kde.org.ar
kdenlive.org
kdevelop.org
kinodv.org
laconi.ca
laptop.com
latex-project.org
launchpad.net
launchpad.net
libreplanet.org
licensedb.org
linux.org
linuxfoundation.org
linuxmint.com
lxde.org
madebyfrog.com
mapfish.org
mapserver.org
maven.org
mepis.org
modxcms.com
mono-project.com
moodle.org
mozilla.org
mplayerhq.hu
netbeans.org
netbsd.org
nixos.org
notabug.org
npmjs.org
ocw.mit.edu
openbravo.com
openbsd.org
opendatacommons.org
openerp.com
openhub.net
openlayers.org
openmovieeditor.org
openoffice.org
opensource.org
opensourcemac.org
opensourcewindows.org
openstreetmap.org
opensuse.org
oreports.com
oscommerce.com
osdn.com
osdn.jp
osgeo.org
osgeo.org
packagist.org
pardus.org.tr
pear.php.net
pentaho.com
perl.org
perlfoundation.org
php.net
php.net
postgresql.org
prism-break.org
projects.eclipse.org
pypi.python.org
python.org
qlandkarte.org
rstudio.com
ruby-lang.org
rubygems.org
sahanafoundation.org
savannah.gnu.org
scribus.net
scripts.sil.org
seul.org
sf.net
silverstripe.org
slackware.com
softwarefreedom.org
sourceforge.net
spi-inc.org
sql-ledger.org
status.net
sugarlabs.org
svn.apache.org
tangocms.org
textpattern.com
tigris.org
tldrlegal.com
trac.edgewall.org
translatewiki.net
tuxfamily.org
ubuntu.com
unlicense.org
videolan.org
vim.org
walking-papers.org
wikimedia.org
wildbit.com
wordpress.org
wtfpl.net
gforge.org
javaforge.com
osinet.fr
ow2.org
x.org
xfce.org
xfree86.org""".split()


import fsd_lookup as wb
import time
import requests
import json
import shelve
import os.path
import pprint

for x in plist:
    #print ("#Starting with " + x)
    lastContinue = {'query-continue': ''}

    while True :
        #print ("#Going to process " + x)
        (r,c) = wb.query_external("*."+x, lastContinue, namespace=0)
        pprint.pprint(r)
        count = 0
        if 'query' in r:
            if 'exturlusage' in r['query']:
                for k in r['query']['exturlusage']:
                    if k['ns'] ==0 :
                        print(
                            "\t".join(
                                [
                                    x, 
                                    str(k['ns']),
                                    str(k['pageid']),
                                    k['title'],
                                    k['url'] 
                                ]
                            ))
                    count = count +1
        if count == 0:
            # no new items found
            break
        if 'error' in r: raise Error(r['error'])
        if 'warnings' in r: print(r['warnings'])
        lastContinue = r['query-continue']
        time.sleep(3)
