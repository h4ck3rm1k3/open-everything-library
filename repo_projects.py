# look for projects that are in

# freshcode.club
# apache.org
# archlinux.org
# asterisk.org
# bazaar.canonical.com
# bitbucket.org
# blender.org
# bt747.org
# centos.org
# civicrm.org
# cpan.org
# cran.rstudio.com
# creativecommons.org


plist2 = """cygwin.com
dboost.org
codeplex.com
codeproject.com
curl.haxx.se
debian.net
debian.org
delphosproject.org
directory.fsf.org
drupal.org
ebian.org
eclipse.org
ekiga.org
emacswiki.org
europython.eu
fedoraproject.org
fossil.include-once.org
foswiki.org
freebsd.org
freecode.com
freetype.org
freshmeat.net
fsf.org
fsfe.org
fsfla.org
gcc.gnu.org
gdal.org
gimp.org
git-scm.com
github.com
gitlab
gitorious.org
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
wordpress.org
wtfpl.net
xfce.org
xfree86.org
x.org
wikimedia.org"""

plist = """
codemen.com
www.osinet.fr
fabric8.io
notabug.org
alioth.debian.org
seul.org
eff.org
www.ow2.org
osdn.com
osdn.jp
launchpad.net
www.javaforge.com
code.google.com
developers.google.com
www.gforge.org
gna.org
freepository.com
cloudforge.com
betavine.net
assembla.com
wildbit.com
getfedora.org
""".split()


import wikidatabase_lookup as wb
import reverse_cats as wp
import time
import requests
import json
import shelve
import os.path
import pprint

for x in plist:
    #print ("#Starting with " + x)
    lastContinue = {'continue': ''}
    
    while True :
        #print ("#Going to process " + x)
        (r,c) = wb.query_external("*."+x, lastContinue, namespace=0)

        count = 0
        if 'query' in r:
            if 'exturlusage' in r['query']:
                for k in r['query']['exturlusage']:
                    print (x, k['ns'], k['pageid'], k['title'], k['url'])
                    count = count +1
        if count == 0:
            # no new items found
            break
        if 'error' in r: raise Error(r['error'])
        if 'warnings' in r: print(r['warnings'])
        lastContinue = r['continue']
        time.sleep(3)
